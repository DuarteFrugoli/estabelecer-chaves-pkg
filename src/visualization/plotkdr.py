# Importa a biblioteca matplotlib para geração de gráficos
import matplotlib.pyplot as plt

def plot_kdr(snr_db, dados_todos_sigmas):
    """
    Função que plota 3 subplots na mesma janela, um para cada parâmetro Rayleigh
    """
    # Cria uma figura com 3 subplots em grid 2x2
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('KDR em função de SNR - Parâmetros Rayleigh', fontsize=16, fontweight='bold')
    
    # Lista dos sigmas ordenados
    sigmas_ordenados = sorted(dados_todos_sigmas.keys())
    
    # Posições dos subplots no grid 2x2
    posicoes = [(0, 0), (0, 1), (1, 0)]
    
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
        ax.set_ylim(0, 100)
        ax.legend()

    # Remove o subplot vazio (posição [1,1])
    fig.delaxes(axes[1, 1])

    # Ajusta o layout automaticamente
    plt.tight_layout()

    # Exibe o gráfico na tela
    plt.show()
