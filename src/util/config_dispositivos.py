"""
Configurações de parâmetros realistas para diferentes tipos de dispositivos IoT.

Este módulo define perfis de dispositivos com características físicas e
limitações computacionais típicas de sistemas de comunicação sem fio reais.

Parâmetros:
    - erro_estimativa_canal: Desvio padrão relativo do erro na estimativa de h
    - velocidade_max_kmh: Velocidade máxima do dispositivo em km/h
    - frequencia_portadora_hz: Frequência da portadora em Hz
    - taxa_bits_bps: Taxa de transmissão em bits por segundo
    - potencia_transmissao_dbm: Potência de transmissão em dBm
    - tempo_coerencia_ms: Tempo de coerência do canal em milissegundos
    
Referências:
    - IEEE 802.15.4 (Zigbee, 6LoWPAN)
    - LoRaWAN Specification
    - NB-IoT (3GPP Release 13)
"""

import numpy as np

# Constantes físicas
VELOCIDADE_LUZ = 3e8  # m/s

PERFIS_DISPOSITIVOS = {
    'pessoa_andando': {
        'descricao': 'Dispositivo vestível em pessoa caminhando (wearable)',
        'erro_estimativa_canal': 0.15,  # 15% de erro na estimativa
        'velocidade_max_kmh': 5.0,  # Caminhada típica
        'frequencia_portadora_hz': 2.4e9,  # 2.4 GHz (WiFi, Bluetooth, Zigbee)
        'taxa_bits_bps': 250e3,  # 250 kbps (IEEE 802.15.4)
        'potencia_transmissao_dbm': 0,  # 1 mW
        'guard_band_sigma': 0.3,  # Moderado (compromisso entre segurança e taxa)
    },
    
    'sensor_estatico': {
        'descricao': 'Sensor fixo em ambiente interno (smart home, industrial)',
        'erro_estimativa_canal': 0.08,  # 8% de erro (ambiente controlado)
        'velocidade_max_kmh': 0.0,  # Estático
        'frequencia_portadora_hz': 868e6,  # 868 MHz (LoRa EU)
        'taxa_bits_bps': 50e3,  # 50 kbps (LoRa SF7)
        'potencia_transmissao_dbm': 14,  # 25 mW (típico LoRa)
        'guard_band_sigma': 0.7,  # CORRIGIDO: Limiar conservador (canal estável, ρ=1.0)
    },
    
    'veiculo_urbano': {
        'descricao': 'Dispositivo em veículo urbano (V2X, telemetria)',
        'erro_estimativa_canal': 0.25,  # 25% de erro (alta mobilidade)
        'velocidade_max_kmh': 60.0,  # Velocidade urbana típica
        'frequencia_portadora_hz': 5.9e9,  # 5.9 GHz (DSRC/C-V2X)
        'taxa_bits_bps': 6e6,  # 6 Mbps (DSRC)
        'potencia_transmissao_dbm': 20,  # 100 mW
        'guard_band_sigma': 0.3,  # Limiar agressivo (canal muito variável, ρ≈0.16)
    },
    
    'drone': {
        'descricao': 'Drone em voo (UAV)',
        'erro_estimativa_canal': 0.30,  # 30% de erro (3D, movimento complexo)
        'velocidade_max_kmh': 40.0,  # Velocidade típica de drone
        'frequencia_portadora_hz': 2.4e9,  # 2.4 GHz
        'taxa_bits_bps': 1e6,  # 1 Mbps
        'potencia_transmissao_dbm': 20,  # 100 mW
        'guard_band_sigma': 0.35,  # Limiar moderado-agressivo (ρ≈0.61)
    },
    
    'nb_iot': {
        'descricao': 'Dispositivo NB-IoT (Narrowband IoT, 3GPP)',
        'erro_estimativa_canal': 0.12,  # 12% de erro
        'velocidade_max_kmh': 10.0,  # Mobilidade baixa
        'frequencia_portadora_hz': 900e6,  # 900 MHz (banda licenciada)
        'taxa_bits_bps': 200e3,  # 200 kbps (downlink)
        'potencia_transmissao_dbm': 23,  # 200 mW (máximo NB-IoT)
        'guard_band_sigma': 0.5,  # Limiar conservador (ρ≈0.95)
    },
    
    # ========== PERFIS 5G ==========
    
    '5g_fr1_n78': {
        'descricao': '5G FR1 banda n78 (3.5 GHz) - Cenário urbano',
        'erro_estimativa_canal': 0.18,  # 18% de erro (ambiente urbano)
        'velocidade_max_kmh': 5.0,  # Pedestres (smartphone)
        'frequencia_portadora_hz': 3.5e9,  # 3.5 GHz (banda n78 - Brasil)
        'taxa_bits_bps': 100e6,  # 100 Mbps (eMBB típico)
        'potencia_transmissao_dbm': 23,  # 200 mW (UE máximo)
        'guard_band_sigma': 0.45,  # Limiar moderado
    },
    
    '5g_fr1_n41': {
        'descricao': '5G FR1 banda n41 (2.5 GHz) - Cobertura ampla',
        'erro_estimativa_canal': 0.16,  # 16% de erro
        'velocidade_max_kmh': 10.0,  # Mobilidade urbana baixa
        'frequencia_portadora_hz': 2.5e9,  # 2.5 GHz (banda n41)
        'taxa_bits_bps': 50e6,  # 50 Mbps
        'potencia_transmissao_dbm': 23,  # 200 mW
        'guard_band_sigma': 0.5,  # Limiar conservador
    },
    
    '5g_mmwave_n257': {
        'descricao': '5G mmWave banda n257 (28 GHz) - Hotspot urbano',
        'erro_estimativa_canal': 0.35,  # 35% de erro (alta variabilidade)
        'velocidade_max_kmh': 3.0,  # Estático ou movimento lento
        'frequencia_portadora_hz': 28e9,  # 28 GHz (mmWave)
        'taxa_bits_bps': 1e9,  # 1 Gbps (capacidade muito alta)
        'potencia_transmissao_dbm': 23,  # 200 mW
        'guard_band_sigma': 0.25,  # Limiar muito agressivo (canal extremamente variável)
    },
    
    '5g_iot_estatico': {
        'descricao': '5G IoT estático (mMTC) - Sensores fixos',
        'erro_estimativa_canal': 0.10,  # 10% de erro (fixo)
        'velocidade_max_kmh': 0.0,  # Estático
        'frequencia_portadora_hz': 3.5e9,  # 3.5 GHz
        'taxa_bits_bps': 1e6,  # 1 Mbps (mMTC)
        'potencia_transmissao_dbm': 14,  # 25 mW (baixo consumo)
        'guard_band_sigma': 0.6,  # Limiar conservador
    },
    
    '5g_urllc': {
        'descricao': '5G URLLC (Ultra-Reliable Low-Latency) - Veículos autônomos',
        'erro_estimativa_canal': 0.22,  # 22% de erro
        'velocidade_max_kmh': 30.0,  # Veículos urbanos
        'frequencia_portadora_hz': 3.7e9,  # 3.7 GHz (banda n77)
        'taxa_bits_bps': 10e6,  # 10 Mbps (URLLC não precisa alta taxa)
        'potencia_transmissao_dbm': 23,  # 200 mW
        'guard_band_sigma': 0.35,  # Limiar moderado-agressivo
    },
}


def calcular_tempo_coerencia(velocidade_kmh, frequencia_hz):
    """
    Calcula o tempo de coerência do canal baseado na velocidade e frequência.
    
    Fórmula de Clarke (modelo clássico):
        Tc ≈ 9/(16*π*fD) segundos
        
    onde fD é a frequência Doppler máxima:
        fD = v * fc / c
        
    Args:
        velocidade_kmh: Velocidade em km/h
        frequencia_hz: Frequência da portadora em Hz
        
    Returns:
        float: Tempo de coerência em segundos
        
    Referência:
        Rappaport, T. S. (2002). Wireless Communications: 
        Principles and Practice. Prentice Hall.
    """
    # Converte velocidade para m/s
    velocidade_ms = velocidade_kmh / 3.6
    
    # Calcula frequência Doppler máxima
    freq_doppler = velocidade_ms * frequencia_hz / VELOCIDADE_LUZ
    
    # Tempo de coerência (fórmula de Clarke)
    if freq_doppler == 0:
        return np.inf  # Canal estático
    
    tempo_coerencia = 9 / (16 * np.pi * freq_doppler)
    
    return tempo_coerencia


def calcular_correlacao_temporal(atraso_ms, tempo_coerencia_s):
    """
    Calcula o coeficiente de correlação temporal entre duas medições do canal.
    
    Modelo exponencial:
        ρ(τ) = exp(-τ/Tc)
        
    onde:
        τ: atraso entre medições
        Tc: tempo de coerência
        
    Args:
        atraso_ms: Atraso entre medições em milissegundos
        tempo_coerencia_s: Tempo de coerência em segundos
        
    Returns:
        float: Coeficiente de correlação (0 a 1)
    """
    atraso_s = atraso_ms / 1000.0
    correlacao = np.exp(-atraso_s / tempo_coerencia_s)
    return correlacao


def obter_parametros_dispositivo(tipo_dispositivo=None):
    """
    Retorna os parâmetros de um dispositivo específico ou permite configuração manual.
    
    Args:
        tipo_dispositivo: Nome do perfil predefinido ou None para retornar estrutura vazia
        
    Returns:
        dict: Parâmetros do dispositivo
        
    Raises:
        ValueError: Se tipo_dispositivo não existir
    """
    if tipo_dispositivo is None:
        # Retorna estrutura padrão para configuração manual
        return {
            'descricao': 'Configuração manual',
            'erro_estimativa_canal': 0.10,
            'velocidade_max_kmh': 5.0,
            'frequencia_portadora_hz': 2.4e9,
            'taxa_bits_bps': 250e3,
            'potencia_transmissao_dbm': 0,
            'guard_band_sigma': 0.5,
        }
    
    if tipo_dispositivo not in PERFIS_DISPOSITIVOS:
        tipos_disponiveis = ', '.join(PERFIS_DISPOSITIVOS.keys())
        raise ValueError(
            f"Tipo de dispositivo '{tipo_dispositivo}' não encontrado. "
            f"Tipos disponíveis: {tipos_disponiveis}"
        )
    
    return PERFIS_DISPOSITIVOS[tipo_dispositivo].copy()


def calcular_parametros_canal(config_dispositivo, atraso_medicao_ms=1.0):
    """
    Calcula parâmetros derivados do canal baseado na configuração do dispositivo.
    
    Args:
        config_dispositivo: Dicionário com parâmetros do dispositivo
        atraso_medicao_ms: Tempo entre medições de Alice e Bob em ms (padrão: 1ms)
        
    Returns:
        dict: Parâmetros calculados do canal incluindo:
            - tempo_coerencia_s
            - freq_doppler_hz
            - correlacao_temporal
    """
    # Calcula tempo de coerência
    tc = calcular_tempo_coerencia(
        config_dispositivo['velocidade_max_kmh'],
        config_dispositivo['frequencia_portadora_hz']
    )
    
    # Calcula frequência Doppler
    v_ms = config_dispositivo['velocidade_max_kmh'] / 3.6
    fd = v_ms * config_dispositivo['frequencia_portadora_hz'] / VELOCIDADE_LUZ
    
    # Calcula correlação temporal
    corr = calcular_correlacao_temporal(atraso_medicao_ms, tc)
    
    return {
        'tempo_coerencia_s': tc,
        'freq_doppler_hz': fd,
        'correlacao_temporal': corr,
    }


def listar_dispositivos():
    """
    Lista todos os perfis de dispositivos disponíveis com suas descrições.
    
    Returns:
        dict: Dicionário com nomes e descrições dos dispositivos
    """
    return {
        nome: perfil['descricao'] 
        for nome, perfil in PERFIS_DISPOSITIVOS.items()
    }
