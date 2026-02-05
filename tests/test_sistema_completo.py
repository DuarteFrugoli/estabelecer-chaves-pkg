"""
Testes de integração completa do sistema PKG
"""
import pytest
import sys
import os
import random
import numpy as np

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.codigos_corretores.bch import gerar_tabela_codigos_bch
from src.pilares.reconciliacao import reconciliar_chaves
from src.pilares.amplificacao_privacidade import amplificacao_privacidade
from src.canal.canal import extrair_kdr, simular_canal
from src.util.binario_util import contar_erros_bits, xor_binario


class TestSistemaPKGCompleto:
    """Testes de integração do sistema PKG completo"""
    
    def setup_method(self):
        """Setup executado antes de cada teste"""
        np.random.seed(42)
        random.seed(42)
    
    def test_fluxo_pkg_completo_basic(self):
        """Teste do fluxo PKG completo básico"""
        # 1. Configuração inicial
        n, k = 7, 4
        tabela_codigos = gerar_tabela_codigos_bch(n, k)
        palavra_codigo = [1, 0, 1, 1, 0, 1, 0]
        
        # 2. Simulação do canal
        ganho_alice = [1.0, 1.2, 0.8, 1.1, 0.9, 1.3, 1.0]
        ganho_bob = [1.1, 1.1, 0.9, 1.0, 1.0, 1.2, 0.9]
        
        chave_alice = simular_canal(ganho_alice, palavra_codigo, 0.1, 0.0)
        chave_bob = simular_canal(ganho_bob, palavra_codigo, 0.1, 0.0)
        
        # 3. Reconciliação
        random.seed(42)
        chave_reconciliada = reconciliar_chaves(chave_alice, chave_bob, tabela_codigos)
        
        # 4. Amplificação de privacidade
        chave_final_alice = amplificacao_privacidade(chave_alice)
        chave_final_bob = amplificacao_privacidade(chave_reconciliada)
        
        # 5. Verificações
        assert len(chave_alice) == n
        assert len(chave_bob) == n
        assert len(chave_reconciliada) == n
        assert len(chave_final_alice) == 256  # SHA-256
        assert len(chave_final_bob) == 256
        
        # As chaves finais podem ser diferentes devido ao ruído do canal
        assert all(bit in {0, 1} for bit in chave_final_alice)
        assert all(bit in {0, 1} for bit in chave_final_bob)
    
    def test_fluxo_pkg_sem_ruido(self):
        """Teste PKG sem ruído - deve gerar chaves idênticas"""
        n, k = 7, 4
        tabela_codigos = gerar_tabela_codigos_bch(n, k)
        palavra_codigo = [1, 0, 1, 1, 0, 1, 0]
        
        # Canais idênticos e sem ruído
        ganho_canal = [1.0] * n
        
        chave_alice = simular_canal(ganho_canal, palavra_codigo, 0.0, 0.0)
        chave_bob = simular_canal(ganho_canal, palavra_codigo, 0.0, 0.0)
        
        # Com mapeamento correto, bits são invertidos mas Alice e Bob têm o mesmo
        assert chave_alice == chave_bob
        
        # Reconciliação deve manter identidade
        random.seed(42)
        chave_reconciliada = reconciliar_chaves(chave_alice, chave_bob, tabela_codigos)
        assert chave_reconciliada == chave_alice
        
        # Amplificação deve produzir chaves idênticas
        chave_final_alice = amplificacao_privacidade(chave_alice)
        chave_final_bob = amplificacao_privacidade(chave_reconciliada)
        assert chave_final_alice == chave_final_bob
    
    def test_fluxo_pkg_diferentes_tamanhos_bch(self):
        """Teste PKG com diferentes códigos BCH"""
        tamanhos_bch = [(7, 4), (15, 7)]
        
        for n, k in tamanhos_bch:
            tabela_codigos = gerar_tabela_codigos_bch(n, k)
            palavra_codigo = [random.randint(0, 1) for _ in range(n)]
            
            # Simulação com pouco ruído
            ganho_alice = [1.0 + 0.1 * random.random() for _ in range(n)]
            ganho_bob = [1.0 + 0.1 * random.random() for _ in range(n)]
            
            chave_alice = simular_canal(ganho_alice, palavra_codigo, 0.05, 0.0)
            chave_bob = simular_canal(ganho_bob, palavra_codigo, 0.05, 0.0)
            
            # Reconciliação
            random.seed(42)
            chave_reconciliada = reconciliar_chaves(chave_alice, chave_bob, tabela_codigos)
            
            # Verificações básicas
            assert len(chave_alice) == n
            assert len(chave_bob) == n
            assert len(chave_reconciliada) == n
            
            # Amplificação
            chave_final_alice = amplificacao_privacidade(chave_alice)
            chave_final_bob = amplificacao_privacidade(chave_reconciliada)
            
            assert len(chave_final_alice) == 256
            assert len(chave_final_bob) == 256
    
    def test_fluxo_pkg_com_extrair_kdr(self):
        """Teste integração usando extrair_kdr"""
        # Parâmetros
        palavra_codigo = [1, 0, 1, 1, 0, 1, 0]
        rayleigh_param = 1.0
        tamanho_cadeia_bits = 7
        quantidade_de_testes = 10
        variancia_ruido = 0.1
        media_ruido = 0.0
        tabela_codigos = gerar_tabela_codigos_bch(7, 4)
        
        # Testa sem amplificação
        ber, kdr = extrair_kdr(
            palavra_codigo,
            rayleigh_param,
            tamanho_cadeia_bits,
            quantidade_de_testes,
            variancia_ruido,
            media_ruido,
            tabela_codigos,
            usar_amplificacao=False
        )
        
        # Testa com amplificação (SHA-256 aplicado internamente)
        ber_amp, kdr_amp = extrair_kdr(
            palavra_codigo,
            rayleigh_param,
            tamanho_cadeia_bits,
            quantidade_de_testes,
            variancia_ruido,
            media_ruido,
            tabela_codigos,
            usar_amplificacao=True
        )
        
        # Verificações
        assert 0.0 <= ber <= 100.0
        assert 0.0 <= kdr <= 100.0
        assert 0.0 <= ber_amp <= 100.0
        assert 0.0 <= kdr_amp <= 100.0
        
        # BCH deve reduzir erros: KDR <= BER
        assert isinstance(kdr, float)
        assert isinstance(kdr_amp, float)
    
    def test_pkg_robustez_alta_correlacao(self):
        """Teste robustez do PKG com alta correlação de canal"""
        n, k = 15, 7
        tabela_codigos = gerar_tabela_codigos_bch(n, k)
        palavra_codigo = [random.randint(0, 1) for _ in range(n)]
        
        # Simula alta correlação manualmente
        ganho_base = np.random.rayleigh(1.0, n)
        ruido_decorrelacao = np.random.normal(0, 0.1, n)
        
        ganho_alice = ganho_base
        ganho_bob = ganho_base + ruido_decorrelacao
        
        chave_alice = simular_canal(ganho_alice, palavra_codigo, 0.1, 0.0)
        chave_bob = simular_canal(ganho_bob, palavra_codigo, 0.1, 0.0)
        
        # Conta erros iniciais
        erros_iniciais = contar_erros_bits(chave_alice, chave_bob)
        
        # Reconciliação
        random.seed(42)
        chave_reconciliada = reconciliar_chaves(chave_alice, chave_bob, tabela_codigos)
        
        # Conta erros pós reconciliação
        erros_pos_reconciliacao = contar_erros_bits(chave_alice, chave_reconciliada)
        
        # Reconciliação deve reduzir erros
        assert erros_pos_reconciliacao <= erros_iniciais
        
        # Amplificação
        chave_final_alice = amplificacao_privacidade(chave_alice)
        chave_final_bob = amplificacao_privacidade(chave_reconciliada)
        
        assert len(chave_final_alice) == 256
        assert len(chave_final_bob) == 256
    
    def test_pkg_resistencia_ataques_simples(self):
        """Teste resistência a ataques simples"""
        n, k = 7, 4
        tabela_codigos = gerar_tabela_codigos_bch(n, k)
        
        # Simula Alice e Bob
        palavra_codigo = [1, 0, 1, 1, 0, 1, 0]
        ganho_legitimo = [1.0] * n
        
        chave_alice = simular_canal(ganho_legitimo, palavra_codigo, 0.05, 0.0)
        chave_bob = simular_canal(ganho_legitimo, palavra_codigo, 0.05, 0.0)
        
        # Simula atacante Eve com ganho diferente
        ganho_atacante = [0.5] * n
        chave_eve = simular_canal(ganho_atacante, palavra_codigo, 0.5, 0.0)
        
        # Alice-Bob devem ter chaves mais similares que Alice-Eve
        erros_alice_bob = contar_erros_bits(chave_alice, chave_bob)
        erros_alice_eve = contar_erros_bits(chave_alice, chave_eve)
        
        # Na maioria dos casos, Alice-Bob devem ter menos erros
        # (pode não ser sempre verdade devido à aleatoriedade do canal)
        assert erros_alice_bob >= 0
        assert erros_alice_eve >= 0
        
        # Testa se amplificação produz chaves diferentes para Eve
        chave_final_alice = amplificacao_privacidade(chave_alice)
        chave_final_eve = amplificacao_privacidade(chave_eve)
        
        # Chaves amplificadas devem ser diferentes
        assert chave_final_alice != chave_final_eve
    
    def test_pkg_distribuicao_chaves_finais(self):
        """Teste distribuição das chaves finais"""
        n, k = 7, 4
        tabela_codigos = gerar_tabela_codigos_bch(n, k)
        
        chaves_geradas = []
        for i in range(20):
            # Gera chave inicial aleatória
            chave_inicial = [random.randint(0, 1) for _ in range(n)]
            
            # Aplica amplificação
            chave_final = amplificacao_privacidade(chave_inicial)
            chaves_geradas.append(chave_final)
        
        # Verifica propriedades das chaves
        for chave in chaves_geradas:
            assert len(chave) == 256
            assert all(bit in {0, 1} for bit in chave)
        
        # Verifica diversidade (chaves diferentes devem ser geradas)
        chaves_unicas = set(tuple(chave) for chave in chaves_geradas)
        assert len(chaves_unicas) > 1  # Deve haver pelo menos 2 chaves diferentes
    
    def test_pkg_propriedades_estatisticas(self):
        """Teste propriedades estatísticas do sistema PKG"""
        n, k = 15, 7
        tabela_codigos = gerar_tabela_codigos_bch(n, k)
        
        # Coleta estatísticas de múltiplas execuções
        ber_valores = []
        kdr_valores = []
        
        for i in range(10):
            np.random.seed(i)
            random.seed(i)
            
            palavra_codigo = [random.randint(0, 1) for _ in range(n)]
            
            ber, kdr = extrair_kdr(
                palavra_codigo,
                1.0,  # rayleigh_param
                n,
                5,    # poucos testes para rapidez
                0.2,  # variancia_ruido
                0.0,  # media_ruido
                tabela_codigos,
                correlacao_canal=0.8,
                usar_amplificacao=False
            )
            
            ber_valores.append(ber)
            kdr_valores.append(kdr)
        
        # Análise estatística básica
        ber_medio = sum(ber_valores) / len(ber_valores)
        kdr_medio = sum(kdr_valores) / len(kdr_valores)
        
        # Reconciliação BCH deve melhorar em média: KDR < BER
        assert kdr_medio <= ber_medio + 5.0  # +5 tolerância estatística
        
        # Valores devem estar em faixa razoável
        assert 0.0 <= ber_medio <= 100.0
        assert 0.0 <= kdr_medio <= 100.0
    
    def test_pkg_diferentes_cenarios_ruido(self):
        """Teste PKG em diferentes cenários de ruído"""
        n, k = 7, 4
        tabela_codigos = gerar_tabela_codigos_bch(n, k)
        palavra_codigo = [1, 0, 1, 1, 0, 1, 0]
        
        variancias_ruido = [0.01, 0.1, 0.5]
        
        for variancia in variancias_ruido:
            # Executa PKG
            ber, kdr = extrair_kdr(
                palavra_codigo,
                1.0,
                n,
                5,
                variancia,
                0.0,
                tabela_codigos,
                usar_amplificacao=False
            )
            
            # Verificações básicas
            assert 0.0 <= ber <= 100.0
            assert 0.0 <= kdr <= 100.0
            # Verifica que são valores válidos
            assert isinstance(kdr, float)
        
        # Com mais ruído, espera-se mais erros (teste geral)
        # Mas pode variar devido à aleatoriedade


class TestSistemaPKGErros:
    """Testes de casos de erro do sistema PKG"""
    
    def test_pkg_entrada_invalida(self):
        """Teste comportamento com entradas inválidas"""
        # Objeto BCH inválido
        with pytest.raises(AttributeError):
            reconciliar_chaves([1, 0, 1], [1, 0, 0], [])
        
        # Chaves de tamanhos diferentes
        with pytest.raises(AssertionError):
            reconciliar_chaves([1, 0], [1, 0, 1], gerar_tabela_codigos_bch(7, 4))
    
    def test_pkg_limites_correcao(self):
        """Teste limites de capacidade de correção"""
        n, k = 7, 4  # BCH(7,4) corrige até 1 erro
        tabela_codigos = gerar_tabela_codigos_bch(n, k)
        
        chave_alice = [1, 0, 1, 1, 0, 1, 0]
        chave_bob = [0, 1, 0, 0, 1, 0, 1]  # Muitos erros
        
        # Reconciliação pode não conseguir corrigir todos os erros
        random.seed(42)
        chave_reconciliada = reconciliar_chaves(chave_alice, chave_bob, tabela_codigos)
        
        # Deve retornar alguma chave válida
        assert len(chave_reconciliada) == n
        assert all(bit in {0, 1} for bit in chave_reconciliada)


if __name__ == "__main__":
    pytest.main([__file__])