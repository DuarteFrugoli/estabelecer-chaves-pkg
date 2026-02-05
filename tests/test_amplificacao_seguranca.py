"""
Testes de Segurança para Amplificação de Privacidade (SHA-256)

Este módulo valida as propriedades criptográficas do SHA-256:
1. Efeito avalanche: 1 bit muda → ~50% dos bits do hash mudam
2. Determinismo: mesma entrada → mesma saída
3. Distribuição uniforme: bits do hash são estatisticamente aleatórios

Nota: Não testamos "KDR pós-SHA" pois:
- SHA-256 é determinístico: KDR=0 → hashes idênticos, KDR>0 → hashes completamente diferentes
- Não há gradação útil para medir em experimentos vs SNR/σ/correlação
"""

import pytest
import numpy as np
from src.pilares.amplificacao_privacidade import amplificacao_privacidade


class TestAmplificacaoSeguranca:
    """Testes de segurança para SHA-256"""
    
    def test_efeito_avalanche(self):
        """
        Propriedade: Mudar 1 bit da entrada deve mudar ~50% dos bits do hash
        
        Referência: FIPS 180-4 (SHA-256 Standard)
        """
        # Chave original
        chave_original = [1, 0, 1, 1, 0, 0, 1, 0] * 16  # 128 bits
        hash_original = amplificacao_privacidade(chave_original)
        
        diferencas = []
        
        # Testa mudando cada bit individualmente
        for i in range(len(chave_original)):
            chave_modificada = chave_original.copy()
            chave_modificada[i] = 1 - chave_modificada[i]  # Flip 1 bit
            
            hash_modificado = amplificacao_privacidade(chave_modificada)
            
            # Conta bits diferentes
            diff = sum(h1 != h2 for h1, h2 in zip(hash_original, hash_modificado))
            diferencas.append(diff)
        
        # Efeito avalanche: ~50% dos 256 bits devem mudar
        media_diff = np.mean(diferencas)
        
        # Aceita intervalo [40%, 60%] (102-154 bits em 256)
        assert 102 <= media_diff <= 154, \
            f"Efeito avalanche fraco: {media_diff:.1f} bits mudaram (esperado ~128)"
        
        print(f"\n✓ Efeito avalanche validado: {media_diff:.1f}/256 bits mudam (ideal: 128)")
    
    def test_determinismo(self):
        """
        Propriedade: Mesma entrada sempre produz mesma saída
        """
        chave = [1, 0, 1, 1, 0, 0, 1, 0] * 16
        
        hash1 = amplificacao_privacidade(chave)
        hash2 = amplificacao_privacidade(chave)
        hash3 = amplificacao_privacidade(chave)
        
        assert hash1 == hash2 == hash3, "SHA-256 não é determinístico!"
        
        print("\n✓ Determinismo validado: mesma entrada → mesma saída")
    
    def test_distribuicao_uniforme_bits(self):
        """
        Propriedade: Bits do hash devem ser ~50% zeros, ~50% uns
        
        Teste estatístico simples: proporção de 1s em múltiplos hashes
        """
        np.random.seed(42)
        
        total_bits = 0
        total_uns = 0
        num_hashes = 100
        
        for i in range(num_hashes):
            # Gera chave aleatória
            chave = np.random.randint(0, 2, 128).tolist()
            hash_result = amplificacao_privacidade(chave)
            
            total_bits += len(hash_result)
            total_uns += sum(hash_result)
        
        proporcao_uns = total_uns / total_bits
        
        # Aceita intervalo [0.45, 0.55] (95% confiança para binomial)
        assert 0.45 <= proporcao_uns <= 0.55, \
            f"Distribuição não-uniforme: {proporcao_uns:.3f} (esperado ~0.5)"
        
        print(f"\n✓ Distribuição uniforme: {proporcao_uns:.3f} uns (ideal: 0.5)")
    
    def test_colisao_improvavel(self):
        """
        Propriedade: Chaves similares produzem hashes completamente diferentes
        
        Exemplo: chaves com 1 bit diferente devem ter hashes não-correlacionados
        """
        np.random.seed(123)
        
        chave1 = np.random.randint(0, 2, 128).tolist()
        chave2 = chave1.copy()
        chave2[0] = 1 - chave2[0]  # Muda apenas 1 bit
        
        hash1 = amplificacao_privacidade(chave1)
        hash2 = amplificacao_privacidade(chave2)
        
        # Conta bits diferentes
        diff = sum(h1 != h2 for h1, h2 in zip(hash1, hash2))
        
        # Deve mudar muitos bits (efeito avalanche)
        assert diff > 100, f"Hashes muito similares: apenas {diff}/256 bits diferentes"
        
        print(f"\n✓ Resistência a colisão: {diff}/256 bits diferentes (bom: >100)")
    
    def test_independencia_entrada(self):
        """
        Propriedade: Entradas diferentes → hashes não-correlacionados
        
        Testa que hashes de chaves aleatórias não compartilham padrões
        """
        np.random.seed(456)
        
        num_testes = 50
        hashes = []
        
        for _ in range(num_testes):
            chave = np.random.randint(0, 2, 128).tolist()
            hash_result = amplificacao_privacidade(chave)
            hashes.append(hash_result)
        
        # Calcula correlação média entre pares de hashes
        correlacoes = []
        for i in range(num_testes):
            for j in range(i+1, num_testes):
                # Correlação = proporção de bits iguais
                bits_iguais = sum(hashes[i][k] == hashes[j][k] for k in range(256))
                corr = bits_iguais / 256
                correlacoes.append(corr)
        
        corr_media = np.mean(correlacoes)
        
        # Hashes aleatórios devem ter ~50% bits iguais (correlação ~0.5)
        assert 0.45 <= corr_media <= 0.55, \
            f"Hashes correlacionados: {corr_media:.3f} (esperado ~0.5)"
        
        print(f"\n✓ Independência: correlação média = {corr_media:.3f} (ideal: 0.5)")
    
    def test_tamanho_saida_fixo(self):
        """
        Propriedade: SHA-256 sempre produz 256 bits
        """
        chaves_tamanhos = [8, 64, 127, 256, 512]
        
        for tam in chaves_tamanhos:
            chave = [1, 0] * (tam // 2) + [1] * (tam % 2)
            hash_result = amplificacao_privacidade(chave)
            
            assert len(hash_result) == 256, \
                f"Tamanho errado: {len(hash_result)} bits (esperado 256)"
        
        print("\n✓ Tamanho fixo: SHA-256 sempre retorna 256 bits")
    
    def test_sensibilidade_posicao(self):
        """
        Propriedade: Mudar bit na posição X ou Y produz mudanças equivalentes
        
        SHA-256 não deve ter "bits fracos" (posições menos sensíveis)
        """
        np.random.seed(789)
        chave_base = np.random.randint(0, 2, 128).tolist()
        hash_base = amplificacao_privacidade(chave_base)
        
        diferencas_por_posicao = []
        
        # Testa cada posição
        for pos in range(len(chave_base)):
            chave_mod = chave_base.copy()
            chave_mod[pos] = 1 - chave_mod[pos]
            
            hash_mod = amplificacao_privacidade(chave_mod)
            diff = sum(h1 != h2 for h1, h2 in zip(hash_base, hash_mod))
            diferencas_por_posicao.append(diff)
        
        # Desvio padrão deve ser pequeno (todas posições igualmente sensíveis)
        std_diff = np.std(diferencas_por_posicao)
        
        # Aceita std < 20 (variação razoável)
        assert std_diff < 20, \
            f"Sensibilidade varia muito: std={std_diff:.1f} (esperado <20)"
        
        print(f"\n✓ Sensibilidade uniforme: std={std_diff:.1f} bits (bom: <20)")


class TestAmplificacaoIntegracaoPKG:
    """Testes de integração com sistema PKG"""
    
    def test_kdr_zero_implica_hashes_identicos(self):
        """
        Se KDR=0 (Alice e Bob têm chave idêntica), hashes devem ser idênticos
        """
        chave_alice = [1, 0, 1, 1, 0, 0, 1, 0] * 16
        chave_bob = chave_alice.copy()  # KDR = 0
        
        hash_alice = amplificacao_privacidade(chave_alice)
        hash_bob = amplificacao_privacidade(chave_bob)
        
        assert hash_alice == hash_bob, "KDR=0 mas hashes diferentes!"
        
        print("\n✓ KDR=0 → hashes idênticos")
    
    def test_kdr_positivo_implica_hashes_diferentes(self):
        """
        Se KDR>0 (chaves diferem), hashes devem ser completamente diferentes
        
        Não há "KDR parcial" no hash: ou funciona (KDR=0) ou falha totalmente
        """
        chave_alice = [1, 0, 1, 1, 0, 0, 1, 0] * 16
        chave_bob = chave_alice.copy()
        chave_bob[0] = 1 - chave_bob[0]  # 1 bit diferente (KDR = 1/128 = 0.78%)
        
        hash_alice = amplificacao_privacidade(chave_alice)
        hash_bob = amplificacao_privacidade(chave_bob)
        
        # Hashes devem ser totalmente diferentes (não 0.78% diferentes!)
        diff = sum(h1 != h2 for h1, h2 in zip(hash_alice, hash_bob))
        
        assert diff > 100, \
            f"KDR baixo (0.78%) mas hashes ainda similares: {diff}/256 bits diferentes"
        
        print(f"\n✓ KDR>0 → hashes completamente diferentes ({diff}/256 bits)")
    
    def test_reconciliacao_bem_sucedida_garante_hash_identico(self):
        """
        Cenário real: Após reconciliação BCH bem-sucedida (KDR=0), 
        amplificação deve produzir chaves finais idênticas
        """
        # Simula reconciliação bem-sucedida
        chave_alice_original = [1, 0, 1, 1, 0, 0, 1, 0] * 16
        chave_bob_bruta = chave_alice_original.copy()
        chave_bob_bruta[5] = 1 - chave_bob_bruta[5]  # BER inicial
        
        # Após reconciliação BCH: Bob corrige erro
        chave_bob_reconciliada = chave_alice_original.copy()  # KDR=0
        
        # Amplificação
        hash_alice = amplificacao_privacidade(chave_alice_original)
        hash_bob = amplificacao_privacidade(chave_bob_reconciliada)
        
        assert hash_alice == hash_bob, \
            "Reconciliação bem-sucedida mas hashes finais diferentes!"
        
        print("\n✓ Fluxo PKG completo: BER → BCH → KDR=0 → Hashes idênticos")


class TestAmplificacaoPerformance:
    """Testes de performance (não-críticos, apenas informativos)"""
    
    def test_tempo_execucao_razoavel(self):
        """SHA-256 deve ser rápido (<1ms por hash)"""
        import time
        
        chave = [1, 0] * 64
        
        start = time.perf_counter()
        for _ in range(1000):
            _ = amplificacao_privacidade(chave)
        elapsed = time.perf_counter() - start
        
        tempo_por_hash = elapsed / 1000 * 1000  # ms
        
        # Deve ser <1ms por hash
        assert tempo_por_hash < 1.0, \
            f"SHA-256 muito lento: {tempo_por_hash:.3f}ms (esperado <1ms)"
        
        print(f"\n✓ Performance: {tempo_por_hash:.3f}ms por hash (bom: <1ms)")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
