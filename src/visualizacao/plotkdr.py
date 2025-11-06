# Importa a biblioteca matplotlib para geração de gráficos
import matplotlib.pyplot as plt

def plot_kdr(snr_db, dados_todos_sigmas):
    """
    Função que plota 4 subplots em grid 2x2, um para cada parâmetro Rayleigh
    """
    # Cria uma figura com 4 subplots em grid 2x2
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('KDR em função de SNR - Parâmetros Rayleigh', fontsize=16, fontweight='bold')
    
    # Lista dos sigmas ordenados
    sigmas_ordenados = sorted(dados_todos_sigmas.keys())
    
    # Posições dos subplots no grid 2x2
    posicoes = [(0, 0), (0, 1), (1, 0), (1, 1)]
    
    for i, sigma in enumerate(sigmas_ordenados):
        dados = dados_todos_sigmas[sigma]
        row, col = posicoes[i]
        ax = axes[row, col]
        
        # Plota as três linhas no subplot atual
        ax.plot(snr_db, dados['kdr_rates'], 
                marker='o', linestyle='-', color='red', linewidth=2,
                label='KDR antes da reconciliação')
        
        ax.plot(snr_db, dados['kdr_pos_rates'], 
                marker='o', linestyle='-', color='blue', linewidth=2,
                label='KDR pós reconciliação')
        
        ax.plot(snr_db, dados['kdr_amplificacao_rates'], 
                marker='s', linestyle='-', color='green', linewidth=2,
                label='KDR pós amplificação (SHA-256)')

        # Configurações de cada subplot
        ax.set_xlabel('SNR (dB)')
        ax.set_ylabel('Key Disagreement Rate (KDR) (%)')
        ax.set_title(f'Rayleigh σ = {sigma}')
        ax.grid(True, alpha=0.3)
        
        # Escala automática do eixo Y baseada nos dados
        todos_valores = (dados['kdr_rates'] + dados['kdr_pos_rates'] + 
                        dados['kdr_amplificacao_rates'])
        y_min = max(0, min(todos_valores) - 5)  # Margem de 5% abaixo do mínimo
        y_max = min(100, max(todos_valores) + 5)  # Margem de 5% acima do máximo
        ax.set_ylim(y_min, y_max)
        
        ax.legend()

    # Ajusta o layout automaticamente
    plt.tight_layout()

    # Exibe o gráfico na tela
    plt.show()
