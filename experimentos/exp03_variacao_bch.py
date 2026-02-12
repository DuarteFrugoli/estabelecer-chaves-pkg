"""
Experimento 3: Variação do Código BCH
Testa o impacto do tamanho e capacidade de correção do BCH no KDR
"""

import sys
import os
import numpy as np
import random
from tqdm import tqdm

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.codigos_corretores.bch import gerar_tabela_codigos_bch, get_tamanho_bits_informacao
from src.canal.canal import extrair_kdr
from experimentos.util_experimentos import (
    salvar_resultado_json,
    salvar_resultado_csv,
    criar_grafico_comparativo_kdr,
    imprimir_sumario_resultados,
    salvar_grafico
)


def experimento_variacao_bch(
    quantidade_de_testes=1000,
    codigos_bch=[(7, 4), (15, 7), (127, 64), (255, 139)],
    rayleigh_param=1.0/np.sqrt(2),
    modulacao='bpsk',
    correlacao_canal=0.9,
    snr_db_range=None
):
    """
    Experimento: Impacto do código BCH no KDR
    
    Args:
        quantidade_de_testes: Número de testes Monte Carlo
        codigos_bch: Lista com tuplas (n, k) dos códigos BCH
        rayleigh_param: Parâmetro σ do Rayleigh
        modulacao: 'bpsk' ou 'qpsk'
        correlacao_canal: Coeficiente de correlação ρ
        snr_db_range: Array com valores de SNR (se None, usa padrão)
    """
    
    print("\n" + "="*70)
    print("EXPERIMENTO 3: VARIAÇÃO DO CÓDIGO BCH")
    print("="*70)
    print(f"Códigos BCH a testar: {codigos_bch}")
    print(f"Quantidade de testes: {quantidade_de_testes}")
    print(f"Parâmetro Rayleigh: {rayleigh_param:.6f}")
    print(f"Modulação: {modulacao.upper()}")
    print(f"Correlação canal: {correlacao_canal}")
    print("="*70 + "\n")
    
    # Configuração
    potencia_sinal = 1.0
    media_ruido = 0.0
    
    if snr_db_range is None:
        snr_db_range = np.linspace(-10, 30, 18)
    
    snr_linear_range = 10 ** (snr_db_range / 10)
    variancias_ruido = potencia_sinal / (2 * snr_linear_range)
    
    # Coleta dados para cada código BCH
    dados_todos_codigos = {}
    
    # Informações sobre capacidade de correção
    capacidades = {7: 1, 15: 2, 127: 10, 255: 15}
    
    for n, k in tqdm(codigos_bch, desc="Testando códigos BCH", colour="yellow"):
        print(f"\n--- Testando BCH({n},{k}) - t={capacidades[n]} erros ---")
        
        # Prepara palavra código
        random.seed(42)
        palavra_codigo = [random.randint(0, 1) for _ in range(n)]
        bch_codigo = gerar_tabela_codigos_bch(n, k)
        
        bmr_rates = []
        kdr_rates = []
        
        for variancia in tqdm(variancias_ruido,
                             desc=f"  BCH({n},{k})",
                             leave=False,
                             colour="green"):
            bmr, kdr = extrair_kdr(
                palavra_codigo,
                rayleigh_param,
                n,
                quantidade_de_testes,
                variancia,
                media_ruido,
                bch_codigo,
                correlacao_canal,
                usar_amplificacao=False,
                modulacao=modulacao,
                erro_estimativa=0.0,
                guard_band_sigma=0.0
            )
            
            bmr_rates.append(bmr)
            kdr_rates.append(kdr)
        
        codigo_str = f"BCH({n},{k})"
        dados_todos_codigos[codigo_str] = {
            'bmr_rates': bmr_rates,
            'kdr_rates': kdr_rates,
            'n': n,
            'k': k,
            't': capacidades[n]
        }
    
    # Prepara resultados
    dados = {
        'parametros': {
            'quantidade_de_testes': quantidade_de_testes,
            'codigos_bch': codigos_bch,
            'rayleigh_param': rayleigh_param,
            'modulacao': modulacao,
            'correlacao_canal': correlacao_canal
        },
        'snr_db': snr_db_range.tolist(),
        'resultados_por_codigo': dados_todos_codigos
    }
    
    # Salva JSON
    salvar_resultado_json(dados, "exp03_variacao_bch",
                         descricao="Análise do impacto do código BCH no KDR")
    
    # Salva CSV
    csv_dados = []
    for i, snr in enumerate(snr_db_range):
        linha = {'SNR_dB': f"{snr:.2f}"}
        for codigo_str in dados_todos_codigos.keys():
            linha[f'{codigo_str}_BMR'] = f"{dados_todos_codigos[codigo_str]['bmr_rates'][i]:.4f}"
            linha[f'{codigo_str}_KDR'] = f"{dados_todos_codigos[codigo_str]['kdr_rates'][i]:.4f}"
        csv_dados.append(linha)
    
    colunas = ['SNR_dB'] + [f'{c}_{tipo}' for c in dados_todos_codigos.keys() for tipo in ['BMR', 'KDR']]
    salvar_resultado_csv(csv_dados, "exp03_variacao_bch", colunas)
    
    # Cria gráficos separados (2 figuras independentes)
    import matplotlib.pyplot as plt
    
    cores = plt.cm.tab10(np.linspace(0, 1, len(dados_todos_codigos)))
    
    # FIGURA 1: BMR Antes da Reconciliação
    fig1, ax1 = plt.subplots(figsize=(8, 6))
    for j, (codigo_str, dados_codigo) in enumerate(dados_todos_codigos.items()):
        ax1.plot(snr_db_range, dados_codigo['bmr_rates'],
                marker='o', linestyle='-', linewidth=2,
                color=cores[j], label=f"{codigo_str} (t={dados_codigo['t']})")
    ax1.set_xlabel('SNR (dB)', fontsize=12)
    ax1.set_ylabel('BMR (%)', fontsize=12)
    ax1.set_title(f'BMR Antes da Reconciliação\n(σ={rayleigh_param:.4f}, {modulacao.upper()}, ρ={correlacao_canal})', 
                 fontsize=13, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.legend(fontsize=10)
    plt.tight_layout()
    salvar_grafico(fig1, "exp03_variacao_bch_01")
    plt.close()
    
    # FIGURA 2: KDR Após Reconciliação BCH
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    for j, (codigo_str, dados_codigo) in enumerate(dados_todos_codigos.items()):
        ax2.plot(snr_db_range, dados_codigo['kdr_rates'],
                marker='s', linestyle='-', linewidth=2,
                color=cores[j], label=f"{codigo_str} (t={dados_codigo['t']})")
    ax2.set_xlabel('SNR (dB)', fontsize=12)
    ax2.set_ylabel('KDR (%)', fontsize=12)
    ax2.set_title(f'KDR Após Reconciliação BCH\n(σ={rayleigh_param:.4f}, {modulacao.upper()}, ρ={correlacao_canal})', 
                 fontsize=13, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.legend(fontsize=10)
    plt.tight_layout()
    salvar_grafico(fig2, "exp03_variacao_bch_02")
    plt.close()
    
    # Sumário por código
    for codigo_str, dados_codigo in dados_todos_codigos.items():
        print(f"\n--- Resultados para {codigo_str} (t={dados_codigo['t']}) ---")
        imprimir_sumario_resultados({
            'BMR': dados_codigo['bmr_rates'],
            'KDR': dados_codigo['kdr_rates']
        })
    
    print("\n[OK] Experimento 3 concluído com sucesso!\n")
    
    return dados


if __name__ == "__main__":
    # Executa experimento com parâmetros padrão
    # ATENÇÃO: Este experimento pode demorar devido aos códigos grandes
    resultados = experimento_variacao_bch(
        quantidade_de_testes=500,  # Reduzido para economizar tempo
        codigos_bch=[(7, 4), (15, 7), (127, 64)],  # Removendo 255 para economizar tempo
        rayleigh_param=1.0/np.sqrt(2),
        modulacao='bpsk',
        correlacao_canal=0.9
    )
