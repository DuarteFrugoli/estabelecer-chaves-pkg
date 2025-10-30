import random
import numpy as np

from ..codigos_corretores.bch import *
from ..util.binario_util import *
from ..pilares.reconciliacao import reconciliar_chaves
from ..pilares.amplificacao_privacidade import amplificacao_privacidade

# Função para calcular y considerando o efeito Rayleigh (h) e ruído gaussiano com BPSK
def simular_canal_bpsk(ganho_canal, palavra_codigo, variancia_ruido, media_ruido):
    """Simula transmissão por canal Rayleigh com ruído gaussiano usando BPSK"""
    # Gera ruído gaussiano vetorizado
    sigma_ruido = np.sqrt(variancia_ruido)
    ruido = np.random.normal(media_ruido, sigma_ruido, len(palavra_codigo))

    # Converte para arrays NumPy para operação vetorizada
    ganho_array = np.array(ganho_canal)
    
    # Mapeia bits {0,1} para símbolos BPSK {-1,+1}
    simbolos_bpsk = 2 * np.array(palavra_codigo) - 1  # 0 -> -1, 1 -> +1

    # Calcula y = h*x + n de forma vetorizada com BPSK
    sinal_recebido_continuo = ganho_array * simbolos_bpsk + ruido

    # Aplica limiarização em 0 (detecção por sinal)
    sinal_recebido = (sinal_recebido_continuo >= 0).astype(int).tolist()
    return sinal_recebido

# Função para calcular y considerando o efeito Rayleigh (h) e ruído gaussiano com QPSK
def simular_canal_qpsk(ganho_canal, palavra_codigo, variancia_ruido, media_ruido):
    """Simula transmissão por canal Rayleigh com ruído gaussiano usando QPSK"""
    # Garante que temos um número par de bits
    if len(palavra_codigo) % 2 != 0:
        palavra_codigo_padded = palavra_codigo + [0]
    else:
        palavra_codigo_padded = palavra_codigo
    
    # Gera ruído gaussiano complexo vetorizado
    sigma_ruido = np.sqrt(variancia_ruido / 2)  # Dividido por 2 para componentes I e Q
    num_simbolos = len(palavra_codigo_padded) // 2
    ruido_i = np.random.normal(media_ruido, sigma_ruido, num_simbolos)
    ruido_q = np.random.normal(media_ruido, sigma_ruido, num_simbolos)
    ruido_complexo = ruido_i + 1j * ruido_q

    # Converte para arrays NumPy
    ganho_array = np.array(ganho_canal[:num_simbolos])
    
    # Mapeia pares de bits para símbolos QPSK
    # 00 -> -1-1j, 01 -> -1+1j, 10 -> +1-1j, 11 -> +1+1j
    simbolos_qpsk = []
    for i in range(0, len(palavra_codigo_padded), 2):
        bit_i = palavra_codigo_padded[i]
        bit_q = palavra_codigo_padded[i+1]
        # Mapeia bits para -1 ou +1
        val_i = 2 * bit_i - 1
        val_q = 2 * bit_q - 1
        simbolos_qpsk.append(val_i + 1j * val_q)
    
    simbolos_qpsk = np.array(simbolos_qpsk)
    
    # Calcula y = h*x + n de forma vetorizada com QPSK
    sinal_recebido_continuo = ganho_array * simbolos_qpsk + ruido_complexo

    # Demodula QPSK - detecta componentes I e Q separadamente
    bits_recebidos = []
    for simbolo in sinal_recebido_continuo:
        # Componente I (parte real)
        bit_i = 1 if simbolo.real >= 0 else 0
        # Componente Q (parte imaginária)
        bit_q = 1 if simbolo.imag >= 0 else 0
        bits_recebidos.extend([bit_i, bit_q])
    
    # Remove padding se foi adicionado
    if len(palavra_codigo) % 2 != 0:
        bits_recebidos = bits_recebidos[:-1]
    
    return bits_recebidos

# Função wrapper que seleciona a modulação apropriada
def simular_canal(ganho_canal, palavra_codigo, variancia_ruido, media_ruido, modulacao='bpsk'):
    """
    Simula transmissão por canal Rayleigh com ruído gaussiano
    
    Args:
        ganho_canal: Ganho do canal (fading Rayleigh)
        palavra_codigo: Lista de bits a transmitir
        variancia_ruido: Variância do ruído gaussiano
        media_ruido: Média do ruído (geralmente 0)
        modulacao: Tipo de modulação ('bpsk' ou 'qpsk')
    
    Returns:
        Lista de bits recebidos após demodulação
    """
    if modulacao.lower() == 'qpsk':
        return simular_canal_qpsk(ganho_canal, palavra_codigo, variancia_ruido, media_ruido)
    else:
        return simular_canal_bpsk(ganho_canal, palavra_codigo, variancia_ruido, media_ruido)

# Função principal do cenário
def extrair_kdr(palavra_codigo, rayleigh_param, tamanho_cadeia_bits, quantidade_de_testes, variancia_ruido, media_ruido, bch_codigo, correlacao_canal=0.9, usar_amplificacao=True, modulacao='bpsk'):
    """Executa a simulação do canal Rayleigh com ruído e gera chaves usando códigos BCH."""
    total_erros = 0  # Soma dos erros bit a bit
    total_erros_pos_reconciliacao = 0  # Soma dos erros pós reconciliação
    total_erros_pos_amplificacao = 0  # Soma erros bit a bit após amplificação
    total_bits = quantidade_de_testes * tamanho_cadeia_bits  # Total de bits comparados
    
    # Para amplificação, sempre compara 256 bits (tamanho do SHA-256)
    total_bits_amplificados = quantidade_de_testes * 256 if usar_amplificacao else total_bits

    for i in range(quantidade_de_testes):
        # Implementa reciprocidade com correlação entre canais
        # Para QPSK, precisamos de ganhos para metade dos símbolos
        num_ganhos = tamanho_cadeia_bits // 2 if modulacao.lower() == 'qpsk' else tamanho_cadeia_bits
        if modulacao.lower() == 'qpsk' and tamanho_cadeia_bits % 2 != 0:
            num_ganhos += 1  # Adiciona um ganho extra se houver padding
        
        # Canal base (Alice)
        ganho_canal_alice = np.random.rayleigh(rayleigh_param, num_ganhos)
        
        # Canal correlacionado (Bob) - reciprocidade parcial
        z_independente = np.random.normal(0, 1, num_ganhos)
        # Aplicando transformação para manter distribuição Rayleigh
        componente_independente = np.random.rayleigh(rayleigh_param, num_ganhos) 
        ganho_canal_bob = (correlacao_canal * ganho_canal_alice + 
                          np.sqrt(1 - correlacao_canal**2) * componente_independente)
        
        # Garante que o ganho seja positivo (característica Rayleigh)
        ganho_canal_bob = np.abs(ganho_canal_bob)

        # Geram os sinais recebidos para os dois canais com reciprocidade
        sinal_recebido_1 = simular_canal(ganho_canal_alice, palavra_codigo, variancia_ruido, media_ruido, modulacao)
        sinal_recebido_2 = simular_canal(ganho_canal_bob, palavra_codigo, variancia_ruido, media_ruido, modulacao)

        # Conta erros bit a bit
        erros = contar_erros_bits(sinal_recebido_1, sinal_recebido_2)
        total_erros += erros

        chave = reconciliar_chaves(sinal_recebido_1, sinal_recebido_2, bch_codigo)
        
        erros_pos_reconciliacao = contar_erros_bits(sinal_recebido_1, chave)
        total_erros_pos_reconciliacao += erros_pos_reconciliacao
        
        # Aplica amplificação de privacidade se solicitado
        if usar_amplificacao:
            # Alice aplica amplificação na sua chave
            chave_alice_amplificada = amplificacao_privacidade(sinal_recebido_1)
            
            # Bob aplica amplificação na chave reconciliada
            chave_bob_amplificada = amplificacao_privacidade(chave)
            
            # Conta erros após amplificação
            erros_pos_amplificacao = contar_erros_bits(chave_alice_amplificada, chave_bob_amplificada)
            total_erros_pos_amplificacao += erros_pos_amplificacao
        
    # Calcula a taxa de discrepância de chave (KDR)
    kdr = 100.0 * total_erros / total_bits

    kdr_pos_reconciliacao = 100.0 * total_erros_pos_reconciliacao / total_bits
    
    if usar_amplificacao:
        kdr_pos_amplificacao = 100.0 * total_erros_pos_amplificacao / total_bits_amplificados
        return kdr, kdr_pos_reconciliacao, kdr_pos_amplificacao

    return kdr, kdr_pos_reconciliacao