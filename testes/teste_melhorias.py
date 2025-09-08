"""
Script de teste automatizado para demonstrar as melhorias implementadas no PKG
"""
import time
import numpy as np
import random
import logging
import sys
import os

# Adiciona o diretório raiz ao path para importar os módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Logger para fazer o acompanhamento do fluxo de execução
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Configuração do handler de log
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)
logger.propagate = False

from codigos_corretores.bch import *
from canal.canal import *
from plotkdr import plot_kdr
from util.util import *

def teste_automatizado():
    """Executa teste automatizado com parâmetros pré-definidos"""
    
    # Parâmetros de teste
    quantidade_de_testes = 100  # Reduzido para teste rápido
    tamanho_cadeia_bits = 15    # Código BCH (15,7,2) - corrige 2 erros
    
    print(f"=== TESTE AUTOMATIZADO DAS MELHORIAS PKG ===")
    print(f"Quantidade de testes: {quantidade_de_testes}")
    print(f"Tamanho da cadeia: {tamanho_cadeia_bits} bits")
    print(f"Melhorias: BPSK, Reciprocidade (ρ=0.9), SNR Corrigido")
    print("="*50)
    
    # Parâmetros de simulação
    potencia_sinal = 1.0
    rayleigh_param = 1.0  # Teste com apenas um parâmetro
    snr_db_range = np.linspace(0, 20, 11)  # 11 valores de 0 a 20 dB
    snr_linear_range = 10 ** (snr_db_range / 10)
    
    # Relação SNR correta para BPSK
    variancias_ruido = potencia_sinal / (2 * snr_linear_range)
    media_ruido = 0
    correlacao_canal = 0.9
    
    # Gera palavra código e tabela BCH
    tamanho_bits_informacao = get_tamanho_bits_informacao(tamanho_cadeia_bits)
    palavra_codigo = [random.randint(0, 1) for _ in range(tamanho_cadeia_bits)]
    logger.info(f"Palavra de código gerada: {palavra_codigo} (k={tamanho_bits_informacao})")
    
    tabela_codigos = gerar_tabela_codigos_bch(tamanho_cadeia_bits, tamanho_bits_informacao)
    logger.info(f"Tabela BCH gerada com {len(tabela_codigos)} códigos")
    
    # Executa simulação
    start_time = time.time()
    kdr_rates = []
    kdr_pos_rates = []
    
    print("\nSimulando para diferentes valores de SNR...")
    for i, variancia in enumerate(variancias_ruido):
        snr_db = snr_db_range[i]
        print(f"SNR = {snr_db:.1f} dB", end=" -> ")
        
        kdr, kdr_pos_reconciliacao = extrair_kdr(
            palavra_codigo,
            rayleigh_param,
            tamanho_cadeia_bits,
            quantidade_de_testes,
            variancia,
            media_ruido,
            tabela_codigos,
            correlacao_canal
        )
        
        kdr_rates.append(kdr)
        kdr_pos_rates.append(kdr_pos_reconciliacao)
        print(f"KDR antes: {kdr:.2f}%, KDR pós: {kdr_pos_reconciliacao:.2f}%")
    
    # Exibe resultados
    execution_time = time.time() - start_time
    print(f"\n=== RESULTADOS ===")
    print(f"Tempo de execução: {execution_time:.2f}s")
    print(f"KDR inicial (SNR=0dB): {kdr_rates[0]:.2f}% -> {kdr_pos_rates[0]:.2f}%")
    print(f"KDR final (SNR=20dB): {kdr_rates[-1]:.2f}% -> {kdr_pos_rates[-1]:.2f}%")
    print(f"Melhoria média: {np.mean(np.array(kdr_rates) - np.array(kdr_pos_rates)):.2f}% pontos")
    
    # Gera gráfico
    plot_kdr(snr_db_range, kdr_rates, kdr_pos_rates, rayleigh_param)
    
    return snr_db_range, kdr_rates, kdr_pos_rates

if __name__ == "__main__":
    teste_automatizado()
