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
    ber_rates = []
    kdr_rates = []
    
    for i, (snr_db, variancia) in enumerate(tqdm(
        zip(snr_db_range, variancias_ruido),
        total=len(snr_db_range),
        desc="Testando SNR",
        colour="green"
    )):
        ber, kdr = extrair_kdr(
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
        
        ber_rates.append(ber)
        kdr_rates.append(kdr)
    
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
        'ber_rates': ber_rates,
        'kdr_rates': kdr_rates
    }
    
    # Salva JSON
    salvar_resultado_json(dados, "exp01_variacao_snr", 
                         descricao="Análise do impacto da SNR no KDR")
    
    # Salva CSV
    csv_dados = []
    for i, snr in enumerate(snr_db_range):
        csv_dados.append({
            'SNR_dB': f"{snr:.2f}",
            'BER': f"{ber_rates[i]:.4f}",
            'KDR': f"{kdr_rates[i]:.4f}"
        })
    
    salvar_resultado_csv(csv_dados, "exp01_variacao_snr",
                        ['SNR_dB', 'BER', 'KDR'])
    
    # Cria gráfico usando util_experimentos
    dados_variacoes = {
        'Padrão': {
            'ber_rates': ber_rates,
            'kdr_rates': kdr_rates
        }
    }
    
    from experimentos.util_experimentos import criar_grafico_comparativo_kdr
    criar_grafico_comparativo_kdr(
        snr_db=snr_db_range,
        dados_variacoes=dados_variacoes,
        titulo=f"Impacto da SNR no BER/KDR (σ={rayleigh_param:.4f}, {modulacao.upper()}, ρ={correlacao_canal})",
        xlabel="SNR (dB)",
        nome_arquivo="exp01_variacao_snr"
    )
    
    # Sumário
    imprimir_sumario_resultados({
        'BER': ber_rates,
        'KDR': kdr_rates
    })
    
    print("\n[OK] Experimento 1 concluído com sucesso!\n")
    
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
