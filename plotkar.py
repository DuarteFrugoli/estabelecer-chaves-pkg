
# Importa a biblioteca matplotlib para geração de gráficos
import matplotlib.pyplot as plt

# TODO: trocar kar por kdr (padrão da literatura)
def plot_kar(snr_db, kar_rates):
    # Função que plota um gráfico de linha com os dados de decibéis e KAR (Key Agreement Rate)

    # Define o tamanho da figura do gráfico
    plt.figure(figsize=(8, 6))

    # Plota os dados com marcadores em cada ponto, linha contínua e cor azul
    plt.plot(snr_db, kar_rates, marker='o', linestyle='-', color='blue')

    # Define o rótulo do eixo X como "Decibéis"
    plt.xlabel('SNR (dB)')

    # Define o rótulo do eixo Y como "Key Agreement Rate"
    plt.ylabel('Key Agreement Rate (KAR)')

    # Define o título do gráfico
    plt.title('KAR em função de SNR')

    # Ativa a grade (linhas de fundo para facilitar a leitura dos valores)
    plt.grid(True)

    # Ajusta o layout automaticamente para não cortar os elementos do gráfico
    plt.tight_layout()

    # trava o eixo Y de 0 a 100
    plt.ylim(0, 100)

    # Exibe o gráfico na tela
    plt.show()
