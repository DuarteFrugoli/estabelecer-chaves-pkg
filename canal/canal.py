import random
import numpy as np

from codigos_corretores.bch import *
from util.binario_util import *

# Função para calcular y considerando o efeito Rayleigh (h) e ruído alto
def simular_canal(ganho_canal, bits_informacao, variancia_ruido, media_ruido):
    """Simula transmissão por canal Rayleigh com ruído gaussiano"""
    # Gera ruído gaussiano vetorizado
    sigma_ruido = np.sqrt(variancia_ruido)
    ruido = np.random.normal(media_ruido, sigma_ruido, len(bits_informacao))

    # Converte para arrays NumPy para operação vetorizada
    ganho_array = np.array(ganho_canal)
    bits_informacao_array = np.array(bits_informacao)

    # Calcula y = h*x + n de forma vetorizada
    sinal_recebido_continuo = ganho_array * bits_informacao_array + ruido

    # Aplica limiarização vetorizada
    sinal_recebido = (sinal_recebido_continuo > 0.5).astype(int).tolist()
    return sinal_recebido

# Função principal do cenário
def extrair_kar_kdr(bits_informacao, rayleigh_param, tamanho_bits_informacao, quantidade_de_testes, variancia_ruido, media_ruido):
    """Executa a simulação do canal Rayleigh com ruído e gera chaves usando códigos BCH."""
    contagem_de_acertos = 0  # Contador de acertos

    for i in range(quantidade_de_testes):
        # Gera ganho_canal_1 e ganho_canal_2 com o parâmetro Rayleigh atual
        ganho_canal_1 = np.random.rayleigh(rayleigh_param, tamanho_bits_informacao)
        ganho_canal_2 = np.random.rayleigh(rayleigh_param, tamanho_bits_informacao)

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