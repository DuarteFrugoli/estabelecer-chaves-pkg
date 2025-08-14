import random
import numpy as np

from codigos_corretores.bch import *
from util.binario_util import *
from pilares.reconciliacao import reconciliar_chaves

# Função para calcular y considerando o efeito Rayleigh (h) e ruído alto
def simular_canal(ganho_canal, palavra_codigo, variancia_ruido, media_ruido):
    """Simula transmissão por canal Rayleigh com ruído gaussiano"""
    # Gera ruído gaussiano vetorizado
    sigma_ruido = np.sqrt(variancia_ruido)
    ruido = np.random.normal(media_ruido, sigma_ruido, len(palavra_codigo))

    # Converte para arrays NumPy para operação vetorizada
    ganho_array = np.array(ganho_canal)
    bits_informacao_array = np.array(palavra_codigo)

    # Calcula y = h*x + n de forma vetorizada
    sinal_recebido_continuo = ganho_array * bits_informacao_array + ruido

    # Aplica limiarização vetorizada
    sinal_recebido = (sinal_recebido_continuo > 0.5).astype(int).tolist()
    return sinal_recebido

# Função principal do cenário
def extrair_kdr(palavra_codigo, rayleigh_param, tamanho_cadeia_bits, quantidade_de_testes, variancia_ruido, media_ruido, tabela_codigos):
    """Executa a simulação do canal Rayleigh com ruído e gera chaves usando códigos BCH."""
    total_erros = 0  # Soma dos erros bit a bit
    total_erros_pos_reconcilicao = 0  # Soma erros bit a bit após a reconciliação
    total_bits = quantidade_de_testes * tamanho_cadeia_bits  # Total de bits comparados

    for i in range(quantidade_de_testes):
        # Gera ganho_canal_1 e ganho_canal_2 com o parâmetro Rayleigh atual
        ganho_canal_1 = np.random.rayleigh(rayleigh_param, tamanho_cadeia_bits)
        ganho_canal_2 = np.random.rayleigh(rayleigh_param, tamanho_cadeia_bits)

        # Geram os sinais recebidos para os dois canais
        sinal_recebido_1 = simular_canal(ganho_canal_1, palavra_codigo, variancia_ruido, media_ruido)
        sinal_recebido_2 = simular_canal(ganho_canal_2, palavra_codigo, variancia_ruido, media_ruido)

        # Conta erros bit a bit
        erros = contar_erros_bits(sinal_recebido_1, sinal_recebido_2)
        total_erros += erros

        chave = reconciliar_chaves(sinal_recebido_1, sinal_recebido_2, tabela_codigos)
        
        erros_pos_reconciliacao = contar_erros_bits(sinal_recebido_1, chave)
        total_erros_pos_reconcilicao += erros_pos_reconciliacao
        
    # Calcula a taxa de discrepância de chave (KDR)
    kdr = 100.0 * total_erros / total_bits

    kdr_pos_reconciliacao = 100.0 * total_erros_pos_reconcilicao / total_bits

    return kdr, kdr_pos_reconciliacao