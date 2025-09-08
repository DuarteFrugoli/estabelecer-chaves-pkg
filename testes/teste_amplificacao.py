"""
Teste da função de amplificação de privacidade
"""
import sys
import os

# Adiciona o diretório raiz ao path para importar os módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pilares.amplificacao_privacidade import amplificacao_privacidade

def teste_amplificacao_privacidade():
    """Testa a função de amplificação de privacidade"""
    
    print("=== TESTE DA AMPLIFICAÇÃO DE PRIVACIDADE ===")
    
    # Teste 1: Chave pequena (15 bits)
    chave_15_bits = [1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1]
    print(f"Chave original (15 bits): {chave_15_bits}")
    print(f"Tamanho original: {len(chave_15_bits)} bits")
    
    chave_final = amplificacao_privacidade(chave_15_bits)
    print(f"Chave após SHA-256: {chave_final[:16]}...{chave_final[-16:]}")
    print(f"Tamanho final: {len(chave_final)} bits")
    print()
    
    # Teste 2: Chave média (127 bits)
    chave_127_bits = [1, 0] * 63 + [1]  # 127 bits alternados terminando em 1
    print(f"Chave original (127 bits): {chave_127_bits[:8]}...{chave_127_bits[-8:]}")
    print(f"Tamanho original: {len(chave_127_bits)} bits")
    
    chave_final_127 = amplificacao_privacidade(chave_127_bits)
    print(f"Chave após SHA-256: {chave_final_127[:16]}...{chave_final_127[-16:]}")
    print(f"Tamanho final: {len(chave_final_127)} bits")
    print()
    
    # Teste 3: Propriedade determinística
    chave_teste = [1, 1, 0, 1, 0, 1, 1, 0]
    resultado1 = amplificacao_privacidade(chave_teste)
    resultado2 = amplificacao_privacidade(chave_teste)
    print(f"Teste determinístico:")
    print(f"Resultado 1 == Resultado 2: {resultado1 == resultado2}")
    print()
    
    # Teste 4: Propriedade de avalanche (pequena mudança -> grande diferença)
    chave_a = [1, 0, 1, 0, 1, 0, 1, 0]
    chave_b = [1, 0, 1, 0, 1, 0, 1, 1]  # Apenas o último bit diferente
    
    resultado_a = amplificacao_privacidade(chave_a)
    resultado_b = amplificacao_privacidade(chave_b)
    
    diferencias = sum(1 for a, b in zip(resultado_a, resultado_b) if a != b)
    porcentagem_diferenca = (diferencias / len(resultado_a)) * 100
    
    print(f"Teste de avalanche:")
    print(f"Chave A: {chave_a}")
    print(f"Chave B: {chave_b}")
    print(f"Bits diferentes no resultado: {diferencias}/{len(resultado_a)}")
    print(f"Porcentagem de diferença: {porcentagem_diferenca:.1f}%")
    print(f"Avalanche adequado (>40%): {'✅' if porcentagem_diferenca > 40 else '❌'}")
    
    return True

if __name__ == "__main__":
    teste_amplificacao_privacidade()
