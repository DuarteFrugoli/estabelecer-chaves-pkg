#!/usr/bin/env python3
"""
Script para comparar BER teórica vs BER simulada para BPSK.

Compara a curva BER calculada analiticamente (teoria em canal AWGN)
com os resultados obtidos através da simulação do canal Rayleigh real.
"""

import numpy as np
import matplotlib.pyplot as plt
from src.visualizacao.teoria_comparacao.plot_bpsk_qpsk import plotar_teorico_vs_simulado_bpsk

if __name__ == "__main__":
    print("\n" + "="*70)
    print("BPSK: BER TEÓRICA vs BER SIMULADA (CANAL RAYLEIGH)")
    print("="*70)
    print("\nEste script compara:")
    print("  • Teórico: Fórmula analítica para canal Rayleigh")
    print("  • Simulado: Simulação real do canal Rayleigh")
    print("\nModulação: BPSK (Binary Phase Shift Keying)")
    print("Objetivo: Validar se a simulação reproduz a teoria")
    print("="*70 + "\n")
    
    # Parâmetros da simulação
    snr_range = np.linspace(-5, 15, 12)  # 12 pontos de SNR (-5 a 15 dB)
    num_testes = 100  # Número de testes por ponto SNR
    rayleigh_sigma = 1.0 / np.sqrt(2)  # σ normalizado: E[|h|²] = 1
    
    print("CONFIGURACOES:")
    print(f"  • Range SNR: {snr_range[0]} a {snr_range[-1]} dB ({len(snr_range)} pontos)")
    print(f"  • Testes por SNR: {num_testes}")
    print(f"  • Bits por teste: 10.000")
    print(f"  • Canal Rayleigh σ: {rayleigh_sigma:.4f} (normalizado)")
    print(f"  • Total de bits simulados: {num_testes * 10000 * len(snr_range):,}")
    print("\nIsso pode levar alguns minutos...\n")
    
    # Gera o gráfico
    fig, ax = plotar_teorico_vs_simulado_bpsk(
        snr_db_range=snr_range,
        num_testes=num_testes,
        rayleigh_sigma=rayleigh_sigma,
        salvar=False
    )
    
    print("\n" + "="*70)
    print("SIMULACAO CONCLUIDA!")
    print("="*70)
    print("\nMostrando grafico na tela...")
    print("  (Feche a janela para encerrar)")
    print("="*70)
    
    # Mostra o gráfico
    plt.show()
