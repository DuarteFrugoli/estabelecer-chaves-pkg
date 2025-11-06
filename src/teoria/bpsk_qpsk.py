"""
Módulo para cálculos teóricos de BER (Bit Error Rate) para modulações BPSK e QPSK.

Este módulo contém as fórmulas teóricas para calcular a taxa de erro de bit
em canais AWGN (Additive White Gaussian Noise) e Rayleigh (fading) para:
- BPSK (Binary Phase Shift Keying)
- QPSK (Quadrature Phase Shift Keying)
"""

import numpy as np
from scipy.special import erfc


def ber_teorica_bpsk(snr_db):
    """
    Calcula a BER teórica para modulação BPSK em canal AWGN.
    
    Fórmula: BER = 0.5 * erfc(sqrt(Eb/N0))
    
    onde:
    - erfc é a função erro complementar
    - Eb/N0 é a relação sinal-ruído por bit (SNR)
    
    Args:
        snr_db (float ou array): SNR em dB (Eb/N0)
        
    Returns:
        float ou array: BER teórica para BPSK
        
    Referência:
        Proakis, J. G., & Salehi, M. (2008). Digital Communications. 
        McGraw-Hill, 5th edition.
    """
    # Converte SNR de dB para linear
    snr_linear = 10 ** (snr_db / 10)
    
    # Calcula BER usando a função erfc
    # BER = 0.5 * erfc(sqrt(Eb/N0))
    ber = 0.5 * erfc(np.sqrt(snr_linear))
    
    return ber


def ber_teorica_qpsk(snr_db):
    """
    Calcula a BER teórica para modulação QPSK em canal AWGN.
    
    Para QPSK ideal (Gray coding), a BER por bit é aproximadamente
    igual à BER do BPSK quando consideramos Eb/N0:
    
    Fórmula: BER ≈ 0.5 * erfc(sqrt(Eb/N0))
    
    Nota: QPSK transmite 2 bits por símbolo, mas a BER por bit
    é aproximadamente igual à do BPSK devido ao mapeamento Gray.
    
    Args:
        snr_db (float ou array): SNR em dB (Eb/N0)
        
    Returns:
        float ou array: BER teórica para QPSK
        
    Referência:
        Proakis, J. G., & Salehi, M. (2008). Digital Communications.
        McGraw-Hill, 5th edition.
    """
    # Para QPSK com Gray coding, a BER por bit é aproximadamente
    # igual à BER do BPSK
    snr_linear = 10 ** (snr_db / 10)
    
    # BER por bit para QPSK (com Gray coding)
    ber = 0.5 * erfc(np.sqrt(snr_linear))
    
    return ber


def ser_teorica_qpsk(snr_db):
    """
    Calcula a SER (Symbol Error Rate) teórica para QPSK em canal AWGN.
    
    A SER (taxa de erro de símbolo) é diferente da BER (taxa de erro de bit).
    Para QPSK:
    
    Fórmula: SER = erfc(sqrt(Es/N0)) - 0.25 * erfc²(sqrt(Es/N0))
    
    Aproximação: SER ≈ erfc(sqrt(Es/N0)) para SNR alto
    
    onde Es/N0 = 2 * Eb/N0 para QPSK (2 bits por símbolo)
    
    Args:
        snr_db (float ou array): SNR em dB (Eb/N0)
        
    Returns:
        float ou array: SER teórica para QPSK
    """
    snr_linear = 10 ** (snr_db / 10)
    
    # Para QPSK, Es/N0 = 2 * Eb/N0 (2 bits por símbolo)
    es_n0 = 2 * snr_linear
    
    # SER exata para QPSK
    term = erfc(np.sqrt(es_n0))
    ser = term - 0.25 * term**2
    
    return ser


def comparar_bpsk_qpsk(snr_db_range):
    """
    Compara as BER teóricas de BPSK e QPSK para um range de SNR.
    
    Args:
        snr_db_range (array): Range de valores SNR em dB
        
    Returns:
        dict: Dicionário contendo:
            - 'snr_db': Array de SNR em dB
            - 'ber_bpsk': Array de BER teórica BPSK
            - 'ber_qpsk': Array de BER teórica QPSK
            - 'ser_qpsk': Array de SER teórica QPSK
    """
    ber_bpsk = ber_teorica_bpsk(snr_db_range)
    ber_qpsk = ber_teorica_qpsk(snr_db_range)
    ser_qpsk = ser_teorica_qpsk(snr_db_range)
    
    return {
        'snr_db': snr_db_range,
        'ber_bpsk': ber_bpsk,
        'ber_qpsk': ber_qpsk,
        'ser_qpsk': ser_qpsk
    }


def ber_teorica_rayleigh_bpsk(snr_db):
    """
    Calcula a BER teórica para modulação BPSK em canal Rayleigh com fading.
    
    Fórmula: BER = 0.5 * (1 - sqrt(SNR / (1 + SNR)))
    
    onde SNR = Eb/N0 (relação sinal-ruído por bit)
    
    IMPORTANTE: Esta fórmula assume canal Rayleigh com potência normalizada,
    ou seja, E[|h|²] = 1. Isso corresponde a σ = 1/√2 ≈ 0.7071.
    
    Args:
        snr_db (float ou array): SNR em dB (Eb/N0)
        
    Returns:
        float ou array: BER teórica para BPSK em Rayleigh
        
    Referência:
        Proakis, J. G., & Salehi, M. (2008). Digital Communications.
        McGraw-Hill, 5th edition. Chapter 14 - Fading Channels.
    """
    # Converte SNR de dB para linear
    snr_linear = 10 ** (snr_db / 10)
    
    # Fórmula BER para BPSK em Rayleigh fading
    ber = 0.5 * (1 - np.sqrt(snr_linear / (1 + snr_linear)))
    
    return ber


def ber_teorica_rayleigh_qpsk(snr_db):
    """
    Calcula a BER teórica para modulação QPSK em canal Rayleigh com fading.
    
    Para QPSK com Gray coding em Rayleigh, a BER por bit é aproximadamente
    igual à do BPSK:
    
    Fórmula: BER ≈ 0.5 * (1 - sqrt(SNR / (1 + SNR)))
    
    IMPORTANTE: Esta fórmula assume canal Rayleigh com potência normalizada,
    ou seja, E[|h|²] = 1. Isso corresponde a σ = 1/√2 ≈ 0.7071.
    
    Args:
        snr_db (float ou array): SNR em dB (Eb/N0)
        
    Returns:
        float ou array: BER teórica para QPSK em Rayleigh
        
    Referência:
        Proakis, J. G., & Salehi, M. (2008). Digital Communications.
        McGraw-Hill, 5th edition. Chapter 14 - Fading Channels.
    """
    # Para QPSK com Gray coding, a BER é similar ao BPSK
    snr_linear = 10 ** (snr_db / 10)
    
    # Fórmula BER para QPSK em Rayleigh fading
    ber = 0.5 * (1 - np.sqrt(snr_linear / (1 + snr_linear)))
    
    return ber


def calcular_ganho_espectral():
    """
    Calcula o ganho espectral de QPSK sobre BPSK.
    
    QPSK transmite 2 bits por símbolo, enquanto BPSK transmite 1 bit por símbolo.
    Portanto, QPSK tem o dobro da eficiência espectral.
    
    Returns:
        dict: Informações sobre ganho espectral
    """
    return {
        'bpsk_bits_por_simbolo': 1,
        'qpsk_bits_por_simbolo': 2,
        'ganho_espectral': 2.0,
        'descricao': 'QPSK transmite o dobro de bits por símbolo em relação ao BPSK'
    }
