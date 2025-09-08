import random
from util.binario_util import xor_binario
from codigos_corretores.bch import *

def reconciliar_chaves(palavra_codigo_1, palavra_codigo_2, tabela_codigos):
    """
    Função para reconciliar chaves entre Alice e Bob usando code-offset (secure sketch).
    
    Algoritmo:
    1. Alice escolhe um código aleatório C da tabela
    2. Alice calcula S = Ka ⊕ C (syndrome)
    3. Alice envia S para Bob (informação de reconciliação)
    4. Bob calcula Cb = S ⊕ Kb = C ⊕ e (onde e = Ka ⊕ Kb é o vetor de erro)
    5. Bob decodifica Cb para encontrar Ĉ (palavra-código mais próxima)
    6. Bob calcula a chave reconciliada: K̂ = S ⊕ Ĉ
    
    Se peso(e) ≤ t (capacidade de correção do BCH), então Ĉ = C e Ka = K̂.
    """
    # 1. Alice escolhe um código aleatório C
    c = random.choice(tabela_codigos)
    
    # 2. Alice calcula o syndrome S = Ka ⊕ C
    s = xor_binario(palavra_codigo_1, c)
    
    # 3. Bob calcula Cb = S ⊕ Kb = C ⊕ (Ka ⊕ Kb) = C ⊕ e
    c_b = xor_binario(palavra_codigo_2, s)
    
    # 4. Bob decodifica Cb para encontrar a palavra-código mais próxima Ĉ
    codigo_decodificado = encontrar_codigo_mais_proximo(c_b, tabela_codigos)
    
    # 5. Bob calcula a chave reconciliada K̂ = S ⊕ Ĉ
    chave = xor_binario(s, codigo_decodificado)

    return chave