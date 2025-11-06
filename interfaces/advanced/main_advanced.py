import time
import numpy as np
import random
import logging
import sys
import os
from tqdm import tqdm

# Adiciona o diretório raiz ao path
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

# Logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)
logger.propagate = False

from src.codigos_corretores.bch import *
from src.canal.canal import *
from src.visualizacao.plotkdr_advanced import plot_kdr_advanced
from src.util.util import *

# Marca o tempo inicial
start_time = time.time()

print("\n" + "="*70)
print("SIMULADOR AVANÇADO DE ESTABELECIMENTO DE CHAVES")
print("="*70)
print("Modo parametrizável - Configure todos os parâmetros da simulação")
print("="*70 + "\n")

# Solicita parâmetros ao usuário
quantidade_de_testes = solicita_entrada("Quantidade de testes: ", int, lambda v: v > 0)
tamanho_cadeia_bits = solicita_entrada("Tamanho da cadeia de bits (7, 15, 127, 255): ", int, lambda v: v in {7, 15, 127, 255})

# Solicita tipo de modulação
print("\nEscolha o tipo de modulação:")
print("1 - BPSK (Binary Phase Shift Keying)")
print("2 - QPSK (Quadrature Phase Shift Keying)")
opcao_modulacao = solicita_entrada("Digite 1 para BPSK ou 2 para QPSK: ", int, lambda v: v in {1, 2})
modulacao = 'bpsk' if opcao_modulacao == 1 else 'qpsk'

# Parâmetros do canal
print("\n" + "="*70)
print("PARÂMETROS DO CANAL")
print("="*70)

rayleigh_param = solicita_entrada(f"Parâmetro Rayleigh (σ) [padrão: {1.0/np.sqrt(2):.6f}]: ", float, lambda v: v > 0)
correlacao_canal = solicita_entrada("Correlação do canal (ρ) [padrão: 0.9]: ", float, lambda v: 0 <= v <= 1)

# Parâmetros de SNR
print("\n" + "="*70)
print("PARÂMETROS DE SNR")
print("="*70)

snr_min = solicita_entrada("SNR mínimo (dB) [padrão: -10]: ", float, lambda v: True)
snr_max = solicita_entrada("SNR máximo (dB) [padrão: 30]: ", float, lambda v: v > snr_min)
snr_pontos = solicita_entrada("Número de pontos SNR [padrão: 18]: ", int, lambda v: v > 0)

snr_db_range = np.linspace(snr_min, snr_max, snr_pontos)
snr_linear_range = 10 ** (snr_db_range / 10)

# Parâmetros de ruído
print("\n" + "="*70)
print("PARÂMETROS DE RUÍDO")
print("="*70)

potencia_sinal = solicita_entrada("Potência do sinal (Es) [padrão: 1.0]: ", float, lambda v: v > 0)
media_ruido = solicita_entrada("Média do ruído [padrão: 0.0]: ", float, lambda v: True)

# SNR = Es/N0, onde sigma² = N0/2
variancias_ruido = potencia_sinal / (2 * snr_linear_range)

# Amplificação de privacidade
print("\n" + "="*70)
print("OPÇÕES AVANÇADAS")
print("="*70)

usar_amplificacao_input = input("Habilitar amplificação de privacidade (SHA-256)? (s/n) [padrão: s]: ").strip().lower()
usar_amplificacao = usar_amplificacao_input != 'n'

# Gera palavra código aleatória
random.seed(42)  # Seed para reprodutibilidade
palavra_codigo = [random.randint(0, 1) for _ in range(tamanho_cadeia_bits)]
tamanho_bits_informacao = get_tamanho_bits_informacao(tamanho_cadeia_bits)

# Gera o objeto BCH
bch_codigo = gerar_tabela_codigos_bch(tamanho_cadeia_bits, tamanho_bits_informacao)

print("\n" + "="*70)
print("INICIANDO SIMULAÇÃO")
print("="*70)
print(f"Modulação: {modulacao.upper()}")
print(f"Quantidade de testes: {quantidade_de_testes}")
print(f"Tamanho da cadeia de bits: {tamanho_cadeia_bits}")
print(f"Parâmetro Rayleigh (σ): {rayleigh_param:.6f}")
print(f"Correlação do canal (ρ): {correlacao_canal:.2f}")
print(f"SNR: {snr_min} a {snr_max} dB ({snr_pontos} pontos)")
print(f"Potência do sinal: {potencia_sinal}")
print(f"Amplificação: {'SIM' if usar_amplificacao else 'NÃO'}")
print("="*70 + "\n")

# Coleta dados
kdr_rates = []
kdr_pos_rates = []
kdr_amplificacao_rates = []

for i, variancia in enumerate(tqdm(variancias_ruido, desc="Progresso", unit="SNR", colour="green")):
    kdr, kdr_pos_reconciliacao, kdr_pos_amplificacao = extrair_kdr(
        palavra_codigo,
        rayleigh_param,
        tamanho_cadeia_bits,
        quantidade_de_testes,
        variancia,
        media_ruido,
        bch_codigo,
        correlacao_canal,
        usar_amplificacao=usar_amplificacao,
        modulacao=modulacao
    )
    kdr_rates.append(kdr)
    kdr_pos_rates.append(kdr_pos_reconciliacao)
    kdr_amplificacao_rates.append(kdr_pos_amplificacao)

print("\n" + "="*70)
print("✓ SIMULAÇÃO CONCLUÍDA COM SUCESSO!")
print("="*70)

# Prepara dados para plot
dados_sigma = {
    'kdr_rates': kdr_rates,
    'kdr_pos_rates': kdr_pos_rates,
    'kdr_amplificacao_rates': kdr_amplificacao_rates
}

# Plota resultado único
plot_kdr_advanced(snr_db_range, dados_sigma, rayleigh_param, modulacao)

# Marca o tempo final
execution_time = time.time() - start_time
hours, rem = divmod(execution_time, 3600)
minutes, seconds = divmod(rem, 60)
print(f"Tempo de execução: {int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}")
print("="*70)