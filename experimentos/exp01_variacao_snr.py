"""
Experimento 1: Variação de SNR
Testa o impacto da relação sinal-ruído no KDR
"""

import sys
import os
import numpy as np
import random
from tqdm import tqdm

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.codigos_corretores.bch import gerar_tabela_codigos_bch, get_tamanho_bits_informacao
from src.canal.canal import extrair_kdr
from experimentos.util_experimentos import (
    salvar_resultado_json,
    salvar_resultado_csv,
    criar_grafico_comparativo_kdr,
    imprimir_sumario_resultados
)


def experimento_variacao_snr(
    tamanho_cadeia_bits=127,
    quantidade_de_testes=1000,
    rayleigh_param=1.0/np.sqrt(2),
    modulacao='bpsk',
    correlacao_canal=0.9,
    snr_min=-10,
    snr_max=30,
    snr_pontos=18
):
    """
    Experimento: Impacto da variação de SNR no KDR
    
    Args:
        tamanho_cadeia_bits: Tamanho do código BCH
        quantidade_de_testes: Número de testes Monte Carlo
        rayleigh_param: Parâmetro σ do Rayleigh
        modulacao: 'bpsk' ou 'qpsk'
        correlacao_canal: Coeficiente de correlação ρ
        snr_min: SNR mínimo em dB
        snr_max: SNR máximo em dB
        snr_pontos: Número de pontos SNR
    """
    
    print("\n" + "="*70)
    print("EXPERIMENTO 1: VARIAÇÃO DE SNR")
    print("="*70)
    print(f"Tamanho código BCH: {tamanho_cadeia_bits}")
    print(f"Quantidade de testes: {quantidade_de_testes}")
    print(f"Parâmetro Rayleigh: {rayleigh_param:.6f}")
    print(f"Modulação: {modulacao.upper()}")
    print(f"Correlação canal: {correlacao_canal}")
    print(f"Range SNR: [{snr_min}, {snr_max}] dB ({snr_pontos} pontos)")
    print("="*70 + "\n")
    
    # Configuração
    potencia_sinal = 1.0
    media_ruido = 0.0
    
    snr_db_range = np.linspace(snr_min, snr_max, snr_pontos)
    snr_linear_range = 10 ** (snr_db_range / 10)
    variancias_ruido = potencia_sinal / (2 * snr_linear_range)
    
    # Prepara palavra código
    random.seed(42)
    palavra_codigo = [random.randint(0, 1) for _ in range(tamanho_cadeia_bits)]
    tamanho_bits_informacao = get_tamanho_bits_informacao(tamanho_cadeia_bits)
    bch_codigo = gerar_tabela_codigos_bch(tamanho_cadeia_bits, tamanho_bits_informacao)
    
    # Coleta dados
    kdr_rates = []
    kdr_pos_rates = []
    kdr_amplificacao_rates = []
    
    for i, (snr_db, variancia) in enumerate(tqdm(
        zip(snr_db_range, variancias_ruido),
        total=len(snr_db_range),
        desc="Testando SNR",
        colour="green"
    )):
        kdr, kdr_pos, kdr_amp = extrair_kdr(
            palavra_codigo,
            rayleigh_param,
            tamanho_cadeia_bits,
            quantidade_de_testes,
            variancia,
            media_ruido,
            bch_codigo,
            correlacao_canal,
            usar_amplificacao=True,
            modulacao=modulacao,
            erro_estimativa=0.0,
            guard_band_sigma=0.0
        )
        
        kdr_rates.append(kdr)
        kdr_pos_rates.append(kdr_pos)
        kdr_amplificacao_rates.append(kdr_amp)
    
    # Prepara resultados
    dados = {
        'parametros': {
            'tamanho_cadeia_bits': tamanho_cadeia_bits,
            'quantidade_de_testes': quantidade_de_testes,
            'rayleigh_param': rayleigh_param,
            'modulacao': modulacao,
            'correlacao_canal': correlacao_canal,
            'snr_min': snr_min,
            'snr_max': snr_max,
            'snr_pontos': snr_pontos
        },
        'snr_db': snr_db_range.tolist(),
        'kdr_rates': kdr_rates,
        'kdr_pos_rates': kdr_pos_rates,
        'kdr_amplificacao_rates': kdr_amplificacao_rates
    }
    
    # Salva JSON
    salvar_resultado_json(dados, "exp01_variacao_snr", 
                         descricao="Análise do impacto da SNR no KDR")
    
    # Salva CSV
    csv_dados = []
    for i, snr in enumerate(snr_db_range):
        csv_dados.append({
            'SNR_dB': f"{snr:.2f}",
            'KDR_antes': f"{kdr_rates[i]:.4f}",
            'KDR_pos_rec': f"{kdr_pos_rates[i]:.4f}",
            'KDR_pos_amp': f"{kdr_amplificacao_rates[i]:.4f}"
        })
    
    salvar_resultado_csv(csv_dados, "exp01_variacao_snr",
                        ['SNR_dB', 'KDR_antes', 'KDR_pos_rec', 'KDR_pos_amp'])
    
    # Cria gráfico
    import matplotlib.pyplot as plt
    
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    
    ax.plot(snr_db_range, kdr_rates, 
           marker='o', linestyle='-', linewidth=2, color='red',
           label='KDR antes da reconciliação')
    
    ax.plot(snr_db_range, kdr_pos_rates,
           marker='s', linestyle='-', linewidth=2, color='blue',
           label='KDR pós reconciliação')
    
    ax.plot(snr_db_range, kdr_amplificacao_rates,
           marker='^', linestyle='-', linewidth=2, color='green',
           label='KDR pós amplificação (SHA-256)')
    
    ax.set_xlabel('SNR (dB)', fontsize=12)
    ax.set_ylabel('Key Disagreement Rate (%)', fontsize=12)
    ax.set_title(f'Impacto da SNR no KDR\n(σ={rayleigh_param:.4f}, {modulacao.upper()}, ρ={correlacao_canal})', 
                fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=10)
    
    from experimentos.util_experimentos import salvar_grafico
    salvar_grafico(fig, "exp01_variacao_snr")
    plt.close()
    
    # Sumário
    imprimir_sumario_resultados({
        'KDR_antes': kdr_rates,
        'KDR_pos_reconciliacao': kdr_pos_rates,
        'KDR_pos_amplificacao': kdr_amplificacao_rates
    })
    
    print("\n✓ Experimento 1 concluído com sucesso!\n")
    
    return dados


if __name__ == "__main__":
    # Executa experimento com parâmetros padrão
    resultados = experimento_variacao_snr(
        tamanho_cadeia_bits=127,
        quantidade_de_testes=1000,
        rayleigh_param=1.0/np.sqrt(2),
        modulacao='bpsk',
        correlacao_canal=0.9
    )
