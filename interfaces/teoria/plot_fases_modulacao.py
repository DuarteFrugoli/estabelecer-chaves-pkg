"""
Plots das fases do processo de modulação BPSK e QPSK.

Este script gera visualizações didáticas mostrando as 3 fases principais:
1. Geração da sequência binária (bits digitais)
2. Sequência binária antipodal (símbolos -1 e +1)
3. Sequência modulada (onda eletromagnética com portadora)

Criado para apresentação e análise dos processos de modulação.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from src.canal.modulacao import ModuladorBPSK, ModuladorQPSK

# Configuração para plots de alta qualidade
plt.rcParams['figure.dpi'] = 150
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['xtick.labelsize'] = 9
plt.rcParams['ytick.labelsize'] = 9
plt.rcParams['legend.fontsize'] = 9

# Parâmetros da simulação
fc = 1e6        # 1 MHz - frequência da portadora
fs = 20e6       # 20 MHz - frequência de amostragem
bit_rate = 100e3  # 100 kbps

# Sequência de bits para demonstração (8 bits)
bits = [1, 0, 1, 1, 0, 0, 1, 0]
n_bits_visualizar = 6  # Mostrar apenas 6 bits para clareza

print("="*70)
print("GERANDO PLOTS DAS FASES DE MODULAÇÃO")
print("="*70)
print(f"\nSequência de bits: {bits[:n_bits_visualizar]}")
print(f"Frequência portadora: {fc/1e6:.1f} MHz")
print(f"Taxa de bits: {bit_rate/1e3:.1f} kbps")

# ============================================================================
# BPSK - FASES DA MODULAÇÃO
# ============================================================================
print("\n" + "-"*70)
print("PROCESSANDO BPSK...")
print("-"*70)

mod_bpsk = ModuladorBPSK(fc=fc, fs=fs, bit_rate=bit_rate)
info_bpsk = mod_bpsk.obter_info()

# Modula a sequência
sinal_bpsk, tempo_bpsk = mod_bpsk.modular(bits)

# Prepara dados para visualização
Tb = info_bpsk['Tb_s']  # Duração de um bit
samples_per_bit = info_bpsk['samples_per_bit']

# Limita para visualização
n_samples_plot = n_bits_visualizar * samples_per_bit
tempo_plot = tempo_bpsk[:n_samples_plot] * 1e6  # em µs
sinal_plot = sinal_bpsk[:n_samples_plot]

# Símbolos antipolares
simbolos_bpsk = [1 - 2*b for b in bits[:n_bits_visualizar]]

# Cria figura para BPSK
fig1, axes1 = plt.subplots(3, 1, figsize=(14, 10))
fig1.suptitle('Fases do Processo de Modulação BPSK', 
              fontsize=16, fontweight='bold', y=0.995)

# --- FASE 1: Sequência Binária Digital ---
ax = axes1[0]
t_bits = np.arange(n_bits_visualizar + 1) * Tb * 1e6

for i, bit in enumerate(bits[:n_bits_visualizar]):
    # Desenha retângulo para cada bit
    t_inicio = i * Tb * 1e6
    t_fim = (i + 1) * Tb * 1e6
    cor = 'royalblue' if bit == 1 else 'lightcoral'
    
    ax.add_patch(Rectangle((t_inicio, 0), Tb * 1e6, bit, 
                           facecolor=cor, edgecolor='black', linewidth=1.5))
    
    # Adiciona texto com o valor do bit
    ax.text((t_inicio + t_fim) / 2, bit / 2, str(bit), 
           ha='center', va='center', fontsize=14, fontweight='bold', color='white')

ax.set_xlim([0, n_bits_visualizar * Tb * 1e6])
ax.set_ylim([-0.1, 1.3])
ax.set_ylabel('Amplitude', fontweight='bold', fontsize=11)
ax.set_title('FASE 1: Sequência Binária Digital (0s e 1s)', 
            fontweight='bold', fontsize=12, pad=10)
ax.grid(True, alpha=0.3, linestyle='--')
ax.set_yticks([0, 1])
ax.set_yticklabels(['0', '1'])

# Adiciona marcadores de tempo
for i in range(n_bits_visualizar + 1):
    ax.axvline(i * Tb * 1e6, color='gray', linestyle=':', alpha=0.5, linewidth=1)

# --- FASE 2: Sequência Antipodal ---
ax = axes1[1]

for i, simbolo in enumerate(simbolos_bpsk):
    t_inicio = i * Tb * 1e6
    t_fim = (i + 1) * Tb * 1e6
    cor = 'forestgreen' if simbolo == 1 else 'orangered'
    
    ax.add_patch(Rectangle((t_inicio, min(0, simbolo)), 
                           Tb * 1e6, abs(simbolo), 
                           facecolor=cor, edgecolor='black', linewidth=1.5))
    
    # Adiciona texto com o valor do símbolo
    ax.text((t_inicio + t_fim) / 2, simbolo / 2, 
           f'{simbolo:+d}', 
           ha='center', va='center', fontsize=14, fontweight='bold', color='white')

ax.axhline(y=0, color='black', linewidth=2)
ax.set_xlim([0, n_bits_visualizar * Tb * 1e6])
ax.set_ylim([-1.5, 1.5])
ax.set_ylabel('Amplitude', fontweight='bold', fontsize=11)
ax.set_title('FASE 2: Sequência Antipodal (Símbolos -1 e +1)', 
            fontweight='bold', fontsize=12, pad=10)
ax.grid(True, alpha=0.3, linestyle='--')
ax.set_yticks([-1, 0, 1])

for i in range(n_bits_visualizar + 1):
    ax.axvline(i * Tb * 1e6, color='gray', linestyle=':', alpha=0.5, linewidth=1)

# --- FASE 3: Sinal Modulado (Onda Eletromagnética) ---
ax = axes1[2]
ax.plot(tempo_plot, sinal_plot, 'darkblue', linewidth=1.2, label='Sinal BPSK')
ax.axhline(y=0, color='black', linewidth=0.8, linestyle='-', alpha=0.5)

# Destaca as transições de fase (inversões de 180°)
for i in range(len(simbolos_bpsk) - 1):
    if simbolos_bpsk[i] != simbolos_bpsk[i+1]:
        t_transicao = (i + 1) * Tb * 1e6
        ax.axvline(t_transicao, color='red', linestyle='--', 
                  alpha=0.7, linewidth=2, label='Inversão de Fase' if i == 0 else '')

ax.set_xlim([0, n_bits_visualizar * Tb * 1e6])
ax.set_xlabel('Tempo (µs)', fontweight='bold', fontsize=11)
ax.set_ylabel('Amplitude', fontweight='bold', fontsize=11)
ax.set_title(f'FASE 3: Sinal Modulado - Onda Eletromagnética (fc = {fc/1e6:.1f} MHz)', 
            fontweight='bold', fontsize=12, pad=10)
ax.grid(True, alpha=0.3, linestyle='--')
ax.legend(loc='upper right')

for i in range(n_bits_visualizar + 1):
    ax.axvline(i * Tb * 1e6, color='gray', linestyle=':', alpha=0.5, linewidth=1)

plt.tight_layout()
plt.savefig('interfaces/teoria/plots/fases_modulacao_bpsk.png', 
            dpi=300, bbox_inches='tight', facecolor='white')
print("Plot BPSK salvo: interfaces/teoria/plots/fases_modulacao_bpsk.png")

# ============================================================================
# QPSK - FASES DA MODULAÇÃO
# ============================================================================
print("\n" + "-"*70)
print("PROCESSANDO QPSK...")
print("-"*70)

mod_qpsk = ModuladorQPSK(fc=fc, fs=fs, bit_rate=bit_rate)
info_qpsk = mod_qpsk.obter_info()

# Modula a sequência
sinal_qpsk, tempo_qpsk = mod_qpsk.modular(bits)

# Prepara dados para visualização
Ts = info_qpsk['Ts_s']  # Duração de um símbolo
samples_per_symbol = info_qpsk['samples_per_symbol']
n_simbolos = n_bits_visualizar // 2

# Limita para visualização
n_samples_plot_qpsk = n_simbolos * samples_per_symbol
tempo_plot_qpsk = tempo_qpsk[:n_samples_plot_qpsk] * 1e6  # em µs
sinal_plot_qpsk = sinal_qpsk[:n_samples_plot_qpsk]

# Símbolos complexos I/Q
simbolos_i = []
simbolos_q = []
norm = info_qpsk['normalizacao']

for i in range(0, n_bits_visualizar, 2):
    bit_i = bits[i]
    bit_q = bits[i+1]
    val_i = (1 - 2 * bit_i) * norm
    val_q = (1 - 2 * bit_q) * norm
    simbolos_i.append(val_i)
    simbolos_q.append(val_q)

# Cria figura para QPSK
fig2, axes2 = plt.subplots(4, 1, figsize=(14, 12))
fig2.suptitle('Fases do Processo de Modulação QPSK', 
              fontsize=16, fontweight='bold', y=0.995)

# --- FASE 1: Sequência Binária Digital ---
ax = axes2[0]

for i, bit in enumerate(bits[:n_bits_visualizar]):
    # Para QPSK, mostra pares de bits
    t_inicio = i * Tb * 1e6
    t_fim = (i + 1) * Tb * 1e6
    cor = 'royalblue' if bit == 1 else 'lightcoral'
    
    ax.add_patch(Rectangle((t_inicio, 0), Tb * 1e6, bit, 
                           facecolor=cor, edgecolor='black', linewidth=1.5))
    
    ax.text((t_inicio + t_fim) / 2, bit / 2, str(bit), 
           ha='center', va='center', fontsize=14, fontweight='bold', color='white')
    
    # Destaca pares de bits
    if i % 2 == 0:
        ax.axvspan(t_inicio, min(t_fim, n_bits_visualizar * Tb * 1e6), 
                  alpha=0.1, color='yellow')

ax.set_xlim([0, n_bits_visualizar * Tb * 1e6])
ax.set_ylim([-0.1, 1.3])
ax.set_ylabel('Amplitude', fontweight='bold', fontsize=11)
ax.set_title('FASE 1: Sequência Binária Digital (Agrupada em pares para QPSK)', 
            fontweight='bold', fontsize=12, pad=10)
ax.grid(True, alpha=0.3, linestyle='--')
ax.set_yticks([0, 1])

for i in range(n_bits_visualizar + 1):
    ax.axvline(i * Tb * 1e6, color='gray', linestyle=':', alpha=0.5, linewidth=1)

# --- FASE 2a: Componente I (In-phase) ---
ax = axes2[1]

for i, val_i in enumerate(simbolos_i):
    t_inicio = i * Ts * 1e6
    t_fim = (i + 1) * Ts * 1e6
    cor = 'mediumseagreen' if val_i > 0 else 'tomato'
    
    ax.add_patch(Rectangle((t_inicio, min(0, val_i)), 
                           Ts * 1e6, abs(val_i), 
                           facecolor=cor, edgecolor='black', linewidth=1.5, alpha=0.8))
    
    ax.text((t_inicio + t_fim) / 2, val_i / 2, 
           f'{val_i:+.2f}', 
           ha='center', va='center', fontsize=12, fontweight='bold', color='white')

ax.axhline(y=0, color='black', linewidth=2)
ax.set_xlim([0, n_bits_visualizar * Tb * 1e6])
ax.set_ylim([-1.0, 1.0])
ax.set_ylabel('Amplitude I', fontweight='bold', fontsize=11)
ax.set_title('FASE 2a: Componente I - In-phase (normalizada)', 
            fontweight='bold', fontsize=12, pad=10)
ax.grid(True, alpha=0.3, linestyle='--')

# --- FASE 2b: Componente Q (Quadrature) ---
ax = axes2[2]

for i, val_q in enumerate(simbolos_q):
    t_inicio = i * Ts * 1e6
    t_fim = (i + 1) * Ts * 1e6
    cor = 'steelblue' if val_q > 0 else 'darkorange'
    
    ax.add_patch(Rectangle((t_inicio, min(0, val_q)), 
                           Ts * 1e6, abs(val_q), 
                           facecolor=cor, edgecolor='black', linewidth=1.5, alpha=0.8))
    
    ax.text((t_inicio + t_fim) / 2, val_q / 2, 
           f'{val_q:+.2f}', 
           ha='center', va='center', fontsize=12, fontweight='bold', color='white')

ax.axhline(y=0, color='black', linewidth=2)
ax.set_xlim([0, n_bits_visualizar * Tb * 1e6])
ax.set_ylim([-1.0, 1.0])
ax.set_ylabel('Amplitude Q', fontweight='bold', fontsize=11)
ax.set_title('FASE 2b: Componente Q - Quadrature (normalizada)', 
            fontweight='bold', fontsize=12, pad=10)
ax.grid(True, alpha=0.3, linestyle='--')

# --- FASE 3: Sinal Modulado ---
ax = axes2[3]
ax.plot(tempo_plot_qpsk, sinal_plot_qpsk, 'darkviolet', linewidth=1.2, label='Sinal QPSK')
ax.axhline(y=0, color='black', linewidth=0.8, linestyle='-', alpha=0.5)

# Marca transições de símbolo
for i in range(n_simbolos + 1):
    t_simbolo = i * Ts * 1e6
    ax.axvline(t_simbolo, color='green', linestyle=':', 
              alpha=0.6, linewidth=1.5)

ax.set_xlim([0, n_bits_visualizar * Tb * 1e6])
ax.set_xlabel('Tempo (µs)', fontweight='bold', fontsize=11)
ax.set_ylabel('Amplitude', fontweight='bold', fontsize=11)
ax.set_title(f'FASE 3: Sinal Modulado - Onda Eletromagnética (fc = {fc/1e6:.1f} MHz)', 
            fontweight='bold', fontsize=12, pad=10)
ax.grid(True, alpha=0.3, linestyle='--')
ax.legend(loc='upper right')

plt.tight_layout()
plt.savefig('interfaces/teoria/plots/fases_modulacao_qpsk.png', 
            dpi=300, bbox_inches='tight', facecolor='white')
print("Plot QPSK salvo: interfaces/teoria/plots/fases_modulacao_qpsk.png")

# ============================================================================
# PLOT COMPARATIVO - ZOOM EM 2 BITS
# ============================================================================
print("\n" + "-"*70)
print("GERANDO PLOT COMPARATIVO COM ZOOM...")
print("-"*70)

n_bits_zoom = 2
samples_zoom_bpsk = n_bits_zoom * samples_per_bit

fig3, axes3 = plt.subplots(2, 3, figsize=(16, 8))
fig3.suptitle('Comparação BPSK vs QPSK - Zoom em 2 Bits', 
              fontsize=16, fontweight='bold')

# BPSK - Coluna 1
# Bits
ax = axes3[0, 0]
for i in range(n_bits_zoom):
    bit = bits[i]
    cor = 'royalblue' if bit == 1 else 'lightcoral'
    ax.add_patch(Rectangle((i * Tb * 1e6, 0), Tb * 1e6, bit, 
                           facecolor=cor, edgecolor='black', linewidth=2))
    ax.text((i + 0.5) * Tb * 1e6, bit/2, str(bit), 
           ha='center', va='center', fontsize=16, fontweight='bold', color='white')
ax.set_xlim([0, n_bits_zoom * Tb * 1e6])
ax.set_ylim([-0.1, 1.2])
ax.set_ylabel('Bits', fontweight='bold')
ax.set_title('BPSK: Bits Digitais', fontweight='bold')
ax.set_yticks([0, 1])
ax.grid(True, alpha=0.3)

# Símbolos
ax = axes3[0, 1]
for i in range(n_bits_zoom):
    simbolo = 1 - 2*bits[i]
    cor = 'forestgreen' if simbolo == 1 else 'orangered'
    ax.add_patch(Rectangle((i * Tb * 1e6, min(0, simbolo)), 
                           Tb * 1e6, abs(simbolo), 
                           facecolor=cor, edgecolor='black', linewidth=2))
    ax.text((i + 0.5) * Tb * 1e6, simbolo/2, f'{simbolo:+d}', 
           ha='center', va='center', fontsize=16, fontweight='bold', color='white')
ax.axhline(0, color='black', linewidth=2)
ax.set_xlim([0, n_bits_zoom * Tb * 1e6])
ax.set_ylim([-1.5, 1.5])
ax.set_ylabel('Símbolos', fontweight='bold')
ax.set_title('BPSK: Antipodal', fontweight='bold')
ax.grid(True, alpha=0.3)

# Modulado
ax = axes3[0, 2]
ax.plot(tempo_bpsk[:samples_zoom_bpsk] * 1e6, 
        sinal_bpsk[:samples_zoom_bpsk], 'darkblue', linewidth=1.5)
ax.axhline(0, color='black', linewidth=0.8)
ax.set_xlim([0, n_bits_zoom * Tb * 1e6])
ax.set_ylabel('Sinal RF', fontweight='bold')
ax.set_title('BPSK: Modulado', fontweight='bold')
ax.grid(True, alpha=0.3)

# QPSK - Coluna 2
# Bits
ax = axes3[1, 0]
for i in range(n_bits_zoom):
    bit = bits[i]
    cor = 'royalblue' if bit == 1 else 'lightcoral'
    ax.add_patch(Rectangle((i * Tb * 1e6, 0), Tb * 1e6, bit, 
                           facecolor=cor, edgecolor='black', linewidth=2))
    ax.text((i + 0.5) * Tb * 1e6, bit/2, str(bit), 
           ha='center', va='center', fontsize=16, fontweight='bold', color='white')
if n_bits_zoom >= 2:
    ax.axvspan(0, n_bits_zoom * Tb * 1e6, alpha=0.1, color='yellow')
ax.set_xlim([0, n_bits_zoom * Tb * 1e6])
ax.set_ylim([-0.1, 1.2])
ax.set_xlabel('Tempo (µs)', fontweight='bold')
ax.set_ylabel('Bits', fontweight='bold')
ax.set_title('QPSK: Bits (1 símbolo)', fontweight='bold')
ax.set_yticks([0, 1])
ax.grid(True, alpha=0.3)

# Símbolos I/Q
ax = axes3[1, 1]
val_i = simbolos_i[0]
val_q = simbolos_q[0]
ax.add_patch(Rectangle((0, min(0, val_i)), n_bits_zoom * Tb * 1e6, abs(val_i), 
                       facecolor='mediumseagreen' if val_i > 0 else 'tomato', 
                       edgecolor='black', linewidth=2, alpha=0.7, label='I'))
ax.add_patch(Rectangle((0, min(0, val_q)), n_bits_zoom * Tb * 1e6, abs(val_q), 
                       facecolor='steelblue' if val_q > 0 else 'darkorange', 
                       edgecolor='black', linewidth=2, alpha=0.5, label='Q'))
ax.text(Tb * 1e6, val_i/2, f'I={val_i:+.2f}', 
       ha='center', va='center', fontsize=14, fontweight='bold')
ax.text(Tb * 1e6, val_q/2, f'Q={val_q:+.2f}', 
       ha='center', va='center', fontsize=14, fontweight='bold')
ax.axhline(0, color='black', linewidth=2)
ax.set_xlim([0, n_bits_zoom * Tb * 1e6])
ax.set_ylim([-1.0, 1.0])
ax.set_xlabel('Tempo (µs)', fontweight='bold')
ax.set_ylabel('Símbolos I/Q', fontweight='bold')
ax.set_title('QPSK: I e Q', fontweight='bold')
ax.legend(loc='upper right')
ax.grid(True, alpha=0.3)

# Modulado
ax = axes3[1, 2]
samples_zoom_qpsk = samples_per_symbol
ax.plot(tempo_qpsk[:samples_zoom_qpsk] * 1e6, 
        sinal_qpsk[:samples_zoom_qpsk], 'darkviolet', linewidth=1.5)
ax.axhline(0, color='black', linewidth=0.8)
ax.set_xlim([0, n_bits_zoom * Tb * 1e6])
ax.set_xlabel('Tempo (µs)', fontweight='bold')
ax.set_ylabel('Sinal RF', fontweight='bold')
ax.set_title('QPSK: Modulado', fontweight='bold')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('interfaces/teoria/plots/comparacao_bpsk_qpsk_zoom.png', 
            dpi=300, bbox_inches='tight', facecolor='white')
print("Plot comparativo salvo: interfaces/teoria/plots/comparacao_bpsk_qpsk_zoom.png")

print("\n" + "="*70)
print("PLOTS GERADOS COM SUCESSO!")
print("="*70)
print("\nArquivos salvos em: interfaces/teoria/plots/")
print("  1. fases_modulacao_bpsk.png")
print("  2. fases_modulacao_qpsk.png")
print("  3. comparacao_bpsk_qpsk_zoom.png")
print("\n" + "="*70)
