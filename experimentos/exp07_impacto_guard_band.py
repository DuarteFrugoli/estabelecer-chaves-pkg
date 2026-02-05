"""
Experimento 7: Impacto do Guard-Band na Segurança e Eficiência
Testa o trade-off entre segurança (contra Eve) e eficiência (taxa de bits)
ao variar o parâmetro guard-band.

IMPORTÂNCIA: Guard-band é um DIFERENCIAL deste sistema PKG!
- GB↑ → Segurança↑ (mais difícil para Eve)
- GB↑ → Eficiência↓ (menos bits aproveitados)
- GB↑ → KDR Bob↓ (pode melhorar concordância)
"""

import sys
import os
import numpy as np
from tqdm import tqdm
from datetime import datetime
import matplotlib.pyplot as plt

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.codigos_corretores.bch import gerar_tabela_codigos_bch
from src.canal.canal import extrair_kdr, medir_seguranca_eve
from experimentos.util_experimentos import (
    salvar_resultado_json,
    salvar_resultado_csv,
    imprimir_sumario_resultados
)


def experimento_impacto_guard_band(
    tamanho_cadeia_bits=127,
    quantidade_de_testes=1000,
    rayleigh_param=1.0/np.sqrt(2),
    modulacao='bpsk',
    snr_db=15.0,  # SNR fixo em cenário bom
    correlacao_alice_bob=0.95,
    correlacao_alice_eve=0.0,  # Eve descorrelacionado espacialmente
    guard_bands=[0.0, 0.1, 0.3, 0.5, 0.7, 1.0],
    erro_estimativa=0.15
):
    """
    Testa impacto do guard-band em:
    1. KDR Alice-Bob (deve diminuir com GB↑)
    2. BER Eve (deve aumentar com GB↑, aproximar de 50%)
    3. Taxa de bits (deve diminuir com GB↑)
    4. Percentual de bits descartados
    
    Args:
        guard_bands: Lista de valores de guard-band (em múltiplos de σ)
        snr_db: SNR fixo para teste (cenário bom)
        correlacao_alice_bob: Correlação temporal legítima
        correlacao_alice_eve: Correlação espacial com Eve (tipicamente ~0)
    """
    
    print("\n" + "="*80)
    print("EXPERIMENTO 7: IMPACTO DO GUARD-BAND")
    print("="*80)
    print(f"\nParâmetros:")
    print(f"  SNR fixo: {snr_db} dB (cenário bom)")
    print(f"  Correlação Alice-Bob: {correlacao_alice_bob}")
    print(f"  Correlação Alice-Eve: {correlacao_alice_eve}")
    print(f"  Erro estimativa canal: {erro_estimativa*100:.1f}%")
    print(f"  Guard-bands testados: {guard_bands}")
    print(f"  Testes por GB: {quantidade_de_testes}")
    print("="*80 + "\n")
    
    # Gerar palavra código e BCH
    palavra_codigo = np.random.randint(2, size=tamanho_cadeia_bits)
    bch_codigo = gerar_tabela_codigos_bch(tamanho_cadeia_bits, 64)
    
    # Calcular variância de ruído a partir do SNR
    variancia_ruido = 10 ** (-snr_db / 10)
    media_ruido = 0.0
    
    # Armazenar resultados
    resultados = {
        'guard_band': [],
        'kdr_bob': [],
        'ber_bob': [],
        'ber_eve_raw': [],
        'ber_eve_pos_bch': [],
        'taxa_bits_bps': [],
        'percentual_descartado': [],
        'corr_h_bob': [],
        'corr_h_eve': []
    }
    
    print("Testando guard-bands:")
    for gb in tqdm(guard_bands, desc="Guard-band"):
        
        # ===== TESTE ALICE-BOB (LEGÍTIMO) =====
        ber_bob, kdr_bob = extrair_kdr(
            palavra_codigo=palavra_codigo,
            rayleigh_param=rayleigh_param,
            tamanho_cadeia_bits=tamanho_cadeia_bits,
            quantidade_de_testes=quantidade_de_testes,
            variancia_ruido=variancia_ruido,
            media_ruido=media_ruido,
            bch_codigo=bch_codigo,
            correlacao_canal=correlacao_alice_bob,
            modulacao=modulacao,
            erro_estimativa=erro_estimativa,
            guard_band_sigma=gb,
            usar_amplificacao=False
        )
        
        # ===== TESTE SEGURANÇA (EVE) =====
        kdr_bob_eve, ber_eve_raw, ber_eve_pos_bch, corr_h_bob, corr_h_eve = medir_seguranca_eve(
            palavra_codigo=palavra_codigo,
            rayleigh_param=rayleigh_param,
            tamanho_cadeia_bits=tamanho_cadeia_bits,
            quantidade_de_testes=quantidade_de_testes,
            variancia_ruido=variancia_ruido,
            media_ruido=media_ruido,
            bch_codigo=bch_codigo,
            correlacao_alice_bob=correlacao_alice_bob,
            correlacao_alice_eve=correlacao_alice_eve,
            modulacao=modulacao,
            erro_estimativa=erro_estimativa,
            guard_band_sigma=gb
        )
        
        # ===== CALCULAR TAXA DE BITS =====
        # Taxa = (bits_aproveitados / tempo_geração)
        # Assumindo tempo fixo, taxa ∝ bits_aproveitados
        # Guard-band descarta ~GB × 100% dos bits
        # Aproximação: bits_aproveitados = n_bch × (1 - fator_descarte_gb)
        
        # Estimativa de descarte por guard-band (baseado em distribuição Rayleigh)
        # GB=0.0 → 0% descarte
        # GB=0.5 → ~30% descarte
        # GB=1.0 → ~50% descarte
        # Função empírica: descarte ≈ 1 - exp(-0.7 × GB)
        percentual_descartado = (1 - np.exp(-0.7 * gb)) * 100
        
        # Taxa relativa (normalizada por GB=0)
        bits_aproveitados = tamanho_cadeia_bits * (1 - percentual_descartado/100)
        # Assumindo 1000 testes/segundo (arbitrário para comparação)
        taxa_bits_bps = bits_aproveitados * 1000
        
        # Armazenar
        resultados['guard_band'].append(gb)
        resultados['kdr_bob'].append(kdr_bob)
        resultados['ber_bob'].append(ber_bob)
        resultados['ber_eve_raw'].append(ber_eve_raw)
        resultados['ber_eve_pos_bch'].append(ber_eve_pos_bch)
        resultados['taxa_bits_bps'].append(taxa_bits_bps)
        resultados['percentual_descartado'].append(percentual_descartado)
        resultados['corr_h_bob'].append(corr_h_bob)
        resultados['corr_h_eve'].append(corr_h_eve)
        
        print(f"\n  GB={gb:.1f}σ:")
        print(f"    KDR Bob: {kdr_bob:.2f}%")
        print(f"    BER Eve (raw): {ber_eve_raw:.2f}%")
        print(f"    Taxa bits: {taxa_bits_bps:.0f} bps")
        print(f"    Descarte: {percentual_descartado:.1f}%")
    
    # ===== SALVAR RESULTADOS =====
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # CSV
    dados_csv = []
    for i in range(len(guard_bands)):
        dados_csv.append({
            'guard_band_sigma': resultados['guard_band'][i],
            'kdr_bob': resultados['kdr_bob'][i],
            'ber_bob': resultados['ber_bob'][i],
            'ber_eve_raw': resultados['ber_eve_raw'][i],
            'ber_eve_pos_bch': resultados['ber_eve_pos_bch'][i],
            'taxa_bits_bps': resultados['taxa_bits_bps'][i],
            'percentual_descartado': resultados['percentual_descartado'][i],
            'correlacao_h_bob': resultados['corr_h_bob'][i],
            'correlacao_h_eve': resultados['corr_h_eve'][i]
        })
    
    colunas_csv = ['guard_band_sigma', 'kdr_bob', 'ber_bob', 'ber_eve_raw', 
                   'ber_eve_pos_bch', 'taxa_bits_bps', 'percentual_descartado',
                   'correlacao_h_bob', 'correlacao_h_eve']
    
    salvar_resultado_csv(
        dados_csv,
        "exp07_impacto_guard_band",
        colunas_csv
    )
    
    # JSON com metadados
    dados_json = {
        'experimento': 'exp07_impacto_guard_band',
        'timestamp': timestamp,
        'parametros': {
            'snr_db': snr_db,
            'correlacao_alice_bob': correlacao_alice_bob,
            'correlacao_alice_eve': correlacao_alice_eve,
            'erro_estimativa': erro_estimativa,
            'guard_bands': guard_bands,
            'quantidade_de_testes': quantidade_de_testes,
            'tamanho_cadeia_bits': tamanho_cadeia_bits
        },
        'resultados': resultados
    }
    
    salvar_resultado_json(
        dados_json,
        "exp07_impacto_guard_band"
    )
    
    # ===== GRÁFICOS =====
    criar_graficos_guard_band(resultados, timestamp)
    
    # ===== SUMÁRIO =====
    print("\n" + "="*80)
    print("SUMÁRIO DOS RESULTADOS")
    print("="*80 + "\n")
    
    print(f"{'GB (σ)':<8} {'KDR Bob':<12} {'BER Eve':<12} {'Taxa (bps)':<12} {'Descarte':<10}")
    print("-"*80)
    for i, gb in enumerate(guard_bands):
        print(f"{gb:<8.1f} {resultados['kdr_bob'][i]:<12.2f} "
              f"{resultados['ber_eve_raw'][i]:<12.2f} "
              f"{resultados['taxa_bits_bps'][i]:<12.0f} "
              f"{resultados['percentual_descartado'][i]:<10.1f}%")
    
    print("\n" + "="*80)
    print("RECOMENDAÇÃO:")
    # Encontrar sweet spot: KDR<1% E BER_Eve>49%
    for i, gb in enumerate(guard_bands):
        if resultados['kdr_bob'][i] < 1.0 and resultados['ber_eve_raw'][i] > 49.0:
            print(f"  GB={gb:.1f}σ → KDR={resultados['kdr_bob'][i]:.2f}%, "
                  f"BER_Eve={resultados['ber_eve_raw'][i]:.2f}%, "
                  f"Taxa={resultados['taxa_bits_bps'][i]:.0f} bps")
            print("  [OK] Bom equilíbrio segurança vs eficiência")
            break
    print("="*80 + "\n")
    
    return resultados, dados_json


def criar_graficos_guard_band(resultados, timestamp):
    """
    Cria gráficos de 3 painéis mostrando impacto do guard-band
    """
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    gb_vals = resultados['guard_band']
    
    # ===== GRÁFICO 1: KDR Alice-Bob vs Guard-Band =====
    axes[0].plot(gb_vals, resultados['kdr_bob'], 'o-', 
                 color='blue', linewidth=2, markersize=8, label='KDR Bob')
    axes[0].axhline(y=1.0, color='red', linestyle='--', linewidth=1.5, 
                    label='Limiar 1% (aceitável)')
    axes[0].set_xlabel('Guard-Band (× σ)', fontsize=12)
    axes[0].set_ylabel('KDR Bob (%)', fontsize=12)
    axes[0].set_title('(a) KDR Alice-Bob (menor = melhor)', fontsize=13, fontweight='bold')
    axes[0].legend(fontsize=10)
    axes[0].grid(True, alpha=0.3)
    
    # ===== GRÁFICO 2: BER Eve vs Guard-Band =====
    axes[1].plot(gb_vals, resultados['ber_eve_raw'], 's-', 
                 color='red', linewidth=2, markersize=8, label='BER Eve (raw)')
    axes[1].plot(gb_vals, resultados['ber_eve_pos_bch'], '^-', 
                 color='orange', linewidth=2, markersize=8, label='BER Eve (pós-BCH)')
    axes[1].axhline(y=50.0, color='green', linestyle='--', linewidth=1.5, 
                    label='50% (chute aleatório)')
    axes[1].set_xlabel('Guard-Band (× σ)', fontsize=12)
    axes[1].set_ylabel('BER Eve (%)', fontsize=12)
    axes[1].set_title('(b) Segurança contra Eve', fontsize=13, fontweight='bold')
    axes[1].legend(fontsize=10)
    axes[1].grid(True, alpha=0.3)
    axes[1].set_ylim([45, 55])
    
    # ===== GRÁFICO 3: Taxa de Bits vs Guard-Band =====
    axes[2].plot(gb_vals, resultados['taxa_bits_bps'], 'D-', 
                 color='purple', linewidth=2, markersize=8, label='Taxa de chaves')
    axes[2].fill_between(gb_vals, 0, resultados['percentual_descartado'], 
                         alpha=0.3, color='gray', label='Bits descartados')
    axes[2].set_xlabel('Guard-Band (× σ)', fontsize=12)
    axes[2].set_ylabel('Taxa (bits/s)', fontsize=12)
    axes[2].set_title('(c) Eficiência do Sistema', fontsize=13, fontweight='bold')
    axes[2].legend(fontsize=10)
    axes[2].grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Salvar
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filepath = os.path.join(base_dir, "resultados", "figuras", 
                           f"exp07_impacto_guard_band_{timestamp}.png")
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    print(f"\n[OK] Grafico salvo: {filepath}")
    plt.close()


if __name__ == "__main__":
    resultados, metadados = experimento_impacto_guard_band(
        quantidade_de_testes=1000,
        guard_bands=[0.0, 0.1, 0.3, 0.5, 0.7, 1.0],
        snr_db=15.0,
        correlacao_alice_bob=0.95,
        correlacao_alice_eve=0.0,
        erro_estimativa=0.15
    )
    
    print("\n[OK] Experimento 7 concluido com sucesso!\n")
