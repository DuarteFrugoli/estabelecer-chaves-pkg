import hashlib

def amplificacao_privacidade(chave_bits):

    # Converte lista de bits para string binária
    chave_bin_str = ''.join(str(bit) for bit in chave_bits)

    # Converte string binária para bytes
    chave_bytes = int(chave_bin_str, 2).to_bytes((len(chave_bin_str) + 7) // 8, byteorder='big')

    # Aplica SHA-256
    hash_digest = hashlib.sha256(chave_bytes).digest()

    # Converte bytes do hash para lista de bits
    chave_final_bits = []
    for byte in hash_digest:
        bits = bin(byte)[2:].zfill(8)
        chave_final_bits.extend(int(b) for b in bits)

    return chave_final_bits