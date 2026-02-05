"""
Experimento 6: Análise de Segurança contra Espionagem (Eve)
Testa descorrelação espacial e temporal entre Alice-Bob vs Alice-Eve
"""

import sys
import os
import numpy as np
import random
import matplotlib.pyplot as plt
from tqdm import tqdm
from datetime import datetime
from scipy.special import j0

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.codigos_corretores.bch import gerar_tabela_codigos_bch, get_tamanho_bits_informacao
from src.canal.canal import extrair_kdr, medir_seguranca_eve
from src.util.config_dispositivos import obter_parametros_dispositivo
from experimentos.util_experimentos import (
    salvar_resultado_json,
    salvar_resultado_csv
)


def calcular_correlacao_espacial(distancia_separacao_m, comprimento_onda_m):
    """
    Calcula correlação espacial baseada no modelo de Clarke
    
    Aproximação: ρ ≈ J0(2π × d / λ)
    Para simplificação: ρ ≈ exp(-2 × d / λ) para d > λ/2
    
    Args:
        distancia_separacao_m: Distância lateral entre Alice-Bob e Alice-Eve
        comprimento_onda_m: Comprimento de onda da portadora
    
    Returns:
        Correlação espacial (0 a 1)
    """
    # Normalizar pela meia onda
    d_normalizado = distancia_separacao_m / (comprimento_onda_m / 2)
    
    # Modelo simplificado de descorrelação espacial
    if d_normalizado < 0.5:
        # Muito próximo: correlação alta
        rho = 1.0 - 0.3 * d_normalizado
    elif d_normalizado < 2.0:
        # Região de transição
        rho = 0.85 - 0.4 * d_normalizado
    else:
        # Longe: descorrelacionado
        rho = 0.1 * np.exp(-0.5 * d_normalizado)
    
    return max(0.0, min(1.0, rho))


def calcular_correlacao_temporal(atraso_ms, freq_doppler_hz):
    """
    Calcula correlação temporal usando modelo de Jakes
    
    ρ(Δt) = J0(2π × fD × Δt)
    
    Args:
        atraso_ms: Atraso entre medições (ms)
        freq_doppler_hz: Frequência Doppler (Hz)
    
    Returns:
        Correlação temporal (0 a 1)
    """
    if freq_doppler_hz == 0:
        return 1.0
    
    atraso_s = atraso_ms / 1000.0
    argumento = 2 * np.pi * freq_doppler_hz * atraso_s
    
    # Função de Bessel J0 (scipy.special)
    rho_temporal = float(j0(argumento))
    
    return max(0.0, min(1.0, abs(rho_temporal)))


def experimento_eve_espacial(
    tamanho_cadeia_bits=127,
    quantidade_de_testes=1000,
    distancia_alice_bob_m=10,
    distancias_eve_m=[0.1, 0.2, 0.5, 1.0, 2.0, 5.0, 10.0],
    snr_db=9,
    perfil_dispositivo='pessoa_andando',
    rayleigh_param=1.0/np.sqrt(2),
    modulacao='bpsk'
):
    """
    Experimento: Descorrelação espacial de Eve
    
    Fixa Alice-Bob em 10m e varia distância lateral de Eve
    Mostra que Eve a poucos centímetros já tem correlação baixa
    """
    
    print("\n" + "="*80)
    print("EXPERIMENTO 9A: DESCORRELAÇÃO ESPACIAL DE EVE")
    print("="*80)
    print(f"Distância Alice-Bob: {distancia_alice_bob_m}m")
    print(f"Distâncias Eve (lateral): {distancias_eve_m} m")
    print(f"SNR: {snr_db} dB")
    print(f"Perfil: {perfil_dispositivo}")
    print(f"Testes: {quantidade_de_testes}")
    print("="*80 + "\n")
    
    # Configuração do dispositivo
    config = obter_parametros_dispositivo(perfil_dispositivo)
    frequencia_hz = config['frequencia_portadora_hz']
    velocidade_kmh = config['velocidade_max_kmh']
    erro_estimativa = config['erro_estimativa_canal']
    guard_band_sigma = config['guard_band_sigma']
    
    # Parâmetros de canal
    velocidade_ms = velocidade_kmh / 3.6
    comprimento_onda = 3e8 / frequencia_hz
    freq_doppler_hz = velocidade_ms / comprimento_onda
    
    # Correlação temporal Alice-Bob (mesmo instante, Δt=0)
    correlacao_alice_bob = 0.95  # Alta correlação (reciprocidade)
    
    print(f"Parametros:")
    print(f"  Frequencia: {frequencia_hz/1e9:.2f} GHz")
    print(f"  Comprimento onda (lambda): {comprimento_onda*100:.1f} cm")
    print(f"  lambda/2: {comprimento_onda*50:.1f} cm")
    print(f"  Velocidade: {velocidade_kmh} km/h")
    print(f"  Doppler: {freq_doppler_hz:.2f} Hz")
    print(f"  Correlacao Alice-Bob: {correlacao_alice_bob:.3f}\n")
    
    # Configuração BCH
    random.seed(42)
    palavra_codigo = [random.randint(0, 1) for _ in range(tamanho_cadeia_bits)]
    tamanho_bits_informacao = get_tamanho_bits_informacao(tamanho_cadeia_bits)
    bch_codigo = gerar_tabela_codigos_bch(tamanho_cadeia_bits, tamanho_bits_informacao)
    
    # SNR
    snr_linear = 10 ** (snr_db / 10)
    potencia_sinal = 1.0
    variancia_ruido = potencia_sinal / (2 * snr_linear)
    media_ruido = 0.0
    
    # Armazenar resultados
    resultados = {
        'distancia_eve_m': [],
        'separacao_lambda_2': [],
        'correlacao_espacial': [],
        'correlacao_alice_eve': [],
        'kdr_bob': [],
        'correlacao_h_alice_bob': [],  # Correlação coeficientes h (análogo ao CSI de Yuan et al.)
        'correlacao_h_alice_eve': []   # Correlação coeficientes h (análogo ao CSI de Yuan et al.)
    }
    
    # Teste Alice-Bob primeiro (referência de KDR legítimo)
    print("Testando Alice-Bob (referência)...")
    ber_bob, kdr_bob_valor = extrair_kdr(
        palavra_codigo=palavra_codigo,
        rayleigh_param=rayleigh_param,
        tamanho_cadeia_bits=tamanho_cadeia_bits,
        quantidade_de_testes=quantidade_de_testes,
        variancia_ruido=variancia_ruido,
        media_ruido=media_ruido,
        bch_codigo=bch_codigo,
        correlacao_canal=correlacao_alice_bob,
        usar_amplificacao=False,
        modulacao=modulacao,
        erro_estimativa=erro_estimativa,
        guard_band_sigma=guard_band_sigma
    )
    
    print(f"[OK] BER Bob: {ber_bob*100:.2f}%")
    print(f"[OK] KDR Bob (pós-BCH): {kdr_bob_valor*100:.2f}%\n")
    
    # Loop sobre distâncias de Eve
    for dist_eve in tqdm(distancias_eve_m, desc="Testando distâncias de Eve"):
        # Calcular correlação espacial Alice-Eve
        rho_espacial = calcular_correlacao_espacial(dist_eve, comprimento_onda)
        
        # Separação em unidades de λ/2
        separacao_lambda_2 = dist_eve / (comprimento_onda / 2)
        
        # Medir correlação de coeficientes h (método Yuan et al.)
        kdr_bob_interno, ber_eve_raw, ber_eve_pos_bch, corr_h_bob, corr_h_eve = medir_seguranca_eve(
            palavra_codigo=palavra_codigo,
            rayleigh_param=rayleigh_param,
            tamanho_cadeia_bits=tamanho_cadeia_bits,
            quantidade_de_testes=quantidade_de_testes,
            variancia_ruido=variancia_ruido,
            media_ruido=media_ruido,
            bch_codigo=bch_codigo,
            correlacao_alice_bob=correlacao_alice_bob,
            correlacao_alice_eve=rho_espacial,
            modulacao=modulacao,
            erro_estimativa=erro_estimativa,
            guard_band_sigma=guard_band_sigma
        )
        
        # Armazenar
        resultados['distancia_eve_m'].append(dist_eve)
        resultados['separacao_lambda_2'].append(separacao_lambda_2)
        resultados['correlacao_espacial'].append(rho_espacial)
        resultados['correlacao_alice_eve'].append(rho_espacial)
        resultados['kdr_bob'].append(kdr_bob_interno)
        resultados['correlacao_h_alice_bob'].append(corr_h_bob)
        resultados['correlacao_h_alice_eve'].append(corr_h_eve)
        
        print(f"  {dist_eve:5.2f}m ({separacao_lambda_2:5.1f}x lambda/2): "
              f"rho_espacial={rho_espacial:.3f}, "
              f"rho_h(A,E)={corr_h_eve:.3f}")
    
    return resultados, kdr_bob_valor, comprimento_onda


def experimento_eve_temporal(
    tamanho_cadeia_bits=127,
    quantidade_de_testes=1000,
    distancia_eve_m=0.5,
    atrasos_ms=[0, 0.1, 0.5, 1.0, 2.0, 5.0, 10.0],
    snr_db=9,
    perfil_dispositivo='pessoa_andando',
    rayleigh_param=1.0/np.sqrt(2),
    modulacao='bpsk'
):
    """
    Experimento: Descorrelação temporal de Eve
    
    Fixa Eve a 50cm e varia dessincronização temporal
    Mostra que mesmo sincronizada, correlação espacial garante segurança
    """
    
    print("\n" + "="*80)
    print("EXPERIMENTO 9B: DESCORRELAÇÃO TEMPORAL DE EVE")
    print("="*80)
    print(f"Distância Eve (fixa): {distancia_eve_m}m")
    print(f"Atrasos de Eve: {atrasos_ms} ms")
    print(f"SNR: {snr_db} dB")
    print(f"Perfil: {perfil_dispositivo}")
    print("="*80 + "\n")
    
    # Configuração
    config = obter_parametros_dispositivo(perfil_dispositivo)
    frequencia_hz = config['frequencia_portadora_hz']
    velocidade_kmh = config['velocidade_max_kmh']
    erro_estimativa = config['erro_estimativa_canal']
    guard_band_sigma = config['guard_band_sigma']
    
    velocidade_ms = velocidade_kmh / 3.6
    comprimento_onda = 3e8 / frequencia_hz
    freq_doppler_hz = velocidade_ms / comprimento_onda
    
    # Correlação espacial fixa
    rho_espacial = calcular_correlacao_espacial(distancia_eve_m, comprimento_onda)
    
    # Correlação temporal Alice-Bob (referência, assumindo sincronização de 1ms típica)
    correlacao_alice_bob = calcular_correlacao_temporal(1.0, freq_doppler_hz)
    
    print(f"Parâmetros:")
    print(f"  Frequência: {frequencia_hz/1e9:.2f} GHz")
    print(f"  Doppler: {freq_doppler_hz:.2f} Hz")
    print(f"  Correlação espacial Eve (fixa): {rho_espacial:.3f}")
    print(f"  Correlação temporal Alice-Bob: {correlacao_alice_bob:.3f}\n")
    
    # BCH
    random.seed(42)
    palavra_codigo = [random.randint(0, 1) for _ in range(tamanho_cadeia_bits)]
    tamanho_bits_informacao = get_tamanho_bits_informacao(tamanho_cadeia_bits)
    bch_codigo = gerar_tabela_codigos_bch(tamanho_cadeia_bits, tamanho_bits_informacao)
    
    # SNR
    snr_linear = 10 ** (snr_db / 10)
    potencia_sinal = 1.0
    variancia_ruido = potencia_sinal / (2 * snr_linear)
    media_ruido = 0.0
    
    # Resultados
    resultados = {
        'atraso_ms': [],
        'correlacao_temporal': [],
        'correlacao_total': [],
        'kdr_bob': [],
        'correlacao_h_alice_bob': [],
        'correlacao_h_alice_eve': []
    }
    
    # Loop sobre atrasos
    for atraso in tqdm(atrasos_ms, desc="Testando atrasos"):
        # Correlação temporal de Eve (dessincronização)
        rho_temporal_eve = calcular_correlacao_temporal(atraso, freq_doppler_hz)
        
        # Correlação total Alice-Eve = espacial × temporal
        correlacao_alice_eve = rho_espacial * rho_temporal_eve
        
        # Medir correlação de coeficientes h (método Yuan et al.)
        kdr_bob_interno, ber_eve_raw, ber_eve_pos_bch, corr_h_bob, corr_h_eve = medir_seguranca_eve(
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
            guard_band_sigma=guard_band_sigma
        )
        
        resultados['atraso_ms'].append(atraso)
        resultados['correlacao_temporal'].append(rho_temporal_eve)
        resultados['correlacao_total'].append(correlacao_alice_eve)
        resultados['kdr_bob'].append(kdr_bob_interno)
        resultados['correlacao_h_alice_bob'].append(corr_h_bob)
        resultados['correlacao_h_alice_eve'].append(corr_h_eve)
        
        print(f"  {atraso:5.1f}ms: rho_temp={rho_temporal_eve:.3f}, "
              f"rho_total={correlacao_alice_eve:.3f}, "
              f"rho_h(A,E)={corr_h_eve:.3f}")
    
    return resultados


def criar_graficos(resultados_espacial, resultados_temporal, kdr_bob, lambda_cm, timestamp):
    """
    Cria dois gráficos: espacial e temporal (correlação de coeficientes h)
    """
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # ===== GRÁFICO 1: Correlação h vs Distância de Eve =====
    ax1.plot(resultados_espacial['distancia_eve_m'], 
             resultados_espacial['correlacao_h_alice_eve'],
             'o-', color='red', linewidth=2, markersize=8,
             label='ρ(h_Alice, h_Eve)')
    
    # Linha de referência Bob
    if len(resultados_espacial['correlacao_h_alice_bob']) > 0:
        corr_bob = resultados_espacial['correlacao_h_alice_bob'][0]
        ax1.axhline(y=corr_bob, color='green', linestyle='--', linewidth=2,
                    label=f'ρ(h_Alice, h_Bob) = {corr_bob:.3f}')
    
    ax1.set_xlabel('Distância Eve de Alice (m)', fontsize=12)
    ax1.set_ylabel('Correlação de coeficientes h', fontsize=12)
    ax1.set_title('Descorrelação Espacial (método Yuan et al.)', fontsize=13, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.legend(fontsize=10)
    ax1.set_ylim([-0.1, 1.0])
    
    # Adicionar linha vertical em λ/2
    lambda_2_m = lambda_cm / 100 / 2
    ax1.axvline(x=lambda_2_m, color='blue', linestyle=':', alpha=0.5,
                label=f'λ/2 = {lambda_cm/2:.1f}cm')
    
    # ===== GRÁFICO 2: Correlação h vs Atraso de Eve =====
    ax2.plot(resultados_temporal['atraso_ms'],
             resultados_temporal['correlacao_h_alice_eve'],
             's-', color='orange', linewidth=2, markersize=8,
             label='ρ(h_Alice, h_Eve) dessincronizada')
    
    # Linha de referência Bob
    if len(resultados_temporal['correlacao_h_alice_bob']) > 0:
        corr_bob_temp = resultados_temporal['correlacao_h_alice_bob'][0]
        ax2.axhline(y=corr_bob_temp, color='green', linestyle='--', linewidth=2,
                    label=f'ρ(h_Alice, h_Bob) = {corr_bob_temp:.3f}')
    
    ax2.set_xlabel('Atraso de medição (ms)', fontsize=12)
    ax2.set_ylabel('Correlação de coeficientes h', fontsize=12)
    ax2.set_title('Descorrelação Temporal: Impacto da Dessincronização', fontsize=13, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.legend(fontsize=10)
    ax2.set_ylim([0, 55])
    
    plt.tight_layout()
    
    # Salvar
    caminho_figura = os.path.join('resultados', 'figuras', f'exp06_analise_eve_{timestamp}.png')
    os.makedirs(os.path.dirname(caminho_figura), exist_ok=True)
    plt.savefig(caminho_figura, dpi=300, bbox_inches='tight')
    print(f"\n[OK] Grafico salvo: {caminho_figura}")
    
    plt.close()


if __name__ == "__main__":
    print("\n" + "="*80)
    print("SUITE DE EXPERIMENTOS: ANÁLISE DE SEGURANÇA CONTRA EVE")
    print("="*80)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # ===== EXPERIMENTO 9A: ESPACIAL =====
    resultados_espacial, kdr_bob, lambda_m = experimento_eve_espacial(
        tamanho_cadeia_bits=127,
        quantidade_de_testes=1000,
        distancia_alice_bob_m=10,
        distancias_eve_m=[0.1, 0.2, 0.5, 1.0, 2.0, 5.0, 10.0],
        snr_db=9,
        perfil_dispositivo='pessoa_andando'
    )
    
    # ===== EXPERIMENTO 9B: TEMPORAL =====
    resultados_temporal = experimento_eve_temporal(
        tamanho_cadeia_bits=127,
        quantidade_de_testes=1000,
        distancia_eve_m=0.5,
        atrasos_ms=[0, 0.1, 0.5, 1.0, 2.0, 5.0, 10.0],
        snr_db=9,
        perfil_dispositivo='pessoa_andando'
    )
    
    # ===== SALVAR RESULTADOS =====
    print("\n" + "="*80)
    print("SALVANDO RESULTADOS")
    print("="*80)
    
    # Preparar dados CSV espacial
    csv_dados_espacial = []
    for i in range(len(resultados_espacial['distancia_eve_m'])):
        csv_dados_espacial.append({
            'distancia_eve_m': f"{resultados_espacial['distancia_eve_m'][i]:.2f}",
            'separacao_lambda_2': f"{resultados_espacial['separacao_lambda_2'][i]:.2f}",
            'correlacao_espacial': f"{resultados_espacial['correlacao_espacial'][i]:.4f}",
            'correlacao_alice_eve': f"{resultados_espacial['correlacao_alice_eve'][i]:.4f}",
            'kdr_bob': f"{resultados_espacial['kdr_bob'][i]:.2f}",
            'correlacao_h_alice_bob': f"{resultados_espacial['correlacao_h_alice_bob'][i]:.4f}",
            'correlacao_h_alice_eve': f"{resultados_espacial['correlacao_h_alice_eve'][i]:.4f}"
        })
    
    colunas_espacial = ['distancia_eve_m', 'separacao_lambda_2', 'correlacao_espacial', 
                        'correlacao_alice_eve', 'kdr_bob', 
                        'correlacao_h_alice_bob', 'correlacao_h_alice_eve']
    salvar_resultado_csv(
        csv_dados_espacial,
        f'exp06_eve_espacial_{timestamp}',
        colunas_espacial
    )
    
    # Preparar dados CSV temporal
    csv_dados_temporal = []
    for i in range(len(resultados_temporal['atraso_ms'])):
        csv_dados_temporal.append({
            'atraso_ms': f"{resultados_temporal['atraso_ms'][i]:.2f}",
            'correlacao_temporal': f"{resultados_temporal['correlacao_temporal'][i]:.4f}",
            'correlacao_total': f"{resultados_temporal['correlacao_total'][i]:.4f}",
            'kdr_bob': f"{resultados_temporal['kdr_bob'][i]:.2f}",
            'correlacao_h_alice_bob': f"{resultados_temporal['correlacao_h_alice_bob'][i]:.4f}",
            'correlacao_h_alice_eve': f"{resultados_temporal['correlacao_h_alice_eve'][i]:.4f}"
        })
    
    colunas_temporal = ['atraso_ms', 'correlacao_temporal', 'correlacao_total', 
                        'kdr_bob', 'correlacao_h_alice_bob', 'correlacao_h_alice_eve']
    salvar_resultado_csv(
        csv_dados_temporal,
        f'exp06_eve_temporal_{timestamp}',
        colunas_temporal
    )
    
    # JSON completo
    dados_completos = {
        'metadados': {
            'experimento': 'exp06_analise_eve',
            'timestamp': timestamp,
            'kdr_bob_referencia': kdr_bob,
            'lambda_cm': lambda_m * 100,
            'lambda_2_cm': lambda_m * 50
        },
        'espacial': resultados_espacial,
        'temporal': resultados_temporal
    }
    
    salvar_resultado_json(
        dados_completos,
        f'exp06_analise_eve_{timestamp}',
        'Análise de segurança contra espionagem (Eve)'
    )
    
    # Gráficos
    criar_graficos(resultados_espacial, resultados_temporal, kdr_bob, lambda_m * 100, timestamp)
    
    # ===== SUMÁRIO FINAL =====
    print("\n" + "="*80)
    print("SUMÁRIO DOS RESULTADOS")
    print("="*80)
    print(f"\n[>] KDR Bob (legitimo): {kdr_bob:.2f}%")
    print(f"\n[*] Correlacao h (metodo Yuan et al.):")
    print(f"  rho(h_Alice, h_Bob) = {resultados_espacial['correlacao_h_alice_bob'][0]:.4f}")
    print(f"  rho(h_Alice, h_Eve) a 10cm = {resultados_espacial['correlacao_h_alice_eve'][0]:.4f}")
    print(f"  rho(h_Alice, h_Eve) a 1m = {resultados_espacial['correlacao_h_alice_eve'][3]:.4f}")
    print(f"  rho(h_Alice, h_Eve) a 5m = {resultados_espacial['correlacao_h_alice_eve'][5]:.4f}")
    print(f"\n[i] Parametros: lambda/2 = {lambda_m*50:.1f}cm, SNR = 9 dB")
    print("="*80 + "\n")
