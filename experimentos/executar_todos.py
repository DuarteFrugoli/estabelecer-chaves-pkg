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
from experimentos.exp02_variacao_sigma import experimento_variacao_sigma
from experimentos.exp03_comparacao_modulacao import experimento_comparacao_modulacao
from experimentos.exp04_variacao_correlacao import experimento_variacao_correlacao
from experimentos.exp05_variacao_bch import experimento_variacao_bch
from experimentos.exp07_perfis_dispositivos import experimento_perfis_dispositivos
from experimentos.exp08_variacao_distancia import (
    experimento_variacao_distancia,
    cenarios_artigo_referencia
)


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
    
    # ========== EXPERIMENTO 2: SIGMA ==========
    print("\n" + "#"*70)
    print("# EXPERIMENTO 2: VARIAÇÃO DO PARÂMETRO RAYLEIGH")
    print("#"*70 + "\n")
    
    try:
        exp02 = experimento_variacao_sigma(
            tamanho_cadeia_bits=127,
            quantidade_de_testes=1000,
            sigmas=[0.5, 1.0/np.sqrt(2), 1.0, 2.0],
            modulacao='bpsk',
            correlacao_canal=0.9
        )
        print("✓ Experimento 2 concluído!")
    except Exception as e:
        print(f"✗ Erro no Experimento 2: {e}")
    
    # ========== EXPERIMENTO 3: MODULAÇÃO ==========
    print("\n" + "#"*70)
    print("# EXPERIMENTO 3: COMPARAÇÃO BPSK vs QPSK")
    print("#"*70 + "\n")
    
    try:
        exp03 = experimento_comparacao_modulacao(
            tamanho_cadeia_bits=127,
            quantidade_de_testes=1000,
            rayleigh_param=1.0/np.sqrt(2),
            correlacao_canal=0.9
        )
        print("✓ Experimento 3 concluído!")
    except Exception as e:
        print(f"✗ Erro no Experimento 3: {e}")
    
    # ========== EXPERIMENTO 4: CORRELAÇÃO ==========
    print("\n" + "#"*70)
    print("# EXPERIMENTO 4: VARIAÇÃO DA CORRELAÇÃO DO CANAL")
    print("#"*70 + "\n")
    
    try:
        exp04 = experimento_variacao_correlacao(
            tamanho_cadeia_bits=127,
            quantidade_de_testes=1000,
            rayleigh_param=1.0/np.sqrt(2),
            modulacao='bpsk',
            correlacoes=[0.7, 0.8, 0.9, 0.95, 0.99]
        )
        print("✓ Experimento 4 concluído!")
    except Exception as e:
        print(f"✗ Erro no Experimento 4: {e}")
    
    # ========== EXPERIMENTO 5: BCH ==========
    print("\n" + "#"*70)
    print("# EXPERIMENTO 5: VARIAÇÃO DO CÓDIGO BCH")
    print("#"*70 + "\n")
    
    try:
        exp05 = experimento_variacao_bch(
            quantidade_de_testes=500,  # Reduzido para economizar tempo
            codigos_bch=[(7, 4), (15, 7), (127, 64)],
            rayleigh_param=1.0/np.sqrt(2),
            modulacao='bpsk',
            correlacao_canal=0.9
        )
        print("✓ Experimento 5 concluído!")
    except Exception as e:
        print(f"✗ Erro no Experimento 5: {e}")
    
    # ========== EXPERIMENTO 7: PERFIS DE DISPOSITIVOS ==========
    print("\n" + "#"*70)
    print("# EXPERIMENTO 7: PERFIS DE DISPOSITIVOS IoT")
    print("#"*70 + "\n")
    
    try:
        exp07 = experimento_perfis_dispositivos(
            tamanho_cadeia_bits=127,
            quantidade_de_testes=1000,
            rayleigh_param=1.0/np.sqrt(2),
            modulacao='bpsk',
            snr_min=-5,
            snr_max=25,
            snr_pontos=16,
            atraso_medicao_ms=1.0
        )
        print("✓ Experimento 7 concluído!")
    except Exception as e:
        print(f"✗ Erro no Experimento 7: {e}")
    
    # ========== EXPERIMENTO 8: VARIAÇÃO DE DISTÂNCIA ==========
    print("\n" + "#"*70)
    print("# EXPERIMENTO 8: VARIAÇÃO DE DISTÂNCIA (ARTIGO)")
    print("#"*70 + "\n")
    
    try:
        # Cenários do artigo de referência (SS1, SNS1, DS1, SS3, SNS3, DS3)
        exp08 = cenarios_artigo_referencia()
        print("✓ Experimento 8 concluído!")
    except Exception as e:
        print(f"✗ Erro no Experimento 8: {e}")
    
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
    
    # Experimento 2: Sigma (reduzido)
    print("\n--- Experimento 2: Sigma (versão rápida) ---")
    exp02 = experimento_variacao_sigma(
        tamanho_cadeia_bits=15,
        quantidade_de_testes=100,
        sigmas=[0.5, 1.0],  # Apenas 2 sigmas
        snr_db_range=np.linspace(-5, 15, 10)
    )
    
    # Experimento 3: Modulação (reduzido)
    print("\n--- Experimento 3: Modulação (versão rápida) ---")
    exp03 = experimento_comparacao_modulacao(
        tamanho_cadeia_bits=15,
        quantidade_de_testes=100,
        snr_db_range=np.linspace(-5, 15, 10)
    )
    
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
