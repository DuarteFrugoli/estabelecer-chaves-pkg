import os
from matplotlib import pyplot as plt

class Plotagem:
    def __init__(self):
        pass

    @staticmethod
    def fix_plot(data):
        return [value for value in data for _ in range(100)]

    def plota_diferencas(self, x, y1, y2, tam):
        indices = range(tam * 100)

        x_fixed = self.fix_plot(x)
        y1_fixed = self.fix_plot(y1)
        y2_fixed = self.fix_plot(y2)

        fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(15, 7), tight_layout=True)

        for ax, y_fixed, title in zip(axes, [y1_fixed, y2_fixed], ['Y1', 'Y2']):
            ax.plot(indices, x_fixed, 'r--', label='X')
            ax.plot(indices, y_fixed, 'b', label=title)
            ax.set_title(title)
            ax.set_xlabel('Índice do Bit')
            ax.set_ylabel('Valor do Bit')
            ax.legend()
            ax.margins(0)

        plt.show()

    def plota(self, porcentagens, nBits):
        cenarios = [
            'Ruído Nulo Canal Unitário',
            'Baixo Ruído Canal Unitário',
            'Baixo Ruído Canal Rayleigh',
            'Alto Ruído Canal Unitário',
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
