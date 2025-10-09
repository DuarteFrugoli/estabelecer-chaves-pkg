import hashlib

def amplificacao_privacidade(chave_bits):
    """
    Aplica amplificação de privacidade usando SHA-256.
    
    A amplificação de privacidade é o terceiro pilar do PKG (Physical Key Generation)
    e tem como objetivo reduzir a informação que um adversário (Eva) pode ter
    sobre a chave final, mesmo que tenha obtido informação parcial durante
    a transmissão pelo canal.
    
    Processo:
    1. Recebe chave pós-reconciliação (com possível vazamento de informação)
    2. Aplica função hash criptográfica (SHA-256)
    3. Gera chave final de 256 bits com alta entropia
    
    Propriedades do SHA-256 que garantem segurança:
    - Determinístico: mesma entrada gera mesma saída
    - Efeito avalanche: pequena mudança gera saída completamente diferente
    - Pré-imagem resistente: difícil encontrar entrada que gere saída específica
    - Distribuição uniforme: bits de saída estatisticamente independentes
    
    Args:
        chave_bits (list): Lista de bits inteiros (0 ou 1) da chave pós-reconciliação
        
    Returns:
        list: Lista de 256 bits representando a chave final amplificada
        
    Raises:
        ValueError: Se a entrada não for uma lista válida de bits
        TypeError: Se os elementos da lista não forem inteiros 0 ou 1
    """
    
    # Validação de entrada
    if not isinstance(chave_bits, list):
        raise TypeError("chave_bits deve ser uma lista")
    
    if len(chave_bits) == 0:
        raise ValueError("chave_bits não pode estar vazia")
    
    if not all(isinstance(bit, int) and bit in {0, 1} for bit in chave_bits):
        raise ValueError("Todos os elementos devem ser inteiros 0 ou 1")

    # Converte lista de bits para string binária
    chave_bin_str = ''.join(str(bit) for bit in chave_bits)

    # Converte string binária para bytes
    # Calcula o número de bytes necessários (arredonda para cima)
    num_bytes = (len(chave_bin_str) + 7) // 8
    chave_bytes = int(chave_bin_str, 2).to_bytes(num_bytes, byteorder='big')

    # Aplica SHA-256 para amplificação de privacidade
    hash_digest = hashlib.sha256(chave_bytes).digest()

    # Converte bytes do hash para lista de bits (sempre 256 bits para SHA-256)
    chave_final_bits = []
    for byte in hash_digest:
        # Converte cada byte para 8 bits, preenchendo com zeros à esquerda
        bits = bin(byte)[2:].zfill(8)
        chave_final_bits.extend(int(b) for b in bits)

    return chave_final_bits

def amplificacao_privacidade_personalizada(chave_bits, tamanho_saida=256, algoritmo='sha256'):
    """
    Versão estendida da amplificação de privacidade com parâmetros configuráveis.
    
    Args:
        chave_bits (list): Lista de bits da chave de entrada
        tamanho_saida (int): Número de bits desejados na saída (padrão: 256)
        algoritmo (str): Algoritmo hash a usar ('sha256', 'sha512', 'sha3_256')
        
    Returns:
        list: Lista de bits da chave amplificada
    """
    
    # Validações
    if tamanho_saida <= 0 or tamanho_saida % 8 != 0:
        raise ValueError("tamanho_saida deve ser positivo e múltiplo de 8")
    
    algoritmos_suportados = {
        'sha256': hashlib.sha256,
        'sha512': hashlib.sha512,
        'sha3_256': hashlib.sha3_256,
        'sha3_512': hashlib.sha3_512
    }
    
    if algoritmo not in algoritmos_suportados:
        raise ValueError(f"Algoritmo não suportado. Use: {list(algoritmos_suportados.keys())}")
    
    # Aplica amplificação básica
    chave_base = amplificacao_privacidade(chave_bits)
    
    # Se o tamanho desejado for diferente de 256, aplica extensão ou truncamento
    if tamanho_saida == 256:
        return chave_base
    elif tamanho_saida < 256:
        # Trunca para o tamanho desejado
        return chave_base[:tamanho_saida]
    else:
        # Estende usando múltiplas aplicações do hash
        chave_estendida = chave_base[:]
        contador = 1
        
        while len(chave_estendida) < tamanho_saida:
            # Aplica hash com contador para gerar mais bits
            entrada_estendida = chave_bits + [contador % 2]
            hash_adicional = amplificacao_privacidade(entrada_estendida)
            chave_estendida.extend(hash_adicional)
            contador += 1
        
        return chave_estendida[:tamanho_saida]