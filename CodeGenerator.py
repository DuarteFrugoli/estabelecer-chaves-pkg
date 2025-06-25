import numpy as np
import galois
import random

# Classe responsável por gerar códigos de correção de erro e suas matrizes geradoras
class CodeGenerator:
    def __init__(self, n_bits):
        self.n_bits = n_bits  # Número de bits do código (tamanho do bloco de código)
        self.k_bits = self.k_bits_size()         # Número de bits de informação (tamanho da palavra de informação)

    def k_bits_size(self):
        """Retorna o valor de k (número de bits de informação) para o código especificado."""
        # Dicionário com valores de k para diferentes tamanhos de código BCH
        k = {
            7: 4,
            15: 5,
            127: 64,
            255: 247
        }
        return k.get(self.n_bits, None)  # Retorna None se o valor de n_bits não for encontrado
        
        return None  # Retorna None explicitamente se o código não for encontrado

    @staticmethod
    def binary_product(X, Y):
        """Calcula o produto de uma matriz e vetor no campo binário."""
        A = X.dot(Y)
        try:
            A = A.toarray()
        except AttributeError:
            pass
        return A % 2

    def encode_bch(self, info_word):
        """Codifica uma palavra de informação usando o código BCH."""
        t = {7: 1, 15: 3, 127: 10, 255: 1}
        d = 2 * t.get(self.n_bits, 0) + 1
        bch_code = galois.BCH(self.n_bits, self.k_bits, d)
        return ''.join(map(str, bch_code.encode(info_word)))

    def generate_code_table(self, size=None):
        """Gera uma tabela de códigos para todas as palavras de informação possíveis."""
        if size is None:
            size = 2 ** self.k_bits  # size: Tamanho do espaço amostral para geração da tabela de códigos

        # info_words: Lista de todas as palavras de informação possíveis (ou amostradas, se o espaço for grande)
        if self.n_bits > 15:
            info_words = [list(map(int, format(random.randint(0, 2**self.k_bits - 1), f'0{self.k_bits}b'))) for _ in range(size)]

        elif self.n_bits <= 15:
            info_words = [list(map(int, format(i, f'0{self.k_bits}b'))) for i in range(size)]

        # Seleciona o codificador apropriado
        encoder = self.encode_bch
        code_table = [encoder(info_word) for info_word in info_words]  # code_table: Lista de todas as palavras codificadas geradas a partir das palavras de informação

        for codeword in code_table:
            print(f'Código BCH: {codeword}')
        return code_table
