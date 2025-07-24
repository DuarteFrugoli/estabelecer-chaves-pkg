import os
from matplotlib import pyplot as plt

class Plotagem:
    def __init__(self):
        pass

    @staticmethod
    def fix_plot(data):
        return [value for value in data for _ in range(100)]

    def plota(self, porcentagens, nBits):
        cenarios = [
            'Alto Ruído Canal Rayleigh'
        ]

        # Apenas BCH será utilizado
        color = 'y'

        fig, ax = plt.subplots(figsize=(17, 7), tight_layout=True)
        bars = ax.bar(range(len(cenarios)), porcentagens, color=color, edgecolor='grey', label='BCH')

        ax.set_xlabel('Cenários')
        ax.set_ylabel('Porcentagem de Acertos (%)')
        ax.set_title(f'Porcentagem de Acertos em Diferentes Cenários para BCH', pad=20)
        ax.set_xticks(range(len(cenarios)))
        ax.set_xticklabels(cenarios, rotation=0, ha='center')
        ax.legend()
        ax.margins(0)

        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, yval, f'{yval:.2f}%', ha='center', va='bottom')

        plt.show()
