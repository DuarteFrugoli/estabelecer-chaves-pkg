"""
Experimento 2: Comparação BPSK vs QPSK
Testa o impacto do tipo de modulação no KDR
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


def experimento_comparacao_modulacao(
    tamanho_cadeia_bits=127,
    quantidade_de_testes=1000,
    rayleigh_param=1.0/np.sqrt(2),
    correlacao_canal=0.9,
    snr_db_range=None
):
    """
    Experimento: Comparação entre BPSK e QPSK
    
    Args:
        tamanho_cadeia_bits: Tamanho do código BCH
        quantidade_de_testes: Número de testes Monte Carlo
        rayleigh_param: Parâmetro σ do Rayleigh
        correlacao_canal: Coeficiente de correlação ρ
        snr_db_range: Array com valores de SNR (se None, usa padrão)
    """
    
    print("\n" + "="*70)
    print("EXPERIMENTO 2: COMPARAÇÃO BPSK vs QPSK")
    print("="*70)
    print(f"Tamanho código BCH: {tamanho_cadeia_bits}")
    print(f"Quantidade de testes: {quantidade_de_testes}")
    print(f"Parâmetro Rayleigh: {rayleigh_param:.6f}")
    print(f"Correlação canal: {correlacao_canal}")
    print("="*70 + "\n")
    
    # Configuração
    potencia_sinal = 1.0
    media_ruido = 0.0
    
    if snr_db_range is None:
        snr_db_range = np.linspace(-10, 30, 18)
    
    snr_linear_range = 10 ** (snr_db_range / 10)
    variancias_ruido = potencia_sinal / (2 * snr_linear_range)
    
    # Prepara palavra código
    random.seed(42)
    palavra_codigo = [random.randint(0, 1) for _ in range(tamanho_cadeia_bits)]
    tamanho_bits_informacao = get_tamanho_bits_informacao(tamanho_cadeia_bits)
    bch_codigo = gerar_tabela_codigos_bch(tamanho_cadeia_bits, tamanho_bits_informacao)
    
    # Coleta dados para cada modulação
    dados_modulacoes = {}
    
    for modulacao in ['bpsk', 'qpsk']:
        print(f"\n--- Testando {modulacao.upper()} ---")
        
        bmr_rates = []
        kdr_rates = []
        
        for variancia in tqdm(variancias_ruido,
                             desc=f"  {modulacao.upper()}",
                             colour="cyan"):
            bmr, kdr = extrair_kdr(
                palavra_codigo,
                rayleigh_param,
                tamanho_cadeia_bits,
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
        
        dados_modulacoes[modulacao] = {
            'bmr_rates': bmr_rates,
            'kdr_rates': kdr_rates
        }
    
    # Prepara resultados
    dados = {
        'parametros': {
            'tamanho_cadeia_bits': tamanho_cadeia_bits,
            'quantidade_de_testes': quantidade_de_testes,
            'rayleigh_param': rayleigh_param,
            'correlacao_canal': correlacao_canal
        },
        'snr_db': snr_db_range.tolist(),
        'resultados': {
            'bpsk': dados_modulacoes['bpsk'],
            'qpsk': dados_modulacoes['qpsk']
        }
    }
    
    # Salva JSON
    salvar_resultado_json(dados, "exp02_comparacao_modulacao",
                         descricao="Comparação entre BPSK e QPSK")
    
    # Salva CSV
    csv_dados = []
    for i, snr in enumerate(snr_db_range):
        csv_dados.append({
            'SNR_dB': f"{snr:.2f}",
            'BPSK_BMR': f"{dados_modulacoes['bpsk']['bmr_rates'][i]:.4f}",
            'BPSK_KDR': f"{dados_modulacoes['bpsk']['kdr_rates'][i]:.4f}",
            'QPSK_BMR': f"{dados_modulacoes['qpsk']['bmr_rates'][i]:.4f}",
            'QPSK_KDR': f"{dados_modulacoes['qpsk']['kdr_rates'][i]:.4f}"
        })
    
    salvar_resultado_csv(csv_dados, "exp02_comparacao_modulacao",
                        ['SNR_dB', 'BPSK_BMR', 'BPSK_KDR', 'QPSK_BMR', 'QPSK_KDR'])
    
    # Cria gráficos separados (2 figuras independentes)
    import matplotlib.pyplot as plt
    
    # FIGURA 1: BMR Antes da Reconciliação
    fig1, ax1 = plt.subplots(figsize=(8, 6))
    ax1.plot(snr_db_range, dados_modulacoes['bpsk']['bmr_rates'],
            marker='o', linestyle='-', linewidth=2, color='blue', label='BPSK')
    ax1.plot(snr_db_range, dados_modulacoes['qpsk']['bmr_rates'],
            marker='s', linestyle='--', linewidth=2, color='red', label='QPSK')
    ax1.set_xlabel('SNR (dB)', fontsize=12)
    ax1.set_ylabel('BMR (%)', fontsize=12)
    ax1.set_title(f'BMR Antes da Reconciliação\n(σ={rayleigh_param:.4f}, ρ={correlacao_canal})', 
                 fontsize=13, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.legend(fontsize=11)
    plt.tight_layout()
    salvar_grafico(fig1, "exp02_comparacao_modulacao_01")
    plt.close()
    
    # FIGURA 2: KDR Após Reconciliação BCH
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    ax2.plot(snr_db_range, dados_modulacoes['bpsk']['kdr_rates'],
            marker='o', linestyle='-', linewidth=2, color='blue', label='BPSK')
    ax2.plot(snr_db_range, dados_modulacoes['qpsk']['kdr_rates'],
            marker='s', linestyle='--', linewidth=2, color='red', label='QPSK')
    ax2.set_xlabel('SNR (dB)', fontsize=12)
    ax2.set_ylabel('KDR (%)', fontsize=12)
    ax2.set_title(f'KDR Após Reconciliação BCH\n(σ={rayleigh_param:.4f}, ρ={correlacao_canal})', 
                 fontsize=13, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.legend(fontsize=11)
    plt.tight_layout()
    salvar_grafico(fig2, "exp02_comparacao_modulacao_02")
    plt.close()
    
    # Sumário
    for modulacao in ['bpsk', 'qpsk']:
        print(f"\n--- Resultados para {modulacao.upper()} ---")
        imprimir_sumario_resultados({
            'BMR': dados_modulacoes[modulacao]['bmr_rates'],
            'KDR': dados_modulacoes[modulacao]['kdr_rates']
        })
    
    print("\n[OK] Experimento 2 concluído com sucesso!\n")
    
    return dados


if __name__ == "__main__":
    # Executa experimento com parâmetros padrão
    resultados = experimento_comparacao_modulacao(
        tamanho_cadeia_bits=127,
        quantidade_de_testes=1000,
        rayleigh_param=1.0/np.sqrt(2),
        correlacao_canal=0.9
    )
