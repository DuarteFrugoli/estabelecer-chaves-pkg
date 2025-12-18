"""
Experimento 6: Análise de Complexidade Computacional
Mede o tempo de execução real dos códigos BCH para discussão de viabilidade
"""

import sys
import os
import numpy as np
import random
import time

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.codigos_corretores.bch import gerar_tabela_codigos_bch, codificar_bch, decodificar_bch
from experimentos.util_experimentos import salvar_resultado_json, salvar_resultado_csv


def medir_tempo_bch(n, k, repeticoes=1000):
    """
    Mede tempo de codificação e decodificação BCH
    
    Args:
        n: Comprimento do código
        k: Bits de informação
        repeticoes: Número de repetições para média
    
    Returns:
        Dicionário com tempos médios em milissegundos
    """
    bch = gerar_tabela_codigos_bch(n, k)
    
    # Testa codificação
    tempos_encode = []
    for _ in range(repeticoes):
        bits_info = [random.randint(0, 1) for _ in range(k)]
        
        inicio = time.perf_counter()
        codigo = codificar_bch(bch, bits_info)
        fim = time.perf_counter()
        
        tempos_encode.append((fim - inicio) * 1000)  # ms
    
    # Testa decodificação (sem erros)
    tempos_decode_limpo = []
    for _ in range(repeticoes):
        bits_info = [random.randint(0, 1) for _ in range(k)]
        codigo = codificar_bch(bch, bits_info)
        
        inicio = time.perf_counter()
        decodificado = decodificar_bch(bch, codigo)
        fim = time.perf_counter()
        
        tempos_decode_limpo.append((fim - inicio) * 1000)
    
    # Testa decodificação (com erros)
    capacidades = {7: 1, 15: 2, 127: 10, 255: 15}
    t = capacidades.get(n, 1)
    
    tempos_decode_erros = []
    for _ in range(repeticoes):
        bits_info = [random.randint(0, 1) for _ in range(k)]
        codigo = codificar_bch(bch, bits_info)
        
        # Introduz erros (até t erros)
        codigo_corrompido = codigo.copy()
        num_erros = min(t, n)  # Não excede capacidade
        posicoes_erro = random.sample(range(n), num_erros)
        for pos in posicoes_erro:
            codigo_corrompido[pos] = 1 - codigo_corrompido[pos]
        
        inicio = time.perf_counter()
        decodificado = decodificar_bch(bch, codigo_corrompido)
        fim = time.perf_counter()
        
        tempos_decode_erros.append((fim - inicio) * 1000)
    
    return {
        'encode_media': np.mean(tempos_encode),
        'encode_std': np.std(tempos_encode),
        'decode_limpo_media': np.mean(tempos_decode_limpo),
        'decode_limpo_std': np.std(tempos_decode_limpo),
        'decode_erros_media': np.mean(tempos_decode_erros),
        'decode_erros_std': np.std(tempos_decode_erros),
        'total_media': np.mean(tempos_encode) + np.mean(tempos_decode_erros)
    }


def experimento_analise_complexidade(
    codigos_bch=[(7, 4), (15, 7), (127, 64), (255, 139)],
    repeticoes=1000
):
    """
    Experimento: Análise de complexidade computacional dos códigos BCH
    
    Args:
        codigos_bch: Lista com tuplas (n, k) dos códigos BCH
        repeticoes: Número de repetições para média
    """
    
    print("\n" + "="*70)
    print("EXPERIMENTO 6: ANÁLISE DE COMPLEXIDADE COMPUTACIONAL")
    print("="*70)
    print(f"Códigos BCH: {codigos_bch}")
    print(f"Repetições por código: {repeticoes}")
    print("="*70 + "\n")
    
    capacidades = {7: 1, 15: 2, 127: 10, 255: 15}
    resultados = {}
    
    for n, k in codigos_bch:
        t = capacidades[n]
        print(f"\n--- Testando BCH({n},{k}) - t={t} ---")
        
        tempos = medir_tempo_bch(n, k, repeticoes)
        
        resultados[f"BCH({n},{k})"] = {
            'n': n,
            'k': k,
            't': t,
            'taxa_codigo': k/n,
            'tempos': tempos
        }
        
        print(f"  Codificação: {tempos['encode_media']:.6f} ms (±{tempos['encode_std']:.6f})")
        print(f"  Decodificação (sem erros): {tempos['decode_limpo_media']:.6f} ms (±{tempos['decode_limpo_std']:.6f})")
        print(f"  Decodificação (com erros): {tempos['decode_erros_media']:.6f} ms (±{tempos['decode_erros_std']:.6f})")
        print(f"  Total (encode + decode c/ erros): {tempos['total_media']:.6f} ms")
    
    # Prepara dados para salvar
    dados = {
        'parametros': {
            'codigos_bch': codigos_bch,
            'repeticoes': repeticoes
        },
        'resultados': resultados
    }
    
    # Salva JSON
    salvar_resultado_json(dados, "exp06_analise_complexidade",
                         descricao="Análise de tempo de execução dos códigos BCH")
    
    # Salva CSV
    csv_dados = []
    for codigo_str, info in resultados.items():
        csv_dados.append({
            'Codigo': codigo_str,
            'n': info['n'],
            'k': info['k'],
            't': info['t'],
            'Taxa': f"{info['taxa_codigo']:.3f}",
            'Encode_ms': f"{info['tempos']['encode_media']:.6f}",
            'Decode_limpo_ms': f"{info['tempos']['decode_limpo_media']:.6f}",
            'Decode_erros_ms': f"{info['tempos']['decode_erros_media']:.6f}",
            'Total_ms': f"{info['tempos']['total_media']:.6f}"
        })
    
    salvar_resultado_csv(csv_dados, "exp06_analise_complexidade",
                        ['Codigo', 'n', 'k', 't', 'Taxa', 'Encode_ms', 
                         'Decode_limpo_ms', 'Decode_erros_ms', 'Total_ms'])
    
    # Cria gráfico comparativo
    import matplotlib.pyplot as plt
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle('Análise de Complexidade Computacional dos Códigos BCH',
                fontsize=14, fontweight='bold')
    
    codigos_labels = list(resultados.keys())
    tempos_encode = [resultados[c]['tempos']['encode_media'] for c in codigos_labels]
    tempos_decode = [resultados[c]['tempos']['decode_erros_media'] for c in codigos_labels]
    tempos_total = [resultados[c]['tempos']['total_media'] for c in codigos_labels]
    
    # Gráfico 1: Tempos individuais
    x = np.arange(len(codigos_labels))
    width = 0.35
    
    ax1.bar(x - width/2, tempos_encode, width, label='Codificação', color='skyblue')
    ax1.bar(x + width/2, tempos_decode, width, label='Decodificação (c/ erros)', color='salmon')
    
    ax1.set_xlabel('Código BCH')
    ax1.set_ylabel('Tempo (ms)')
    ax1.set_title('Tempo de Codificação vs Decodificação')
    ax1.set_xticks(x)
    ax1.set_xticklabels(codigos_labels, rotation=15)
    ax1.legend()
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Gráfico 2: Tempo total e escalabilidade
    ax2.plot(codigos_labels, tempos_total, marker='o', linewidth=2, 
            markersize=8, color='green')
    ax2.set_xlabel('Código BCH')
    ax2.set_ylabel('Tempo Total (ms)')
    ax2.set_title('Tempo Total (Codificação + Decodificação)')
    ax2.set_xticklabels(codigos_labels, rotation=15)
    ax2.grid(True, alpha=0.3)
    
    # Adiciona linha de limite IoT (exemplo: 10ms)
    ax2.axhline(y=10, color='red', linestyle='--', linewidth=1, label='Limite IoT (~10ms)')
    ax2.legend()
    
    plt.tight_layout()
    
    from experimentos.util_experimentos import salvar_grafico
    salvar_grafico(fig, "exp06_analise_complexidade")
    plt.close()
    
    # Análise de viabilidade
    print("\n" + "="*70)
    print("ANÁLISE DE VIABILIDADE")
    print("="*70)
    
    limite_iot_basico = 10.0  # ms
    limite_iot_industrial = 50.0  # ms
    
    for codigo_str, info in resultados.items():
        tempo_total = info['tempos']['total_media']
        
        print(f"\n{codigo_str}:")
        print(f"  Tempo total: {tempo_total:.3f} ms")
        
        if tempo_total < limite_iot_basico:
            print(f"  ✅ Viável para IoT básico (< {limite_iot_basico} ms)")
        elif tempo_total < limite_iot_industrial:
            print(f"  ⚠️ Viável para IoT industrial (< {limite_iot_industrial} ms)")
        else:
            print(f"  ❌ Apenas para dispositivos móveis/5G (> {limite_iot_industrial} ms)")
    
    print("\n✓ Experimento 6 concluído com sucesso!\n")
    
    return dados


if __name__ == "__main__":
    # Executa experimento
    resultados = experimento_analise_complexidade(
        codigos_bch=[(7, 4), (15, 7), (127, 64), (255, 139)],
        repeticoes=1000
    )
