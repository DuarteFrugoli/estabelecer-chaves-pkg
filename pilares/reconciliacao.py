import random
from util.binario_util import xor_binario
from codigos_corretores.bch import *

def reconciliar_chaves(palavra_codigo_1, palavra_codigo_2, tabela_codigos):
    """Função para reconciliar chaves entre Alice e Bob"""

    c = random.choice(tabela_codigos)
    s = xor_binario(palavra_codigo_1, c)
    c_b = xor_binario(palavra_codigo_2, s)
    chave = xor_binario(s, encontrar_codigo_mais_proximo(c_b, tabela_codigos))

    return chave