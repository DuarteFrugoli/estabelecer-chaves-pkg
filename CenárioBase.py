from abc import ABC, abstractmethod

# Classe base abstrata para cenários de canais
class CenárioBase(ABC):
    def __init__(self, media, variancia, ntestes):
        # Inicializa os parâmetros do cenário
        self.media = media
        self.variancia = variancia
        self.ntestes = ntestes

    @abstractmethod
    def cenario(self):
        # Método abstrato para executar o cenário (deve ser implementado nas subclasses)
        pass

    @abstractmethod
    def calculaY(self):
        # Método abstrato para calcular Y (deve ser implementado nas subclasses)
        pass

    def encontraErros(self, x, y):
        # Conta o número de erros entre duas listas de bits x e y
        return sum(1 for i in range(len(x)) if y[i] != x[i])

    def hamming_distance(self, s1, s2):
        # Calcula a distância de Hamming entre duas strings binárias
        length = min(len(s1), len(s2))
        return sum(ch1 != ch2 for ch1, ch2 in zip(s1[:length], s2[:length]))

    def comparacao_mais_proxima(self, y, tabela):
        # Compara y com todos os códigos na tabela e retorna o mais próximo (menor distância de Hamming)
        min_dist = float('inf')
        pos = -1

        for i, code in enumerate(tabela):
            aux = self.hamming_distance(y, code)
            if aux < min_dist:
                pos = i
                min_dist = aux

        return tabela[pos]

    def encontraParidade(self, y, tabela):
        # Encontra a paridade entre y e o código mais próximo na tabela
        fc = self.comparacao_mais_proxima(y, tabela)
        P = self.subtract_binary(fc, y)
        return P

    def comparaSinais(self, y, P, tabela):
        # Compara sinais para gerar a chave final
        fc = self.comparacao_mais_proxima(self.subtract_binary(y, P), tabela)
        min_len = min(len(fc), len(P))
        fc_padded = fc[:min_len]
        P_padded = P[:min_len]
        return self.xor_binary(fc_padded, P_padded)

    def subtract_binary(self, fc, y):
        # Subtrai dois valores binários (bit a bit, XOR)
        assert len(fc) == len(y), "Os valores devem ter o mesmo número de dígitos binários."
        min_len = min(len(fc), len(y))
        return ''.join('0' if a == b else '1' for a, b in zip(fc[:min_len], y[:min_len]))

    def xor_binary(self, fc, P):
        # Realiza operação XOR entre duas strings binárias
        assert len(fc) == len(P), "Os valores devem ter o mesmo número de dígitos binários."
        return ''.join('0' if a == b else '1' for a, b in zip(fc, P))