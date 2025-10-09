import galois
import random

from ..util.binario_util import calcular_distancia_hamming

# Retorna o valor de k (número de bits de informação) para o código especificado
def get_tamanho_bits_informacao(tamanho_cadeia_bits):
    """Retorna o valor de k (número de bits de informação) para o código especificado."""
    # Dicionário com valores de k para diferentes tamanhos de código BCH
    tamanho_bits_informacao = {
        7: 4,
        15: 7,
        127: 64,
        255: 139
    }
    return tamanho_bits_informacao.get(tamanho_cadeia_bits, None) # Retorna None se o valor de tamanho_cadeia_bits não for encontrado

def instanciar_codigo_bch(tamanho_cadeia_bits, tamanho_bits_informacao):
    """Instancia um objeto BCH com os parâmetros especificados."""
    t = {7: 1, 15: 2, 127: 10, 255: 15} # Número de erros que o código pode corrigir
    d = 2 * t.get(tamanho_cadeia_bits, 0) + 1 # Distância mínima do código
    return galois.BCH(tamanho_cadeia_bits, tamanho_bits_informacao, d)

def codificar_bch(bch, bits_informacao):
    """Codifica uma palavra de informação usando o código BCH."""
    return bch.encode(bits_informacao).tolist()

def decodificar_bch(bch, bits_codificados):
    """Decodifica uma palavra codificada usando o código BCH."""
    return bch.decode(bits_codificados).tolist()

def gerar_tabela_codigos_bch(tamanho_cadeia_bits, tamanho_bits_informacao, tamanho_espaco_amostral=None):
    """Gera uma tabela de códigos para todas as palavras de informação possíveis (sem repetições)."""
    # Instancia o código BCH
    bch = instanciar_codigo_bch(tamanho_cadeia_bits, tamanho_bits_informacao)

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
    tabela_codigos = [codificar_bch(bch, bits_informacao) for bits_informacao in palavras_informacao]

    return tabela_codigos

def encontrar_codigo_mais_proximo(sinal_recebido, bch_codigo):
    """
    Encontra o código mais próximo usando decodificação BCH.
    """
    try:
        import numpy as np
        if isinstance(sinal_recebido, list):
            sinal_recebido = np.array(sinal_recebido, dtype=np.uint8)
        
        # Decodifica e obtém a mensagem de informação
        mensagem_decodificada = bch_codigo.decode(sinal_recebido)
        
        # Re-codifica para obter a palavra-código completa
        codigo_mais_proximo = bch_codigo.encode(mensagem_decodificada)
        
        return codigo_mais_proximo.tolist()
        
    except Exception:
        # Se a decodificação falhar, retorna o sinal original
        return sinal_recebido.tolist() if hasattr(sinal_recebido, 'tolist') else sinal_recebido

def gerar_tabela_codigos_bch(tamanho_cadeia_bits, tamanho_bits_informacao, tamanho_espaco_amostral=None):
    """
    Retorna o objeto BCH instanciado.
    Mantém compatibilidade com o código existente.
    """
    return instanciar_codigo_bch(tamanho_cadeia_bits, tamanho_bits_informacao)