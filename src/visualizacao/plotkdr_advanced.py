# Importa a biblioteca matplotlib para geração de gráficos
import matplotlib.pyplot as plt

def plot_kdr_advanced(snr_db, dados_sigma, rayleigh_sigma, modulacao='bpsk'):
    """
    Função que plota um único gráfico com os dados de KDR para parâmetros personalizados.
    
    Args:
        snr_db (array): Array de valores SNR em dB
        dados_sigma (dict): Dicionário com 'kdr_rates', 'kdr_pos_rates', 'kdr_amplificacao_rates'
        rayleigh_sigma (float): Valor do parâmetro sigma usado na simulação
        modulacao (str): Tipo de modulação ('bpsk' ou 'qpsk')
    """
    # Cria figura única
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Título descritivo
    potencia_media = 2 * rayleigh_sigma**2
    potencia_db = 10 * potencia_media if potencia_media > 0 else 0
    
    fig.suptitle(f'KDR em função de SNR - Simulação Avançada\n'
                 f'Modulação: {modulacao.upper()} | σ = {rayleigh_sigma:.4f} (E[|h|²] = {potencia_media:.4f})',
                 fontsize=14, fontweight='bold')
    
    # Plota as três linhas
    ax.plot(snr_db, dados_sigma['kdr_rates'], 
            marker='o', linestyle='-', color='red', linewidth=2, markersize=6,
            label='KDR antes da reconciliação')
    
    ax.plot(snr_db, dados_sigma['kdr_pos_rates'], 
            marker='o', linestyle='-', color='blue', linewidth=2, markersize=6,
            label='KDR pós reconciliação')
    
    ax.plot(snr_db, dados_sigma['kdr_amplificacao_rates'], 
            marker='s', linestyle='-', color='green', linewidth=2, markersize=6,
            label='KDR pós amplificação (SHA-256)')

    # Configurações do gráfico
    ax.set_xlabel('SNR (dB)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Key Disagreement Rate (KDR) (%)', fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3, linestyle='--')
    
    # Escala automática do eixo Y baseada nos dados
    todos_valores = (dados_sigma['kdr_rates'] + dados_sigma['kdr_pos_rates'] + 
                    dados_sigma['kdr_amplificacao_rates'])
    y_min = max(0, min(todos_valores) - 5)  # Margem de 5% abaixo
    y_max = min(100, max(todos_valores) + 5)  # Margem de 5% acima
    ax.set_ylim(y_min, y_max)
    
    # Limites do eixo X
    ax.set_xlim([snr_db[0], snr_db[-1]])
    
    # Legenda
    ax.legend(fontsize=11, loc='best', framealpha=0.95, shadow=True)
    
    # Adiciona informações técnicas
    info_text = (
        f"Parâmetros:\n"
        f"• Rayleigh σ = {rayleigh_sigma:.6f}\n"
        f"• E[|h|²] = {potencia_media:.4f}\n"
        f"• Modulação: {modulacao.upper()}\n"
        f"• SNR: {snr_db[0]:.1f} a {snr_db[-1]:.1f} dB\n"
        f"• Pontos: {len(snr_db)}"
    )
    
    ax.text(0.02, 0.98, info_text,
            transform=ax.transAxes, fontsize=9,
            verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='lightyellow', 
                     alpha=0.9, edgecolor='orange', linewidth=2))
    
    # Ajusta o layout
    plt.tight_layout()
    
    # Exibe o gráfico
    plt.show()


if __name__ == "__main__":
    """
    Teste básico da função
    """
    import numpy as np
    
    # Dados de teste
    snr_range = np.linspace(-10, 30, 18)
    dados_teste = {
        'kdr_rates': np.linspace(80, 10, 18),
        'kdr_pos_rates': np.linspace(50, 2, 18),
        'kdr_amplificacao_rates': np.linspace(30, 0.5, 18)
    }
    
    plot_kdr_advanced(snr_range, dados_teste, 1.0/np.sqrt(2), 'bpsk')
