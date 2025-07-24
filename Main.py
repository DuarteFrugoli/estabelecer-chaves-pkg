import time
import numpy as np
import random

# Importa as classes necessárias
from CodeGenerator import CodeGenerator
from Cenário5 import AltoRuidoCanalRayleigh
from Plotagem import Plotagem
from plotkar import plot_kar
from util import *

# quantidade_de_testes: Quantidade de testes a serem realizados
# tamanho_cadeia_bits: Tamanho da cadeia de bits
# palavra_informacao: Palavra de informação aleatória gerada
# canal_rayleigh_1, canal_rayleigh_2: Vetores de canal Rayleigh para simulação (ganho de canal)
# tabela: Tabela de códigos gerada
# tamanho_espaco_amostral: Tamanho do espaço amostral para geração da tabela de códigos
# canais: Dicionário com instâncias dos cenários de canal
# porcentagens_acerto: Lista de porcentagens_acerto de acerto para cada cenário
# execution_time: Tempo total de execução da simulação
# escala_rayleigh: Parâmetro de escala para a distribuição Rayleigh (sigma)

potencia_sinal = 1.0 # potência do sinal (1.0 pois o que importa é o SNR)
escala_rayleigh = 1.0 # parâmetro de escala para a distribuição Rayleigh (0.1 a 5.0)
rayleigh_params = [0.5, 1.0, 2.0] # parâmetros Rayleigh para teste
snr_db_range = np.linspace(-10, 30, 18) # 10 valores de SNR de -10 a 30 dB
variancias_ruido = potencia_sinal / (10 ** (snr_db_range / 10))

def inicializa_variaveis(tamanho_cadeia_bits):
    """Inicializa as variáveis globais para os cenários."""
    palavra_informacao = [random.randint(0, 1) for _ in range(tamanho_cadeia_bits)]  # palavra_informacao: Palavra de informação aleatória
    canal_rayleigh_1 = np.random.rayleigh(escala_rayleigh, tamanho_cadeia_bits)               # canal_rayleigh_1: Vetor de canal Rayleigh
    canal_rayleigh_2 = np.random.rayleigh(escala_rayleigh, tamanho_cadeia_bits)               # canal_rayleigh_2: Vetor de canal Rayleigh
    tamanho_espaco_amostral = None if tamanho_cadeia_bits <= 15 else solicita_entrada(
        "Entre com tamanho do espaço amostral: ", int, lambda v: v > 0
    )
    code_generator = CodeGenerator(tamanho_cadeia_bits)
    tabela = code_generator.generate_code_table(tamanho_espaco_amostral)  # tabela: Tabela de códigos gerada

    return palavra_informacao, canal_rayleigh_1, canal_rayleigh_2, tabela, tamanho_espaco_amostral


def inicializa_canais(media, variancia, quantidade_de_testes):
    """Inicializa os canais de comunicação."""
    return {
        "alto_ruido_rayleigh": AltoRuidoCanalRayleigh(media, variancia, quantidade_de_testes),
    }

def coletar_porcentagens(canais, palavra_informacao, canal_rayleigh_1, canal_rayleigh_2, tamanho_espaco_amostral, tabela, tamanho_cadeia_bits):
    """Coleta as porcentagens_acerto de acertos para cada cenário."""
    return [
        canais["alto_ruido_rayleigh"].cenario(palavra_informacao, canal_rayleigh_1, canal_rayleigh_2, tamanho_espaco_amostral, tabela, tamanho_cadeia_bits),
    ]


# Marca o tempo inicial
start_time = time.time()

# Solicita parâmetros ao usuário
quantidade_de_testes = solicita_entrada("Entre com a quantidade de testes: ", int, lambda v: v > 0)

tamanho_cadeia_bits = solicita_entrada("Entre com o tamanho da cadeia de Bits (7, 15, 127, 255): ", int, lambda v: v in {7, 15, 127, 255})

# Inicializa variáveis e canais
palavra_informacao, canal_rayleigh_1, canal_rayleigh_2, tabela, tamanho_espaco_amostral = inicializa_variaveis(tamanho_cadeia_bits)
canais = inicializa_canais(media=0.5, variancia=1.5, quantidade_de_testes=quantidade_de_testes)

# Coleta as porcentagens_acerto de acertos
porcentagens_acerto = coletar_porcentagens(canais, palavra_informacao, canal_rayleigh_1, canal_rayleigh_2, tamanho_espaco_amostral, tabela, tamanho_cadeia_bits)

# Plota os resultados
Plotagem().plota(porcentagens_acerto, len(palavra_informacao))

# Marca o tempo final e exibe o tempo de execução
execution_time = time.time() - start_time
hours, rem = divmod(execution_time, 3600)
minutes, seconds = divmod(rem, 60)
print(f"Tempo de execução da simulação: {int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}")

# Gera e plota os resultados para diferentes parâmetros Rayleigh
for rayleigh_param in rayleigh_params:
    snrs_db = []
    kar_rates = []
    for variancia in variancias_ruido:
        # Gera canal_rayleigh_1 e canal_rayleigh_2 com o parâmetro Rayleigh atual
        canal_rayleigh_1 = np.random.rayleigh(rayleigh_param, tamanho_cadeia_bits)
        canal_rayleigh_2 = np.random.rayleigh(rayleigh_param, tamanho_cadeia_bits)
        canal = AltoRuidoCanalRayleigh(media=0.5, variancia=variancia, ntestes=quantidade_de_testes)
        porcentagem = canal.cenario(palavra_informacao, canal_rayleigh_1, canal_rayleigh_2, size=tamanho_espaco_amostral, tabela=tabela, nBits=tamanho_cadeia_bits)
        snr_db = 10 * np.log10(potencia_sinal / variancia)
        snrs_db.append(snr_db)
        kar_rates.append(porcentagem)
    plot_kar(snrs_db, kar_rates)