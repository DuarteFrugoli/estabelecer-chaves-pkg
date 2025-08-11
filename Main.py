import time
import numpy as np
import random
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO) # DEBUG, INFO, WARNING, ERROR, CRITICAL

# Configuração do handler de log
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)
logger.propagate = False  # Não propaga para o root logger

from codigos_corretores.bch import *
from canal.canal import *
from plotkar import plot_kar
from util.util import *

potencia_sinal = 1.0 # potência do sinal (1.0 pois o que importa é o SNR)
rayleigh_params = [0.5, 1.0, 2.0] # parâmetros Rayleigh (sigma), pode ir de 0.1 a 5.0
snr_db_range = np.linspace(-10, 30, 18) # 18 valores de SNR de -10 a 30 dB
snr_linear_range = 10 ** (snr_db_range / 10)
variancias_ruido = potencia_sinal / snr_linear_range # variâncias do ruído para cada SNR
media_ruido = 0 # média do ruído (padrão 0.0)

# Marca o tempo inicial
start_time = time.time()

# Solicita parâmetros ao usuário
quantidade_de_testes = solicita_entrada("Entre com a quantidade de testes: ", int, lambda v: v > 0)
tamanho_cadeia_bits = solicita_entrada("Entre com o tamanho da cadeia de Bits (7, 15, 127, 255): ", int, lambda v: v in {7, 15, 127, 255})

# Bits de informação (k bits) - dados originais antes da codificação
tamanho_bits_informacao = get_tamanho_bits_informacao(tamanho_cadeia_bits)
bits_informacao = [random.randint(0, 1) for _ in range(tamanho_bits_informacao)]  # Gera bits de informação aleatórios

# Pede o tamanho do espaço amostral caso o tamanho da cadeia de bits seja maior que 15
tamanho_espaco_amostral = None if tamanho_cadeia_bits <= 15 else solicita_entrada(
    "Entre com tamanho do espaço amostral: ", int, lambda v: v > 0
)

# Gera a tabela de códigos BCH para o tamanho da cadeia de bits especificado
tabela_codigos = gerar_tabela_codigos_bch(tamanho_cadeia_bits, tamanho_bits_informacao, tamanho_espaco_amostral)

# Gera e plota os resultados para diferentes parâmetros Rayleigh
for rayleigh_param in rayleigh_params:
    percentuais_acordo = []
    for variancia in variancias_ruido:
        kar, kdr = extrair_kar_kdr(
            bits_informacao,
            rayleigh_param,
            tamanho_bits_informacao,
            quantidade_de_testes,
            variancia,
            media_ruido
            )
        percentuais_acordo.append(kar)
    plot_kar(snr_db_range, percentuais_acordo, rayleigh_param)

# Marca o tempo final e exibe o tempo de execução
execution_time = time.time() - start_time
hours, rem = divmod(execution_time, 3600)
minutes, seconds = divmod(rem, 60)
print(f"Tempo de execução da simulação: {int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}")