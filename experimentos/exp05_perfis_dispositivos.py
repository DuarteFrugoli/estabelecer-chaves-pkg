"""
Experimento 5: Perfis de Dispositivos IoT
Testa o desempenho de PKG para diferentes perfis de dispositivos
"""

import sys
import os
import numpy as np
import random
from tqdm import tqdm
from datetime import datetime

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Caminho base do projeto (raiz)
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from src.codigos_corretores.bch import gerar_tabela_codigos_bch, get_tamanho_bits_informacao
from src.canal.canal import extrair_kdr
from src.util.config_dispositivos import (
    PERFIS_DISPOSITIVOS,
    calcular_parametros_canal,
    obter_parametros_dispositivo
)
from experimentos.util_experimentos import (
    salvar_resultado_json,
    salvar_resultado_csv,
    criar_grafico_comparativo_kdr,
    imprimir_sumario_resultados
)


def experimento_perfis_dispositivos(
    tamanho_cadeia_bits=127,
    quantidade_de_testes=1000,
    rayleigh_param=1.0/np.sqrt(2),
    modulacao='bpsk',
    snr_min=-5,
    snr_max=25,
    snr_pontos=16,
    atraso_medicao_ms=1.0
):
    """
    Experimento: Desempenho de PKG para diferentes perfis de dispositivos IoT
    
    Testa os 5 perfis implementados:
    1. pessoa_andando (v=5 km/h, fc=2.4 GHz)
    2. sensor_estatico (v=0 km/h, fc=868 MHz)
    3. veiculo_urbano (v=60 km/h, fc=5.9 GHz)
    4. drone (v=40 km/h, fc=2.4 GHz)
    5. nb_iot (v=10 km/h, fc=900 MHz)
    
    Args:
        tamanho_cadeia_bits: Tamanho do código BCH
        quantidade_de_testes: Número de testes Monte Carlo
        rayleigh_param: Parâmetro σ do Rayleigh
        modulacao: 'bpsk' ou 'qpsk'
        snr_min: SNR mínimo em dB
        snr_max: SNR máximo em dB
        snr_pontos: Número de pontos SNR
        atraso_medicao_ms: Atraso entre medições de Alice e Bob
    """
    
    print("\n" + "="*80)
    print("EXPERIMENTO 5: PERFIS DE DISPOSITIVOS IoT")
    print("="*80)
    print(f"Tamanho código BCH: {tamanho_cadeia_bits}")
    print(f"Quantidade de testes: {quantidade_de_testes}")
    print(f"Parâmetro Rayleigh: {rayleigh_param:.6f}")
    print(f"Modulação: {modulacao.upper()}")
    print(f"Range SNR: [{snr_min}, {snr_max}] dB ({snr_pontos} pontos)")
    print(f"Atraso medição: {atraso_medicao_ms} ms")
    print("="*80 + "\n")
    
    # Configuração
    potencia_sinal = 1.0
    media_ruido = 0.0
    
    snr_db_range = np.linspace(snr_min, snr_max, snr_pontos)
    snr_linear_range = 10 ** (snr_db_range / 10)
    variancias_ruido = potencia_sinal / (2 * snr_linear_range)
    
    # Prepara palavra código
    random.seed(42)
    palavra_codigo = [random.randint(0, 1) for _ in range(tamanho_cadeia_bits)]
    tamanho_bits_informacao = get_tamanho_bits_informacao(tamanho_cadeia_bits)
    bch_codigo = gerar_tabela_codigos_bch(tamanho_cadeia_bits, tamanho_bits_informacao)
    
    # Resultados por perfil
    resultados_perfis = {}
    
    # Lista de perfis a testar
    perfis = ['pessoa_andando', 'sensor_estatico', 'veiculo_urbano', 'drone', 'nb_iot']
    
    print("Perfis a testar:")
    for i, perfil in enumerate(perfis, 1):
        config = obter_parametros_dispositivo(perfil)
        params_canal = calcular_parametros_canal(config, atraso_medicao_ms)
        
        print(f"{i}. {perfil}:")
        print(f"   - Velocidade: {config['velocidade_max_kmh']} km/h")
        print(f"   - Frequência: {config['frequencia_portadora_hz']/1e9:.2f} GHz")
        print(f"   - Erro estimação: {config['erro_estimativa_canal']*100:.1f}%")
        print(f"   - Guard band: {config['guard_band_sigma']} sigma")
        print(f"   - Tc: {params_canal['tempo_coerencia_s']*1000:.2f} ms")
        print(f"   - fD: {params_canal['freq_doppler_hz']:.2f} Hz")
        print(f"   - rho: {params_canal['correlacao_temporal']:.4f}")
    
    print("\n" + "="*80)
    print("Iniciando testes...")
    print("="*80 + "\n")
    
    # Testa cada perfil
    for perfil_nome in perfis:
        print(f"\n{'='*80}")
        print(f"TESTANDO PERFIL: {perfil_nome.upper()}")
        print(f"{'='*80}\n")
        
        # Obtém parâmetros do perfil
        config = obter_parametros_dispositivo(perfil_nome)
        params_canal = calcular_parametros_canal(config, atraso_medicao_ms)
        
        # Extrai parâmetros para a simulação
        erro_estimativa = config['erro_estimativa_canal']
        guard_band_sigma = config['guard_band_sigma']
        correlacao_temporal = params_canal['correlacao_temporal']
        
        print(f"Parâmetros da simulação:")
        print(f"  - Correlação temporal (rho): {correlacao_temporal:.4f}")
        print(f"  - Erro de estimação: {erro_estimativa*100:.1f}%")
        print(f"  - Guard band: {guard_band_sigma} sigma")
        print(f"  - Tempo coerência: {params_canal['tempo_coerencia_s']*1000:.2f} ms")
        print()
        
        # Coleta dados para este perfil
        ber_rates = []
        kdr_rates = []
        
        for i, (snr_db, variancia) in enumerate(tqdm(
            zip(snr_db_range, variancias_ruido),
            total=len(snr_db_range),
            desc=f"SNR {perfil_nome}",
            colour="cyan"
        )):
            ber, kdr = extrair_kdr(
                palavra_codigo,
                rayleigh_param,
                tamanho_cadeia_bits,
                quantidade_de_testes,
                variancia,
                media_ruido,
                bch_codigo,
                correlacao_temporal,  # Usa correlação calculada do perfil
                usar_amplificacao=False,
                modulacao=modulacao,
                erro_estimativa=erro_estimativa,  # Usa erro do perfil
                guard_band_sigma=guard_band_sigma  # Usa guard band do perfil
            )
            
            ber_rates.append(ber)
            kdr_rates.append(kdr)
        
        # Armazena resultados
        resultados_perfis[perfil_nome] = {
            'config': config,
            'params_canal': params_canal,
            'snr_db': snr_db_range.tolist(),
            'ber_rates': ber_rates,
            'kdr_rates': kdr_rates,
        }
        
        # Encontra SNR mínimo para KDR < 1%
        snr_min_viavel = None
        for snr, kdr in zip(snr_db_range, kdr_rates):
            if kdr < 0.01:  # 1%
                snr_min_viavel = snr
                break
        
        print(f"\nResumo {perfil_nome}:")
        print(f"  - BER inicial (SNR={snr_db_range[0]:.1f}dB): {ber_rates[0]:.2f}%")
        print(f"  - KDR inicial (SNR={snr_db_range[0]:.1f}dB): {kdr_rates[0]:.2f}%")
        print(f"  - KDR final (SNR={snr_db_range[-1]:.1f}dB): {kdr_rates[-1]:.2f}%")
        if snr_min_viavel:
            print(f"  - SNR mínimo para KDR<1%: {snr_min_viavel:.1f} dB")
        else:
            print(f"  - SNR mínimo para KDR<1%: Não alcançado (>25dB)")
    
    # Salva resultados
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Prepara dados para CSV
    csv_data = {
        'perfil': [],
        'velocidade_kmh': [],
        'frequencia_ghz': [],
        'erro_estimativa': [],
        'guard_band_sigma': [],
        'tempo_coerencia_ms': [],
        'freq_doppler_hz': [],
        'correlacao_temporal': [],
        'snr_db': [],
        'ber': [],
        'kdr': [],
    }
    
    for perfil_nome, resultado in resultados_perfis.items():
        config = resultado['config']
        params = resultado['params_canal']
        
        for snr, ber, kdr in zip(
            resultado['snr_db'],
            resultado['ber_rates'],
            resultado['kdr_rates']
        ):
            csv_data['perfil'].append(perfil_nome)
            csv_data['velocidade_kmh'].append(config['velocidade_max_kmh'])
            csv_data['frequencia_ghz'].append(config['frequencia_portadora_hz']/1e9)
            csv_data['erro_estimativa'].append(config['erro_estimativa_canal'])
            csv_data['guard_band_sigma'].append(config['guard_band_sigma'])
            csv_data['tempo_coerencia_ms'].append(params['tempo_coerencia_s']*1000)
            csv_data['freq_doppler_hz'].append(params['freq_doppler_hz'])
            csv_data['correlacao_temporal'].append(params['correlacao_temporal'])
            csv_data['snr_db'].append(snr)
            csv_data['ber'].append(ber)
            csv_data['kdr'].append(kdr)
    
    # Salva CSV
    colunas_csv = list(csv_data.keys())
    dados_csv = [
        {col: csv_data[col][i] for col in colunas_csv}
        for i in range(len(csv_data['perfil']))
    ]
    salvar_resultado_csv(
        dados_csv,
        "exp05_perfis_dispositivos",
        colunas_csv
    )
    
    # Prepara dados para JSON
    json_data = {
        'experimento': 'exp05_perfis_dispositivos',
        'timestamp': timestamp,
        'configuracao': {
            'tamanho_cadeia_bits': tamanho_cadeia_bits,
            'quantidade_de_testes': quantidade_de_testes,
            'rayleigh_param': rayleigh_param,
            'modulacao': modulacao,
            'snr_range_db': [snr_min, snr_max],
            'snr_pontos': snr_pontos,
            'atraso_medicao_ms': atraso_medicao_ms,
        },
        'resultados': resultados_perfis
    }
    
    # Salva JSON
    salvar_resultado_json(
        json_data,
        "exp05_perfis_dispositivos",
        "Perfis de dispositivos IoT"
    )
    
    # Cria gráfico comparativo
    print("\n" + "="*80)
    print("Gerando gráfico comparativo...")
    print("="*80 + "\n")
    
    # Prepara dados para gráfico
    dados_grafico = {}
    for perfil_nome, resultado in resultados_perfis.items():
        dados_grafico[perfil_nome] = {
            'snr_db': resultado['snr_db'],
            'ber_rates': resultado['ber_rates'],
            'kdr_rates': resultado['kdr_rates'],
        }
    
    criar_grafico_perfis_dispositivos(
        dados_grafico,
        f"exp05_perfis_dispositivos_{timestamp}",
        base_dir
    )
    
    # Imprime sumário
    print("\n" + "="*80)
    print("SUMÁRIO DOS RESULTADOS")
    print("="*80 + "\n")
    
    print(f"{'Perfil':<20} {'SNR Min (dB)':<15} {'rho':<10} {'Erro (%)':<10} {'GB (sigma)':<10}")
    print("-" * 80)
    
    for perfil_nome, resultado in resultados_perfis.items():
        params = resultado['params_canal']
        config = resultado['config']
        
        # Encontra SNR mínimo
        snr_min_viavel = "N/A"
        for snr, kdr in zip(resultado['snr_db'], resultado['kdr_rates']):
            if kdr < 0.01:
                snr_min_viavel = f"{snr:.1f}"
                break
        
        print(f"{perfil_nome:<20} {snr_min_viavel:<15} "
              f"{params['correlacao_temporal']:<10.4f} "
              f"{config['erro_estimativa_canal']*100:<10.1f} "
              f"{config['guard_band_sigma']:<10.2f}")
    
    print("\n" + "="*80)
    print("EXPERIMENTO CONCLUÍDO!")
    print("="*80)
    print(f"Resultados salvos com timestamp: {timestamp}")
    print(f"  - CSV: resultados/dados/exp05_perfis_dispositivos_{timestamp}.csv")
    print(f"  - JSON: resultados/dados/exp05_perfis_dispositivos_{timestamp}.json")
    print(f"  - Gráfico: resultados/figuras/exp05_perfis_dispositivos_{timestamp}.png")
    print("="*80 + "\n")
    
    return resultados_perfis


def criar_grafico_perfis_dispositivos(dados_grafico, nome_arquivo, base_dir):
    """
    Cria gráfico comparativo dos perfis de dispositivos.
    
    Args:
        dados_grafico: Dict com dados de cada perfil
        nome_arquivo: Nome base para salvar o arquivo
        base_dir: Diretório raiz do projeto
    """
    import matplotlib.pyplot as plt
    
    # Configurações do gráfico
    plt.style.use('seaborn-v0_8-darkgrid')
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Cores para cada perfil
    cores = {
        'pessoa_andando': '#1f77b4',
        'sensor_estatico': '#2ca02c',
        'veiculo_urbano': '#d62728',
        'drone': '#ff7f0e',
        'nb_iot': '#9467bd'
    }
    
    # Labels bonitos
    labels = {
        'pessoa_andando': 'Pessoa Andando (5 km/h)',
        'sensor_estatico': 'Sensor Estático (0 km/h)',
        'veiculo_urbano': 'Veículo Urbano (60 km/h)',
        'drone': 'Drone (40 km/h)',
        'nb_iot': 'NB-IoT (10 km/h)'
    }
    
    # Plot 1: BER (antes da reconciliação)
    for perfil, dados in dados_grafico.items():
        axes[0].plot(
            dados['snr_db'],
            [b * 100 for b in dados['ber_rates']],
            marker='o',
            linewidth=2,
            label=labels[perfil],
            color=cores[perfil]
        )
    
    axes[0].set_xlabel('SNR (dB)', fontsize=12)
    axes[0].set_ylabel('BER (%)', fontsize=12)
    axes[0].set_title('BER Antes da Reconciliação', fontsize=14, fontweight='bold')
    axes[0].legend(loc='upper right', fontsize=10)
    axes[0].grid(True, alpha=0.3)
    axes[0].set_ylim([0, 50])
    
    # Plot 2: KDR (após reconciliação BCH)
    for perfil, dados in dados_grafico.items():
        axes[1].plot(
            dados['snr_db'],
            [k * 100 for k in dados['kdr_rates']],
            marker='s',
            linewidth=2,
            label=labels[perfil],
            color=cores[perfil]
        )
    
    axes[1].set_xlabel('SNR (dB)', fontsize=12)
    axes[1].set_ylabel('KDR (%)', fontsize=12)
    axes[1].set_title('KDR Após Reconciliação (BCH)', fontsize=14, fontweight='bold')
    axes[1].legend(loc='upper right', fontsize=10)
    axes[1].grid(True, alpha=0.3)
    axes[1].axhline(y=1.0, color='r', linestyle='--', linewidth=1, label='Limiar 1%')
    axes[1].set_ylim([0, 20])
    
    plt.tight_layout()
    
    # Salva figura com caminho absoluto
    dir_figuras = os.path.join(base_dir, 'resultados', 'figuras')
    os.makedirs(dir_figuras, exist_ok=True)
    caminho = os.path.join(dir_figuras, f'{nome_arquivo}.png')
    plt.savefig(caminho, dpi=300, bbox_inches='tight')
    print(f"Gráfico salvo: {caminho}")
    plt.close()


if __name__ == "__main__":
    # Executa experimento com configurações padrão
    resultados = experimento_perfis_dispositivos(
        tamanho_cadeia_bits=127,
        quantidade_de_testes=1000,
        rayleigh_param=1.0/np.sqrt(2),
        modulacao='bpsk',
        snr_min=-5,
        snr_max=25,
        snr_pontos=16,
        atraso_medicao_ms=1.0
    )
