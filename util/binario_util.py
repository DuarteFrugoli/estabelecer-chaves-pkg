def calcular_distancia_hamming(seq1, seq2):
    """Calcula a distância de Hamming entre duas listas de bits. Gera erro se os tamanhos forem diferentes."""
    assert len(seq1) == len(seq2), f"Listas devem ter o mesmo comprimento: {len(seq1)} vs {len(seq2)}"
    return sum(a != b for a, b in zip(seq1, seq2))

def contar_erros_bits(seq1, seq2):
    """Conta o número de bits diferentes entre duas listas de bits. Gera erro se os tamanhos forem diferentes."""
    # Tem a mesma funcionalidade que calcular_distancia_hamming, mas é mais explícita
    return calcular_distancia_hamming(seq1, seq2)

def xor_binario(seq1, seq2):
    """Realiza operação XOR entre duas listas de bits"""
    assert len(seq1) == len(seq2), f"Listas devem ter o mesmo comprimento: {len(seq1)} vs {len(seq2)}"
    return [0 if a == b else 1 for a, b in zip(seq1, seq2)]