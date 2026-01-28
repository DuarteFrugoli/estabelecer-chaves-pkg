import random
import numpy as np

from ..codigos_corretores.bch import *
from ..util.binario_util import *
from ..pilares.reconciliacao import reconciliar_chaves
from ..pilares.amplificacao_privacidade import amplificacao_privacidade


def gerar_ganho_canal_rayleigh(rayleigh_param, num_amostras, erro_estimativa=0.0):
    """
    Gera coeficientes de canal Rayleigh com estimativa imperfeita.
    
    Args:
        rayleigh_param: Parâmetro sigma da distribuição Rayleigh
        num_amostras: Número de coeficientes a gerar
        erro_estimativa: Desvio padrão relativo do erro de estimação (0.0 a 1.0)
                        0.0 = estimação perfeita
                        0.1 = 10% de erro
                        
    Returns:
        tuple: (ganho_real, ganho_estimado)
               ganho_real: Ganho real do canal
               ganho_estimado: Ganho estimado (com erro)
               
    Notas:
        Em sistemas reais, o ganho do canal precisa ser estimado usando
        símbolos piloto. Esta estimativa sempre contém erro devido a:
        - Ruído no canal
        - Limitações do estimador
        - Tempo de processamento
    """
    # Gera ganho real do canal
    ganho_real = np.random.rayleigh(rayleigh_param, num_amostras)
    
    if erro_estimativa == 0.0:
        # Estimação perfeita (caso ideal)
        return ganho_real, ganho_real
    
    # Adiciona erro gaussiano proporcional à magnitude do ganho
    # Erro tem desvio padrão = erro_estimativa * |h|
    erro = np.random.normal(0, erro_estimativa * ganho_real, num_amostras)
    ganho_estimado = ganho_real + erro
    
    # Garante que ganho estimado seja positivo (característica Rayleigh)
    ganho_estimado = np.abs(ganho_estimado)
    
    return ganho_real, ganho_estimado


def aplicar_correlacao_temporal(ganho_alice, rayleigh_param, correlacao):
    """
    Gera ganho de canal correlacionado temporalmente para Bob.
    
    Modelo de Jakes simplificado para reciprocidade de canal:
        h_Bob = rho * h_Alice + sqrt(1-rho^2) * h_independente
        
    Args:
        ganho_alice: Ganho do canal de Alice
        rayleigh_param: Parâmetro sigma da distribuição Rayleigh
        correlacao: Coeficiente de correlação temporal (0 a 1)
                   1.0 = canais idênticos (medição simultânea)
                   0.0 = canais independentes (medições muito distantes no tempo)
                   
    Returns:
        ndarray: Ganho correlacionado para Bob
        
    Referência:
        Jakes, W. C. (1974). Microwave Mobile Communications. Wiley.
    """
    num_amostras = len(ganho_alice)
    
    # Componente independente
    ganho_independente = np.random.rayleigh(rayleigh_param, num_amostras)
    
    # Aplica modelo de correlação
    ganho_bob = (correlacao * ganho_alice + 
                 np.sqrt(1 - correlacao**2) * ganho_independente)
    
    # Garante valores positivos
    ganho_bob = np.abs(ganho_bob)
    
    return ganho_bob

def simular_canal_bpsk(ganho_canal, palavra_codigo, variancia_ruido, media_ruido, 
                        ganho_estimado=None, guard_band_sigma=0.0):
    """
    Simula transmissão por canal Rayleigh com ruído gaussiano usando BPSK.
    
    Args:
        ganho_canal: Ganho real do canal (usado na transmissão)
        palavra_codigo: Lista de bits a transmitir
        variancia_ruido: Variância do ruído gaussiano
        media_ruido: Média do ruído (geralmente 0)
        ganho_estimado: Ganho estimado do canal (se None, usa ganho_canal)
        guard_band_sigma: Parâmetro para limiarização adaptativa (0.0 = limiar fixo em 0)
                         Valores típicos: 0.3-0.8 para sistemas reais
        
    Returns:
        list: Bits recebidos após demodulação
        
    Notas:
        - Se ganho_estimado for fornecido, simula estimação imperfeita do canal
        - guard_band_sigma > 0 aplica limiar adaptativo baseado em ruído
    """
    # Gera ruído gaussiano vetorizado
    sigma_ruido = np.sqrt(variancia_ruido)
    ruido = np.random.normal(media_ruido, sigma_ruido, len(palavra_codigo))

    # Converte para arrays NumPy para operação vetorizada
    ganho_real = np.array(ganho_canal)
    
    # Mapeia bits {0,1} para símbolos BPSK {+1,-1}
    simbolos_bpsk = 1 - 2 * np.array(palavra_codigo)  # 0 -> +1, 1 -> -1

    # Calcula y = h*x + n de forma vetorizada com BPSK
    # Usa ganho REAL na transmissão (física do canal)
    sinal_recebido_continuo = ganho_real * simbolos_bpsk + ruido

    # Demodulação com limiar adaptativo
    if guard_band_sigma > 0 and ganho_estimado is not None:
        # Usa ganho ESTIMADO na demodulação (estimação imperfeita)
        ganho_est = np.array(ganho_estimado)
        
        # CORRIGIDO: Limiar deve ser multiplicado por |h_est|, não dividido!
        # Limiar absoluto = guard_band_sigma * sigma_ruido * |h_est|
        # Isso porque comparamos y = h*x + n diretamente, não y/h
        limiar = guard_band_sigma * sigma_ruido * ganho_est
        
        # Decisão com zona morta (guard band)
        # Reduz erros quando sinal está próximo do limiar
        sinal_recebido = np.zeros(len(sinal_recebido_continuo), dtype=int)
        for i, y in enumerate(sinal_recebido_continuo):
            if y > limiar[i]:
                sinal_recebido[i] = 0  # Símbolo +1 -> bit 0
            elif y < -limiar[i]:
                sinal_recebido[i] = 1  # Símbolo -1 -> bit 1
            else:
                # Zona de incerteza: escolha baseada no sinal mais provável
                # (poderia ser erasure em sistemas reais)
                sinal_recebido[i] = 0 if y >= 0 else 1
    else:
        # Limiarização padrão em 0 (estimação perfeita ou guard_band desabilitado)
        sinal_recebido = (sinal_recebido_continuo >= 0).astype(int)
    
    return sinal_recebido.tolist()

def simular_canal_qpsk(ganho_canal, palavra_codigo, variancia_ruido, media_ruido,
                        ganho_estimado=None, guard_band_sigma=0.0):
    """
    Simula transmissão por canal Rayleigh com ruído gaussiano usando QPSK.
    
    Args:
        ganho_canal: Ganho real do canal (complexo)
        palavra_codigo: Lista de bits a transmitir
        variancia_ruido: Variância do ruído gaussiano
        media_ruido: Média do ruído
        ganho_estimado: Ganho estimado do canal (se None, usa ganho_canal)
        guard_band_sigma: Parâmetro para limiarização adaptativa
        
    Returns:
        list: Bits recebidos após demodulação
    """
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
    ganho_real = np.array(ganho_canal[:num_simbolos])
    
    # Mapeia pares de bits para símbolos QPSK normalizados
    normalizacao = 1 / np.sqrt(2)
    simbolos_qpsk = []
    for i in range(0, len(palavra_codigo_padded), 2):
        bit_i = palavra_codigo_padded[i]
        bit_q = palavra_codigo_padded[i+1]
        val_i = 2 * bit_i - 1
        val_q = 2 * bit_q - 1
        simbolos_qpsk.append((val_i + 1j * val_q) * normalizacao)
    
    simbolos_qpsk = np.array(simbolos_qpsk)
    
    # Calcula y = h*x + n com ganho REAL
    sinal_recebido_continuo = ganho_real * simbolos_qpsk + ruido_complexo

    # Demodula QPSK
    bits_recebidos = []
    
    if guard_band_sigma > 0 and ganho_estimado is not None:
        # CORRIGIDO: Limiar multiplicado por |h_est|, não dividido!
        # Para QPSK, usa sqrt(2) porque potência está distribuída em I e Q
        ganho_est = np.array(ganho_estimado[:num_simbolos])
        limiar = guard_band_sigma * sigma_ruido * np.sqrt(2) * np.abs(ganho_est)
        
        for idx, simbolo in enumerate(sinal_recebido_continuo):
            # Componente I
            if simbolo.real > limiar[idx]:
                bit_i = 0
            elif simbolo.real < -limiar[idx]:
                bit_i = 1
            else:
                bit_i = 0 if simbolo.real >= 0 else 1
            
            # Componente Q
            if simbolo.imag > limiar[idx]:
                bit_q = 0
            elif simbolo.imag < -limiar[idx]:
                bit_q = 1
            else:
                bit_q = 0 if simbolo.imag >= 0 else 1
                
            bits_recebidos.extend([bit_i, bit_q])
    else:
        # Limiar fixo em 0
        for simbolo in sinal_recebido_continuo:
            bit_i = 1 if simbolo.real >= 0 else 0
            bit_q = 1 if simbolo.imag >= 0 else 0
            bits_recebidos.extend([bit_i, bit_q])
    
    # Remove padding se foi adicionado
    if len(palavra_codigo) % 2 != 0:
        bits_recebidos = bits_recebidos[:-1]
    
    return bits_recebidos

# Função wrapper que seleciona a modulação apropriada
def simular_canal(ganho_canal, palavra_codigo, variancia_ruido, media_ruido, modulacao='bpsk',
                  ganho_estimado=None, guard_band_sigma=0.0):
    """
    Simula transmissão por canal Rayleigh com ruído gaussiano.
    
    Args:
        ganho_canal: Ganho do canal (fading Rayleigh)
        palavra_codigo: Lista de bits a transmitir
        variancia_ruido: Variância do ruído gaussiano
        media_ruido: Média do ruído (geralmente 0)
        modulacao: Tipo de modulação ('bpsk' ou 'qpsk')
        ganho_estimado: Ganho estimado (para estimação imperfeita)
        guard_band_sigma: Parâmetro de limiarização adaptativa
    
    Returns:
        Lista de bits recebidos após demodulação
    """
    if modulacao.lower() == 'qpsk':
        return simular_canal_qpsk(ganho_canal, palavra_codigo, variancia_ruido, 
                                   media_ruido, ganho_estimado, guard_band_sigma)
    else:
        return simular_canal_bpsk(ganho_canal, palavra_codigo, variancia_ruido, 
                                   media_ruido, ganho_estimado, guard_band_sigma)
        return simular_canal_bpsk(ganho_canal, palavra_codigo, variancia_ruido, media_ruido)

# Função principal do cenário
def extrair_kdr(palavra_codigo, rayleigh_param, tamanho_cadeia_bits, quantidade_de_testes, 
                variancia_ruido, media_ruido, bch_codigo, correlacao_canal=0.9, 
                usar_amplificacao=True, modulacao='bpsk', erro_estimativa=0.0, 
                guard_band_sigma=0.0):
    """
    Executa a simulação do canal Rayleigh com ruído e gera chaves usando códigos BCH.
    
    Args:
        palavra_codigo: Palavra de código de referência
        rayleigh_param: Parâmetro sigma do canal Rayleigh
        tamanho_cadeia_bits: Tamanho da cadeia de bits
        quantidade_de_testes: Número de simulações Monte Carlo
        variancia_ruido: Variância do ruído gaussiano
        media_ruido: Média do ruído
        bch_codigo: Objeto BCH para correção de erros
        correlacao_canal: Correlação temporal entre canais Alice-Bob (0 a 1)
        usar_amplificacao: Habilitar amplificação de privacidade (SHA-256)
        modulacao: Tipo de modulação ('bpsk' ou 'qpsk')
        erro_estimativa: Erro relativo na estimativa do canal (0.0 a 1.0)
        guard_band_sigma: Parâmetro de limiarização adaptativa (0.0 = desabilitado)
        
    Returns:
        tuple: (kdr, kdr_pos_reconciliacao, kdr_pos_amplificacao) se usar_amplificacao=True
               (kdr, kdr_pos_reconciliacao) se usar_amplificacao=False
               
    Notas:
        - erro_estimativa=0.0: estimativa perfeita (caso ideal, não realista)
        - erro_estimativa=0.10: 10% de erro (típico para sistemas práticos)
        - guard_band_sigma=0.0: sem limiar adaptativo (limiar fixo em 0)
        - guard_band_sigma=0.5: limiar adaptativo conservador (reduz erros)
    """
    total_erros = 0  # Soma dos erros bit a bit
    total_erros_pos_reconciliacao = 0  # Soma dos erros pós reconciliação
    total_erros_pos_amplificacao = 0  # Soma erros bit a bit após amplificação
    total_bits = quantidade_de_testes * tamanho_cadeia_bits  # Total de bits comparados
    
    # Para amplificação, sempre compara 256 bits (tamanho do SHA-256)
    total_bits_amplificados = quantidade_de_testes * 256 if usar_amplificacao else total_bits

    for i in range(quantidade_de_testes):
        # Determina número de ganhos necessários
        num_ganhos = tamanho_cadeia_bits // 2 if modulacao.lower() == 'qpsk' else tamanho_cadeia_bits
        if modulacao.lower() == 'qpsk' and tamanho_cadeia_bits % 2 != 0:
            num_ganhos += 1
        
        # Gera ganho do canal de Alice com estimativa imperfeita
        ganho_real_alice, ganho_estimado_alice = gerar_ganho_canal_rayleigh(
            rayleigh_param, num_ganhos, erro_estimativa
        )
        
        # Gera canal correlacionado para Bob (reciprocidade)
        ganho_real_bob = aplicar_correlacao_temporal(
            ganho_real_alice, rayleigh_param, correlacao_canal
        )
        
        # Bob também tem erro de estimação
        if erro_estimativa > 0:
            erro_bob = np.random.normal(0, erro_estimativa * ganho_real_bob, num_ganhos)
            ganho_estimado_bob = np.abs(ganho_real_bob + erro_bob)
        else:
            ganho_estimado_bob = ganho_real_bob

        # Gera os sinais recebidos
        # IMPORTANTE: Usa ganho REAL na transmissão, ESTIMADO na demodulação
        sinal_recebido_1 = simular_canal(
            ganho_real_alice, palavra_codigo, variancia_ruido, media_ruido, modulacao,
            ganho_estimado_alice, guard_band_sigma
        )
        sinal_recebido_2 = simular_canal(
            ganho_real_bob, palavra_codigo, variancia_ruido, media_ruido, modulacao,
            ganho_estimado_bob, guard_band_sigma
        )

        # Conta erros bit a bit antes da reconciliação
        erros = contar_erros_bits(sinal_recebido_1, sinal_recebido_2)
        total_erros += erros

        # Reconciliação de chaves usando BCH
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


def medir_seguranca_eve(palavra_codigo, rayleigh_param, tamanho_cadeia_bits, quantidade_de_testes,
                        variancia_ruido, media_ruido, bch_codigo, 
                        correlacao_alice_bob=0.95, correlacao_alice_eve=0.0,
                        modulacao='bpsk', erro_estimativa=0.0, guard_band_sigma=0.0):
    """
    Mede a segurança contra espionagem (Eve) comparando correlação dos coeficientes de canal.
    
    Método inspirado no artigo Yuan et al. (IEEE ICCC 2022):
    - Yuan et al.: Mede correlação entre CSI real extraído de hardware WiFi
    - Nossa simulação: Mede correlação entre coeficientes h do canal Rayleigh simulado
    
    Ambos avaliam se Eve consegue observar um canal similar ao de Bob.
    
    Args:
        correlacao_alice_bob: Correlação temporal entre Alice e Bob (típico: 0.9-0.99)
        correlacao_alice_eve: Correlação espacial entre Alice e Eve (típico: 0.0-0.6)
        Outros parâmetros: Idênticos a extrair_kdr()
        
    Returns:
        tuple: (kdr_bob, correlacao_h_bob, correlacao_h_eve)
            - kdr_bob: KDR interno Alice-Bob (deve ser baixo, ~0-5%)
            - correlacao_h_bob: Correlação entre coeficientes h de Alice e Bob (~0.9-0.99)
            - correlacao_h_eve: Correlação entre coeficientes h de Alice e Eve (~0.3-0.6)
            
    Nota: Yuan et al. obtiveram ρ(AP,STA)=0.942 vs ρ(Eve,STA)=0.560 a 30cm
    """
    total_bits_bch = quantidade_de_testes * tamanho_cadeia_bits
    
    erros_bob_interno = 0
    
    # Armazenar coeficientes de canal (amplitudes h) para calcular correlação
    # Equivalente ao CSI que Yuan et al. extraem de hardware WiFi
    h_alice_list = []
    h_bob_list = []
    h_eve_list = []
    
    for i in range(quantidade_de_testes):
        # Determina número de ganhos necessários
        num_ganhos = tamanho_cadeia_bits // 2 if modulacao.lower() == 'qpsk' else tamanho_cadeia_bits
        if modulacao.lower() == 'qpsk' and tamanho_cadeia_bits % 2 != 0:
            num_ganhos += 1
        
        # ===== CANAL ALICE (base comum) =====
        ganho_real_alice, ganho_estimado_alice = gerar_ganho_canal_rayleigh(
            rayleigh_param, num_ganhos, erro_estimativa
        )
        
        # ===== CANAL BOB (correlacionado com Alice - reciprocidade temporal) =====
        ganho_real_bob = aplicar_correlacao_temporal(
            ganho_real_alice, rayleigh_param, correlacao_alice_bob
        )
        if erro_estimativa > 0:
            erro_bob = np.random.normal(0, erro_estimativa * ganho_real_bob, num_ganhos)
            ganho_estimado_bob = np.abs(ganho_real_bob + erro_bob)
        else:
            ganho_estimado_bob = ganho_real_bob
        
        # ===== CANAL EVE (descorrelacionado espacialmente de Alice) =====
        ganho_real_eve = aplicar_correlacao_temporal(
            ganho_real_alice, rayleigh_param, correlacao_alice_eve
        )
        if erro_estimativa > 0:
            erro_eve = np.random.normal(0, erro_estimativa * ganho_real_eve, num_ganhos)
            ganho_estimado_eve = np.abs(ganho_real_eve + erro_eve)
        else:
            ganho_estimado_eve = ganho_real_eve
        
        # Armazenar coeficientes de canal h (equivalente ao CSI do artigo Yuan)
        h_alice_list.extend(ganho_estimado_alice)
        h_bob_list.extend(ganho_estimado_bob)
        h_eve_list.extend(ganho_estimado_eve)
        
        # ===== GERAR SINAIS RECEBIDOS (para calcular KDR de Bob) =====
        sinal_recebido_bob = simular_canal(
            ganho_real_bob, palavra_codigo, variancia_ruido, media_ruido, modulacao,
            ganho_estimado_bob, guard_band_sigma
        )
        
        sinal_recebido_alice = simular_canal(
            ganho_real_alice, palavra_codigo, variancia_ruido, media_ruido, modulacao,
            ganho_estimado_alice, guard_band_sigma
        )
        
        # ===== RECONCILIAÇÃO (apenas Alice-Bob) =====
        chave_bob_bch = reconciliar_chaves(sinal_recebido_alice, sinal_recebido_bob, bch_codigo)
        
        # KDR interno Bob
        erros_bob_interno += contar_erros_bits(sinal_recebido_alice, chave_bob_bch)
    
    # Calcular correlação de Pearson entre coeficientes de canal h
    # Método análogo ao do artigo Yuan et al., mas com h simulado ao invés de CSI real
    correlacao_h_bob = np.corrcoef(h_alice_list, h_bob_list)[0, 1]
    correlacao_h_eve = np.corrcoef(h_alice_list, h_eve_list)[0, 1]
    
    kdr_bob = 100.0 * erros_bob_interno / total_bits_bch
    
    return kdr_bob, correlacao_h_bob, correlacao_h_eve