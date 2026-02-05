import random
import numpy as np

from ..codigos_corretores.bch import *
from ..util.binario_util import *
from ..pilares.reconciliacao import reconciliar_chaves
from ..pilares.amplificacao_privacidade import amplificacao_privacidade


def gerar_csi_complexo(sigma, num_amostras, erro_estimativa=0.0):
    """
    Gera CSI complexo (h = I + jQ) com componentes Gaussianas.
    
    A amplitude |h| = √(I² + Q²) segue distribuição Rayleigh.
    Este é o modelo correto de canal wireless usado por Yuan et al.
    
    Args:
        sigma: Parâmetro de escala (σ) das componentes Gaussianas
               E[I] = E[Q] = 0
               Var(I) = Var(Q) = σ²
               E[|h|²] = 2σ² (potência média)
        num_amostras: Número de coeficientes CSI a gerar
        erro_estimativa: Desvio padrão relativo do erro de estimação (0.0 a 1.0)
                        
    Returns:
        tuple: (h_real, h_estimado)
               h_real: CSI complexo real (array complexo)
               h_estimado: CSI estimado com erro (array complexo)
               
    Notas:
        - Componentes I/Q são Gaussianas independentes N(0, σ²)
        - Amplitude |h| segue Rayleigh(σ)
        - Fase ∠h segue Uniforme[0, 2π]
        - Modelo equivalente ao CSI extraído de hardware WiFi (Yuan et al.)
    """
    # Gera componentes I (in-phase) e Q (quadrature) Gaussianas
    I_real = np.random.normal(0, sigma, num_amostras)
    Q_real = np.random.normal(0, sigma, num_amostras)
    
    # CSI complexo: h = I + jQ
    h_real = I_real + 1j * Q_real
    
    if erro_estimativa == 0.0:
        # Estimação perfeita (caso ideal)
        return h_real, h_real
    
    # Adiciona erro gaussiano nas componentes I e Q
    # Erro proporcional à magnitude |h|
    amplitude_real = np.abs(h_real)
    erro_I = np.random.normal(0, erro_estimativa * amplitude_real, num_amostras)
    erro_Q = np.random.normal(0, erro_estimativa * amplitude_real, num_amostras)
    
    # CSI estimado com erro
    I_estimado = I_real + erro_I
    Q_estimado = Q_real + erro_Q
    h_estimado = I_estimado + 1j * Q_estimado
    
    return h_real, h_estimado


def gerar_ganho_canal_rayleigh(rayleigh_param, num_amostras, erro_estimativa=0.0):
    """
    DEPRECADO: Usar gerar_csi_complexo() para correlações corretas.
    
    Gera amplitude Rayleigh (envelope de CSI complexo).
    Mantido para compatibilidade com código legado.
    """
    # Usa CSI complexo internamente e retorna apenas amplitude
    h_real, h_estimado = gerar_csi_complexo(rayleigh_param, num_amostras, erro_estimativa)
    return np.abs(h_real), np.abs(h_estimado)


def aplicar_correlacao_complexa(h_alice, sigma, correlacao):
    """
    Gera CSI complexo correlacionado (temporal ou espacial).
    
    Modelo de correlação para componentes Gaussianas I/Q:
        I_Bob = ρ * I_Alice + √(1-ρ²) * I_independente
        Q_Bob = ρ * Q_Alice + √(1-ρ²) * Q_independente
        
    Este modelo preserva correlação EXATA para Gaussianas.
        
    Args:
        h_alice: CSI complexo de Alice (array complexo)
        sigma: Parâmetro σ das componentes Gaussianas
        correlacao: Coeficiente de correlação (-1 a 1)
                   +1.0 = canais idênticos
                    0.0 = canais independentes  
                   -1.0 = canais anticorrelacionados
                   
    Returns:
        ndarray complexo: CSI correlacionado
        
    Notas:
        - Correlação pode ser POSITIVA (reciprocidade temporal)
        - Correlação pode ser NEGATIVA (descorrelação espacial com J₀ < 0)
        - Preserva correlação exata: corr(I_A, I_B) = ρ
        
    Referências:
        Jakes, W. C. (1974). Microwave Mobile Communications. Wiley.
        Clarke, R. H. (1968). A Statistical Theory of Mobile-Radio Reception.
    """
    num_amostras = len(h_alice)
    
    # Separa componentes I e Q de Alice
    I_alice = np.real(h_alice)
    Q_alice = np.imag(h_alice)
    
    # Gera componentes independentes (Gaussianas)
    I_ind = np.random.normal(0, sigma, num_amostras)
    Q_ind = np.random.normal(0, sigma, num_amostras)
    
    # Aplica correlação (funciona para ρ positivo OU negativo!)
    I_bob = correlacao * I_alice + np.sqrt(1 - correlacao**2) * I_ind
    Q_bob = correlacao * Q_alice + np.sqrt(1 - correlacao**2) * Q_ind
    
    # CSI complexo correlacionado
    h_bob = I_bob + 1j * Q_bob
    
    return h_bob


def aplicar_correlacao_temporal(ganho_alice, rayleigh_param, correlacao):
    """
    DEPRECADO: Usar aplicar_correlacao_complexa() para correlações corretas.
    
    Modelo antigo (apenas amplitude Rayleigh).
    Mantido para compatibilidade com código legado.
        
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
        tuple: (ber, kdr) - BER antes reconciliação, KDR após reconciliação
               
    Notas:
        - BER (Bit Error Rate): Taxa de erros ANTES da reconciliação
        - KDR (Key Disagreement Rate): Taxa de erros APÓS reconciliação BCH
        - erro_estimativa=0.0: estimativa perfeita (caso ideal, não realista)
        - erro_estimativa=0.10: 10% de erro (típico para sistemas práticos)
        - guard_band_sigma=0.0: sem limiar adaptativo (limiar fixo em 0)
        - guard_band_sigma=0.5: limiar adaptativo conservador (reduz erros)
    """
    total_erros_raw = 0  # Soma dos erros antes reconciliação (BER)
    total_erros_pos_reconciliacao = 0  # Soma dos erros após reconciliação (KDR)
    total_bits = quantidade_de_testes * tamanho_cadeia_bits  # Total de bits comparados

    for i in range(quantidade_de_testes):
        # Determina número de ganhos necessários
        num_ganhos = tamanho_cadeia_bits // 2 if modulacao.lower() == 'qpsk' else tamanho_cadeia_bits
        if modulacao.lower() == 'qpsk' and tamanho_cadeia_bits % 2 != 0:
            num_ganhos += 1
        
        # Gera ganho do canal de Alice com estimativa imperfeita
        # NOVO: Usa CSI complexo (I/Q Gaussiano) para correlações corretas
        h_real_alice, h_estimado_alice = gerar_csi_complexo(
            rayleigh_param, num_ganhos, erro_estimativa
        )
        
        # Gera canal correlacionado para Bob (reciprocidade temporal)
        # NOVO: Usa aplicar_correlacao_complexa para correlação exata
        h_real_bob = aplicar_correlacao_complexa(
            h_real_alice, rayleigh_param, correlacao_canal
        )
        
        # Bob também tem erro de estimação
        if erro_estimativa > 0:
            amplitude_bob = np.abs(h_real_bob)
            erro_I = np.random.normal(0, erro_estimativa * amplitude_bob, num_ganhos)
            erro_Q = np.random.normal(0, erro_estimativa * amplitude_bob, num_ganhos)
            h_estimado_bob = h_real_bob + (erro_I + 1j * erro_Q)
        else:
            h_estimado_bob = h_real_bob
        
        # Extrai amplitude |h| para uso na quantização
        # A amplitude segue distribuição Rayleigh automaticamente
        ganho_real_alice = np.abs(h_real_alice)
        ganho_estimado_alice = np.abs(h_estimado_alice)
        ganho_real_bob = np.abs(h_real_bob)
        ganho_estimado_bob = np.abs(h_estimado_bob)

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

        # Conta erros bit a bit ANTES da reconciliação (BER)
        erros_raw = contar_erros_bits(sinal_recebido_1, sinal_recebido_2)
        total_erros_raw += erros_raw

        # Reconciliação de chaves usando BCH
        chave = reconciliar_chaves(sinal_recebido_1, sinal_recebido_2, bch_codigo)
        
        # Conta erros APÓS reconciliação (KDR)
        erros_pos_reconciliacao = contar_erros_bits(sinal_recebido_1, chave)
        total_erros_pos_reconciliacao += erros_pos_reconciliacao
        
        # Amplificação de privacidade (SHA-256) é aplicada apenas se solicitado
        # Nota: Não faz sentido medir "KDR pós-amplificação" porque:
        # 1. SHA-256 é determinístico: mesma entrada → mesma saída
        # 2. Se chaves diferem 1 bit → hashes completamente diferentes (efeito avalanche)
        # 3. Se KDR=0 → hashes idênticos, se KDR>0 → hashes totalmente diferentes
        if usar_amplificacao:
            chave_alice_amplificada = amplificacao_privacidade(sinal_recebido_1)
            chave_bob_amplificada = amplificacao_privacidade(chave)
        
    # Calcula taxas de erro
    ber = 100.0 * total_erros_raw / total_bits  # BER: antes reconciliação
    kdr = 100.0 * total_erros_pos_reconciliacao / total_bits  # KDR: após reconciliação
    
    # Retorna sempre (ber, kdr) independente de usar_amplificacao
    # Amplificação é aplicada internamente mas não retorna métrica separada
    return ber, kdr


def gerar_chave_do_canal(h_estimado, guard_band_sigma=0.0, limiar=None):
    """
    Gera bits de chave diretamente da amplitude do canal CSI (key generation from channel).
    
    Este é o método correto para geração de chave física em sistemas QKD wireless.
    Diferente de transmissão de dados, aqui não há palavra_codigo transmitida.
    Alice e Bob observam o MESMO canal (reciprocidade) e quantizam independentemente.
    Eve observa canal DIFERENTE (descorrelação espacial) e obtém bits descorrelacionados.
    
    Processo:
    1. Calcula amplitude |h| = √(I² + Q²) do CSI complexo
    2. Aplica guard band (opcional): descarta bits próximos ao limiar
    3. Quantiza: bit = 1 se |h| > limiar, bit = 0 caso contrário
    
    Args:
        h_estimado: CSI complexo estimado (array complexo)
        guard_band_sigma: Largura da banda de guarda em múltiplos de σ (padrão: 0.0)
                         Valores típicos: 0.0 (sem guard band), 0.5, 1.0
        limiar: Limiar de quantização (padrão: None = usa mediana de h_estimado)
                IMPORTANTE: Alice e Bob devem usar o MESMO limiar!
                Eve usa limiar diferente (mediana do SEU canal)
    
    Returns:
        ndarray: Bits de chave extraídos (0s e 1s)
        
    Notas:
        - Método baseado em reciprocidade de canal wireless
        - Alice e Bob devem obter bits similares (canal correlacionado)
        - Eve obtém bits aleatórios (canal descorrelacionado espacialmente)
        - Taxa de bits descartados aumenta com guard_band_sigma
    """
    # Calcula amplitude do canal
    amplitude = np.abs(h_estimado)
    
    # Calcula limiar de quantização
    if limiar is None:
        limiar = np.median(amplitude)
    
    if guard_band_sigma > 0:
        # Aplica guard band: descarta medições próximas ao limiar
        # Largura da banda: ±guard_band_sigma * σ_amplitude
        sigma_amplitude = np.std(amplitude)
        guard_band_width = guard_band_sigma * sigma_amplitude
        
        # Cria máscara: manter apenas bits longe do limiar
        mask = np.abs(amplitude - limiar) > guard_band_width
        
        # Quantiza apenas valores aceitos
        bits_validos = (amplitude[mask] > limiar).astype(int)
        
        return bits_validos
    else:
        # Sem guard band: quantiza todos os bits
        bits = (amplitude > limiar).astype(int)
        return bits


def gerar_chave_list_encoding(h_estimado, min_separacao_samples=10):
    """
    Gera bits usando List-Encoding (ProxiMate, MobiSys 2011).
    
    List-encoding usa extremos (máximos e mínimos) da amplitude do canal ao invés
    de threshold fixo. Isso reduz significativamente o BER entre Alice e Bob.
    
    Vantagens sobre quantização simples:
    - BER reduzido: ~15% vs ~30% (melhora de 2x)
    - Bits mais confiáveis (extremos são mais fáceis de identificar)
    - Funciona melhor em canais com alta variação temporal
    
    Desvantagens:
    - Taxa de geração menor (~0.5 bits/Tc vs 1 bit/Tc)
    - Requer comunicação de lista de índices L
    
    Processo (Alice):
    1. Identifica máximos locais → bit 1
    2. Identifica mínimos locais → bit 0
    3. Extremos separados por pelo menos min_separacao_samples
    4. Retorna (bits, indices_extremos)
    
    Processo (Bob):
    1. Recebe lista de índices L de Alice
    2. Para cada índice, encontra extremo mais próximo no SEU canal
    3. Classifica como máximo (1) ou mínimo (0)
    
    Args:
        h_estimado: CSI complexo estimado (array complexo)
        min_separacao_samples: Separação mínima entre extremos (default: 10)
                              Deve ser >= Tc (coherence time) em samples
    
    Returns:
        tuple: (bits, indices)
               bits: Array de bits extraídos (0s e 1s)
               indices: Índices dos extremos no array original
    
    Referência:
        Mathur et al., "ProxiMate: Proximity-based Secure Pairing using 
        Ambient Wireless Signals", MobiSys 2011
    """
    from scipy.signal import find_peaks
    
    # Calcula amplitude do canal
    amplitude = np.abs(h_estimado)
    
    # Encontra máximos locais (peaks)
    # distance: separação mínima entre peaks
    peaks, _ = find_peaks(amplitude, distance=min_separacao_samples)
    
    # Encontra mínimos locais (valleys)
    # Invertemos o sinal para encontrar vales como picos
    valleys, _ = find_peaks(-amplitude, distance=min_separacao_samples)
    
    # Combina extremos (peaks e valleys)
    # peaks → bit 1, valleys → bit 0
    extremos = []
    bits = []
    
    for peak_idx in peaks:
        extremos.append((peak_idx, 1))  # (índice, bit)
    
    for valley_idx in valleys:
        extremos.append((valley_idx, 0))  # (índice, bit)
    
    # Ordena por índice temporal
    extremos.sort(key=lambda x: x[0])
    
    # Separa índices e bits
    if len(extremos) > 0:
        indices = np.array([e[0] for e in extremos])
        bits = np.array([e[1] for e in extremos])
    else:
        indices = np.array([], dtype=int)
        bits = np.array([], dtype=int)
    
    return bits, indices


def reconciliar_list_encoding(h_estimado_bob, indices_alice, window_size=5):
    """
    Bob usa lista de índices de Alice para extrair bits (List-Encoding).
    
    Para cada índice na lista de Alice, Bob procura o extremo mais próximo
    no SEU canal e classifica como máximo (1) ou mínimo (0).
    
    Args:
        h_estimado_bob: CSI complexo de Bob
        indices_alice: Índices dos extremos identificados por Alice
        window_size: Janela de busca ao redor de cada índice (default: 5)
    
    Returns:
        ndarray: Bits extraídos por Bob
    """
    amplitude_bob = np.abs(h_estimado_bob)
    bits_bob = []
    
    for idx_alice in indices_alice:
        # Define janela de busca
        start = max(0, idx_alice - window_size)
        end = min(len(amplitude_bob), idx_alice + window_size + 1)
        
        # Extrai janela
        window = amplitude_bob[start:end]
        
        if len(window) == 0:
            continue
        
        # Encontra índice do extremo na janela
        idx_max = np.argmax(window)
        idx_min = np.argmin(window)
        
        # Índice central da janela
        idx_center = idx_alice - start
        
        # Verifica qual extremo está mais próximo do índice de Alice
        dist_max = abs(idx_max - idx_center)
        dist_min = abs(idx_min - idx_center)
        
        if dist_max < dist_min:
            # Máximo mais próximo → bit 1
            bits_bob.append(1)
        else:
            # Mínimo mais próximo → bit 0
            bits_bob.append(0)
    
    return np.array(bits_bob)


def medir_seguranca_eve(palavra_codigo, rayleigh_param, tamanho_cadeia_bits, quantidade_de_testes,
                        variancia_ruido, media_ruido, bch_codigo, 
                        correlacao_alice_bob=0.95, correlacao_alice_eve=0.0,
                        modulacao='bpsk', erro_estimativa=0.0, guard_band_sigma=0.0):
    """
    Simula KEY GENERATION FROM CHANNEL e ataque de espionagem (Eve).
    
    IMPORTANTE: Este é o método correto para geração de chave física!
    Não há transmissão de palavra_codigo. Alice e Bob quantizam diretamente
    seus canais (correlacionados por reciprocidade) para gerar bits compartilhados.
    
    Cenário correto:
    1. Alice observa h_Alice e quantiza: bits_Alice = (|h_Alice| > limiar)
    2. Bob observa h_Bob (correlacionado temporalmente) e quantiza: bits_Bob = (|h_Bob| > limiar)
    3. Eve observa h_Eve (descorrelacionado espacialmente) e quantiza: bits_Eve = (|h_Eve| > limiar)
    4. Eve obtém ~50% BER (chute aleatório) devido à descorrelação espacial
    
    Diferença fundamental:
    - Transmissão de dados (ERRADO): palavra_codigo transmitido, todos demodulam
    - Key generation (CORRETO): cada um quantiza SEU canal, sem transmissão
    
    Referência: Yuan et al. (IEEE ICCC 2022) - Physical Layer Key Generation
    
    Args:
        correlacao_alice_bob: Correlação temporal entre Alice e Bob (típico: 0.9-0.99)
        correlacao_alice_eve: Correlação espacial entre Alice e Eve
                             Pode ser POSITIVA ou NEGATIVA!
                             Exemplo: J₀(5) ≈ -0.18 a 10cm com λ=12.5cm
        guard_band_sigma: Se >0, Eve também usa guard_band (cenário otimista para Eve)
        Outros parâmetros: Idênticos a extrair_kdr()
        
    Returns:
        tuple: (kdr_bob, ber_eve_raw, ber_eve_pos_bch, correlacao_h_bob, correlacao_h_eve)
            - kdr_bob: KDR interno Alice-Bob (deve ser baixo, ~0-5%)
            - ber_eve_raw: BER de Eve antes de reconciliar (~50% = chute aleatório)
            - ber_eve_pos_bch: BER de Eve após tentar reconciliar com BCH
            - correlacao_h_bob: Correlação CSI Alice-Bob (~0.95)
            - correlacao_h_eve: Correlação CSI Alice-Eve (pode ser negativo!)
            
    Nota: Sistema seguro → ber_eve_raw ≈ 50% (Eve não consegue extrair chave)
    """
    total_bits_bch = 0  # Será incrementado dinamicamente conforme blocos processados
    
    erros_bob_interno = 0
    erros_eve_raw = 0  # Erros de Eve antes de reconciliar
    erros_eve_pos_bch = 0  # Erros de Eve após reconciliar
    
    # Armazenar componentes I/Q do CSI complexo para calcular correlação
    I_alice_list = []
    Q_alice_list = []
    I_bob_list = []
    Q_bob_list = []
    I_eve_list = []
    Q_eve_list = []
    
    for i in range(quantidade_de_testes):
        # Gerar MUITO MAIS CSI para compensar guard band
        # Guard band pode remover até 70% dos bits
        # Gerar 5x mais bits para garantir pelo menos 1 bloco BCH completo
        multiplicador_guard_band = 5 if guard_band_sigma > 0 else 1
        num_ganhos_necessarios = tamanho_cadeia_bits * multiplicador_guard_band
        
        # Determina número de ganhos para a modulação
        if modulacao.lower() == 'qpsk':
            num_ganhos = num_ganhos_necessarios // 2
            if num_ganhos_necessarios % 2 != 0:
                num_ganhos += 1
        else:
            num_ganhos = num_ganhos_necessarios
        
        # ===== CANAL ALICE (base comum) =====
        h_real_alice, h_estimado_alice = gerar_csi_complexo(
            rayleigh_param, num_ganhos, erro_estimativa
        )
        
        # ===== CANAL BOB (correlacionado temporalmente com Alice) =====
        h_real_bob = aplicar_correlacao_complexa(
            h_real_alice, rayleigh_param, correlacao_alice_bob
        )
        if erro_estimativa > 0:
            amplitude_bob = np.abs(h_real_bob)
            erro_I = np.random.normal(0, erro_estimativa * amplitude_bob, num_ganhos)
            erro_Q = np.random.normal(0, erro_estimativa * amplitude_bob, num_ganhos)
            h_estimado_bob = h_real_bob + (erro_I + 1j * erro_Q)
        else:
            h_estimado_bob = h_real_bob
        
        # ===== CANAL EVE (correlacionado espacialmente - pode ser NEGATIVO!) =====
        h_real_eve = aplicar_correlacao_complexa(
            h_real_alice, rayleigh_param, correlacao_alice_eve
        )
        if erro_estimativa > 0:
            amplitude_eve = np.abs(h_real_eve)
            erro_I = np.random.normal(0, erro_estimativa * amplitude_eve, num_ganhos)
            erro_Q = np.random.normal(0, erro_estimativa * amplitude_eve, num_ganhos)
            h_estimado_eve = h_real_eve + (erro_I + 1j * erro_Q)
        else:
            h_estimado_eve = h_real_eve
        
        # Armazenar componentes I/Q (para correlação)
        I_alice_list.extend(np.real(h_estimado_alice))
        Q_alice_list.extend(np.imag(h_estimado_alice))
        I_bob_list.extend(np.real(h_estimado_bob))
        Q_bob_list.extend(np.imag(h_estimado_bob))
        I_eve_list.extend(np.real(h_estimado_eve))
        Q_eve_list.extend(np.imag(h_estimado_eve))
        
        # ===== KEY GENERATION FROM CHANNEL (sem transmissão!) =====
        # Cada participante quantiza SEU PRÓPRIO canal estimado
        # IMPORTANTE: Alice e Bob devem usar o MESMO limiar (Alice define)
        # Eve não conhece limiar de Alice e usa o seu próprio
        
        # Alice define o limiar (mediana do seu canal)
        limiar_alice = np.median(np.abs(h_estimado_alice))
        
        # Alice e Bob usam o limiar de Alice (compartilhado via reciprocidade)
        bits_alice = gerar_chave_do_canal(h_estimado_alice, guard_band_sigma, limiar_alice)
        bits_bob = gerar_chave_do_canal(h_estimado_bob, guard_band_sigma, limiar_alice)
        
        # Eve NÃO conhece o limiar de Alice! Usa o dela (mediana do SEU canal)
        bits_eve = gerar_chave_do_canal(h_estimado_eve, guard_band_sigma, limiar=None)  # None = usa própria mediana
        
        # Ajustar comprimento: truncar ao menor tamanho (não preencher!)
        # Preencher com zeros criaria correlação artificial
        min_len = min(len(bits_alice), len(bits_bob), len(bits_eve))
        bits_alice_trunk = bits_alice[:min_len]
        bits_bob_trunk = bits_bob[:min_len]
        bits_eve_trunk = bits_eve[:min_len]
        
        # Se não temos bits suficientes para BCH, pular esta iteração
        if min_len < bch_codigo.n:
            continue
        
        # Truncar para múltiplo do tamanho BCH
        n_bch = bch_codigo.n
        num_blocos = min_len // n_bch
        bits_uteis = num_blocos * n_bch
        
        bits_alice_bch = bits_alice_trunk[:bits_uteis]
        bits_bob_bch = bits_bob_trunk[:bits_uteis]
        bits_eve_bch = bits_eve_trunk[:bits_uteis]
        
        # Processar blocos de tamanho n_bch
        for bloco_idx in range(num_blocos):
            inicio = bloco_idx * n_bch
            fim = (bloco_idx + 1) * n_bch
            
            bloco_alice = bits_alice_bch[inicio:fim]
            bloco_bob = bits_bob_bch[inicio:fim]
            bloco_eve = bits_eve_bch[inicio:fim]
            
            # ===== RECONCILIAÇÃO (Alice-Bob legítimo) =====
            # Bob usa Information Reconciliation para corrigir erros
            chave_bob_bch = reconciliar_chaves(bloco_alice, bloco_bob, bch_codigo)
            
            # KDR interno Bob (deve ser baixo - canais correlacionados)
            erros_bob_interno += contar_erros_bits(bloco_alice, chave_bob_bch)
            
            # ===== ATAQUE DE EVE =====
            # Cenário 1: Eve usa bits crus do canal dela (ataque passivo)
            # Esperado: ~50% BER (bits aleatórios, canal descorrelacionado)
            erros_eve_raw += contar_erros_bits(bloco_alice, bloco_eve)
            
            # Cenário 2: Eve intercepta mensagens BCH públicas e tenta reconciliar
            # Mesmo com reconciliação, Eve não consegue corrigir porque seus bits
            # são FUNDAMENTALMENTE diferentes (canal descorrelacionado)
            chave_eve_bch = reconciliar_chaves(bloco_alice, bloco_eve, bch_codigo)
            erros_eve_pos_bch += contar_erros_bits(bloco_alice, chave_eve_bch)
            
            # Atualizar total de bits processados
            total_bits_bch += n_bch
    
    # Calcular correlação de Pearson entre componentes I e Q do CSI
    # Método equivalente ao de Yuan et al. com CSI real de hardware WiFi
    # 
    # IMPORTANTE: Correlação calculada nas componentes Gaussianas I/Q, não na amplitude!
    # Isso permite correlação NEGATIVA (quando J₀ < 0)
    #
    # Média das correlações I e Q (ambas devem ser similares)
    corr_I_bob = np.corrcoef(I_alice_list, I_bob_list)[0, 1]
    corr_Q_bob = np.corrcoef(Q_alice_list, Q_bob_list)[0, 1]
    correlacao_h_bob = (corr_I_bob + corr_Q_bob) / 2
    
    corr_I_eve = np.corrcoef(I_alice_list, I_eve_list)[0, 1]
    corr_Q_eve = np.corrcoef(Q_alice_list, Q_eve_list)[0, 1]
    correlacao_h_eve = (corr_I_eve + corr_Q_eve) / 2
    
    # Calcular métricas
    kdr_bob = 100.0 * erros_bob_interno / total_bits_bch
    ber_eve_raw = 100.0 * erros_eve_raw / total_bits_bch
    ber_eve_pos_bch = 100.0 * erros_eve_pos_bch / total_bits_bch
    
    return kdr_bob, ber_eve_raw, ber_eve_pos_bch, correlacao_h_bob, correlacao_h_eve