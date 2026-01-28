"""
Experimento 8: Variação de Distância (Alinhado com Artigo de Referência)
Testa o desempenho de PKG para diferentes distâncias entre dispositivos,
comparável aos cenários do artigo Yuan et al. (IEEE ICCC 2022)
"""

import sys
import os
import numpy as np
import random
from tqdm import tqdm
from datetime import datetime
from scipy.special import j0

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.codigos_corretores.bch import gerar_tabela_codigos_bch, get_tamanho_bits_informacao
from src.canal.canal import extrair_kdr
from src.util.config_dispositivos import obter_parametros_dispositivo
from experimentos.util_experimentos import (
    salvar_resultado_json,
    salvar_resultado_csv,
    criar_grafico_comparativo_kdr,
    imprimir_sumario_resultados
)


def calcular_path_loss_indoor(distancia_m, frequencia_hz, tipo='LOS'):
    """
    Calcula path loss para ambiente indoor
    
    Modelos:
    - LOS (Line-of-Sight): PL = 20*log10(f) + 20*log10(d) + 32.4
    - NLOS (Non-Line-of-Sight): PL = 20*log10(f) + 30*log10(d) + 32.4 + penetração
    
    Args:
        distancia_m: Distância em metros
        frequencia_hz: Frequência da portadora em Hz
        tipo: 'LOS' ou 'NLOS'
    
    Returns:
        Path loss em dB
    """
    frequencia_ghz = frequencia_hz / 1e9
    
    if tipo == 'LOS':
        # Free Space Path Loss (FSPL)
        pl_db = 20 * np.log10(frequencia_ghz) + 20 * np.log10(distancia_m) + 32.4
    else:  # NLOS
        # Modelo ITU Indoor com obstrução
        pl_db = 20 * np.log10(frequencia_ghz) + 30 * np.log10(distancia_m) + 32.4 + 10  # +10dB parede
    
    return pl_db


def calcular_snr_por_distancia(distancia_m, frequencia_hz, potencia_tx_dbm=14, 
                                 figura_ruido_db=7, tipo='LOS'):
    """
    Calcula SNR baseado na distância e parâmetros do sistema
    
    Args:
        distancia_m: Distância entre Alice e Bob
        frequencia_hz: Frequência da portadora
        potencia_tx_dbm: Potência de transmissão (dBm)
        figura_ruido_db: Figura de ruído do receptor
        tipo: 'LOS' ou 'NLOS'
    
    Returns:
        SNR em dB
    """
    # Path loss
    pl_db = calcular_path_loss_indoor(distancia_m, frequencia_hz, tipo)
    
    # Potência recebida
    potencia_rx_dbm = potencia_tx_dbm - pl_db
    
    # Ruído térmico: N = -174 + 10*log10(BW) + NF
    # BW típico WiFi: 20 MHz
    bandwidth_hz = 20e6
    ruido_termico_dbm = -174 + 10 * np.log10(bandwidth_hz) + figura_ruido_db
    
    # SNR = Potência Recebida - Ruído
    snr_db = potencia_rx_dbm - ruido_termico_dbm
    
    return snr_db


def experimento_variacao_distancia(
    tamanho_cadeia_bits=127,
    quantidade_de_testes=1000,
    rayleigh_param=1.0/np.sqrt(2),
    modulacao='bpsk',
    perfil_dispositivo='sensor_estatico',
    distancias_m=[1, 2, 3, 5, 10, 20, 50, 100],
    tipo_canal='LOS',
    potencia_tx_dbm=14,
    atraso_medicao_ms=1.0
):
    """
    Experimento: Desempenho de PKG variando distância entre dispositivos
    
    Cenários similares ao artigo de referência:
    - SS1, SS3: Static Sight (LOS) 1m, 3m
    - SNS1, SNS3: Static Non-Sight (NLOS) 1m, 3m
    - DS1, DS3: Dynamic Sight (LOS) 1m, 3m
    
    Args:
        tamanho_cadeia_bits: Tamanho do código BCH
        quantidade_de_testes: Número de testes Monte Carlo
        rayleigh_param: Parâmetro σ do Rayleigh
        modulacao: 'bpsk' ou 'qpsk'
        perfil_dispositivo: 'sensor_estatico', 'pessoa_andando', etc.
        distancias_m: Lista de distâncias a testar
        tipo_canal: 'LOS' ou 'NLOS'
        potencia_tx_dbm: Potência de transmissão em dBm
        atraso_medicao_ms: Atraso entre medições de Alice e Bob
    """
    
    print("\n" + "="*80)
    print("EXPERIMENTO 8: VARIAÇÃO DE DISTÂNCIA (ALINHADO COM ARTIGO)")
    print("="*80)
    print(f"Perfil: {perfil_dispositivo}")
    print(f"Tipo canal: {tipo_canal}")
    print(f"Distâncias: {distancias_m} metros")
    print(f"Potência TX: {potencia_tx_dbm} dBm")
    print(f"Tamanho código BCH: {tamanho_cadeia_bits}")
    print(f"Quantidade de testes: {quantidade_de_testes}")
    print(f"Parâmetro Rayleigh: {rayleigh_param:.6f}")
    print(f"Modulação: {modulacao.upper()}")
    print(f"Atraso medição: {atraso_medicao_ms} ms")
    print("="*80 + "\n")
    
    # Obter configuração do dispositivo
    config_dispositivo = obter_parametros_dispositivo(perfil_dispositivo)
    frequencia_hz = config_dispositivo['frequencia_portadora_hz']
    velocidade_kmh = config_dispositivo['velocidade_max_kmh']
    erro_estimativa = config_dispositivo['erro_estimativa_canal']
    guard_band_sigma = config_dispositivo['guard_band_sigma']
    
    # Calcular parâmetros de canal baseados na velocidade
    velocidade_ms = velocidade_kmh / 3.6
    comprimento_onda = 3e8 / frequencia_hz
    freq_doppler_hz = velocidade_ms / comprimento_onda
    
    # Tempo de coerência: Tc ≈ 1/(2*fD)
    if freq_doppler_hz > 0:
        tempo_coerencia_ms = 1000 / (2 * freq_doppler_hz)
    else:
        tempo_coerencia_ms = float('inf')
    
    # Correlação temporal (modelo de Jakes)
    if freq_doppler_hz > 0:
        correlacao_temporal = float(j0(2 * np.pi * freq_doppler_hz * atraso_medicao_ms / 1000))
    else:
        correlacao_temporal = 1.0
    
    print(f"\nParâmetros do perfil '{perfil_dispositivo}':")
    print(f"  - Velocidade: {velocidade_kmh} km/h")
    print(f"  - Frequência: {frequencia_hz/1e9:.3f} GHz")
    print(f"  - Freq. Doppler: {freq_doppler_hz:.2f} Hz")
    print(f"  - Tempo coerência: {tempo_coerencia_ms:.2f} ms")
    print(f"  - Correlação temporal (ρ): {correlacao_temporal:.4f}")
    print(f"  - Erro estimativa: {erro_estimativa*100:.1f}%")
    print(f"  - Guard band: {guard_band_sigma}σ")
    print()
    
    # Configuração
    potencia_sinal = 1.0
    media_ruido = 0.0
    
    # Prepara palavra código
    random.seed(42)
    palavra_codigo = [random.randint(0, 1) for _ in range(tamanho_cadeia_bits)]
    tamanho_bits_informacao = get_tamanho_bits_informacao(tamanho_cadeia_bits)
    bch_codigo = gerar_tabela_codigos_bch(tamanho_cadeia_bits, tamanho_bits_informacao)
    
    # Armazenar resultados
    resultados = {
        'distancia_m': [],
        'snr_db': [],
        'path_loss_db': [],
        'kdr_antes': [],
        'kdr_pos_reconciliacao': [],
        'kdr_pos_amplificacao': []
    }
    
    # Loop sobre distâncias
    for distancia_m in tqdm(distancias_m, desc=f"Testando distâncias ({tipo_canal})"):
        # Calcular SNR para esta distância
        snr_db = calcular_snr_por_distancia(
            distancia_m, 
            frequencia_hz, 
            potencia_tx_dbm, 
            tipo=tipo_canal
        )
        snr_linear = 10 ** (snr_db / 10)
        variancia_ruido = potencia_sinal / (2 * snr_linear)
        
        # Calcular path loss
        pl_db = calcular_path_loss_indoor(distancia_m, frequencia_hz, tipo_canal)
        
        print(f"\nDistância: {distancia_m}m → SNR: {snr_db:.2f} dB (PL: {pl_db:.1f} dB)")
        
        # Extrair KDR
        kdr_antes, kdr_pos_bch, kdr_pos_sha = extrair_kdr(
            palavra_codigo=palavra_codigo,
            rayleigh_param=rayleigh_param,
            tamanho_cadeia_bits=tamanho_cadeia_bits,
            quantidade_de_testes=quantidade_de_testes,
            variancia_ruido=variancia_ruido,
            media_ruido=media_ruido,
            bch_codigo=bch_codigo,
            correlacao_canal=correlacao_temporal,
            modulacao=modulacao,
            erro_estimativa=erro_estimativa,
            guard_band_sigma=guard_band_sigma
        )
        
        # Armazenar resultados
        resultados['distancia_m'].append(distancia_m)
        resultados['snr_db'].append(snr_db)
        resultados['path_loss_db'].append(pl_db)
        resultados['kdr_antes'].append(kdr_antes)
        resultados['kdr_pos_reconciliacao'].append(kdr_pos_bch)
        resultados['kdr_pos_amplificacao'].append(kdr_pos_sha)
        
        print(f"  KDR antes: {kdr_antes:.2f}%")
        print(f"  KDR pós-BCH: {kdr_pos_bch:.2f}%")
        print(f"  KDR pós-SHA256: {kdr_pos_sha:.2f}%")
    
    # Timestamp para arquivos
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_base = f"exp08_distancia_{perfil_dispositivo}_{tipo_canal}_{timestamp}"
    
    # Preparar metadados
    metadados = {
        'experimento': 'exp08_variacao_distancia',
        'perfil_dispositivo': perfil_dispositivo,
        'tipo_canal': tipo_canal,
        'velocidade_kmh': velocidade_kmh,
        'frequencia_ghz': frequencia_hz / 1e9,
        'correlacao_temporal': correlacao_temporal,
        'tempo_coerencia_ms': tempo_coerencia_ms if tempo_coerencia_ms != float('inf') else 'infinito',
        'freq_doppler_hz': freq_doppler_hz,
        'erro_estimativa': erro_estimativa,
        'guard_band_sigma': guard_band_sigma,
        'potencia_tx_dbm': potencia_tx_dbm,
        'distancias_m': distancias_m,
        'tamanho_cadeia_bits': tamanho_cadeia_bits,
        'quantidade_testes': quantidade_de_testes,
        'rayleigh_param': rayleigh_param,
        'modulacao': modulacao,
        'atraso_medicao_ms': atraso_medicao_ms,
        'timestamp': timestamp
    }
    
    # Salvar resultados
    print("\n" + "="*80)
    print("SALVANDO RESULTADOS")
    print("="*80)
    
    # JSON
    caminho_json = salvar_resultado_json(
        resultados,
        nome_base,
        str(metadados)
    )
    print(f"JSON: {caminho_json}")
    
    # CSV - preparar dados
    csv_dados = []
    for i in range(len(resultados['distancia_m'])):
        csv_dados.append({
            'distancia_m': resultados['distancia_m'][i],
            'snr_db': f"{resultados['snr_db'][i]:.2f}",
            'path_loss_db': f"{resultados['path_loss_db'][i]:.2f}",
            'kdr_antes': f"{resultados['kdr_antes'][i]:.6f}",
            'kdr_pos_reconciliacao': f"{resultados['kdr_pos_reconciliacao'][i]:.6f}",
            'kdr_pos_amplificacao': f"{resultados['kdr_pos_amplificacao'][i]:.6f}"
        })
    
    caminho_csv = salvar_resultado_csv(
        csv_dados,
        nome_base,
        ['distancia_m', 'snr_db', 'path_loss_db', 'kdr_antes', 'kdr_pos_reconciliacao', 'kdr_pos_amplificacao']
    )
    print(f"CSV: {caminho_csv}")
    
    # Gráfico
    caminho_grafico = criar_grafico_distancia(
        nome_base,
        resultados,
        metadados
    )
    print(f"Gráfico: {caminho_grafico}")
    
    # Sumário
    print("\n" + "="*80)
    print("SUMÁRIO DOS RESULTADOS")
    print("="*80)
    imprimir_sumario_resultados(resultados)
    
    return resultados, metadados


def criar_grafico_distancia(nome_base, resultados, metadados):
    """Cria gráfico KDR vs Distância"""
    import matplotlib.pyplot as plt
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    distancias = resultados['distancia_m']
    
    # Gráfico 1: KDR vs Distância
    ax1.plot(distancias, resultados['kdr_antes'], 'o-', color='red', 
             linewidth=2, markersize=8, label='KDR antes reconciliação')
    ax1.plot(distancias, resultados['kdr_pos_reconciliacao'], 's-', color='blue', 
             linewidth=2, markersize=8, label='KDR pós reconciliação')
    ax1.plot(distancias, resultados['kdr_pos_amplificacao'], '^-', color='green', 
             linewidth=2, markersize=8, label='KDR pós amplificação')
    
    ax1.set_xlabel('Distância (m)', fontsize=12)
    ax1.set_ylabel('KDR (%)', fontsize=12)
    ax1.set_title(f"KDR vs Distância - {metadados['perfil_dispositivo']} ({metadados['tipo_canal']})", 
                  fontsize=13, fontweight='bold')
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)
    ax1.set_xscale('log')
    
    # Gráfico 2: SNR vs Distância
    ax2.plot(distancias, resultados['snr_db'], 'o-', color='purple', 
             linewidth=2, markersize=8, label='SNR calculado')
    ax2.axhline(y=11, color='red', linestyle='--', linewidth=2, label='SNR mínimo (11 dB)')
    
    ax2.set_xlabel('Distância (m)', fontsize=12)
    ax2.set_ylabel('SNR (dB)', fontsize=12)
    ax2.set_title(f"SNR vs Distância - fc={metadados['frequencia_ghz']:.2f} GHz", 
                  fontsize=13, fontweight='bold')
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3)
    ax2.set_xscale('log')
    
    plt.tight_layout()
    
    # Salvar
    caminho_base = os.path.join(
        os.path.dirname(__file__),
        '..',
        'resultados',
        'figuras'
    )
    os.makedirs(caminho_base, exist_ok=True)
    
    caminho_completo = os.path.join(caminho_base, f"{nome_base}.png")
    plt.savefig(caminho_completo, dpi=300, bbox_inches='tight')
    plt.close()
    
    return caminho_completo


def cenarios_artigo_referencia():
    """
    Reproduz os 6 cenários do artigo de referência (Yuan et al. IEEE ICCC 2022)
    
    Cenários:
    - SS1: Static Sight 1m
    - SNS1: Static Non-Sight 1m
    - DS1: Dynamic Sight 1m
    - SS3: Static Sight 3m
    - SNS3: Static Non-Sight 3m
    - DS3: Dynamic Sight 3m
    """
    print("\n" + "="*80)
    print("CENÁRIOS DO ARTIGO DE REFERÊNCIA (Yuan et al. IEEE ICCC 2022)")
    print("="*80 + "\n")
    
    cenarios = [
        ('sensor_estatico', 'LOS', [1], 'SS1'),      # Static Sight 1m
        ('sensor_estatico', 'NLOS', [1], 'SNS1'),    # Static Non-Sight 1m
        ('pessoa_andando', 'LOS', [1], 'DS1'),       # Dynamic Sight 1m
        ('sensor_estatico', 'LOS', [3], 'SS3'),      # Static Sight 3m
        ('sensor_estatico', 'NLOS', [3], 'SNS3'),    # Static Non-Sight 3m
        ('pessoa_andando', 'LOS', [3], 'DS3'),       # Dynamic Sight 3m
    ]
    
    todos_resultados = {}
    
    for perfil, tipo, distancias, nome_cenario in cenarios:
        print(f"\n{'='*60}")
        print(f"Cenário {nome_cenario}: {perfil}, {tipo}, {distancias[0]}m")
        print('='*60)
        
        resultados, metadados = experimento_variacao_distancia(
            perfil_dispositivo=perfil,
            tipo_canal=tipo,
            distancias_m=distancias,
            quantidade_de_testes=1000
        )
        
        todos_resultados[nome_cenario] = {
            'resultados': resultados,
            'metadados': metadados
        }
    
    # Sumário comparativo
    print("\n" + "="*80)
    print("SUMÁRIO COMPARATIVO - CENÁRIOS DO ARTIGO")
    print("="*80)
    print(f"{'Cenário':<8} {'Perfil':<18} {'Tipo':<6} {'Dist':<6} {'SNR (dB)':<10} {'KDR pós-BCH (%)':<15}")
    print("-"*80)
    
    for nome, dados in todos_resultados.items():
        res = dados['resultados']
        meta = dados['metadados']
        print(f"{nome:<8} {meta['perfil_dispositivo']:<18} {meta['tipo_canal']:<6} "
              f"{res['distancia_m'][0]:<6}m {res['snr_db'][0]:<10.2f} "
              f"{res['kdr_pos_reconciliacao'][0]:<15.2f}")
    
    return todos_resultados


if __name__ == "__main__":
    # Teste 1: Varrer distâncias para sensor estático LOS
    print("TESTE 1: Sensor Estático - LOS")
    experimento_variacao_distancia(
        perfil_dispositivo='sensor_estatico',
        tipo_canal='LOS',
        distancias_m=[1, 2, 3, 5, 10, 20, 50, 100],
        quantidade_de_testes=1000
    )
    
    print("\n" + "="*80 + "\n")
    
    # Teste 2: Cenários do artigo de referência
    print("TESTE 2: Reproduzir cenários do artigo")
    cenarios_artigo_referencia()
