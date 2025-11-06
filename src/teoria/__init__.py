"""
Módulo de cálculos teóricos para sistemas de comunicação digital.

Este módulo contém implementações de fórmulas teóricas para análise
de desempenho de sistemas de comunicação, incluindo:
- Cálculos de BER (Bit Error Rate)
- Cálculos de SER (Symbol Error Rate)
- Análise de modulações (BPSK, QPSK)
- Métricas de desempenho
"""

from .bpsk_qpsk import (
    ber_teorica_bpsk,
    ber_teorica_qpsk,
    ser_teorica_qpsk,
    comparar_bpsk_qpsk,
    calcular_ganho_espectral
)

__all__ = [
    'ber_teorica_bpsk',
    'ber_teorica_qpsk',
    'ser_teorica_qpsk',
    'comparar_bpsk_qpsk',
    'calcular_ganho_espectral'
]
