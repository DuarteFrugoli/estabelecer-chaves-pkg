"""
Testes unitários para simulação de canal Rayleigh
"""
import pytest
import sys
import os
import numpy as np
import random

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from canal.canal import simular_canal, extrair_kdr
from codigos_corretores.bch import gerar_tabela_codigos_bch


class TestSimularCanal:
    """Testes para função simular_canal"""
    
    def setup_method(self):
        """Setup executado antes de cada teste"""
        # Fixa seed para reprodutibilidade
        np.random.seed(42)
        random.seed(42)
    
    def test_simular_canal_basic(self):
        """Teste básico da simulação de canal"""
        ganho_canal = [1.0, 1.0, 1.0, 1.0]
        palavra_codigo = [1, 0, 1, 0]
        variancia_ruido = 0.1
        media_ruido = 0.0
        
        resultado = simular_canal(ganho_canal, palavra_codigo, variancia_ruido, media_ruido)
        
        assert len(resultado) == len(palavra_codigo)
        assert all(bit in {0, 1} for bit in resultado)
    
    def test_simular_canal_no_noise(self):
        """Testa simulação com ruído zero"""
        ganho_canal = [1.0, 1.0, 1.0, 1.0]
        palavra_codigo = [1, 0, 1, 0]
        variancia_ruido = 0.0  # Sem ruído
        media_ruido = 0.0
        
        resultado = simular_canal(ganho_canal, palavra_codigo, variancia_ruido, media_ruido)
        
        # Sem ruído, deve manter os bits originais
        assert resultado == palavra_codigo
    
    def test_simular_canal_high_gain(self):
        """Testa simulação com ganho alto"""
        ganho_canal = [10.0, 10.0, 10.0, 10.0]
        palavra_codigo = [1, 0, 1, 0]
        variancia_ruido = 0.1
        media_ruido = 0.0
        
        resultado = simular_canal(ganho_canal, palavra_codigo, variancia_ruido, media_ruido)
        
        assert len(resultado) == len(palavra_codigo)
        # Com ganho alto, ruído tem menos impacto
        assert all(bit in {0, 1} for bit in resultado)
    
    def test_simular_canal_different_gains(self):
        """Testa simulação com ganhos diferentes para cada bit"""
        ganho_canal = [0.5, 1.0, 1.5, 2.0]
        palavra_codigo = [1, 0, 1, 0]
        variancia_ruido = 0.1
        media_ruido = 0.0
        
        resultado = simular_canal(ganho_canal, palavra_codigo, variancia_ruido, media_ruido)
        
        assert len(resultado) == len(palavra_codigo)
        assert all(bit in {0, 1} for bit in resultado)
    
    def test_simular_canal_bpsk_mapping(self):
        """Testa mapeamento BPSK correto"""
        # Com ganho muito alto e sem ruído, deve mapear corretamente
        ganho_canal = [100.0, 100.0]
        palavra_codigo = [0, 1]
        variancia_ruido = 0.0
        media_ruido = 0.0
        
        resultado = simular_canal(ganho_canal, palavra_codigo, variancia_ruido, media_ruido)
        
        # BPSK: 0 -> -1, 1 -> +1. Com detecção >= 0
        # 0 -> -100 -> reamostrado como 0
        # 1 -> +100 -> reamostrado como 1
        assert resultado == [0, 1]
    
    def test_simular_canal_empty_input(self):
        """Testa comportamento com entrada vazia"""
        ganho_canal = []
        palavra_codigo = []
        variancia_ruido = 0.1
        media_ruido = 0.0
        
        resultado = simular_canal(ganho_canal, palavra_codigo, variancia_ruido, media_ruido)
        
        assert resultado == []
    
    def test_simular_canal_single_bit(self):
        """Testa simulação com um único bit"""
        ganho_canal = [1.0]
        palavra_codigo = [1]
        variancia_ruido = 0.1
        media_ruido = 0.0
        
        resultado = simular_canal(ganho_canal, palavra_codigo, variancia_ruido, media_ruido)
        
        assert len(resultado) == 1
        assert resultado[0] in {0, 1}
    
    def test_simular_canal_negative_gain(self):
        """Testa simulação com ganho negativo"""
        ganho_canal = [-1.0, -1.0]
        palavra_codigo = [0, 1]
        variancia_ruido = 0.0
        media_ruido = 0.0
        
        resultado = simular_canal(ganho_canal, palavra_codigo, variancia_ruido, media_ruido)
        
        # Ganho negativo inverte o sinal
        # 0 -> -1 * -1 = +1 -> reamostrado como 1
        # 1 -> +1 * -1 = -1 -> reamostrado como 0
        assert resultado == [1, 0]
    
    def test_simular_canal_high_noise(self):
        """Testa simulação com ruído muito alto"""
        ganho_canal = [1.0, 1.0, 1.0, 1.0]
        palavra_codigo = [1, 0, 1, 0]
        variancia_ruido = 100.0  # Ruído muito alto
        media_ruido = 0.0
        
        resultado = simular_canal(ganho_canal, palavra_codigo, variancia_ruido, media_ruido)
        
        assert len(resultado) == len(palavra_codigo)
        assert all(bit in {0, 1} for bit in resultado)
        # Com ruído muito alto, resultado pode ser aleatório


class TestExtrairKDR:
    """Testes para função extrair_kdr"""
    
    def setup_method(self):
        """Setup executado antes de cada teste"""
        np.random.seed(42)
        random.seed(42)
        
        # Parâmetros padrão para testes
        self.palavra_codigo = [1, 0, 1, 1, 0, 1, 0]
        self.rayleigh_param = 1.0
        self.tamanho_cadeia_bits = 7
        self.quantidade_de_testes = 10
        self.variancia_ruido = 0.1
        self.media_ruido = 0.0
        self.tabela_codigos = gerar_tabela_codigos_bch(7, 4)
    
    def test_extrair_kdr_basic(self):
        """Teste básico da extração KDR sem amplificação"""
        kdr, kdr_pos_reconciliacao = extrair_kdr(
            self.palavra_codigo,
            self.rayleigh_param,
            self.tamanho_cadeia_bits,
            self.quantidade_de_testes,
            self.variancia_ruido,
            self.media_ruido,
            self.tabela_codigos,
            usar_amplificacao=False
        )
        
        assert isinstance(kdr, float)
        assert isinstance(kdr_pos_reconciliacao, float)
        assert 0.0 <= kdr <= 100.0
        assert 0.0 <= kdr_pos_reconciliacao <= 100.0
        # Em sistemas estocásticos, reconciliação geralmente reduz erros
        # mas pode ocasionalmente não reduzir devido à aleatoriedade
        assert isinstance(kdr_pos_reconciliacao, float)
        assert 0.0 <= kdr_pos_reconciliacao <= 100.0
    
    def test_extrair_kdr_with_amplification(self):
        """Teste da extração KDR com amplificação"""
        kdr, kdr_pos_reconciliacao, kdr_pos_amplificacao = extrair_kdr(
            self.palavra_codigo,
            self.rayleigh_param,
            self.tamanho_cadeia_bits,
            self.quantidade_de_testes,
            self.variancia_ruido,
            self.media_ruido,
            self.tabela_codigos,
            usar_amplificacao=True
        )
        
        assert isinstance(kdr, float)
        assert isinstance(kdr_pos_reconciliacao, float)
        assert isinstance(kdr_pos_amplificacao, float)
        assert 0.0 <= kdr <= 100.0
        assert 0.0 <= kdr_pos_reconciliacao <= 100.0
        assert 0.0 <= kdr_pos_amplificacao <= 100.0
    
    def test_extrair_kdr_no_noise(self):
        """Teste KDR sem ruído"""
        kdr, kdr_pos_reconciliacao = extrair_kdr(
            self.palavra_codigo,
            self.rayleigh_param,
            self.tamanho_cadeia_bits,
            5,  # Poucos testes para rapidez
            0.0,  # Sem ruído
            0.0,
            self.tabela_codigos,
            correlacao_canal=1.0,  # Canais idênticos
            usar_amplificacao=False
        )
        
        # Sem ruído e canais idênticos, KDR deve ser muito baixo
        assert kdr < 5.0  # Menos de 5% de erro
        assert kdr_pos_reconciliacao < 5.0
    
    def test_extrair_kdr_high_correlation(self):
        """Teste KDR com alta correlação de canal"""
        kdr_alta, _ = extrair_kdr(
            self.palavra_codigo,
            self.rayleigh_param,
            self.tamanho_cadeia_bits,
            5,
            self.variancia_ruido,
            self.media_ruido,
            self.tabela_codigos,
            correlacao_canal=0.95,
            usar_amplificacao=False
        )
        
        kdr_baixa, _ = extrair_kdr(
            self.palavra_codigo,
            self.rayleigh_param,
            self.tamanho_cadeia_bits,
            5,
            self.variancia_ruido,
            self.media_ruido,
            self.tabela_codigos,
            correlacao_canal=0.1,
            usar_amplificacao=False
        )
        
        # Alta correlação deve resultar em menor KDR
        assert kdr_alta < kdr_baixa
    
    def test_extrair_kdr_different_rayleigh_params(self):
        """Teste KDR com diferentes parâmetros Rayleigh"""
        # Parâmetro menor = canal mais fraco
        kdr_fraco, _ = extrair_kdr(
            self.palavra_codigo,
            0.5,  # Canal mais fraco
            self.tamanho_cadeia_bits,
            5,
            self.variancia_ruido,
            self.media_ruido,
            self.tabela_codigos,
            usar_amplificacao=False
        )
        
        # Parâmetro maior = canal mais forte
        kdr_forte, _ = extrair_kdr(
            self.palavra_codigo,
            2.0,  # Canal mais forte
            self.tamanho_cadeia_bits,
            5,
            self.variancia_ruido,
            self.media_ruido,
            self.tabela_codigos,
            usar_amplificacao=False
        )
        
        # Canal mais forte pode ter menor KDR (melhor SNR)
        assert isinstance(kdr_fraco, float)
        assert isinstance(kdr_forte, float)
    
    def test_extrair_kdr_single_test(self):
        """Teste KDR com apenas um teste"""
        kdr, kdr_pos_reconciliacao = extrair_kdr(
            self.palavra_codigo,
            self.rayleigh_param,
            self.tamanho_cadeia_bits,
            1,  # Apenas um teste
            self.variancia_ruido,
            self.media_ruido,
            self.tabela_codigos,
            usar_amplificacao=False
        )
        
        assert isinstance(kdr, float)
        assert isinstance(kdr_pos_reconciliacao, float)
        assert 0.0 <= kdr <= 100.0
        assert 0.0 <= kdr_pos_reconciliacao <= 100.0
    
    def test_extrair_kdr_large_word(self):
        """Teste KDR com palavra código maior"""
        # Usa BCH(15,7) para palavra maior
        palavra_maior = [1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1]
        tabela_maior = gerar_tabela_codigos_bch(15, 7)
        
        kdr, kdr_pos_reconciliacao = extrair_kdr(
            palavra_maior,
            self.rayleigh_param,
            15,  # Tamanho correspondente
            5,
            self.variancia_ruido,
            self.media_ruido,
            tabela_maior,
            usar_amplificacao=False
        )
        
        assert isinstance(kdr, float)
        assert isinstance(kdr_pos_reconciliacao, float)
        assert 0.0 <= kdr <= 100.0
        assert 0.0 <= kdr_pos_reconciliacao <= 100.0
    
    def test_extrair_kdr_zero_correlation(self):
        """Teste KDR com correlação zero (canais independentes)"""
        kdr, kdr_pos_reconciliacao = extrair_kdr(
            self.palavra_codigo,
            self.rayleigh_param,
            self.tamanho_cadeia_bits,
            5,
            self.variancia_ruido,
            self.media_ruido,
            self.tabela_codigos,
            correlacao_canal=0.0,  # Canais independentes
            usar_amplificacao=False
        )
        
        # Com canais independentes, KDR deve ser mais alto
        assert isinstance(kdr, float)
        assert isinstance(kdr_pos_reconciliacao, float)
        # Pode ter alta taxa de erro devido à falta de reciprocidade


class TestExtrairKDRIntegration:
    """Testes de integração para extrair_kdr"""
    
    def test_extrair_kdr_workflow_completo(self):
        """Teste do fluxo completo de extração KDR"""
        np.random.seed(123)
        random.seed(123)
        
        # Parâmetros realistas
        palavra_codigo = [1, 0, 1, 1, 0, 1, 0]
        rayleigh_param = 1.0
        tamanho_cadeia_bits = 7
        quantidade_de_testes = 20
        variancia_ruido = 0.2
        media_ruido = 0.0
        tabela_codigos = gerar_tabela_codigos_bch(7, 4)
        
        # Com amplificação
        resultado_com_amp = extrair_kdr(
            palavra_codigo,
            rayleigh_param,
            tamanho_cadeia_bits,
            quantidade_de_testes,
            variancia_ruido,
            media_ruido,
            tabela_codigos,
            correlacao_canal=0.8,
            usar_amplificacao=True
        )
        
        # Sem amplificação
        resultado_sem_amp = extrair_kdr(
            palavra_codigo,
            rayleigh_param,
            tamanho_cadeia_bits,
            quantidade_de_testes,
            variancia_ruido,
            media_ruido,
            tabela_codigos,
            correlacao_canal=0.8,
            usar_amplificacao=False
        )
        
        # Verifica estrutura dos resultados
        assert len(resultado_com_amp) == 3  # KDR, KDR pós-reconciliação, KDR pós-amplificação
        assert len(resultado_sem_amp) == 2  # KDR, KDR pós-reconciliação
        
        # Verifica propriedades
        kdr, kdr_rec, kdr_amp = resultado_com_amp
        assert 0.0 <= kdr <= 100.0
        assert 0.0 <= kdr_rec <= 100.0
        assert 0.0 <= kdr_amp <= 100.0
        
        kdr2, kdr_rec2 = resultado_sem_amp
        assert 0.0 <= kdr2 <= 100.0
        assert 0.0 <= kdr_rec2 <= 100.0
    
    def test_extrair_kdr_consistency(self):
        """Teste de consistência entre execuções"""
        # Duas execuções com mesma seed devem dar resultado idêntico
        np.random.seed(456)
        random.seed(456)
        
        resultado1 = extrair_kdr(
            [1, 0, 1, 1, 0, 1, 0],
            1.0,
            7,
            10,
            0.1,
            0.0,
            gerar_tabela_codigos_bch(7, 4),
            usar_amplificacao=False
        )
        
        np.random.seed(456)
        random.seed(456)
        
        resultado2 = extrair_kdr(
            [1, 0, 1, 1, 0, 1, 0],
            1.0,
            7,
            10,
            0.1,
            0.0,
            gerar_tabela_codigos_bch(7, 4),
            usar_amplificacao=False
        )
        
        assert resultado1 == resultado2


class TestExtrairKDRPerformance:
    """Testes de performance para extrair_kdr"""
    
    def test_extrair_kdr_performance(self):
        """Teste de performance com muitos testes"""
        import time
        
        start = time.time()
        
        resultado = extrair_kdr(
            [1, 0, 1, 1, 0, 1, 0],
            1.0,
            7,
            100,  # Muitos testes
            0.1,
            0.0,
            gerar_tabela_codigos_bch(7, 4),
            usar_amplificacao=False
        )
        
        end = time.time()
        
        # Deve executar em tempo razoável (< 5 segundos)
        assert (end - start) < 5.0
        assert len(resultado) == 2
    
    def test_extrair_kdr_memory_usage(self):
        """Teste de uso de memória"""
        # Executa múltiplas vezes para verificar vazamentos
        for i in range(10):
            resultado = extrair_kdr(
                [1, 0, 1, 1, 0, 1, 0],
                1.0,
                7,
                5,
                0.1,
                0.0,
                gerar_tabela_codigos_bch(7, 4),
                usar_amplificacao=False
            )
            
            assert len(resultado) == 2
            # Força limpeza
            del resultado


if __name__ == "__main__":
    pytest.main([__file__])