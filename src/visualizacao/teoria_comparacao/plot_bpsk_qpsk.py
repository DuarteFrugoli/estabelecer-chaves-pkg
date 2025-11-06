"""
Módulo para comparação entre BER teórica e BER simulada em canal Rayleigh.

Compara as curvas BER teóricas (fórmulas analíticas para Rayleigh) com os 
resultados práticos obtidos através da simulação do canal Rayleigh.
Valida se a simulação está reproduzindo corretamente o comportamento teórico.
"""

import numpy as np
import matplotlib.pyplot as plt
from src.teoria.bpsk_qpsk import ber_teorica_rayleigh_bpsk, ber_teorica_rayleigh_qpsk
from src.canal.canal import simular_canal


def simular_ber_pratica(snr_db_range, modulacao='bpsk', num_bits=10000, num_testes=100, rayleigh_sigma=1.0/np.sqrt(2)):
    """
    Simula a BER prática usando canal Rayleigh (com fading).
    
    Args:
        snr_db_range (array): Range de SNR em dB
        modulacao (str): 'bpsk' ou 'qpsk'
        num_bits (int): Número de bits por teste
        num_testes (int): Número de testes para média estatística
        rayleigh_sigma (float): Parâmetro sigma do canal Rayleigh (padrão: 1/√2 para potência normalizada)
        
    Returns:
        array: BER simulada para cada valor de SNR
    """
    ber_simulada = []
    
    for snr_db in snr_db_range:
        # Converte SNR de dB para linear
        snr_linear = 10 ** (snr_db / 10)
        
        # Calcula variância do ruído: sigma² = Es / (2·SNR)
        # Assumindo energia de símbolo Es = 1
        variancia_ruido = 1.0 / (2 * snr_linear)
        media_ruido = 0.0
        
        total_erros = 0
        total_bits = 0
        
        for _ in range(num_testes):
            # Gera sequência de bits aleatória
            bits_transmitidos = [np.random.randint(0, 2) for _ in range(num_bits)]
            
            # Canal Rayleigh: ganho variável com fading
            num_ganhos = num_bits // 2 if modulacao == 'qpsk' and num_bits % 2 == 0 else num_bits
            if modulacao == 'qpsk' and num_bits % 2 != 0:
                num_ganhos = (num_bits + 1) // 2
            else:
                num_ganhos = num_bits
                
            ganho_canal = np.random.rayleigh(rayleigh_sigma, num_ganhos)  # Fading Rayleigh
            
            # Simula canal
            bits_recebidos = simular_canal(ganho_canal, bits_transmitidos, 
                                          variancia_ruido, media_ruido, modulacao)
            
            # Conta erros
            erros = sum(1 for b_tx, b_rx in zip(bits_transmitidos, bits_recebidos) if b_tx != b_rx)
            total_erros += erros
            total_bits += num_bits
        
        # Calcula BER média
        ber = total_erros / total_bits if total_bits > 0 else 0
        ber_simulada.append(ber)
    
    return np.array(ber_simulada)


def plotar_teorico_vs_simulado_bpsk(snr_db_range=None, num_testes=100, 
                                     rayleigh_sigma=1.0/np.sqrt(2), salvar=False, 
                                     nome_arquivo='bpsk_teorico_vs_simulado.png'):
    """
    Plota comparação entre BER teórica e simulada para canal Rayleigh (BPSK).
    
    Args:
        snr_db_range (array, optional): Range de SNR em dB
        num_testes (int): Número de testes para simulação
        rayleigh_sigma (float): Parâmetro sigma do canal Rayleigh
        salvar (bool): Se True, salva o gráfico
        nome_arquivo (str): Nome do arquivo
        
    Returns:
        tuple: (fig, ax)
    """
    if snr_db_range is None:
        snr_db_range = np.linspace(-5, 15, 15)  # Menos pontos para simulação
    
    print(f"\n🔄 Simulando BER prática para BPSK ({num_testes} testes por SNR)...")
    
    # Calcula BER teórica (Rayleigh)
    ber_teorica = ber_teorica_rayleigh_bpsk(snr_db_range)
    
    # Simula BER prática (Rayleigh)
    ber_simulada = simular_ber_pratica(snr_db_range, 'bpsk', 
                                       num_bits=10000, 
                                       num_testes=num_testes,
                                       rayleigh_sigma=rayleigh_sigma)
    
    # Cria figura
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Plota curvas
    ax.semilogy(snr_db_range, ber_teorica, 'b-', linewidth=2.5, 
                label='Teórico: Rayleigh', zorder=2)
    ax.semilogy(snr_db_range, ber_simulada, 'ro--', linewidth=2, 
                markersize=8, markerfacecolor='red', markeredgewidth=1.5,
                label=f'Simulado: Rayleigh (σ={rayleigh_sigma})', zorder=3)
    
    # Configurações
    ax.set_xlabel('Eb/N0 (dB)', fontsize=13, fontweight='bold')
    ax.set_ylabel('Taxa de Erro de Bit (BER)', fontsize=13, fontweight='bold')
    ax.set_title(f'BPSK: BER Teórica vs Simulada (Canal Rayleigh)\n'
                 f'{num_testes} testes por ponto', 
                 fontsize=14, fontweight='bold', pad=20)
    
    ax.grid(True, which='both', linestyle='--', alpha=0.4)
    ax.legend(fontsize=11, loc='upper right', framealpha=0.95)
    
    ax.set_ylim([1e-5, 0.5])
    ax.set_xlim([snr_db_range[0], snr_db_range[-1]])
    
    # Adiciona informações
    info_text = (
        f"Simulação:\n"
        f"• {num_testes} testes/SNR\n"
        f"• 10.000 bits/teste\n"
        f"• Rayleigh σ={rayleigh_sigma}\n"
        f"• Modulação: BPSK\n\n"
        f"Validação:\n"
        f"Curvas devem coincidir se\n"
        f"simulação Rayleigh correta"
    )
    
    ax.text(0.02, 0.02, info_text,
            transform=ax.transAxes, fontsize=9,
            verticalalignment='bottom',
            bbox=dict(boxstyle='round', facecolor='lightyellow', 
                     alpha=0.8, edgecolor='orange', linewidth=1.5))
    
    plt.tight_layout()
    
    if salvar:
        plt.savefig(nome_arquivo, dpi=300, bbox_inches='tight')
        print(f"✓ Gráfico salvo: {nome_arquivo}")
    
    return fig, ax


def plotar_teorico_vs_simulado_qpsk(snr_db_range=None, num_testes=100, 
                                     rayleigh_sigma=1.0/np.sqrt(2), salvar=False, 
                                     nome_arquivo='qpsk_teorico_vs_simulado.png'):
    """
    Plota comparação entre BER teórica e simulada para canal Rayleigh (QPSK).
    
    Args:
        snr_db_range (array, optional): Range de SNR em dB
        num_testes (int): Número de testes para simulação
        rayleigh_sigma (float): Parâmetro sigma do canal Rayleigh
        salvar (bool): Se True, salva o gráfico
        nome_arquivo (str): Nome do arquivo
        
    Returns:
        tuple: (fig, ax)
    """
    if snr_db_range is None:
        snr_db_range = np.linspace(-5, 15, 15)
    
    print(f"\n🔄 Simulando BER prática para QPSK ({num_testes} testes por SNR)...")
    
    # Calcula BER teórica (Rayleigh)
    ber_teorica = ber_teorica_rayleigh_qpsk(snr_db_range)
    
    # Simula BER prática (Rayleigh)
    ber_simulada = simular_ber_pratica(snr_db_range, 'qpsk', 
                                       num_bits=10000, 
                                       num_testes=num_testes,
                                       rayleigh_sigma=rayleigh_sigma)
    
    # Cria figura
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Plota curvas
    ax.semilogy(snr_db_range, ber_teorica, 'g-', linewidth=2.5, 
                label='Teórico: Rayleigh', zorder=2)
    ax.semilogy(snr_db_range, ber_simulada, 'ms--', linewidth=2, 
                markersize=8, markerfacecolor='magenta', markeredgewidth=1.5,
                label=f'Simulado: Rayleigh (σ={rayleigh_sigma})', zorder=3)
    
    # Configurações
    ax.set_xlabel('Eb/N0 (dB)', fontsize=13, fontweight='bold')
    ax.set_ylabel('Taxa de Erro de Bit (BER)', fontsize=13, fontweight='bold')
    ax.set_title(f'QPSK: BER Teórica vs Simulada (Canal Rayleigh)\n'
                 f'{num_testes} testes por ponto', 
                 fontsize=14, fontweight='bold', pad=20)
    
    ax.grid(True, which='both', linestyle='--', alpha=0.4)
    ax.legend(fontsize=11, loc='upper right', framealpha=0.95)
    
    ax.set_ylim([1e-5, 0.5])
    ax.set_xlim([snr_db_range[0], snr_db_range[-1]])
    
    # Adiciona informações
    info_text = (
        f"Simulação:\n"
        f"• {num_testes} testes/SNR\n"
        f"• 10.000 bits/teste\n"
        f"• Rayleigh σ={rayleigh_sigma}\n"
        f"• Modulação: QPSK\n\n"
        f"Validação:\n"
        f"Curvas devem coincidir se\n"
        f"simulação Rayleigh correta"
    )
    
    ax.text(0.02, 0.02, info_text,
            transform=ax.transAxes, fontsize=9,
            verticalalignment='bottom',
            bbox=dict(boxstyle='round', facecolor='lightcyan', 
                     alpha=0.8, edgecolor='blue', linewidth=1.5))
    
    plt.tight_layout()
    
    if salvar:
        plt.savefig(nome_arquivo, dpi=300, bbox_inches='tight')
        print(f"✓ Gráfico salvo: {nome_arquivo}")
    
    return fig, ax


def plotar_comparacao_ambas_modulacoes(snr_db_range=None, num_testes=100,
                                        rayleigh_sigma=1.0/np.sqrt(2), salvar=False,
                                        nome_arquivo='comparacao_completa_teorico_vs_simulado.png'):
    """
    Plota comparação de BPSK e QPSK: teoria vs simulação em canal Rayleigh.
    
    Args:
        snr_db_range (array, optional): Range de SNR em dB
        num_testes (int): Número de testes para simulação
        rayleigh_sigma (float): Parâmetro sigma do canal Rayleigh
        salvar (bool): Se True, salva o gráfico
        nome_arquivo (str): Nome do arquivo
        
    Returns:
        tuple: (fig, ax)
    """
    if snr_db_range is None:
        snr_db_range = np.linspace(-5, 15, 15)
    
    print(f"\n🔄 Simulando BER para BPSK e QPSK...")
    
    # BPSK
    ber_teorica_bpsk_vals = ber_teorica_rayleigh_bpsk(snr_db_range)
    ber_simulada_bpsk = simular_ber_pratica(snr_db_range, 'bpsk', 
                                            num_bits=10000, num_testes=num_testes,
                                            rayleigh_sigma=rayleigh_sigma)
    
    # QPSK
    ber_teorica_qpsk_vals = ber_teorica_rayleigh_qpsk(snr_db_range)
    ber_simulada_qpsk = simular_ber_pratica(snr_db_range, 'qpsk', 
                                            num_bits=10000, num_testes=num_testes,
                                            rayleigh_sigma=rayleigh_sigma)
    
    # Cria figura
    fig, ax = plt.subplots(figsize=(14, 9))
    
    # Plota BPSK
    ax.semilogy(snr_db_range, ber_teorica_bpsk_vals, 'b-', linewidth=2.5, 
                label='BPSK - Teórico (Rayleigh)', zorder=2)
    ax.semilogy(snr_db_range, ber_simulada_bpsk, 'ro--', linewidth=2, 
                markersize=8, markerfacecolor='red', markeredgewidth=1.5,
                label=f'BPSK - Simulado (Rayleigh)', zorder=3)
    
    # Plota QPSK
    ax.semilogy(snr_db_range, ber_teorica_qpsk_vals, 'g-', linewidth=2.5, 
                label='QPSK - Teórico (Rayleigh)', zorder=2)
    ax.semilogy(snr_db_range, ber_simulada_qpsk, 'ms--', linewidth=2, 
                markersize=8, markerfacecolor='magenta', markeredgewidth=1.5,
                label=f'QPSK - Simulado (Rayleigh)', zorder=3)
    
    # Configurações
    ax.set_xlabel('Eb/N0 (dB)', fontsize=14, fontweight='bold')
    ax.set_ylabel('Taxa de Erro de Bit (BER)', fontsize=14, fontweight='bold')
    ax.set_title(f'BER Teórica vs Simulada: Canal Rayleigh\n'
                 f'BPSK e QPSK (σ={rayleigh_sigma})', 
                 fontsize=15, fontweight='bold', pad=20)
    
    ax.grid(True, which='both', linestyle='--', alpha=0.4)
    ax.legend(fontsize=12, loc='upper right', framealpha=0.95, ncol=2)
    
    ax.set_ylim([1e-5, 0.5])
    ax.set_xlim([snr_db_range[0], snr_db_range[-1]])
    
    # Adiciona informações
    info_text = (
        f"Simulação:\n"
        f"• {num_testes} testes/SNR\n"
        f"• 10.000 bits/teste\n"
        f"• Rayleigh σ={rayleigh_sigma}\n\n"
        f"Validação:\n"
        f"• Sólido: Teoria Rayleigh\n"
        f"• Tracejado: Simulação\n"
        f"• Curvas devem coincidir\n"
        f"• BPSK ≈ QPSK (Eb/N0)"
    )
    
    ax.text(0.02, 0.98, info_text,
            transform=ax.transAxes, fontsize=10,
            verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='lightgray', 
                     alpha=0.9, edgecolor='black', linewidth=2))
    
    plt.tight_layout()
    
    if salvar:
        plt.savefig(nome_arquivo, dpi=300, bbox_inches='tight')
        print(f"✓ Gráfico salvo: {nome_arquivo}")
    
    return fig, ax


def gerar_todos_graficos_comparacao(snr_db_range=None, num_testes=100, 
                                     rayleigh_sigma=1.0/np.sqrt(2), salvar=True):
    """
    Gera todos os gráficos de comparação teoria vs simulação em canal Rayleigh.
    
    Args:
        snr_db_range (array, optional): Range de SNR em dB
        num_testes (int): Número de testes
        rayleigh_sigma (float): Parâmetro sigma do Rayleigh
        salvar (bool): Se True, salva os gráficos
        
    Returns:
        dict: Dicionário com todas as figuras
    """
    print("\n" + "="*70)
    print("COMPARAÇÃO: Teoria Rayleigh vs Simulação Rayleigh")
    print("="*70)
    print(f"Parâmetros: {num_testes} testes/SNR, Rayleigh σ={rayleigh_sigma}")
    print("="*70 + "\n")
    
    figuras = {}
    
    print("1. BPSK: Teoria vs Simulação Rayleigh...")
    figuras['bpsk'] = plotar_teorico_vs_simulado_bpsk(snr_db_range, num_testes, 
                                                       rayleigh_sigma, salvar)
    
    print("2. QPSK: Teoria vs Simulação Rayleigh...")
    figuras['qpsk'] = plotar_teorico_vs_simulado_qpsk(snr_db_range, num_testes, 
                                                       rayleigh_sigma, salvar)
    
    print("3. Comparação Completa (ambas modulações)...")
    figuras['completo'] = plotar_comparacao_ambas_modulacoes(snr_db_range, num_testes, 
                                                              rayleigh_sigma, salvar)
    
    print("\n" + "="*70)
    print("✓ TODOS OS GRÁFICOS GERADOS!")
    print("="*70 + "\n")
    
    return figuras


if __name__ == "__main__":
    """
    Execução direta para gerar gráficos de exemplo.
    """
    import matplotlib.pyplot as plt
    
    # Define parâmetros
    snr_range = np.linspace(-5, 15, 12)  # 12 pontos de SNR
    num_testes = 50  # 50 testes por ponto (ajuste conforme necessário)
    rayleigh_sigma = 1.0 / np.sqrt(2)  # σ normalizado (E[|h|²] = 1)
    
    # Gera todos os gráficos
    figuras = gerar_todos_graficos_comparacao(snr_range, num_testes, 
                                               rayleigh_sigma, salvar=True)
    
    # Mostra os gráficos
    plt.show()
