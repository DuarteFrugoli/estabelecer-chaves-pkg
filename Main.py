import time
import numpy as np
import random
import logging

# Logger para fazer o acompanhamento do fluxo de execução
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO) # DEBUG, INFO, WARNING, ERROR, CRITICAL

# Configuração do handler de log
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)
logger.propagate = False  # Não propaga para o root logger

from codigos_corretores.bch import *
from canal.canal import *
from plotkdr import plot_kdr
from util.util import *

potencia_sinal = 1.0 # potência do sinal (Es = 1 para BPSK)
rayleigh_params = [0.5, 1.0, 2.0] # parâmetros Rayleigh (sigma), pode ir de 0.1 a 5.0
snr_db_range = np.linspace(-10, 30, 18) # 18 valores de SNR de -10 a 30 dB
snr_linear_range = 10 ** (snr_db_range / 10)

# Relação SNR correta para BPSK
# SNR = Es/N0, onde sigma² = N0/2 para canal real de banda base
# Logo: sigma² = Es / (2·SNR) = 1 / (2·SNR_linear)
variancias_ruido = potencia_sinal / (2 * snr_linear_range)  # variâncias corretas para BPSK
media_ruido = 0 # média do ruído (padrão 0.0)

# Coeficiente de correlação entre canais Alice-Bob (reciprocidade)
correlacao_canal = 0.9  # Valor típico entre 0.8 e 0.99

# Marca o tempo inicial
start_time = time.time()

# Solicita parâmetros ao usuário
quantidade_de_testes = solicita_entrada("Entre com a quantidade de testes: ", int, lambda v: v > 0)
tamanho_cadeia_bits = solicita_entrada("Entre com o tamanho da cadeia de Bits (7, 15, 127, 255): ", int, lambda v: v in {7, 15, 127, 255})

# Pergunta se deseja usar amplificação de privacidade
print("\nAMPLIFICAÇÃO DE PRIVACIDADE")
print("A amplificação de privacidade aplica função hash SHA-256 para gerar chaves de 256 bits com segurança criptográfica.")
usar_amplificacao = input("Deseja usar amplificação de privacidade? (s/N): ").lower().strip() in ['s', 'sim', 'yes', 'y']

if usar_amplificacao:
    print("Amplificação habilitada - Chaves finais terão 256 bits")
else:
    print("Amplificação desabilitada - Usando apenas reconciliação BCH")

# Bits de informação (k bits) - dados originais antes da codificação
tamanho_bits_informacao = get_tamanho_bits_informacao(tamanho_cadeia_bits)
palavra_codigo = [random.randint(0, 1) for _ in range(tamanho_cadeia_bits)]  # Gera bits de informação aleatórios
logger.info(f"Palavra de código gerada: {palavra_codigo} (tamanho {tamanho_cadeia_bits} bits, k={tamanho_bits_informacao})")

# Pede o tamanho do espaço amostral caso o tamanho da cadeia de bits seja maior que 15
tamanho_espaco_amostral = None if tamanho_cadeia_bits <= 15 else solicita_entrada(
    "Entre com tamanho do espaço amostral: ", int, lambda v: v > 0
)

# Gera a tabela de códigos BCH para o tamanho da cadeia de bits especificado
tabela_codigos = gerar_tabela_codigos_bch(tamanho_cadeia_bits, tamanho_bits_informacao, tamanho_espaco_amostral)

# Gera e plota os resultados para diferentes parâmetros Rayleigh
for rayleigh_param in rayleigh_params:
    kdr_rates = []
    kdr_pos_rates = []
    kdr_amplificacao_rates = [] if usar_amplificacao else None
    
    for variancia in variancias_ruido:
        if usar_amplificacao:
            kdr, kdr_pos_reconciliacao, kdr_pos_amplificacao = extrair_kdr(
                palavra_codigo,
                rayleigh_param,
                tamanho_cadeia_bits,
                quantidade_de_testes,
                variancia,
                media_ruido,
                tabela_codigos,
                correlacao_canal,
                usar_amplificacao=True
            )
            kdr_rates.append(kdr)
            kdr_pos_rates.append(kdr_pos_reconciliacao)
            kdr_amplificacao_rates.append(kdr_pos_amplificacao)
        else:
            kdr, kdr_pos_reconciliacao = extrair_kdr(
                palavra_codigo,
                rayleigh_param,
                tamanho_cadeia_bits,
                quantidade_de_testes,
                variancia,
                media_ruido,
                tabela_codigos,
                correlacao_canal,
                usar_amplificacao=False
            )
            kdr_rates.append(kdr)
            kdr_pos_rates.append(kdr_pos_reconciliacao)
    
    # Plota com ou sem amplificação conforme escolha do usuário
    plot_kdr(snr_db_range, kdr_rates, kdr_pos_rates, rayleigh_param, kdr_amplificacao_rates)

# Marca o tempo final e exibe o tempo de execução
execution_time = time.time() - start_time
hours, rem = divmod(execution_time, 3600)
minutes, seconds = divmod(rem, 60)
print(f"Tempo de execução da simulação: {int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}")