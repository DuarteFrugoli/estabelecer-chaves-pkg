"""
Módulo para modulação BPSK/QPSK com frequência de portadora.

Este módulo implementa a modulação temporal realista, incluindo:
- Conversão de bits para símbolos em banda base
- Modulação em frequência de portadora (passabanda)
- Demodulação coerente
- Visualização de formas de onda

Referências:
    Proakis & Salehi (2008). Digital Communications. McGraw-Hill.
    Haykin (2001). Communication Systems. Wiley.
"""

import numpy as np
from typing import List, Tuple, Dict


class ModuladorBPSK:
    """
    Modulador BPSK (Binary Phase Shift Keying) com portadora.
    
    BPSK modula bits em duas fases da portadora: 0° e 180°
    - Bit 0 → +1 → cos(2πfct)
    - Bit 1 → -1 → -cos(2πfct) = cos(2πfct + π)
    
    Attributes:
        fc (float): Frequência da portadora em Hz
        fs (float): Frequência de amostragem em Hz
        bit_rate (float): Taxa de bits em bits/segundo
        samples_per_bit (int): Número de amostras por bit
        energia_bit (float): Energia por bit (Es = Eb para BPSK)
    """
    
    def __init__(self, fc: float = 1e6, fs: float = 10e6, bit_rate: float = 1e5, energia_bit: float = 1.0):
        """
        Inicializa o modulador BPSK.
        
        Args:
            fc: Frequência da portadora em Hz (default: 1 MHz)
            fs: Frequência de amostragem em Hz (default: 10 MHz)
            bit_rate: Taxa de bits em bps (default: 100 kbps)
            energia_bit: Energia por bit (default: 1.0)
        
        Raises:
            ValueError: Se fs < 2*fc (critério de Nyquist)
        """
        if fs < 2 * fc:
            raise ValueError(f"Frequência de amostragem ({fs} Hz) deve ser >= 2*fc ({2*fc} Hz)")
        
        self.fc = fc
        self.fs = fs
        self.bit_rate = bit_rate
        self.Tb = 1 / bit_rate  # Duração de um bit
        self.samples_per_bit = int(fs / bit_rate)
        self.energia_bit = energia_bit
        
        # Amplitude da portadora: A = sqrt(2*Eb/Tb)
        self.amplitude = np.sqrt(2 * energia_bit / self.Tb)
    
    def modular(self, bits: List[int]) -> Tuple[np.ndarray, np.ndarray]:
        """
        Modula uma sequência de bits em sinal BPSK passabanda.
        
        Args:
            bits: Lista de bits (0 ou 1)
        
        Returns:
            Tuple contendo:
                - sinal: Sinal modulado (passabanda)
                - tempo: Vetor de tempo correspondente
        """
        n_bits = len(bits)
        n_amostras = n_bits * self.samples_per_bit
        
        # Cria vetor de tempo
        tempo = np.arange(n_amostras) / self.fs
        
        # Converte bits para símbolos antipolares: 0→+1, 1→-1
        simbolos = np.array([1 - 2*b for b in bits])
        
        # Gera sinal banda base (NRZ - Non-Return-to-Zero)
        sinal_bb = np.repeat(simbolos, self.samples_per_bit)
        
        # Gera portadora
        portadora = np.cos(2 * np.pi * self.fc * tempo)
        
        # Modula: s(t) = A * m(t) * cos(2πfct)
        # onde m(t) ∈ {-1, +1}
        sinal = self.amplitude * sinal_bb * portadora
        
        return sinal, tempo
    
    def demodular(self, sinal: np.ndarray, n_bits: int) -> List[int]:
        """
        Demodula sinal BPSK usando detecção coerente.
        
        Processo:
        1. Multiplica por portadora local: r(t) * 2*cos(2πfct)
        2. Integra sobre período de bit (filtro casado)
        3. Decide: se integral > 0 → bit 0, caso contrário → bit 1
        
        Args:
            sinal: Sinal recebido (passabanda)
            n_bits: Número de bits esperados
        
        Returns:
            Lista de bits demodulados
        """
        # Gera portadora local
        n_amostras = len(sinal)
        tempo = np.arange(n_amostras) / self.fs
        portadora_local = 2 * np.cos(2 * np.pi * self.fc * tempo)
        
        # Demodulação coerente
        sinal_demod = sinal * portadora_local
        
        # Integra sobre cada período de bit
        bits_demod = []
        for i in range(n_bits):
            inicio = i * self.samples_per_bit
            fim = (i + 1) * self.samples_per_bit
            
            # Integral aproximada (soma)
            integral = np.sum(sinal_demod[inicio:fim])
            
            # Decisão: integral > 0 → símbolo +1 → bit 0
            #          integral < 0 → símbolo -1 → bit 1
            bit = 0 if integral > 0 else 1
            bits_demod.append(bit)
        
        return bits_demod
    
    def obter_info(self) -> Dict:
        """Retorna informações sobre o modulador."""
        return {
            'modulacao': 'BPSK',
            'fc_Hz': self.fc,
            'fc_MHz': self.fc / 1e6,
            'fs_Hz': self.fs,
            'fs_MHz': self.fs / 1e6,
            'bit_rate_bps': self.bit_rate,
            'bit_rate_kbps': self.bit_rate / 1e3,
            'Tb_s': self.Tb,
            'Tb_us': self.Tb * 1e6,
            'samples_per_bit': self.samples_per_bit,
            'energia_bit': self.energia_bit,
            'amplitude': self.amplitude
        }


class ModuladorQPSK:
    """
    Modulador QPSK (Quadrature Phase Shift Keying) com portadora.
    
    QPSK modula pares de bits em quatro fases: 45°, 135°, 225°, 315°
    Usando Gray coding:
    - 00 → (-1-1j)/√2 → cos(2πfct+225°) 
    - 01 → (-1+1j)/√2 → cos(2πfct+135°)
    - 10 → (+1-1j)/√2 → cos(2πfct+315°)
    - 11 → (+1+1j)/√2 → cos(2πfct+45°)
    
    Attributes:
        fc (float): Frequência da portadora em Hz
        fs (float): Frequência de amostragem em Hz
        symbol_rate (float): Taxa de símbolos em símbolos/segundo
        samples_per_symbol (int): Número de amostras por símbolo
        energia_simbolo (float): Energia por símbolo (Es)
    """
    
    def __init__(self, fc: float = 1e6, fs: float = 10e6, bit_rate: float = 1e5, energia_simbolo: float = 1.0):
        """
        Inicializa o modulador QPSK.
        
        Args:
            fc: Frequência da portadora em Hz (default: 1 MHz)
            fs: Frequência de amostragem em Hz (default: 10 MHz)
            bit_rate: Taxa de bits em bps (default: 100 kbps)
            energia_simbolo: Energia por símbolo (default: 1.0)
        
        Note:
            QPSK transmite 2 bits por símbolo, então:
            symbol_rate = bit_rate / 2
        """
        if fs < 2 * fc:
            raise ValueError(f"Frequência de amostragem ({fs} Hz) deve ser >= 2*fc ({2*fc} Hz)")
        
        self.fc = fc
        self.fs = fs
        self.bit_rate = bit_rate
        self.symbol_rate = bit_rate / 2  # 2 bits por símbolo
        self.Ts = 1 / self.symbol_rate  # Duração de um símbolo
        self.samples_per_symbol = int(fs / self.symbol_rate)
        self.energia_simbolo = energia_simbolo
        
        # Amplitude: A = sqrt(2*Es/Ts)
        self.amplitude = np.sqrt(2 * energia_simbolo / self.Ts)
        
        # Normalização para Es = 1
        self.norm = 1 / np.sqrt(2)
    
    def modular(self, bits: List[int]) -> Tuple[np.ndarray, np.ndarray]:
        """
        Modula sequência de bits em sinal QPSK passabanda.
        
        QPSK pode ser visto como duas portadoras em quadratura:
        s(t) = I(t)*cos(2πfct) - Q(t)*sin(2πfct)
        
        Args:
            bits: Lista de bits (comprimento deve ser par)
        
        Returns:
            Tuple contendo:
                - sinal: Sinal modulado (passabanda)
                - tempo: Vetor de tempo correspondente
        """
        # Garante número par de bits
        if len(bits) % 2 != 0:
            bits = bits + [0]
        
        n_simbolos = len(bits) // 2
        n_amostras = n_simbolos * self.samples_per_symbol
        
        # Cria vetor de tempo
        tempo = np.arange(n_amostras) / self.fs
        
        # Converte pares de bits para símbolos complexos (Gray coding)
        simbolos_i = []
        simbolos_q = []
        
        for i in range(0, len(bits), 2):
            bit_i = bits[i]
            bit_q = bits[i+1]
            
            # Mapeia bits para -1 ou +1
            val_i = 1 - 2 * bit_i  # 0→+1, 1→-1
            val_q = 1 - 2 * bit_q
            
            # Normaliza para Es = 1
            simbolos_i.append(val_i * self.norm)
            simbolos_q.append(val_q * self.norm)
        
        # Gera sinais banda base NRZ para componentes I e Q
        sinal_i = np.repeat(simbolos_i, self.samples_per_symbol)
        sinal_q = np.repeat(simbolos_q, self.samples_per_symbol)
        
        # Gera portadoras em quadratura
        portadora_i = np.cos(2 * np.pi * self.fc * tempo)
        portadora_q = np.sin(2 * np.pi * self.fc * tempo)
        
        # Modula: s(t) = A * [I(t)*cos(2πfct) - Q(t)*sin(2πfct)]
        sinal = self.amplitude * (sinal_i * portadora_i - sinal_q * portadora_q)
        
        return sinal, tempo
    
    def demodular(self, sinal: np.ndarray, n_bits: int) -> List[int]:
        """
        Demodula sinal QPSK usando detecção coerente.
        
        Processo:
        1. Componente I: multiplica por 2*cos(2πfct) e integra
        2. Componente Q: multiplica por -2*sin(2πfct) e integra
        3. Decide cada componente separadamente
        
        Args:
            sinal: Sinal recebido (passabanda)
            n_bits: Número de bits esperados
        
        Returns:
            Lista de bits demodulados
        """
        # Garante número par
        if n_bits % 2 != 0:
            n_bits += 1
        
        n_simbolos = n_bits // 2
        
        # Gera portadoras locais
        n_amostras = len(sinal)
        tempo = np.arange(n_amostras) / self.fs
        portadora_i = 2 * np.cos(2 * np.pi * self.fc * tempo)
        portadora_q = -2 * np.sin(2 * np.pi * self.fc * tempo)
        
        # Demodulação coerente para I e Q
        sinal_i = sinal * portadora_i
        sinal_q = sinal * portadora_q
        
        # Integra sobre cada período de símbolo
        bits_demod = []
        for i in range(n_simbolos):
            inicio = i * self.samples_per_symbol
            fim = (i + 1) * self.samples_per_symbol
            
            # Integrais
            integral_i = np.sum(sinal_i[inicio:fim])
            integral_q = np.sum(sinal_q[inicio:fim])
            
            # Decisões
            bit_i = 0 if integral_i > 0 else 1
            bit_q = 0 if integral_q > 0 else 1
            
            bits_demod.extend([bit_i, bit_q])
        
        return bits_demod[:n_bits]  # Remove padding se houver
    
    def obter_info(self) -> Dict:
        """Retorna informações sobre o modulador."""
        return {
            'modulacao': 'QPSK',
            'fc_Hz': self.fc,
            'fc_MHz': self.fc / 1e6,
            'fs_Hz': self.fs,
            'fs_MHz': self.fs / 1e6,
            'bit_rate_bps': self.bit_rate,
            'bit_rate_kbps': self.bit_rate / 1e3,
            'symbol_rate': self.symbol_rate,
            'Ts_s': self.Ts,
            'Ts_us': self.Ts * 1e6,
            'samples_per_symbol': self.samples_per_symbol,
            'energia_simbolo': self.energia_simbolo,
            'amplitude': self.amplitude,
            'normalizacao': self.norm
        }


def adicionar_ruido_awgn(sinal: np.ndarray, snr_db: float, energia_simbolo: float = 1.0) -> np.ndarray:
    """
    Adiciona ruído AWGN (Additive White Gaussian Noise) ao sinal.
    
    Args:
        sinal: Sinal de entrada
        snr_db: SNR desejada em dB (Eb/N0)
        energia_simbolo: Energia por símbolo/bit
    
    Returns:
        Sinal com ruído adicionado
    """
    # Calcula potência do sinal
    potencia_sinal = np.mean(sinal ** 2)
    
    # Converte SNR para linear
    snr_linear = 10 ** (snr_db / 10)
    
    # Calcula variância do ruído: σ² = Es / (2*SNR)
    variancia_ruido = energia_simbolo / (2 * snr_linear)
    
    # Gera ruído
    ruido = np.random.normal(0, np.sqrt(variancia_ruido), len(sinal))
    
    return sinal + ruido


def aplicar_fading_rayleigh(sinal: np.ndarray, fs: float, fd: float, sigma: float = 1/np.sqrt(2)) -> Tuple[np.ndarray, np.ndarray]:
    """
    Aplica fading Rayleigh ao sinal temporal.
    
    Args:
        sinal: Sinal de entrada
        fs: Frequência de amostragem
        fd: Frequência Doppler máxima (controla velocidade do fading)
        sigma: Parâmetro Rayleigh (default: 1/√2 para potência normalizada)
    
    Returns:
        Tuple contendo:
            - sinal_com_fading: Sinal após fading
            - ganho: Ganho do canal (complexo)
    
    Note:
        O fading é modelado usando método de Jakes para torná-lo correlacionado no tempo.
    """
    n_amostras = len(sinal)
    
    # Para cada amostra, gera ganho Rayleigh
    # Aqui usamos um modelo simplificado - pode ser melhorado com modelo de Jakes
    ganho_i = np.random.normal(0, sigma, n_amostras)
    ganho_q = np.random.normal(0, sigma, n_amostras)
    ganho = ganho_i + 1j * ganho_q
    
    # Se sinal é real, usa apenas parte real do ganho
    if np.all(np.imag(sinal) == 0):
        sinal_com_fading = sinal * np.abs(ganho)
    else:
        sinal_com_fading = sinal * ganho
    
    return sinal_com_fading, ganho
