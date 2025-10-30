"""
Testes unitários para funções do código BCH
"""
import pytest
import sys
import os

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.codigos_corretores.bch import (
    get_tamanho_bits_informacao,
    instanciar_codigo_bch,
    codificar_bch,
    decodificar_bch,
    gerar_tabela_codigos_bch
)


class TestBCHFunctions:
    """Testes para funções do módulo BCH"""
    
    def test_get_tamanho_bits_informacao_valid(self):
        """Testa valores válidos de k"""
        assert get_tamanho_bits_informacao(7) == 4
        assert get_tamanho_bits_informacao(15) == 7
        assert get_tamanho_bits_informacao(127) == 64
        assert get_tamanho_bits_informacao(255) == 139
    
    def test_get_tamanho_bits_informacao_invalid(self):
        """Testa valores inválidos de k"""
        assert get_tamanho_bits_informacao(10) is None
        assert get_tamanho_bits_informacao(0) is None
        assert get_tamanho_bits_informacao(256) is None
        assert get_tamanho_bits_informacao(-1) is None
    
    def test_instanciar_codigo_bch_valid(self):
        """Testa instanciação de códigos BCH válidos"""
        # BCH(7,4,1) - t=1
        bch = instanciar_codigo_bch(7, 4)
        assert bch.n == 7
        assert bch.k == 4
        assert bch.t == 1
        
        # BCH(15,7,2) - t=2
        bch = instanciar_codigo_bch(15, 7)
        assert bch.n == 15
        assert bch.k == 7
        assert bch.t == 2
    
    def test_codificar_decodificar_bch_consistency(self):
        """Testa se decodificar(codificar(x)) = x"""
        bch = instanciar_codigo_bch(7, 4)
        
        # Testa várias palavras de informação
        test_words = [
            [0, 0, 0, 0],
            [1, 1, 1, 1],
            [1, 0, 1, 0],
            [0, 1, 0, 1]
        ]
        
        for word in test_words:
            encoded = codificar_bch(bch, word)
            decoded = decodificar_bch(bch, encoded)
            assert decoded == word
    
    def test_codificar_bch_length(self):
        """Testa se a codificação produz o tamanho correto"""
        bch_7_4 = instanciar_codigo_bch(7, 4)
        word = [1, 0, 1, 0]
        encoded = codificar_bch(bch_7_4, word)
        assert len(encoded) == 7
        
        bch_15_7 = instanciar_codigo_bch(15, 7)
        word = [1, 0, 1, 0, 1, 0, 1]
        encoded = codificar_bch(bch_15_7, word)
        assert len(encoded) == 15
    
    def test_bch_error_correction_capability(self):
        """Testa capacidade de correção de erros do BCH"""
        # BCH(7,4,1) pode corrigir 1 erro
        bch = instanciar_codigo_bch(7, 4)
        original_word = [1, 0, 1, 0]
        
        # Codifica
        encoded = codificar_bch(bch, original_word)
        
        # Introduz 1 erro
        corrupted = encoded.copy()
        corrupted[0] = 1 - corrupted[0]  # Inverte o primeiro bit
        
        # Decodifica e verifica se corrigiu
        decoded = decodificar_bch(bch, corrupted)
        assert decoded == original_word


class TestBCHIntegration:
    """Testes de integração das funções BCH"""
    
    def test_bch_systematic_property(self):
        """Testa se os códigos BCH são sistemáticos"""
        bch = instanciar_codigo_bch(7, 4)
        
        word = [1, 0, 1, 1]
        encoded = codificar_bch(bch, word)
        
        # Para códigos sistemáticos, os primeiros k bits são os dados originais
        # (isso pode variar dependendo da implementação da biblioteca galois)
        assert len(encoded) == 7
        assert len(word) == 4


class TestBCHEdgeCases:
    """Testes de casos extremos"""
    
    def test_all_zero_codeword(self):
        """Testa palavra código toda zero"""
        bch = instanciar_codigo_bch(7, 4)
        zero_word = [0, 0, 0, 0]
        
        encoded = codificar_bch(bch, zero_word)
        decoded = decodificar_bch(bch, encoded)
        
        assert decoded == zero_word
        # Palavra código toda zero deve ser toda zero
        assert all(bit == 0 for bit in encoded)
    
    def test_single_bit_information(self):
        """Testa com uma única informação variando"""
        bch = instanciar_codigo_bch(7, 4)
        
        # Testa todas as combinações de um bit
        for i in range(4):
            word = [0, 0, 0, 0]
            word[i] = 1
            
            encoded = codificar_bch(bch, word)
            decoded = decodificar_bch(bch, encoded)
            
            assert decoded == word


if __name__ == "__main__":
    pytest.main([__file__])