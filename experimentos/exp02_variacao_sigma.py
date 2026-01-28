"""
Experimento 2: Variação do Parâmetro Rayleigh (σ)
Testa o impacto da intensidade do desvanecimento no KDR
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
    imprimir_sumario_resultados
)


def experimento_variacao_sigma(
    tamanho_cadeia_bits=127,
    quantidade_de_testes=1000,
    sigmas=[0.5, 1.0/np.sqrt(2), 1.0, 2.0],
    modulacao='bpsk',
    correlacao_canal=0.9,
    snr_db_range=None
):
    """
    Experimento: Impacto do parâmetro Rayleigh σ no KDR
    
    Args:
        tamanho_cadeia_bits: Tamanho do código BCH
        quantidade_de_testes: Número de testes Monte Carlo
        sigmas: Lista com valores de σ a testar
        modulacao: 'bpsk' ou 'qpsk'
        correlacao_canal: Coeficiente de correlação ρ
        snr_db_range: Array com valores de SNR (se None, usa padrão)
    """
    
    print("\n" + "="*70)
    print("EXPERIMENTO 2: VARIAÇÃO DO PARÂMETRO RAYLEIGH (σ)")
    print("="*70)
    print(f"Tamanho código BCH: {tamanho_cadeia_bits}")
    print(f"Quantidade de testes: {quantidade_de_testes}")
    print(f"Valores de σ: {sigmas}")
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
    
    # Prepara palavra código
    random.seed(42)
    palavra_codigo = [random.randint(0, 1) for _ in range(tamanho_cadeia_bits)]
    tamanho_bits_informacao = get_tamanho_bits_informacao(tamanho_cadeia_bits)
    bch_codigo = gerar_tabela_codigos_bch(tamanho_cadeia_bits, tamanho_bits_informacao)
    
    # Coleta dados para cada σ
    dados_todos_sigmas = {}
    
    for sigma in tqdm(sigmas, desc="Testando σ", colour="blue"):
        kdr_rates = []
        kdr_pos_rates = []
        kdr_amplificacao_rates = []
        
        for variancia in tqdm(variancias_ruido, 
                             desc=f"  σ={sigma:.4f}",
                             leave=False,
                             colour="green"):
            kdr, kdr_pos, kdr_amp = extrair_kdr(
                palavra_codigo,
                sigma,
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
        
        dados_todos_sigmas[sigma] = {
            'kdr_rates': kdr_rates,
            'kdr_pos_rates': kdr_pos_rates,
            'kdr_amplificacao_rates': kdr_amplificacao_rates
        }
    
    # Prepara resultados
    dados = {
        'parametros': {
            'tamanho_cadeia_bits': tamanho_cadeia_bits,
            'quantidade_de_testes': quantidade_de_testes,
            'sigmas': sigmas,
            'modulacao': modulacao,
            'correlacao_canal': correlacao_canal
        },
        'snr_db': snr_db_range.tolist(),
        'resultados_por_sigma': {str(s): dados_todos_sigmas[s] for s in sigmas}
    }
    
    # Salva JSON
    salvar_resultado_json(dados, "exp02_variacao_sigma",
                         descricao="Análise do impacto do parâmetro Rayleigh σ no KDR")
    
    # Salva CSV consolidado
    csv_dados = []
    for i, snr in enumerate(snr_db_range):
        linha = {'SNR_dB': f"{snr:.2f}"}
        for sigma in sigmas:
            linha[f'σ={sigma:.4f}_antes'] = f"{dados_todos_sigmas[sigma]['kdr_rates'][i]:.4f}"
            linha[f'σ={sigma:.4f}_pos'] = f"{dados_todos_sigmas[sigma]['kdr_pos_rates'][i]:.4f}"
        csv_dados.append(linha)
    
    colunas = ['SNR_dB'] + [f'σ={s:.4f}_{tipo}' for s in sigmas for tipo in ['antes', 'pos']]
    salvar_resultado_csv(csv_dados, "exp02_variacao_sigma", colunas)
    
    # Cria gráfico comparativo
    criar_grafico_comparativo_kdr(
        snr_db_range,
        dados_todos_sigmas,
        f'Impacto do Parâmetro Rayleigh σ no KDR\n({modulacao.upper()}, ρ={correlacao_canal})',
        'SNR (dB)',
        "exp02_variacao_sigma",
        legenda_template="σ = {:.4f}"
    )
    
    # Sumário por sigma
    for sigma in sigmas:
        print(f"\n--- Resultados para σ = {sigma:.4f} ---")
        imprimir_sumario_resultados({
            'KDR_antes': dados_todos_sigmas[sigma]['kdr_rates'],
            'KDR_pos_reconciliacao': dados_todos_sigmas[sigma]['kdr_pos_rates'],
            'KDR_pos_amplificacao': dados_todos_sigmas[sigma]['kdr_amplificacao_rates']
        })
    
    print("\n✓ Experimento 2 concluído com sucesso!\n")
    
    return dados


if __name__ == "__main__":
    # Executa experimento com parâmetros padrão
    resultados = experimento_variacao_sigma(
        tamanho_cadeia_bits=127,
        quantidade_de_testes=1000,
        sigmas=[0.5, 1.0/np.sqrt(2), 1.0, 2.0],
        modulacao='bpsk',
        correlacao_canal=0.9
    )
