"""
Experimento 4: Variação da Correlação do Canal (ρ)
Testa o impacto da reciprocidade do canal no KDR
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


def experimento_variacao_correlacao(
    tamanho_cadeia_bits=127,
    quantidade_de_testes=1000,
    rayleigh_param=1.0/np.sqrt(2),
    modulacao='bpsk',
    correlacoes=[0.7, 0.8, 0.9, 0.95, 0.99],
    snr_db_range=None
):
    """
    Experimento: Impacto da correlação do canal (reciprocidade) no KDR
    
    Args:
        tamanho_cadeia_bits: Tamanho do código BCH
        quantidade_de_testes: Número de testes Monte Carlo
        rayleigh_param: Parâmetro σ do Rayleigh
        modulacao: 'bpsk' ou 'qpsk'
        correlacoes: Lista com valores de ρ a testar
        snr_db_range: Array com valores de SNR (se None, usa padrão)
    """
    
    print("\n" + "="*70)
    print("EXPERIMENTO 4: VARIAÇÃO DA CORRELAÇÃO DO CANAL (ρ)")
    print("="*70)
    print(f"Tamanho código BCH: {tamanho_cadeia_bits}")
    print(f"Quantidade de testes: {quantidade_de_testes}")
    print(f"Parâmetro Rayleigh: {rayleigh_param:.6f}")
    print(f"Modulação: {modulacao.upper()}")
    print(f"Valores de ρ: {correlacoes}")
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
    
    # Coleta dados para cada ρ
    dados_todas_correlacoes = {}
    
    for rho in tqdm(correlacoes, desc="Testando ρ", colour="magenta"):
        kdr_rates = []
        kdr_pos_rates = []
        kdr_amplificacao_rates = []
        
        for variancia in tqdm(variancias_ruido,
                             desc=f"  ρ={rho:.2f}",
                             leave=False,
                             colour="green"):
            kdr, kdr_pos, kdr_amp = extrair_kdr(
                palavra_codigo,
                rayleigh_param,
                tamanho_cadeia_bits,
                quantidade_de_testes,
                variancia,
                media_ruido,
                bch_codigo,
                rho,  # Variando correlação
                usar_amplificacao=True,
                modulacao=modulacao
            )
            
            kdr_rates.append(kdr)
            kdr_pos_rates.append(kdr_pos)
            kdr_amplificacao_rates.append(kdr_amp)
        
        dados_todas_correlacoes[rho] = {
            'kdr_rates': kdr_rates,
            'kdr_pos_rates': kdr_pos_rates,
            'kdr_amplificacao_rates': kdr_amplificacao_rates
        }
    
    # Prepara resultados
    dados = {
        'parametros': {
            'tamanho_cadeia_bits': tamanho_cadeia_bits,
            'quantidade_de_testes': quantidade_de_testes,
            'rayleigh_param': rayleigh_param,
            'modulacao': modulacao,
            'correlacoes': correlacoes
        },
        'snr_db': snr_db_range.tolist(),
        'resultados_por_correlacao': {str(r): dados_todas_correlacoes[r] for r in correlacoes}
    }
    
    # Salva JSON
    salvar_resultado_json(dados, "exp04_variacao_correlacao",
                         descricao="Análise do impacto da correlação do canal ρ no KDR")
    
    # Salva CSV
    csv_dados = []
    for i, snr in enumerate(snr_db_range):
        linha = {'SNR_dB': f"{snr:.2f}"}
        for rho in correlacoes:
            linha[f'ρ={rho:.2f}_antes'] = f"{dados_todas_correlacoes[rho]['kdr_rates'][i]:.4f}"
            linha[f'ρ={rho:.2f}_pos'] = f"{dados_todas_correlacoes[rho]['kdr_pos_rates'][i]:.4f}"
        csv_dados.append(linha)
    
    colunas = ['SNR_dB'] + [f'ρ={r:.2f}_{tipo}' for r in correlacoes for tipo in ['antes', 'pos']]
    salvar_resultado_csv(csv_dados, "exp04_variacao_correlacao", colunas)
    
    # Cria gráfico comparativo
    criar_grafico_comparativo_kdr(
        snr_db_range,
        dados_todas_correlacoes,
        f'Impacto da Correlação do Canal ρ no KDR\n(σ={rayleigh_param:.4f}, {modulacao.upper()})',
        'SNR (dB)',
        "exp04_variacao_correlacao",
        legenda_template="ρ = {:.2f}"
    )
    
    # Sumário por correlação
    for rho in correlacoes:
        print(f"\n--- Resultados para ρ = {rho:.2f} ---")
        imprimir_sumario_resultados({
            'KDR_antes': dados_todas_correlacoes[rho]['kdr_rates'],
            'KDR_pos_reconciliacao': dados_todas_correlacoes[rho]['kdr_pos_rates'],
            'KDR_pos_amplificacao': dados_todas_correlacoes[rho]['kdr_amplificacao_rates']
        })
    
    print("\n✓ Experimento 4 concluído com sucesso!\n")
    
    return dados


if __name__ == "__main__":
    # Executa experimento com parâmetros padrão
    resultados = experimento_variacao_correlacao(
        tamanho_cadeia_bits=127,
        quantidade_de_testes=1000,
        rayleigh_param=1.0/np.sqrt(2),
        modulacao='bpsk',
        correlacoes=[0.7, 0.8, 0.9, 0.95, 0.99]
    )
