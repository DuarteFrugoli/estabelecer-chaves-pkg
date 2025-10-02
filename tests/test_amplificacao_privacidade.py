"""
Testes unitários para amplificação de privacidade
"""
import pytest
import sys
import os
import hashlib

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pilares.amplificacao_privacidade import amplificacao_privacidade, amplificacao_privacidade_personalizada


class TestAmplificacaoPrivacidade:
    """Testes para função de amplificação de privacidade"""
    
    def test_amplificacao_basic(self):
        """Testa amplificação básica"""
        chave_bits = [1, 0, 1, 1, 0, 0, 1, 0]
        resultado = amplificacao_privacidade(chave_bits)
        
        # Sempre deve retornar 256 bits
        assert len(resultado) == 256
        
        # Todos os elementos devem ser 0 ou 1
        assert all(bit in {0, 1} for bit in resultado)
    
    def test_amplificacao_deterministic(self):
        """Testa se a amplificação é determinística"""
        chave_bits = [1, 0, 1, 0, 1, 0, 1, 0]
        
        resultado1 = amplificacao_privacidade(chave_bits)
        resultado2 = amplificacao_privacidade(chave_bits)
        
        # Mesma entrada deve gerar mesma saída
        assert resultado1 == resultado2
    
    def test_amplificacao_avalanche_effect(self):
        """Testa efeito avalanche (pequena mudança → grande diferença)"""
        chave1 = [1, 0, 0, 0, 0, 0, 0, 0]
        chave2 = [0, 0, 0, 0, 0, 0, 0, 0]  # Apenas 1 bit diferente
        
        resultado1 = amplificacao_privacidade(chave1)
        resultado2 = amplificacao_privacidade(chave2)
        
        # Deve ser muito diferente (pelo menos 50% dos bits diferentes)
        diferencas = sum(a != b for a, b in zip(resultado1, resultado2))
        assert diferencas > 100  # Pelo menos 100 bits diferentes de 256
    
    def test_amplificacao_empty_input(self):
        """Testa erro com entrada vazia"""
        with pytest.raises(ValueError, match="chave_bits não pode estar vazia"):
            amplificacao_privacidade([])
    
    def test_amplificacao_invalid_type(self):
        """Testa erro com tipo inválido"""
        with pytest.raises(TypeError, match="chave_bits deve ser uma lista"):
            amplificacao_privacidade("not a list")
    
    def test_amplificacao_invalid_bits(self):
        """Testa erro com bits inválidos"""
        with pytest.raises(ValueError, match="Todos os elementos devem ser inteiros 0 ou 1"):
            amplificacao_privacidade([0, 1, 2, 0])  # 2 não é bit válido
        
        with pytest.raises(ValueError, match="Todos os elementos devem ser inteiros 0 ou 1"):
            amplificacao_privacidade([0, 1, "1", 0])  # String não é válida
    
    def test_amplificacao_single_bit(self):
        """Testa com um único bit"""
        resultado_0 = amplificacao_privacidade([0])
        resultado_1 = amplificacao_privacidade([1])
        
        assert len(resultado_0) == 256
        assert len(resultado_1) == 256
        assert resultado_0 != resultado_1
    
    def test_amplificacao_long_input(self):
        """Testa com entrada longa"""
        chave_longa = [i % 2 for i in range(1000)]  # 1000 bits
        resultado = amplificacao_privacidade(chave_longa)
        
        assert len(resultado) == 256
        assert all(bit in {0, 1} for bit in resultado)
    
    def test_amplificacao_all_zeros(self):
        """Testa com todos zeros"""
        chave_zeros = [0] * 32
        resultado = amplificacao_privacidade(chave_zeros)
        
        assert len(resultado) == 256
        # Não deve ser todos zeros (SHA-256 de zero não é zero)
        assert any(bit == 1 for bit in resultado)
    
    def test_amplificacao_all_ones(self):
        """Testa com todos uns"""
        chave_ones = [1] * 32
        resultado = amplificacao_privacidade(chave_ones)
        
        assert len(resultado) == 256
        # Deve ser diferente de todos zeros e todos uns
        assert any(bit == 0 for bit in resultado)
        assert any(bit == 1 for bit in resultado)
    
    def test_amplificacao_known_vector(self):
        """Testa com vetor conhecido para verificar consistência"""
        # Entrada simples: 8 bits = 1 byte = 0xAA = 170
        chave_bits = [1, 0, 1, 0, 1, 0, 1, 0]  # 0xAA
        resultado = amplificacao_privacidade(chave_bits)
        
        # Verifica que o hash SHA-256 de 0xAA é calculado corretamente
        expected_hash = hashlib.sha256(bytes([0xAA])).digest()
        expected_bits = []
        for byte in expected_hash:
            bits = bin(byte)[2:].zfill(8)
            expected_bits.extend(int(b) for b in bits)
        
        assert resultado == expected_bits


class TestAmplificacaoPrivacidadePersonalizada:
    """Testes para função personalizada de amplificação"""
    
    def test_amplificacao_personalizada_default(self):
        """Testa comportamento padrão da versão personalizada"""
        chave_bits = [1, 0, 1, 0, 1, 0, 1, 0]
        
        resultado_basico = amplificacao_privacidade(chave_bits)
        resultado_personalizado = amplificacao_privacidade_personalizada(chave_bits)
        
        # Comportamento padrão deve ser igual ao básico
        assert resultado_basico == resultado_personalizado
    
    def test_amplificacao_personalizada_truncate(self):
        """Testa truncamento para tamanho menor"""
        chave_bits = [1, 0, 1, 0, 1, 0, 1, 0]
        resultado = amplificacao_privacidade_personalizada(chave_bits, tamanho_saida=128)
        
        assert len(resultado) == 128
        assert all(bit in {0, 1} for bit in resultado)
    
    def test_amplificacao_personalizada_extend(self):
        """Testa extensão para tamanho maior"""
        chave_bits = [1, 0, 1, 0, 1, 0, 1, 0]
        resultado = amplificacao_privacidade_personalizada(chave_bits, tamanho_saida=512)
        
        assert len(resultado) == 512
        assert all(bit in {0, 1} for bit in resultado)
    
    def test_amplificacao_personalizada_invalid_size(self):
        """Testa erro com tamanho inválido"""
        chave_bits = [1, 0, 1, 0]
        
        with pytest.raises(ValueError, match="tamanho_saida deve ser positivo e múltiplo de 8"):
            amplificacao_privacidade_personalizada(chave_bits, tamanho_saida=0)
        
        with pytest.raises(ValueError, match="tamanho_saida deve ser positivo e múltiplo de 8"):
            amplificacao_privacidade_personalizada(chave_bits, tamanho_saida=9)  # Não múltiplo de 8
    
    def test_amplificacao_personalizada_algorithms(self):
        """Testa diferentes algoritmos"""
        chave_bits = [1, 0, 1, 0, 1, 0, 1, 0]
        
        # Testa SHA-256
        resultado_sha256 = amplificacao_privacidade_personalizada(chave_bits, algoritmo='sha256')
        assert len(resultado_sha256) == 256
        
        # Testa SHA-512 (deve ser truncado para 256)
        resultado_sha512 = amplificacao_privacidade_personalizada(chave_bits, algoritmo='sha512')
        assert len(resultado_sha512) == 256
        
        # Verifica que ambos os algoritmos funcionam (podem ter resultado igual por acaso)
        assert all(bit in {0, 1} for bit in resultado_sha256)
        assert all(bit in {0, 1} for bit in resultado_sha512)
    
    def test_amplificacao_personalizada_invalid_algorithm(self):
        """Testa erro com algoritmo inválido"""
        chave_bits = [1, 0, 1, 0]
        
        with pytest.raises(ValueError, match="Algoritmo não suportado"):
            amplificacao_privacidade_personalizada(chave_bits, algoritmo='md5')


class TestAmplificacaoIntegration:
    """Testes de integração e casos reais"""
    
    def test_consistency_with_reconciliation(self):
        """Testa consistência quando usada após reconciliação"""
        # Simula saída típica de reconciliação BCH
        chave_reconciliada = [1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1]
        
        resultado = amplificacao_privacidade(chave_reconciliada)
        
        assert len(resultado) == 256
        assert all(bit in {0, 1} for bit in resultado)
    
    def test_statistical_properties(self):
        """Testa propriedades estatísticas básicas"""
        chave_bits = [1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1]
        resultado = amplificacao_privacidade(chave_bits)
        
        # Conta 0s e 1s
        zeros = resultado.count(0)
        ones = resultado.count(1)
        
        # Deve ter distribuição razoavelmente equilibrada
        # (não muito desequilibrada, mas SHA-256 pode ter variação)
        assert zeros > 50  # Pelo menos 50 zeros de 256
        assert ones > 50   # Pelo menos 50 uns de 256
        assert zeros + ones == 256
    
    def test_multiple_rounds_independence(self):
        """Testa independência entre múltiplas aplicações"""
        chave_base = [1, 0, 1, 0, 1, 0, 1, 0]
        
        # Aplica amplificação múltiplas vezes com entradas similares
        resultados = []
        for i in range(5):
            chave_variada = chave_base + [i % 2]
            resultado = amplificacao_privacidade(chave_variada)
            resultados.append(resultado)
        
        # Verifica independência estatística (deve haver diferenças na maioria dos casos)
        diferencas = 0
        total_comparacoes = 0
        for i in range(len(resultados)):
            for j in range(i+1, len(resultados)):
                total_comparacoes += 1
                if resultados[i] != resultados[j]:
                    diferencas += 1
        
        # Pelo menos 50% devem ser diferentes (tolerância realista para hash)
        assert diferencas >= 0.5 * total_comparacoes


class TestAmplificacaoSecurity:
    """Testes focados em propriedades de segurança"""
    
    def test_preimage_resistance_simulation(self):
        """Simula teste de resistência à pré-imagem"""
        # Gera um resultado alvo
        chave_alvo = [1, 1, 0, 0, 1, 1, 0, 0]
        resultado_alvo = amplificacao_privacidade(chave_alvo)
        
        # Tenta encontrar outra entrada que gere o mesmo resultado
        # (isso deveria ser computacionalmente inviável, mas testamos algumas tentativas)
        encontrou_colisao = False
        for i in range(100):  # Testa apenas algumas tentativas
            chave_teste = [(i >> j) & 1 for j in range(8)]
            if chave_teste != chave_alvo:
                resultado_teste = amplificacao_privacidade(chave_teste)
                if resultado_teste == resultado_alvo:
                    encontrou_colisao = True
                    break
        
        # Não deveria encontrar colisão facilmente
        assert not encontrou_colisao
    
    def test_bit_independence(self):
        """Testa independência entre bits de saída"""
        chave_base = [1, 0, 1, 0, 1, 0, 1, 0]
        resultado_base = amplificacao_privacidade(chave_base)
        
        # Muda apenas um bit da entrada
        chave_modificada = chave_base.copy()
        chave_modificada[0] = 1 - chave_modificada[0]
        resultado_modificado = amplificacao_privacidade(chave_modificada)
        
        # Calcula diferenças por posição
        diferencas = [a != b for a, b in zip(resultado_base, resultado_modificado)]
        num_diferencas = sum(diferencas)
        
        # Deve ter muitas diferenças distribuídas
        assert num_diferencas > 50  # Efeito avalanche significativo
        
        # As diferenças devem estar distribuídas, não concentradas
        primeira_metade = sum(diferencas[:128])
        segunda_metade = sum(diferencas[128:])
        
        # Ambas as metades devem ter algumas diferenças
        assert primeira_metade > 10
        assert segunda_metade > 10


if __name__ == "__main__":
    pytest.main([__file__])