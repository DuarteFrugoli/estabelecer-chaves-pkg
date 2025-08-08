import random
import numpy as np

from bch import *

# TODO: organizar funções em diferentes arquivos

def calcular_distancia_hamming(seq1, seq2):
    """Calcula a distância de Hamming entre duas listas de bits. Gera erro se os tamanhos forem diferentes."""
    assert len(seq1) == len(seq2), f"Listas devem ter o mesmo comprimento: {len(seq1)} vs {len(seq2)}"
    return sum(a != b for a, b in zip(seq1, seq2))

def contar_erros_bits(seq1, seq2):
    """Conta o número de bits diferentes entre duas listas de bits. Gera erro se os tamanhos forem diferentes."""
    # Tem a mesma funcionalidade que calcular_distancia_hamming, mas é mais explícita
    return calcular_distancia_hamming(seq1, seq2)

def encontrar_codigo_mais_proximo(sinal_recebido, tabela_codigos):
    """
    Compara sinal_recebido com todos os códigos na tabela e retorna o mais próximo (menor distância de Hamming).
    """
    if not tabela_codigos:
        raise ValueError("A tabela de códigos está vazia.")

    min_dist = float('inf')
    indice_min = -1

    for i, code in enumerate(tabela_codigos):
        aux = calcular_distancia_hamming(sinal_recebido, code)
        if aux < min_dist:
            indice_min = i
            min_dist = aux

    return tabela_codigos[indice_min]

def xor_binario(seq1, seq2):
    """Realiza operação XOR entre duas listas de bits"""
    assert len(seq1) == len(seq2), f"Listas devem ter o mesmo comprimento: {len(seq1)} vs {len(seq2)}"
    return [0 if a == b else 1 for a, b in zip(seq1, seq2)]

# FIXME: antiga classe AltoRuidoCanalRayleigh

# Função para calcular y considerando o efeito Rayleigh (h) e ruído alto
def simular_canal(ganho_canal, bits_informacao, variancia_ruido, media_ruido):
    """Simula transmissão por canal Rayleigh com ruído gaussiano"""
    # Gera ruído gaussiano vetorizado
    sigma = np.sqrt(variancia_ruido)
    ruido = np.random.normal(media_ruido, sigma, len(bits_informacao))

    # Converte para arrays NumPy para operação vetorizada
    ganho_array = np.array(ganho_canal)
    bits_informacao_array = np.array(bits_informacao)

    # Calcula y = h*x + n de forma vetorizada
    sinal_recebido_continuo = ganho_array * bits_informacao_array + ruido

    # Aplica limiarização vetorizada
    sinal_recebido = (sinal_recebido_continuo > 0.5).astype(int).tolist()
    return sinal_recebido

# Função principal do cenário
def extrair_kar_kdr(bits_informacao, ganho_canal_1, ganho_canal_2, quantidade_de_testes, variancia_ruido, media_ruido):
    """Executa a simulação do canal Rayleigh com ruído e gera chaves usando códigos BCH."""
    contagem_de_acertos = 0  # Contador de acertos

    for i in range(quantidade_de_testes):
        # Geram os sinais recebidos para os dois canais
        sinal_recebido_1 = simular_canal(ganho_canal_1, bits_informacao, variancia_ruido, media_ruido)
        sinal_recebido_2 = simular_canal(ganho_canal_2, bits_informacao, variancia_ruido, media_ruido)

        # Contabiliza acertos (se os sinais recebidos forem iguais)
        if sinal_recebido_1 == sinal_recebido_2:
            contagem_de_acertos += 1
        
    # Calcula a porcentagem de acertos e de erros (kar e kdr)
    kar = contagem_de_acertos * 100.0 / quantidade_de_testes
    kdr = 100.0 - kar

    return kar, kdr

def reconciliar_chaves():
    """Função para reconciliar chaves entre Alice e Bob"""
    # Placeholder para implementação futura

    # c = random.choice(tabela_codigos)
        # s = xor_binario(palavra_codigo_1, c)
        # c_B = xor_binario(palavra_codigo_2, s)
        # chave = xor_binario(s, encontrar_codigo_mais_proximo(c_B, tabela_codigos))
        # print(f"Chave gerada por código de BCH:", chave)

        # Verifica se a chave gerada é igual ao sinal_recebido_1
        # if sinal_recebido_1 == chave:
        #     contagem_de_acertos += 1
        # else:
        #     print(f"Não são iguais por BCH")
    return None

def executar_simulacao():
    """Executa a simulação do canal Rayleigh com os parâmetros definidos."""
    # Placeholder para implementação da simulação
    return None