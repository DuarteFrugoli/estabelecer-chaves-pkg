import random

from CenárioBase import CenárioBase
from Plotagem import Plotagem

class AltoRuidoCanalRayleigh(CenárioBase, Plotagem):
    # Função para calcular y considerando o efeito Rayleigh (h) e ruído alto
    def calculaY(self, h, x, variancia, media, ntestes):
        # Gera ruído gaussiano
        # TODO: colocar a função em um lugar melhor e consertar os nomes
        def gerar_ruido_gaussiano(variancia, media):
            return [random.gauss(media, variancia) for _ in range(len(x))]

        n = gerar_ruido_gaussiano(variancia, media)
        # Calcula y aplicando o efeito Rayleigh e limiarização
        y = [1 if h[i] * x[i] + n[i] > 0.5 else 0 for i in range(len(x))]
        return y

    # Função principal do cenário
    def cenario(self, x, h1, h2, size, tabela, nBits):

        print("Cenário 5: Alto Ruido Canal Rayleigh\n")

        contagem_de_acertos = 0  # Contador de acertos

        for i in range(self.ntestes):
            print(f'Teste {i+1}/{self.ntestes}')
            print('x =', x)

            # Gera y1 com h1 e ruído alto
            y1 = self.calculaY(x, h1, self.variancia, self.media, nBits)
            print('y1 =', y1)
            erros_y1 = self.encontraErros(x, y1)
            print('Erros do y1 =', erros_y1)

            # Gera y2 com h2 e ruído alto
            y2 = self.calculaY(x, h2, self.variancia, self.media, nBits)
            print('y2 =', y2)
            erros_y2 = self.encontraErros(x, y2)
            print('Erros do y2 =', erros_y2)

            # Converte listas para strings binárias
            toStringY1 = ''.join(map(str, y1))
            toStringY2 = ''.join(map(str, y2))

            c = random.choice(tabela)
            s = self.xor_binary(toStringY1, c)
            c_B = self.xor_binary(toStringY2 , s)
            chave = self.xor_binary(s, self.comparacao_mais_proxima(c_B, tabela))
            print(f"Chave gerada por código de BCH:", chave)

            # Verifica se a chave gerada é igual ao y1
            if toStringY1 == chave:
                contagem_de_acertos += 1
            else:
                print(f"Não são iguais por BCH")


            print("\n--------------------------------------------------------")


        # Calcula a porcentagem de acertos
        porcentagem_de_acertos = contagem_de_acertos * 100.00 / self.ntestes
        print(f"Porcentagem de vezes que a chave gerada foi encontrada na tabela BCH: {porcentagem_de_acertos:.2f}%")

        return porcentagem_de_acertos