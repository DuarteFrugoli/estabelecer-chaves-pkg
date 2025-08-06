import numpy as np
import galois
import random

def get_tamanho_bits_informacao(tamanho_cadeia_bits):
    """Retorna o valor de k (número de bits de informação) para o código especificado."""
    # Dicionário com valores de k para diferentes tamanhos de código BCH
    tamanho_bits_informacao = {
        7: 4,
        15: 5,
        127: 64,
        255: 247
    }
    return tamanho_bits_informacao.get(tamanho_cadeia_bits, None)  # Retorna None se o valor de tamanho_cadeia_bits não for encontrado

def binary_product(X, Y):
    """Calcula o produto de uma matriz e vetor no campo binário."""
    A = X.dot(Y)
    try:
        A = A.toarray()
    except AttributeError:
        pass
    return A % 2

def encode_bch(tamanho_cadeia_bits, tamanho_bits_informacao, info_word):
    """Codifica uma palavra de informação usando o código BCH."""
    t = {7: 1, 15: 3, 127: 10, 255: 1}
    d = 2 * t.get(tamanho_cadeia_bits, 0) + 1
    bch_code = galois.BCH(tamanho_cadeia_bits, tamanho_bits_informacao, d)
    return ''.join(map(str, bch_code.encode(info_word)))

def generate_code_table(tamanho_cadeia_bits, tamanho_espaco_amostral=None):
    """Gera uma tabela de códigos para todas as palavras de informação possíveis."""
    tamanho_bits_informacao = get_tamanho_bits_informacao(tamanho_cadeia_bits)

    if tamanho_espaco_amostral is None:
        tamanho_espaco_amostral = 2 ** tamanho_bits_informacao  # tamanho_espaco_amostral: Tamanho do espaço amostral para geração da tabela de códigos

    # info_words: Lista de todas as palavras de informação possíveis (ou amostradas, se o espaço for grande)
    if tamanho_cadeia_bits > 15:
        info_words = [list(map(int, format(random.randint(0, 2**tamanho_bits_informacao - 1), f'0{tamanho_bits_informacao}b'))) for _ in range(tamanho_espaco_amostral)]

    elif tamanho_cadeia_bits <= 15:
        info_words = [list(map(int, format(i, f'0{tamanho_bits_informacao}b'))) for i in range(tamanho_espaco_amostral)]

    # Seleciona o codificador apropriado
    code_table = [encode_bch(tamanho_cadeia_bits, tamanho_bits_informacao, info_word) for info_word in info_words]  # code_table: Lista de todas as palavras codificadas geradas a partir das palavras de informação

    for codeword in code_table:
        print(f'Código BCH: {codeword}')
    return code_table