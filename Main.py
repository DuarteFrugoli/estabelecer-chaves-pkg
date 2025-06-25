import time
import numpy as np
import random

# Importa as classes necessárias
from CodeGenerator import CodeGenerator
from Cenário1 import RuidoNuloCanalUnitario
from Cenário2 import BaixoRuidoCanalUnitario
from Cenário3 import BaixoRuidoCanalRayleigh
from Cenário4 import AltoRuidoCanalUnitario
from Cenário5 import AltoRuidoCanalRayleigh
from Plotagem import Plotagem

# ntestes: Quantidade de testes a serem realizados
# plot: Flag para indicar se deve plotar os sinais (1 para sim, 0 para não)
# nBits: Tamanho da cadeia de bits
# x: Palavra de informação aleatória gerada
# h1, h2: Vetores de canal Rayleigh para simulação
# tabela: Tabela de códigos gerada
# size: Tamanho do espaço amostral para geração da tabela de códigos
# canais: Dicionário com instâncias dos cenários de canal
# porcentagens: Lista de porcentagens de acerto para cada cenário
# execution_time: Tempo total de execução da simulação

def solicita_entrada(mensagem, tipo=int, validacao=None):
    """Solicita e valida a entrada do usuário."""
    while True:
        try:
            valor = tipo(input(mensagem))
            if validacao and not validacao(valor):
                raise ValueError("Entrada inválida.")
            return valor
        except ValueError as e:
            print(e)


def inicializa_variaveis(nBits):
    """Inicializa as variáveis globais para os cenários."""
    x = [random.randint(0, 1) for _ in range(nBits)]  # x: Palavra de informação aleatória
    h1 = np.random.rayleigh(1.0, nBits)               # h1: Vetor de canal Rayleigh
    h2 = np.random.rayleigh(1.0, nBits)               # h2: Vetor de canal Rayleigh
    size = None if nBits <= 15 else solicita_entrada(
        "Entre com tamanho do espaço amostral: ", int, lambda v: v > 0
    )
    code_generator = CodeGenerator(nBits)
    tabela = code_generator.generate_code_table(size)  # tabela: Tabela de códigos gerada

    return x, h1, h2, tabela, size


def inicializa_canais(media, variancia, ntestes):
    """Inicializa os canais de comunicação."""
    return {
        "ruido_nulo": RuidoNuloCanalUnitario(media, variancia, ntestes),
        "baixo_ruido_unitario": BaixoRuidoCanalUnitario(media, variancia, ntestes),
        "baixo_ruido_rayleigh": BaixoRuidoCanalRayleigh(media, variancia, ntestes),
        "alto_ruido_unitario": AltoRuidoCanalUnitario(media, variancia, ntestes),
        "alto_ruido_rayleigh": AltoRuidoCanalRayleigh(media, variancia, ntestes),
    }

def coletar_porcentagens(canais, x, h1, h2, plot, size, tabela, nBits):
    """Coleta as porcentagens de acertos para cada cenário."""
    return [
        canais["ruido_nulo"].cenario(x, plot, size, tabela),
        canais["baixo_ruido_unitario"].cenario(x, plot, size, tabela),
        canais["baixo_ruido_rayleigh"].cenario(x, h1, h2, plot, size, tabela, nBits),
        canais["alto_ruido_unitario"].cenario(x, plot, size, tabela, nBits),
        canais["alto_ruido_rayleigh"].cenario(x, h1, h2, plot, size, tabela, nBits),
    ]


# Marca o tempo inicial
start_time = time.time()

# Solicita parâmetros ao usuário
ntestes = solicita_entrada("Entre com a quantidade de testes: ", int, lambda v: v > 0)
plot = 1 if solicita_entrada("Deseja realizar a Plotagem dos sinais? 'y' para sim, 'n' para nao \n", str, lambda v: v in {"y", "n"}) == "y" else 0

nBits = solicita_entrada("Entre com o tamanho da cadeia de Bits (7, 15, 127, 255): ", int, lambda v: v in {7, 15, 127, 255})

# Inicializa variáveis e canais
x, h1, h2, tabela, size = inicializa_variaveis(nBits)
canais = inicializa_canais(media=0.5, variancia=1.5, ntestes=ntestes)

# Coleta as porcentagens de acertos
porcentagens = coletar_porcentagens(canais, x, h1, h2, plot, size, tabela, nBits)

# Plota os resultados
Plotagem().plota(porcentagens, len(x))

# Marca o tempo final e exibe o tempo de execução
execution_time = time.time() - start_time
hours, rem = divmod(execution_time, 3600)
minutes, seconds = divmod(rem, 60)
print(f"Tempo de execução da simulação: {int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}")
