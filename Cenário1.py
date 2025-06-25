import random

from CenárioBase import CenárioBase
from Plotagem import Plotagem

# Classe que representa o cenário de ruído nulo em canal unitário
class RuidoNuloCanalUnitario(CenárioBase, Plotagem):
    def calculaY(self, x):
        # Converte cada valor de x em 1 se for maior que 0.5, senão 0
        return [1 if x[i] > 0.5 else 0 for i in range(len(x))]

    def cenario(self, x, plot, size, tabela):
        # Executa o cenário de ruído nulo no canal unitário

        print("Cenário 1: Ruido Nulo Canal Unitario\n")

        contagem_de_acertos = 0  # Conta quantas vezes a chave gerada foi correta

        for i in range(self.ntestes):
            print(f'Teste {i+1}/{self.ntestes}')
            print('x =', x)

            y1 = self.calculaY(x)  # Primeira saída do canal
            print('y1 =', y1)
            erros_y1 = self.encontraErros(x, y1)  # Conta erros entre x e y1
            print('Erros do y1 =', erros_y1)

            y2 = self.calculaY(x)  # Segunda saída do canal
            print('y2 =', y2)
            erros_y2 = self.encontraErros(x, y2)  # Conta erros entre x e y2
            print('Erros do y2 =', erros_y2)

            if plot:
                # Plota as diferenças entre x, y1 e y2
                self.plota_diferencas(x, y1, y2, len(x))

            toStringY1 = ''.join(map(str, y1))  # Converte y1 para string binária
            toStringY2 = ''.join(map(str, y2))  # Converte y2 para string binária
            
            # Método de reconciliação 2
            c = random.choice(tabela)  # Seleciona código aleatório da tabela
            s = self.xor_binary(toStringY1, c)
            c_B = self.xor_binary(toStringY2 , s)
            chave = self.xor_binary(s, self.comparacao_mais_proxima(c_B, tabela))
            print(f"Chave gerada por código BCH:", chave)

            if toStringY1 == chave:
                # Conta acerto se a chave gerada for igual a y1
                contagem_de_acertos += 1
            else:
                print(f"Não são iguais por BCH")

            print("\n--------------------------------------------------------")

        # Calcula a porcentagem de acertos
        porcentagem_de_acertos = contagem_de_acertos * 100.00 / self.ntestes
        print(f"Porcentagem de vezes que a chave gerada foi encontrada na tabela BCH: {porcentagem_de_acertos:.2f}%")

        if plot:
            # Plota os sinais e a porcentagem de acertos
            self.plotar(x, y1, y2, len(x), porcentagem_de_acertos)

        return porcentagem_de_acertos
