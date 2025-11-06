"""
Módulo de visualização de comparações teóricas.

Este módulo contém funções para gerar gráficos de comparação
entre BER teórica e BER simulada para BPSK e QPSK.
"""

from .plot_bpsk_qpsk import (
    simular_ber_pratica,
    plotar_teorico_vs_simulado_bpsk,
    plotar_teorico_vs_simulado_qpsk,
    plotar_comparacao_ambas_modulacoes,
    gerar_todos_graficos_comparacao
)

__all__ = [
    # Gráficos teóricos puros
    'plotar_ber_comparacao',
    'plotar_ber_e_ser_qpsk',
    'plotar_comparacao_completa',
    'gerar_todos_graficos',
    
    # Comparação teórico vs simulado
    'plotar_teorico_vs_simulado_bpsk',
    'plotar_teorico_vs_simulado_qpsk',
    'plotar_comparacao_ambas_modulacoes',
    'gerar_todos_graficos_comparacao'
]
