# Importa a biblioteca matplotlib para geração de gráficos
import matplotlib.pyplot as plt

def plot_kdr(snr_db, dados_todos_sigmas):
    """
    Função que plota 3 subplots na mesma janela, um para cada parâmetro Rayleigh
    """
    # Cria uma figura com 3 subplots em linha
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle('KDR em função de SNR - Parâmetros Rayleigh', fontsize=16, fontweight='bold')
    
    # Lista dos sigmas ordenados
    sigmas_ordenados = sorted(dados_todos_sigmas.keys())
    
    for i, sigma in enumerate(sigmas_ordenados):
        dados = dados_todos_sigmas[sigma]
        ax = axes[i]
        
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

    # Ajusta o layout automaticamente
    plt.tight_layout()

    # Exibe o gráfico na tela
    plt.show()
