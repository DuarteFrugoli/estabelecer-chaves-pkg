"""
Script de teste rápido para calcular distâncias ideais por tecnologia
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.util.config_dispositivos import obter_parametros_dispositivo
import numpy as np


def calcular_distancia_maxima(frequencia_hz, snr_minimo_db=11, potencia_tx_dbm=23, tipo='LOS'):
    """
    Calcula distância máxima para PKG viável
    
    Args:
        frequencia_hz: Frequência da portadora
        snr_minimo_db: SNR mínimo para KDR < 1%
        potencia_tx_dbm: Potência de transmissão
        tipo: 'LOS' ou 'NLOS'
    
    Returns:
        float: Distância em metros
    """
    # Ruído térmico: N = -174 + 10*log10(BW) + NF
    bandwidth_hz = 20e6  # 20 MHz típico
    figura_ruido_db = 9  # Figura de ruído típica
    ruido_termico_dbm = -174 + 10 * np.log10(bandwidth_hz) + figura_ruido_db
    
    # Potência recebida mínima
    potencia_rx_min_dbm = ruido_termico_dbm + snr_minimo_db
    
    # Path loss máximo permitido
    pl_max_db = potencia_tx_dbm - potencia_rx_min_dbm
    
    # Resolver distância da equação de path loss
    frequencia_ghz = frequencia_hz / 1e9
    
    if tipo == 'LOS':
        # FSPL: PL = 20*log10(f) + 20*log10(d) + 32.4
        # PL - 20*log10(f) - 32.4 = 20*log10(d)
        log_d = (pl_max_db - 20 * np.log10(frequencia_ghz) - 32.4) / 20
        distancia_m = 10 ** log_d
    else:  # NLOS
        # ITU Indoor: PL = 20*log10(f) + 30*log10(d) + 32.4 + 10
        log_d = (pl_max_db - 20 * np.log10(frequencia_ghz) - 32.4 - 10) / 30
        distancia_m = 10 ** log_d
    
    return distancia_m


def main():
    print("\n" + "="*80)
    print("DISTÂNCIAS MÁXIMAS PARA PKG (SNR ≥ 11 dB)")
    print("="*80 + "\n")
    
    perfis = [
        ('5g_fr1_n78', '5G FR1 n78 (3.5 GHz)'),
        ('5g_fr1_n41', '5G FR1 n41 (2.5 GHz)'),
        ('5g_mmwave_n257', '5G mmWave (28 GHz)'),
        ('nb_iot', 'NB-IoT (900 MHz)'),
        ('sensor_estatico', 'LoRa (868 MHz)'),
        ('pessoa_andando', 'WiFi 2.4 GHz'),
        ('veiculo_urbano', 'V2X (5.9 GHz)'),
    ]
    
    print(f"{'Tecnologia':<30} {'Freq (GHz)':<12} {'LOS (m)':<12} {'NLOS (m)':<12} {'Velocidade':<12}")
    print("-"*80)
    
    for perfil, nome in perfis:
        config = obter_parametros_dispositivo(perfil)
        freq_ghz = config['frequencia_portadora_hz'] / 1e9
        velocidade = config['velocidade_max_kmh']
        potencia = config['potencia_transmissao_dbm']
        
        dist_los = calcular_distancia_maxima(
            config['frequencia_portadora_hz'], 
            potencia_tx_dbm=potencia,
            tipo='LOS'
        )
        dist_nlos = calcular_distancia_maxima(
            config['frequencia_portadora_hz'], 
            potencia_tx_dbm=potencia,
            tipo='NLOS'
        )
        
        print(f"{nome:<30} {freq_ghz:<12.2f} {dist_los:<12.1f} {dist_nlos:<12.1f} {velocidade:<12.1f}")
    
    print("\n" + "="*80)
    print("RECOMENDAÇÕES PARA ARTIGO IC")
    print("="*80 + "\n")
    
    print("📱 5G URBANO (FR1 - 3.5 GHz):")
    print("   Distâncias teste: [5, 10, 20, 30, 50, 100] metros")
    print("   Aplicação: Smartphone ↔ Smartphone (compartilhamento seguro)")
    print(f"   Distância máxima LOS: ~{dist_los:.0f}m | NLOS: ~{dist_nlos:.0f}m\n")
    
    print("📡 IoT (NB-IoT - 900 MHz):")
    print("   Distâncias teste: [50, 100, 200, 500, 1000] metros")
    print("   Aplicação: Sensor ↔ Gateway (autenticação)")
    print("   Distância máxima LOS: ~466m | NLOS: ~119m\n")
    
    print("🏢 5G mmWave (28 GHz):")
    print("   Distâncias teste: [1, 2, 3, 5, 10] metros")
    print("   Aplicação: Hotspot indoor (alta taxa, curto alcance)")
    print("   Distância máxima LOS: ~4.4m | NLOS: ~1.7m\n")
    
    print("🏠 WiFi 2.4 GHz (Wearables):")
    print("   Distâncias teste: [1, 3, 5, 10, 20] metros")
    print("   Aplicação: Smartwatch ↔ Smartphone")
    print("   Distância máxima LOS: ~91m | NLOS: ~36m\n")
    
    print("\n" + "="*80)
    print("DIFERENÇA COM ARTIGO DE REFERÊNCIA")
    print("="*80 + "\n")
    
    print("ARTIGO (Yuan et al.):")
    print("   Arquitetura: Multi-usuário (1 AP → 3 STAs)")
    print("   Distância: AP ↔ STA (1m ou 3m)")
    print("   Tecnologia: WiFi ESP32\n")
    
    print("NOSSO TRABALHO:")
    print("   Arquitetura: Ponto-a-ponto (Alice ↔ Bob)")
    print("   Distância: Alice ↔ Bob (direto)")
    print("   Tecnologias: WiFi, 5G FR1, 5G mmWave, NB-IoT, LoRa")
    print("   DIFERENCIAL: Até 1000m (IoT) e análise 5G!\n")
    
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
