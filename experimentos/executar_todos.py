"""
Script Master: Executa todos os experimentos sistematicamente
"""

import sys
import os
from datetime import datetime
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Importa todos os experimentos
from experimentos.exp01_variacao_snr import experimento_variacao_snr
from experimentos.exp02_comparacao_modulacao import experimento_comparacao_modulacao
from experimentos.exp03_variacao_bch import experimento_variacao_bch
from experimentos.exp04_analise_complexidade import experimento_analise_complexidade
from experimentos.exp05_perfis_dispositivos import experimento_perfis_dispositivos
from experimentos.exp06_analise_eve import experimento_eve_espacial, experimento_eve_temporal
from experimentos.exp07_impacto_guard_band import experimento_impacto_guard_band


def executar_bateria_completa():
    """
    Executa todos os experimentos em sequência
    
    ATENÇÃO: Este processo pode levar várias horas!
    """
    
    print("\n" + "="*70)
    print("BATERIA COMPLETA DE EXPERIMENTOS")
    print("Sistema de Geração de Chaves em Camada Física")
    print("="*70)
    print(f"Início: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70 + "\n")
    
    inicio_total = datetime.now()
    
    # ========== EXPERIMENTO 1: SNR ==========
    print("\n" + "#"*70)
    print("# EXPERIMENTO 1: VARIAÇÃO DE SNR")
    print("#"*70 + "\n")
    
    try:
        exp01 = experimento_variacao_snr(
            tamanho_cadeia_bits=127,
            quantidade_de_testes=1000,
            rayleigh_param=1.0/np.sqrt(2),
            modulacao='bpsk',
            correlacao_canal=0.9
        )
        print("✓ Experimento 1 concluído!")
    except Exception as e:
        print(f"✗ Erro no Experimento 1: {e}")
    
    # ========== EXPERIMENTO 2: MODULAÇÃO ==========
    print("\n" + "#"*70)
    print("# EXPERIMENTO 2: COMPARAÇÃO BPSK vs QPSK")
    print("#"*70 + "\n")
    
    try:
        exp02 = experimento_comparacao_modulacao(
            tamanho_cadeia_bits=127,
            quantidade_de_testes=1000,
            rayleigh_param=1.0/np.sqrt(2),
            correlacao_canal=0.9
        )
        print("✓ Experimento 2 concluído!")
    except Exception as e:
        print(f"✗ Erro no Experimento 2: {e}")
    
    # ========== EXPERIMENTO 3: BCH ==========
    print("\n" + "#"*70)
    print("# EXPERIMENTO 3: VARIAÇÃO DO CÓDIGO BCH")
    print("#"*70 + "\n")
    
    try:
        exp03 = experimento_variacao_bch(
            quantidade_de_testes=500,  # Reduzido para economizar tempo
            codigos_bch=[(7, 4), (15, 7), (127, 64)],
            rayleigh_param=1.0/np.sqrt(2),
            modulacao='bpsk',
            correlacao_canal=0.9
        )
        print("✓ Experimento 3 concluído!")
    except Exception as e:
        print(f"✗ Erro no Experimento 3: {e}")
    
    # ========== EXPERIMENTO 4: COMPLEXIDADE ==========
    print("\n" + "#"*70)
    print("# EXPERIMENTO 4: ANÁLISE DE COMPLEXIDADE COMPUTACIONAL")
    print("#"*70 + "\n")
    
    try:
        exp04 = experimento_analise_complexidade()
        print("✓ Experimento 4 concluído!")
    except Exception as e:
        print(f"✗ Erro no Experimento 4: {e}")
    
    # ========== EXPERIMENTO 5: PERFIS DE DISPOSITIVOS ==========
    print("\n" + "#"*70)
    print("# EXPERIMENTO 5: PERFIS DE DISPOSITIVOS IoT")
    print("#"*70 + "\n")
    
    try:
        exp05 = experimento_perfis_dispositivos(
            tamanho_cadeia_bits=127,
            quantidade_de_testes=1000,
            rayleigh_param=1.0/np.sqrt(2),
            modulacao='bpsk',
            snr_min=-5,
            snr_max=25,
            snr_pontos=16,
            atraso_medicao_ms=1.0
        )
        print("✓ Experimento 5 concluído!")
    except Exception as e:
        print(f"✗ Erro no Experimento 5: {e}")
    
    # ========== EXPERIMENTO 6: ANÁLISE SEGURANÇA (EVE) ==========
    print("\n" + "#"*70)
    print("# EXPERIMENTO 6: ANÁLISE DE SEGURANÇA CONTRA EVE")
    print("#"*70 + "\n")
    
    try:
        # 6A: Descorrelação espacial
        print("\n--- 6A: Descorrelação Espacial ---")
        exp06a, kdr_bob, lambda_m = experimento_eve_espacial(
            quantidade_de_testes=1000,
            distancias_eve_m=[0.1, 0.2, 0.5, 1.0, 2.0, 5.0, 10.0]
        )
        
        # 6B: Descorrelação temporal
        print("\n--- 6B: Descorrelação Temporal ---")
        exp06b = experimento_eve_temporal(
            quantidade_de_testes=1000,
            atrasos_ms=[0.0, 0.1, 0.5, 1.0, 2.0, 5.0, 10.0]
        )
        
        print("✓ Experimento 6 concluído!")
    except Exception as e:
        print(f"✗ Erro no Experimento 6: {e}")
    
    # ========== EXPERIMENTO 7: IMPACTO GUARD-BAND ==========
    print("\n" + "#"*70)
    print("# EXPERIMENTO 7: IMPACTO DO GUARD-BAND")
    print("#"*70 + "\n")
    
    try:
        exp07 = experimento_impacto_guard_band(
            quantidade_de_testes=1000,
            guard_bands=[0.0, 0.1, 0.3, 0.5, 0.7, 1.0],
            snr_db=15.0,
            correlacao_alice_bob=0.95,
            correlacao_alice_eve=0.0
        )
        print("✓ Experimento 7 concluído!")
    except Exception as e:
        print(f"✗ Erro no Experimento 7: {e}")
    
    # ========== FINALIZAÇÃO ==========
    fim_total = datetime.now()
    duracao = fim_total - inicio_total
    
    print("\n" + "="*70)
    print("BATERIA COMPLETA FINALIZADA")
    print("="*70)
    print(f"Início: {inicio_total.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Fim: {fim_total.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Duração total: {duracao}")
    print("="*70)
    print("\n✓ Todos os resultados foram salvos em:")
    print("  - resultados/dados/ (JSON e CSV)")
    print("  - resultados/figuras/ (PNG)")
    print("\nVocê pode usar esses dados para escrever o artigo!")
    print("="*70 + "\n")


def executar_bateria_rapida():
    """
    Executa versão rápida dos experimentos (para testes)
    """
    
    print("\n" + "="*70)
    print("BATERIA RÁPIDA DE EXPERIMENTOS (TESTE)")
    print("="*70 + "\n")
    
    # Experimento 1: SNR (reduzido)
    print("\n--- Experimento 1: SNR (versão rápida) ---")
    exp01 = experimento_variacao_snr(
        tamanho_cadeia_bits=15,  # Código pequeno
        quantidade_de_testes=100,  # Poucos testes
        snr_pontos=10  # Menos pontos
    )
    
    # Experimento 2: Modulação (reduzido)
    print("\n--- Experimento 2: Modulação (versão rápida) ---")
    exp02 = experimento_comparacao_modulacao(
        tamanho_cadeia_bits=15,
        quantidade_de_testes=100,
        snr_db_range=np.linspace(-5, 15, 10)
    )
    
    # Experimento 4: Complexidade
    print("\n--- Experimento 4: Complexidade (versão rápida) ---")
    exp04 = experimento_analise_complexidade()
    
    print("\n✓ Bateria rápida concluída!")
    print("Os resultados foram salvos nas pastas resultados/\n")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Executa bateria de experimentos PKG')
    parser.add_argument('--modo', choices=['completo', 'rapido'], default='rapido',
                       help='Modo de execução: completo (várias horas) ou rapido (minutos)')
    
    args = parser.parse_args()
    
    if args.modo == 'completo':
        print("\n⚠️  ATENÇÃO: Modo COMPLETO pode levar várias horas!")
        resposta = input("Deseja continuar? (s/n): ")
        if resposta.lower() == 's':
            executar_bateria_completa()
        else:
            print("Execução cancelada.")
    else:
        executar_bateria_rapida()
