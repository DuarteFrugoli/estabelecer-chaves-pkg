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