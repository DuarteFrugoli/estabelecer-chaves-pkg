"""
Testes unitários para funções de utilidades binárias
"""
import pytest
import sys
import os

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from util.binario_util import calcular_distancia_hamming, contar_erros_bits, xor_binario


class TestBinarioUtil:
    """Testes para funções de operações binárias"""
    
    def test_calcular_distancia_hamming_identical(self):
        """Testa distância de Hamming entre sequências idênticas"""
        seq1 = [0, 1, 0, 1, 1, 0]
        seq2 = [0, 1, 0, 1, 1, 0]
        assert calcular_distancia_hamming(seq1, seq2) == 0
    
    def test_calcular_distancia_hamming_different(self):
        """Testa distância de Hamming entre sequências diferentes"""
        seq1 = [0, 1, 0, 1, 1, 0]
        seq2 = [1, 1, 1, 1, 0, 0]
        # Diferenças: posições 0, 2, 4 = 3 diferenças
        assert calcular_distancia_hamming(seq1, seq2) == 3
    
    def test_calcular_distancia_hamming_empty(self):
        """Testa distância de Hamming entre sequências vazias"""
        assert calcular_distancia_hamming([], []) == 0
    
    def test_calcular_distancia_hamming_different_lengths(self):
        """Testa erro quando sequências têm tamanhos diferentes"""
        seq1 = [0, 1, 0]
        seq2 = [1, 1]
        with pytest.raises(AssertionError):
            calcular_distancia_hamming(seq1, seq2)
    
    def test_contar_erros_bits_consistency(self):
        """Testa se contar_erros_bits produz mesmo resultado que calcular_distancia_hamming"""
        seq1 = [1, 0, 1, 1, 0, 1, 0]
        seq2 = [0, 0, 1, 0, 1, 1, 1]
        
        hamming = calcular_distancia_hamming(seq1, seq2)
        erros = contar_erros_bits(seq1, seq2)
        
        assert hamming == erros
    
    def test_xor_binario_basic(self):
        """Testa operação XOR básica"""
        seq1 = [0, 1, 0, 1]
        seq2 = [1, 1, 0, 0]
        expected = [1, 0, 0, 1]  # 0⊕1=1, 1⊕1=0, 0⊕0=0, 1⊕0=1
        
        assert xor_binario(seq1, seq2) == expected
    
    def test_xor_binario_identity(self):
        """Testa propriedade de identidade do XOR (A ⊕ A = 0)"""
        seq = [1, 0, 1, 1, 0, 1]
        expected = [0, 0, 0, 0, 0, 0]
        
        assert xor_binario(seq, seq) == expected
    
    def test_xor_binario_zero_element(self):
        """Testa propriedade do elemento neutro (A ⊕ 0 = A)"""
        seq = [1, 0, 1, 1, 0]
        zeros = [0, 0, 0, 0, 0]
        
        assert xor_binario(seq, zeros) == seq
    
    def test_xor_binario_commutative(self):
        """Testa propriedade comutativa do XOR (A ⊕ B = B ⊕ A)"""
        seq1 = [1, 0, 1, 0, 1]
        seq2 = [0, 1, 1, 1, 0]
        
        assert xor_binario(seq1, seq2) == xor_binario(seq2, seq1)
    
    def test_xor_binario_different_lengths(self):
        """Testa erro quando sequências têm tamanhos diferentes"""
        seq1 = [0, 1, 0]
        seq2 = [1, 1, 0, 1]
        
        with pytest.raises(AssertionError):
            xor_binario(seq1, seq2)
    
    def test_xor_binario_empty(self):
        """Testa XOR de sequências vazias"""
        assert xor_binario([], []) == []


class TestBinarioUtilEdgeCases:
    """Testes de casos extremos para operações binárias"""
    
    def test_large_sequences(self):
        """Testa operações com sequências grandes"""
        size = 1000
        seq1 = [i % 2 for i in range(size)]  # [0, 1, 0, 1, ...]
        seq2 = [(i + 1) % 2 for i in range(size)]  # [1, 0, 1, 0, ...]
        
        # Todas as posições são diferentes
        assert calcular_distancia_hamming(seq1, seq2) == size
        
        # XOR deve resultar em todos 1s
        xor_result = xor_binario(seq1, seq2)
        assert all(bit == 1 for bit in xor_result)
        assert len(xor_result) == size
    
    def test_single_bit(self):
        """Testa operações com um único bit"""
        assert calcular_distancia_hamming([0], [1]) == 1
        assert calcular_distancia_hamming([0], [0]) == 0
        assert xor_binario([0], [1]) == [1]
        assert xor_binario([1], [1]) == [0]
    
    def test_alternating_pattern(self):
        """Testa com padrões alternados"""
        pattern1 = [0, 1] * 50  # 100 bits alternados
        pattern2 = [1, 0] * 50  # 100 bits alternados invertidos
        
        # Todas as posições são diferentes
        assert calcular_distancia_hamming(pattern1, pattern2) == 100
        
        # XOR deve ser todos 1s
        xor_result = xor_binario(pattern1, pattern2)
        assert all(bit == 1 for bit in xor_result)


if __name__ == "__main__":
    pytest.main([__file__])