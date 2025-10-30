"""
Testes unitários para reconciliação de chaves
"""
import pytest
import sys
import os
import random

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.pilares.reconciliacao import reconciliar_chaves
from src.codigos_corretores.bch import gerar_tabela_codigos_bch, get_tamanho_bits_informacao
from src.util.binario_util import calcular_distancia_hamming, xor_binario


class TestReconciliacaoChaves:
    """Testes para função de reconciliação de chaves"""
    
    def setup_method(self):
        """Setup executado antes de cada teste"""
        # Usa BCH(7,4) para testes rápidos
        self.n = 7
        self.k = 4
        self.tabela_codigos = gerar_tabela_codigos_bch(self.n, self.k)
    
    def test_reconciliacao_identical_keys(self):
        """Testa reconciliação quando as chaves são idênticas"""
        chave_alice = [1, 0, 1, 1, 0, 1, 0]
        chave_bob = [1, 0, 1, 1, 0, 1, 0]  # Idêntica
        
        # Fixa seed para reprodutibilidade
        random.seed(42)
        chave_reconciliada = reconciliar_chaves(chave_alice, chave_bob, self.tabela_codigos)
        
        # Quando não há erros, a reconciliação deve ser perfeita
        assert len(chave_reconciliada) == self.n
        assert chave_reconciliada == chave_alice
    
    def test_reconciliacao_single_error(self):
        """Testa reconciliação com um único erro"""
        chave_alice = [1, 0, 1, 1, 0, 1, 0]
        chave_bob = [1, 0, 1, 0, 0, 1, 0]  # 1 erro na posição 3
        
        # BCH(7,4) pode corrigir 1 erro
        random.seed(42)
        chave_reconciliada = reconciliar_chaves(chave_alice, chave_bob, self.tabela_codigos)
        
        assert len(chave_reconciliada) == self.n
        # A chave reconciliada deve ser igual à de Alice
        assert chave_reconciliada == chave_alice
    
    def test_reconciliacao_deterministic_with_seed(self):
        """Testa que a reconciliação é determinística com seed fixo"""
        chave_alice = [1, 0, 1, 1, 0, 1, 0]
        chave_bob = [1, 0, 0, 1, 0, 1, 0]  # 1 erro
        
        # Duas execuções com mesma seed
        random.seed(123)
        resultado1 = reconciliar_chaves(chave_alice, chave_bob, self.tabela_codigos)
        
        random.seed(123)
        resultado2 = reconciliar_chaves(chave_alice, chave_bob, self.tabela_codigos)
        
        assert resultado1 == resultado2
    
    def test_reconciliacao_multiple_errors_correctable(self):
        """Testa reconciliação com múltiplos erros corrigíveis"""
        # Usa BCH(15,7) que pode corrigir até 2 erros
        n, k = 15, 7
        tabela_15_7 = gerar_tabela_codigos_bch(n, k)
        
        chave_alice = [1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1]
        chave_bob = [1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1]  # 2 erros
        
        random.seed(42)
        chave_reconciliada = reconciliar_chaves(chave_alice, chave_bob, tabela_15_7)
        
        assert len(chave_reconciliada) == n
        # Com 2 erros ou menos, deve reconciliar perfeitamente
        assert chave_reconciliada == chave_alice
    
    def test_reconciliacao_invalid_bch_object(self):
        """Testa erro quando objeto BCH é inválido"""
        chave_alice = [1, 0, 1, 1, 0, 1, 0]
        chave_bob = [1, 0, 1, 0, 0, 1, 0]
        
        # Passa um objeto inválido ao invés de BCH
        with pytest.raises(AttributeError):
            reconciliar_chaves(chave_alice, chave_bob, [])
    
    def test_reconciliacao_wrong_length_keys(self):
        """Testa erro quando chaves têm tamanho diferente da tabela"""
        chave_alice = [1, 0, 1]  # Muito curta para BCH(7,4)
        chave_bob = [1, 0, 0]
        
        # Deve gerar erro no XOR devido a tamanhos incompatíveis
        with pytest.raises(AssertionError):
            reconciliar_chaves(chave_alice, chave_bob, self.tabela_codigos)
    
    def test_reconciliacao_properties_xor(self):
        """Testa propriedades matemáticas da reconciliação"""
        chave_alice = [1, 0, 1, 1, 0, 1, 0]
        chave_bob = [1, 0, 1, 0, 0, 1, 0]
        
        # Calcula erro entre as chaves
        erro = xor_binario(chave_alice, chave_bob)
        num_erros = sum(erro)
        
        # Se o número de erros é pequeno, reconciliação deve funcionar
        if num_erros <= 1:  # BCH(7,4) corrige até 1 erro
            random.seed(42)
            chave_reconciliada = reconciliar_chaves(chave_alice, chave_bob, self.tabela_codigos)
            assert chave_reconciliada == chave_alice
    
    def test_reconciliacao_multiple_runs_statistics(self):
        """Testa estatísticas de múltiplas execuções"""
        chave_alice = [1, 0, 1, 1, 0, 1, 0]
        chave_bob = [1, 0, 1, 0, 0, 1, 0]  # 1 erro
        
        sucessos = 0
        num_testes = 50
        
        for i in range(num_testes):
            random.seed(i)
            try:
                chave_reconciliada = reconciliar_chaves(chave_alice, chave_bob, self.tabela_codigos)
                if chave_reconciliada == chave_alice:
                    sucessos += 1
            except:
                pass
        
        # Com 1 erro em BCH(7,4), deve ter alta taxa de sucesso
        taxa_sucesso = sucessos / num_testes
        assert taxa_sucesso > 0.8  # Pelo menos 80% de sucesso
    
    def test_reconciliacao_symmetry(self):
        """Testa se a reconciliação tem propriedades simétricas esperadas"""
        chave_alice = [1, 0, 1, 1, 0, 1, 0]
        chave_bob = [1, 0, 1, 0, 0, 1, 0]
        
        # Testa múltiplas execuções com diferentes seeds
        random.seed(42)
        resultado1 = reconciliar_chaves(chave_alice, chave_bob, self.tabela_codigos)
        
        random.seed(43)
        resultado2 = reconciliar_chaves(chave_alice, chave_bob, self.tabela_codigos)
        
        # Os resultados podem ser diferentes devido à aleatoriedade na escolha do código
        # mas ambos devem ter o mesmo tamanho
        assert len(resultado1) == len(resultado2) == self.n


class TestReconciliacaoIntegration:
    """Testes de integração para reconciliação"""
    
    def test_reconciliacao_workflow_completo(self):
        """Testa fluxo completo da reconciliação"""
        # 1. Gera parâmetros
        n, k = 15, 7
        tabela = gerar_tabela_codigos_bch(n, k)
        
        # 2. Simula chaves observadas por Alice e Bob
        chave_alice = [random.randint(0, 1) for _ in range(n)]
        
        # 3. Introduz alguns erros para Bob (≤ capacidade de correção)
        chave_bob = chave_alice.copy()
        posicoes_erro = random.sample(range(n), 2)  # 2 erros máximo para BCH(15,7)
        for pos in posicoes_erro:
            chave_bob[pos] = 1 - chave_bob[pos]
        
        # 4. Executa reconciliação
        random.seed(42)
        chave_reconciliada = reconciliar_chaves(chave_alice, chave_bob, tabela)
        
        # 5. Verifica resultados
        assert len(chave_reconciliada) == n
        # Se introduzimos ≤ 2 erros, reconciliação deve funcionar
        assert chave_reconciliada == chave_alice
    
    def test_reconciliacao_different_bch_sizes(self):
        """Testa reconciliação com diferentes tamanhos de BCH"""
        test_params = [(7, 4), (15, 7)]
        
        for n, k in test_params:
            tabela = gerar_tabela_codigos_bch(n, k)
            
            # Chaves de teste
            chave_alice = [random.randint(0, 1) for _ in range(n)]
            chave_bob = chave_alice.copy()
            
            # Introduz 1 erro (todos os BCH testados podem corrigir ≥ 1 erro)
            chave_bob[0] = 1 - chave_bob[0]
            
            random.seed(42)
            resultado = reconciliar_chaves(chave_alice, chave_bob, tabela)
            
            assert len(resultado) == n
            assert resultado == chave_alice


class TestReconciliacaoPerformance:
    """Testes de performance e eficiência"""
    
    def test_reconciliacao_large_table(self):
        """Testa reconciliação com tabela grande"""
        # Para códigos pequenos, testa com tabela completa
        n, k = 15, 7
        tabela = gerar_tabela_codigos_bch(n, k)
        
        chave_alice = [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1]
        chave_bob = [1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1]  # 1 erro
        
        import time
        start = time.time()
        
        random.seed(42)
        resultado = reconciliar_chaves(chave_alice, chave_bob, tabela)
        
        end = time.time()
        
        # Deve ser rápido (< 1 segundo)
        assert (end - start) < 1.0
        assert resultado == chave_alice
    
    def test_reconciliacao_memory_efficiency(self):
        """Testa eficiência de memória"""
        n, k = 7, 4
        tabela = gerar_tabela_codigos_bch(n, k)
        
        # Executa múltiplas reconciliações
        for i in range(100):
            chave_alice = [random.randint(0, 1) for _ in range(n)]
            chave_bob = chave_alice.copy()
            if i % 2 == 0:  # Introduz erro em metade dos casos
                chave_bob[i % n] = 1 - chave_bob[i % n]
            
            random.seed(i)
            resultado = reconciliar_chaves(chave_alice, chave_bob, tabela)
            
            # Verificações básicas
            assert len(resultado) == n
            assert all(bit in {0, 1} for bit in resultado)


class TestReconciliacaoEdgeCases:
    """Testes de casos extremos"""
    
    def test_reconciliacao_all_zeros(self):
        """Testa reconciliação com chaves todos zeros"""
        n, k = 7, 4
        tabela = gerar_tabela_codigos_bch(n, k)
        
        chave_alice = [0] * n
        chave_bob = [0] * n
        
        random.seed(42)
        resultado = reconciliar_chaves(chave_alice, chave_bob, tabela)
        
        assert len(resultado) == n
        assert resultado == chave_alice
    
    def test_reconciliacao_all_ones(self):
        """Testa reconciliação com chaves todos uns"""
        n, k = 7, 4
        tabela = gerar_tabela_codigos_bch(n, k)
        
        chave_alice = [1] * n
        chave_bob = [1] * n
        
        random.seed(42)
        resultado = reconciliar_chaves(chave_alice, chave_bob, tabela)
        
        assert len(resultado) == n
        assert resultado == chave_alice
    
    def test_reconciliacao_maximum_correctable_errors(self):
        """Testa reconciliação no limite da capacidade de correção"""
        # BCH(15,7) pode corrigir t=2 erros
        n, k = 15, 7
        tabela = gerar_tabela_codigos_bch(n, k)
        
        chave_alice = [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1]
        chave_bob = chave_alice.copy()
        
        # Introduz exatamente 2 erros (limite)
        chave_bob[0] = 1 - chave_bob[0]
        chave_bob[7] = 1 - chave_bob[7]
        
        random.seed(42)
        resultado = reconciliar_chaves(chave_alice, chave_bob, tabela)
        
        assert len(resultado) == n
        # No limite da capacidade, deve ainda funcionar
        assert resultado == chave_alice


if __name__ == "__main__":
    pytest.main([__file__])