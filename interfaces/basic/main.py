import time
import numpy as np
import random
import logging
import sys
import os

# Adiciona o diretório raiz ao path para permitir imports relativos
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

# Logger para fazer o acompanhamento do fluxo de execução
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO) # DEBUG, INFO, WARNING, ERROR, CRITICAL

# Configuração do handler de log
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)
logger.propagate = False  # Não propaga para o root logger

from src.codigos_corretores.bch import *
from src.canal.canal import *
from src.visualization.plotkdr import plot_kdr
from src.util.util import *

potencia_sinal = 1.0 # potência do sinal (Es = 1 para BPSK)
rayleigh_params = [0.5, 1.0, 2.0] # parâmetros Rayleigh (sigma), pode ir de 0.1 a 5.0
snr_db_range = np.linspace(-10, 30, 18) # 18 valores de SNR de -10 a 30 dB
snr_linear_range = 10 ** (snr_db_range / 10)

# SNR = Es/N0, onde sigma² = N0/2 para canal real de banda base
# Logo: sigma² = Es / (2·SNR) = 1 / (2·SNR_linear)
variancias_ruido = potencia_sinal / (2 * snr_linear_range)
media_ruido = 0 # média do ruído (padrão 0.0)

# Coeficiente de correlação entre canais Alice-Bob (reciprocidade)
correlacao_canal = 0.9  # Valor típico entre 0.8 e 0.99

# Marca o tempo inicial
start_time = time.time()

# Solicita parâmetros ao usuário
quantidade_de_testes = solicita_entrada("Entre com a quantidade de testes: ", int, lambda v: v > 0)
tamanho_cadeia_bits = solicita_entrada("Entre com o tamanho da cadeia de Bits (7, 15, 127, 255): ", int, lambda v: v in {7, 15, 127, 255})

# Amplificação de privacidade sempre habilitada
usar_amplificacao = True
print("\nAmplificação de privacidade habilitada - Chaves finais terão 256 bits")

# Palavra de código original/referência (n bits) - base para geração de síndrome BCH
tamanho_bits_informacao = get_tamanho_bits_informacao(tamanho_cadeia_bits)
palavra_codigo = [random.randint(0, 1) for _ in range(tamanho_cadeia_bits)]  # Gera bits de informação aleatórios
logger.info(f"Palavra de código gerada: {palavra_codigo} (tamanho {tamanho_cadeia_bits} bits, k={tamanho_bits_informacao})")

# Pede o tamanho do espaço amostral caso o tamanho da cadeia de bits seja maior que 15
# REMOVIDO: Não é mais necessário com BCH real

# Gera o objeto BCH (não precisa mais de tabela de códigos)
bch_codigo = gerar_tabela_codigos_bch(tamanho_cadeia_bits, tamanho_bits_informacao)

# Coleta dados para todos os parâmetros Rayleigh
dados_todos_sigmas = {}

for rayleigh_param in rayleigh_params:
    kdr_rates = []
    kdr_pos_rates = []
    kdr_amplificacao_rates = []
    
    for variancia in variancias_ruido:
        kdr, kdr_pos_reconciliacao, kdr_pos_amplificacao = extrair_kdr(
            palavra_codigo,
            rayleigh_param,
            tamanho_cadeia_bits,
            quantidade_de_testes,
            variancia,
            media_ruido,
            bch_codigo,
            correlacao_canal,
            usar_amplificacao=True
        )
        kdr_rates.append(kdr)
        kdr_pos_rates.append(kdr_pos_reconciliacao)
        kdr_amplificacao_rates.append(kdr_pos_amplificacao)
    
    # Armazena os dados para este sigma
    dados_todos_sigmas[rayleigh_param] = {
        'kdr_rates': kdr_rates,
        'kdr_pos_rates': kdr_pos_rates,
        'kdr_amplificacao_rates': kdr_amplificacao_rates
    }

# Plota todos os sigmas em um único gráfico
plot_kdr(snr_db_range, dados_todos_sigmas)

# Marca o tempo final e exibe o tempo de execução
execution_time = time.time() - start_time
hours, rem = divmod(execution_time, 3600)
minutes, seconds = divmod(rem, 60)
print(f"Tempo de execução da simulação: {int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}")