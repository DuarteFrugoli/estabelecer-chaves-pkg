import galois
import random

from util.binario_util import calcular_distancia_hamming

# Retorna o valor de k (número de bits de informação) para o código especificado
def get_tamanho_bits_informacao(tamanho_cadeia_bits):
    """Retorna o valor de k (número de bits de informação) para o código especificado."""
    # Dicionário com valores de k para diferentes tamanhos de código BCH
    tamanho_bits_informacao = {
        7: 4,
        15: 5,
        127: 64,
        255: 247
    }
    return tamanho_bits_informacao.get(tamanho_cadeia_bits, None) # Retorna None se o valor de tamanho_cadeia_bits não for encontrado

def codificar_bch(tamanho_cadeia_bits, tamanho_bits_informacao, bits_informacao):
    """Codifica uma palavra de informação usando o código BCH."""
    t = {7: 1, 15: 3, 127: 10, 255: 8} # Número de erros que o código pode corrigir
    d = 2 * t.get(tamanho_cadeia_bits, 0) + 1 # Distância mínima do código
    codigo_bch = galois.BCH(tamanho_cadeia_bits, tamanho_bits_informacao, d) 
    return codigo_bch.encode(bits_informacao).tolist()

def gerar_tabela_codigos_bch(tamanho_cadeia_bits, tamanho_bits_informacao, tamanho_espaco_amostral=None):
    """Gera uma tabela de códigos para todas as palavras de informação possíveis (sem repetições)."""
    # Se o tamanho do espaço amostral não for especificado, calcula automaticamente
    if tamanho_espaco_amostral is None:
        tamanho_espaco_amostral = 2 ** tamanho_bits_informacao

    # palavras_informacao: Lista de todas as palavras de informação possíveis (ou amostradas, se o espaço for grande)
    if tamanho_cadeia_bits > 15:
        palavras_informacao_set = set()
        while len(palavras_informacao_set) < tamanho_espaco_amostral:
            palavra = tuple(map(int, format(random.randint(0, 2**tamanho_bits_informacao - 1), f'0{tamanho_bits_informacao}b')))
            palavras_informacao_set.add(palavra)
        palavras_informacao = [list(p) for p in palavras_informacao_set]
    else:
        palavras_informacao = [list(map(int, format(i, f'0{tamanho_bits_informacao}b'))) for i in range(tamanho_espaco_amostral)]

    # Codifica as palavras de informação do espaço amostral usando o código BCH
    tabela_codigos = [codificar_bch(tamanho_cadeia_bits, tamanho_bits_informacao, bits_informacao) for bits_informacao in palavras_informacao]

    return tabela_codigos

def encontrar_codigo_mais_proximo(sinal_recebido, tabela_codigos):
    """
    Compara sinal_recebido com todos os códigos na tabela e retorna o mais próximo (menor distância de Hamming).
    """
    if not tabela_codigos:
        raise ValueError("A tabela de códigos está vazia.")

    min_dist = float('inf')
    indice_min = -1

    for i, code in enumerate(tabela_codigos):
        aux = calcular_distancia_hamming(sinal_recebido, code)
        if aux < min_dist:
            indice_min = i
            min_dist = aux

    return tabela_codigos[indice_min]