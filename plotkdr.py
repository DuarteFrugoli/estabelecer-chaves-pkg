# Importa a biblioteca matplotlib para geração de gráficos
import matplotlib.pyplot as plt

def plot_kdr(snr_db, kdr_rates, kdr_pos_rates, rayleigh_param, kdr_amplificacao_rates=None):
    """Função que plota um gráfico de linha com os dados de decibéis e KDR (Key Disagreement Rate) antes e pós reconciliação"""
    # Define o tamanho da figura do gráfico
    plt.figure(figsize=(10, 6))

    # Plota KDR antes da reconciliação em vermelho
    plt.plot(snr_db, kdr_rates, marker='o', linestyle='-', color='red', label='KDR antes da reconciliação')

    # Plota KDR pós reconciliação em azul
    plt.plot(snr_db, kdr_pos_rates, marker='o', linestyle='-', color='blue', label='KDR pós reconciliação')

    # Plota KDR pós amplificação se fornecido
    if kdr_amplificacao_rates is not None:
        plt.plot(snr_db, kdr_amplificacao_rates, marker='s', linestyle='-', color='green', label='KDR pós amplificação (SHA-256)')

    # Define o rótulo do eixo X como "Decibéis"
    plt.xlabel('SNR (dB)')

    # Define o rótulo do eixo Y como "Key Disagreement Rate"
    plt.ylabel('Key Disagreement Rate (KDR) (%)')

    # Define o título do gráfico
    titulo = f'KDR em função de SNR (Rayleigh sigma = {rayleigh_param})'
    if kdr_amplificacao_rates is not None:
        titulo += ' - Com Amplificação de Privacidade'
    plt.title(titulo)

    # Ativa a grade (linhas de fundo para facilitar a leitura dos valores)
    plt.grid(True)

    # Ajusta o layout automaticamente para não cortar os elementos do gráfico
    plt.tight_layout()

    # trava o eixo Y de 0 a 100
    plt.ylim(0, 100)

    # Adiciona legenda para os rótulos das linhas
    plt.legend()

    # Exibe o gráfico na tela
    plt.show()
