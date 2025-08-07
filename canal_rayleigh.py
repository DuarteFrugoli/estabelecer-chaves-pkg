import random
import numpy as np

# TODO: organizar funções em diferentes arquivos

def encontraErros(palavra_informacao, y):
    # Conta o número de erros entre duas listas de bits palavra_informacao e y
    return sum(1 for i in range(len(palavra_informacao)) if y[i] != palavra_informacao[i])

def hamming_distance(s1, s2):
    # Calcula a distância de Hamming entre duas strings binárias
    length = min(len(s1), len(s2))
    return sum(ch1 != ch2 for ch1, ch2 in zip(s1[:length], s2[:length]))

def comparacao_mais_proxima(y, tabela):
    # Compara y com todos os códigos na tabela e retorna o mais próximo (menor distância de Hamming)
    min_dist = float('inf')
    pos = -1

    for i, code in enumerate(tabela):
        aux = hamming_distance(y, code)
        if aux < min_dist:
            pos = i
            min_dist = aux

    return tabela[pos]

def encontraParidade(y, tabela):
    # Encontra a paridade entre y e o código mais próximo na tabela
    fc = comparacao_mais_proxima(y, tabela)
    P = subtract_binary(fc, y)
    return P

def comparaSinais(y, P, tabela):
    # Compara sinais para gerar a chave final
    fc = comparacao_mais_proxima(subtract_binary(y, P), tabela)
    min_len = min(len(fc), len(P))
    fc_padded = fc[:min_len]
    P_padded = P[:min_len]
    return xor_binary(fc_padded, P_padded)

def subtract_binary(fc, y):
    # Subtrai dois valores binários (bit a bit, XOR)
    assert len(fc) == len(y), "Os valores devem ter o mesmo número de dígitos binários."
    min_len = min(len(fc), len(y))
    return ''.join('0' if a == b else '1' for a, b in zip(fc[:min_len], y[:min_len]))

def xor_binary(fc, P):
    # Realiza operação XOR entre duas strings binárias
    assert len(fc) == len(P), "Os valores devem ter o mesmo número de dígitos binários."
    return ''.join('0' if a == b else '1' for a, b in zip(fc, P))

# FIXME: antiga classe AltoRuidoCanalRayleigh

# Função para calcular y considerando o efeito Rayleigh (h) e ruído alto
def calculaY(h, palavra_informacao, variancia, media, ntestes):
    # Gera ruído gaussiano
    # TODO: colocar a função em um lugar melhor e consertar os nomes
    # TODO: adicionar utilidade para o sigma e entender como ele se relaciona com as variâncias
    # TODO: melhor usar np.random.normal ao invés de random.gauss
    def gerar_ruido_gaussiano(variancia, media):
        sigma = np.sqrt(variancia)
        return [random.gauss(media, variancia) for _ in range(len(palavra_informacao))]

    n = gerar_ruido_gaussiano(variancia, media)
    # Calcula y aplicando o efeito Rayleigh e limiarização
    y = [1 if h[i] * palavra_informacao[i] + n[i] > 0.5 else 0 for i in range(len(palavra_informacao))]
    return y

# Função principal do cenário
def cenario(palavra_informacao, canal_rayleigh_1, canal_rayleigh_2, tamanho_espaco_amostral, tabela, tamanho_cadeia_bits, ntestes, variancia, media):

    print("Cenário 5: Alto Ruido Canal Rayleigh\n")

    contagem_de_acertos = 0  # Contador de acertos

    for i in range(ntestes):
        print(f'Teste {i+1}/{ntestes}')
        print('palavra_informacao =', palavra_informacao)

        # Gera y1 com canal_rayleigh_1 e ruído alto
        y1 = calculaY(palavra_informacao, canal_rayleigh_1, variancia, media, tamanho_cadeia_bits)
        print('y1 =', y1)
        erros_y1 = encontraErros(palavra_informacao, y1)
        print('Erros do y1 =', erros_y1)

        # Gera y2 com canal_rayleigh_2 e ruído alto
        y2 = calculaY(palavra_informacao, canal_rayleigh_2, variancia, media, tamanho_cadeia_bits)
        print('y2 =', y2)
        erros_y2 = encontraErros(palavra_informacao, y2)
        print('Erros do y2 =', erros_y2)

        # Converte listas para strings binárias
        toStringY1 = ''.join(map(str, y1))
        toStringY2 = ''.join(map(str, y2))

        c = random.choice(tabela)
        s = xor_binary(toStringY1, c)
        c_B = xor_binary(toStringY2 , s)
        chave = xor_binary(s, comparacao_mais_proxima(c_B, tabela))
        print(f"Chave gerada por código de BCH:", chave)

        # Verifica se a chave gerada é igual ao y1
        if toStringY1 == chave:
            contagem_de_acertos += 1
        else:
            print(f"Não são iguais por BCH")


        print("\n--------------------------------------------------------")


    # Calcula a porcentagem de acertos
    porcentagem_de_acertos = contagem_de_acertos * 100.00 / ntestes
    print(f"Porcentagem de vezes que a chave gerada foi encontrada na tabela BCH: {porcentagem_de_acertos:.2f}%")

    return porcentagem_de_acertos