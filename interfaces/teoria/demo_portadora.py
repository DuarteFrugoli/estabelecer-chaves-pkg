"""
Demonstração de modulação BPSK/QPSK com frequência de portadora.

Este script mostra:
1. Sequência de bits original
2. Sinal em banda base (antipodal)
3. Sinal modulado com portadora
4. Efeito do canal (fading + ruído)
5. Demodulação e recuperação dos bits
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

import numpy as np
import matplotlib.pyplot as plt
from src.canal.modulacao import ModuladorBPSK, ModuladorQPSK, adicionar_ruido_awgn

# Configurações
fc = 1e6  # 1 MHz - frequência da portadora
fs = 20e6  # 20 MHz - frequência de amostragem
bit_rate = 100e3  # 100 kbps

# Sequência de bits para teste
bits_teste = [1, 0, 1, 1, 0, 0, 1, 0]

print("="*70)
print("DEMONSTRAÇÃO: MODULAÇÃO COM PORTADORA")
print("="*70)

# ============================================================================
# BPSK
# ============================================================================
print("\n" + "="*70)
print("1. MODULAÇÃO BPSK")
print("="*70)

mod_bpsk = ModuladorBPSK(fc=fc, fs=fs, bit_rate=bit_rate)
info_bpsk = mod_bpsk.obter_info()

print(f"\nParâmetros:")
print(f"  Frequência portadora: {info_bpsk['fc_MHz']:.2f} MHz")
print(f"  Frequência amostragem: {info_bpsk['fs_MHz']:.2f} MHz")
print(f"  Taxa de bits: {info_bpsk['bit_rate_kbps']:.1f} kbps")
print(f"  Duração do bit (Tb): {info_bpsk['Tb_us']:.2f} µs")
print(f"  Amostras por bit: {info_bpsk['samples_per_bit']}")
print(f"  Amplitude: {info_bpsk['amplitude']:.4f}")

# Modula
sinal_bpsk, tempo_bpsk = mod_bpsk.modular(bits_teste)

print(f"\nBits originais: {bits_teste}")
print(f"Amostras geradas: {len(sinal_bpsk)}")
print(f"Duração total: {len(sinal_bpsk)/fs * 1e6:.2f} µs")

# Adiciona ruído
snr_db = 10
sinal_bpsk_ruido = adicionar_ruido_awgn(sinal_bpsk, snr_db)

# Demodula
bits_recuperados_bpsk = mod_bpsk.demodular(sinal_bpsk_ruido, len(bits_teste))

print(f"\nApós canal com SNR = {snr_db} dB:")
print(f"  Bits recuperados: {bits_recuperados_bpsk}")
print(f"  Erros: {sum(a != b for a, b in zip(bits_teste, bits_recuperados_bpsk))}")

# ============================================================================
# QPSK
# ============================================================================
print("\n" + "="*70)
print("2. MODULAÇÃO QPSK")
print("="*70)

mod_qpsk = ModuladorQPSK(fc=fc, fs=fs, bit_rate=bit_rate)
info_qpsk = mod_qpsk.obter_info()

print(f"\nParâmetros:")
print(f"  Frequência portadora: {info_qpsk['fc_MHz']:.2f} MHz")
print(f"  Taxa de bits: {info_qpsk['bit_rate_kbps']:.1f} kbps")
print(f"  Taxa de símbolos: {info_qpsk['symbol_rate']/1e3:.1f} ksps")
print(f"  Duração do símbolo (Ts): {info_qpsk['Ts_us']:.2f} µs")
print(f"  Amostras por símbolo: {info_qpsk['samples_per_symbol']}")
print(f"  Normalização: {info_qpsk['normalizacao']:.4f}")

# Modula
sinal_qpsk, tempo_qpsk = mod_qpsk.modular(bits_teste)

print(f"\nBits originais: {bits_teste}")
print(f"Número de símbolos: {len(bits_teste)//2}")
print(f"Amostras geradas: {len(sinal_qpsk)}")

# Adiciona ruído
sinal_qpsk_ruido = adicionar_ruido_awgn(sinal_qpsk, snr_db)

# Demodula
bits_recuperados_qpsk = mod_qpsk.demodular(sinal_qpsk_ruido, len(bits_teste))

print(f"\nApós canal com SNR = {snr_db} dB:")
print(f"  Bits recuperados: {bits_recuperados_qpsk}")
print(f"  Erros: {sum(a != b for a, b in zip(bits_teste, bits_recuperados_qpsk))}")

# ============================================================================
# VISUALIZAÇÃO
# ============================================================================
print("\n" + "="*70)
print("3. GERANDO GRÁFICOS")
print("="*70)

fig, axes = plt.subplots(4, 2, figsize=(15, 12))
fig.suptitle('Modulação BPSK e QPSK com Portadora', fontsize=16, fontweight='bold')

# Parâmetros para visualização (mostra só primeiros 3 bits)
n_bits_plot = 3
samples_plot_bpsk = n_bits_plot * mod_bpsk.samples_per_bit
samples_plot_qpsk = (n_bits_plot // 2 + 1) * mod_qpsk.samples_per_symbol

# --- BPSK ---
# 1. Bits digitais
ax = axes[0, 0]
t_bits = np.arange(len(bits_teste[:n_bits_plot]) + 1) * mod_bpsk.Tb * 1e6
bits_plot = np.repeat(bits_teste[:n_bits_plot], 2)
t_bits_plot = np.repeat(t_bits, 2)[1:-1]
ax.plot(t_bits_plot, bits_plot, 'b-', linewidth=2)
ax.set_ylabel('Amplitude', fontweight='bold')
ax.set_title('BPSK: Sequência de Bits', fontweight='bold')
ax.set_ylim([-0.2, 1.2])
ax.grid(True, alpha=0.3)
ax.set_xlim([0, n_bits_plot * mod_bpsk.Tb * 1e6])

# 2. Sinal banda base (antipodal)
ax = axes[1, 0]
simbolos = [1 - 2*b for b in bits_teste[:n_bits_plot]]
t_bb = np.arange(len(simbolos) + 1) * mod_bpsk.Tb * 1e6
simbolos_plot = np.repeat(simbolos, 2)
t_bb_plot = np.repeat(t_bb, 2)[1:-1]
ax.plot(t_bb_plot, simbolos_plot, 'g-', linewidth=2)
ax.set_ylabel('Amplitude', fontweight='bold')
ax.set_title('BPSK: Sinal Banda Base (Antipodal)', fontweight='bold')
ax.set_ylim([-1.5, 1.5])
ax.grid(True, alpha=0.3)
ax.set_xlim([0, n_bits_plot * mod_bpsk.Tb * 1e6])

# 3. Sinal modulado (portadora)
ax = axes[2, 0]
ax.plot(tempo_bpsk[:samples_plot_bpsk] * 1e6, sinal_bpsk[:samples_plot_bpsk], 'r-', linewidth=0.8)
ax.set_ylabel('Amplitude', fontweight='bold')
ax.set_title('BPSK: Sinal Modulado (Passabanda)', fontweight='bold')
ax.grid(True, alpha=0.3)
ax.set_xlim([0, n_bits_plot * mod_bpsk.Tb * 1e6])

# 4. Sinal com ruído
ax = axes[3, 0]
ax.plot(tempo_bpsk[:samples_plot_bpsk] * 1e6, sinal_bpsk_ruido[:samples_plot_bpsk], 'purple', linewidth=0.8, alpha=0.7)
ax.set_xlabel('Tempo (µs)', fontweight='bold')
ax.set_ylabel('Amplitude', fontweight='bold')
ax.set_title(f'BPSK: Sinal Recebido (SNR = {snr_db} dB)', fontweight='bold')
ax.grid(True, alpha=0.3)
ax.set_xlim([0, n_bits_plot * mod_bpsk.Tb * 1e6])

# --- QPSK ---
# 1. Bits digitais
ax = axes[0, 1]
ax.plot(t_bits_plot, bits_plot, 'b-', linewidth=2)
ax.set_ylabel('Amplitude', fontweight='bold')
ax.set_title('QPSK: Sequência de Bits', fontweight='bold')
ax.set_ylim([-0.2, 1.2])
ax.grid(True, alpha=0.3)
ax.set_xlim([0, n_bits_plot * mod_bpsk.Tb * 1e6])

# 2. Símbolos complexos (diagrama de constelação como linha temporal)
ax = axes[1, 1]
n_simbolos_plot = n_bits_plot // 2 + 1
simbolos_i = []
simbolos_q = []
for i in range(0, n_bits_plot, 2):
    if i+1 < len(bits_teste):
        val_i = (1 - 2 * bits_teste[i]) * mod_qpsk.norm
        val_q = (1 - 2 * bits_teste[i+1]) * mod_qpsk.norm
        simbolos_i.append(val_i)
        simbolos_q.append(val_q)

t_simbolos = np.arange(len(simbolos_i) + 1) * mod_qpsk.Ts * 1e6
simbolos_i_plot = np.repeat(simbolos_i, 2)
simbolos_q_plot = np.repeat(simbolos_q, 2)
t_simbolos_plot = np.repeat(t_simbolos, 2)[1:-1]
ax.plot(t_simbolos_plot, simbolos_i_plot, 'g-', linewidth=2, label='I (In-phase)')
ax.plot(t_simbolos_plot, simbolos_q_plot, 'orange', linewidth=2, label='Q (Quadrature)')
ax.set_ylabel('Amplitude', fontweight='bold')
ax.set_title('QPSK: Componentes I e Q', fontweight='bold')
ax.legend(loc='upper right')
ax.grid(True, alpha=0.3)
ax.set_xlim([0, n_bits_plot * mod_bpsk.Tb * 1e6])

# 3. Sinal modulado
ax = axes[2, 1]
ax.plot(tempo_qpsk[:samples_plot_qpsk] * 1e6, sinal_qpsk[:samples_plot_qpsk], 'r-', linewidth=0.8)
ax.set_ylabel('Amplitude', fontweight='bold')
ax.set_title('QPSK: Sinal Modulado (Passabanda)', fontweight='bold')
ax.grid(True, alpha=0.3)
ax.set_xlim([0, n_bits_plot * mod_bpsk.Tb * 1e6])

# 4. Sinal com ruído
ax = axes[3, 1]
ax.plot(tempo_qpsk[:samples_plot_qpsk] * 1e6, sinal_qpsk_ruido[:samples_plot_qpsk], 'purple', linewidth=0.8, alpha=0.7)
ax.set_xlabel('Tempo (µs)', fontweight='bold')
ax.set_ylabel('Amplitude', fontweight='bold')
ax.set_title(f'QPSK: Sinal Recebido (SNR = {snr_db} dB)', fontweight='bold')
ax.grid(True, alpha=0.3)
ax.set_xlim([0, n_bits_plot * mod_bpsk.Tb * 1e6])

plt.tight_layout()
plt.savefig('interfaces/teoria/plots/modulacao_portadora.png', dpi=300, bbox_inches='tight')
print("\nGrafico salvo em: interfaces/teoria/plots/modulacao_portadora.png")

# ============================================================================
# DIAGRAMA DE CONSTELAÇÃO QPSK
# ============================================================================
fig2, ax = plt.subplots(1, 1, figsize=(8, 8))

# Símbolos QPSK ideais
simbolos_ideal = [
    (-1-1j) * mod_qpsk.norm,  # 00
    (-1+1j) * mod_qpsk.norm,  # 01
    (+1-1j) * mod_qpsk.norm,  # 10
    (+1+1j) * mod_qpsk.norm   # 11
]

labels = ['00', '01', '10', '11']
for s, label in zip(simbolos_ideal, labels):
    ax.plot(s.real, s.imag, 'bo', markersize=15)
    ax.text(s.real * 1.2, s.imag * 1.2, label, ha='center', va='center', 
            fontsize=12, fontweight='bold')
    ax.arrow(0, 0, s.real * 0.9, s.imag * 0.9, head_width=0.05, 
             head_length=0.05, fc='blue', ec='blue', alpha=0.5)

ax.axhline(y=0, color='k', linewidth=0.5)
ax.axvline(x=0, color='k', linewidth=0.5)
ax.grid(True, alpha=0.3)
ax.set_xlabel('I (In-phase)', fontweight='bold', fontsize=12)
ax.set_ylabel('Q (Quadrature)', fontweight='bold', fontsize=12)
ax.set_title('Diagrama de Constelação QPSK (Gray Coding)', fontweight='bold', fontsize=14)
ax.set_xlim([-1, 1])
ax.set_ylim([-1, 1])
ax.set_aspect('equal')

# Adiciona círculo unitário normalizado
circle = plt.Circle((0, 0), mod_qpsk.norm, color='red', fill=False, 
                    linestyle='--', linewidth=2, alpha=0.5, label='|s| = 1/√2')
ax.add_patch(circle)
ax.legend(loc='upper right')

plt.tight_layout()
plt.savefig('interfaces/teoria/plots/constelacao_qpsk.png', dpi=300, bbox_inches='tight')
print("Diagrama salvo em: interfaces/teoria/plots/constelacao_qpsk.png")

plt.show()

print("\n" + "="*70)
print("DEMONSTRAÇÃO CONCLUÍDA!")
print("="*70)
