"""
Testes unitários para configuração de dispositivos IoT
"""
import pytest
import sys
import os
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.util.config_dispositivos import (
    obter_parametros_dispositivo,
    calcular_tempo_coerencia,
    calcular_correlacao_temporal,
    calcular_parametros_canal,
    listar_dispositivos
)


class TestListarDispositivos:
    """Testes para listagem de dispositivos"""
    
    def test_listar_dispositivos(self):
        """Testa se a lista de dispositivos é retornada corretamente"""
        perfis = listar_dispositivos()
        
        assert isinstance(perfis, dict)
        assert len(perfis) >= 5  # Pelo menos 5 perfis predefinidos
        assert 'pessoa_andando' in perfis
        assert 'sensor_estatico' in perfis
        assert 'veiculo_urbano' in perfis


class TestObterParametros:
    """Testes para obtenção de parâmetros"""
    
    def test_obter_parametros_pessoa_andando(self):
        """Testa obtenção de parâmetros de pessoa andando"""
        config = obter_parametros_dispositivo('pessoa_andando')
        
        assert config['erro_estimativa_canal'] == 0.15
        assert config['velocidade_max_kmh'] == 5.0
        assert config['guard_band_sigma'] == 0.3
    
    def test_obter_parametros_sensor_estatico(self):
        """Testa obtenção de parâmetros de sensor estático"""
        config = obter_parametros_dispositivo('sensor_estatico')
        
        assert config['erro_estimativa_canal'] == 0.08
        assert config['velocidade_max_kmh'] == 0.0
        assert config['guard_band_sigma'] == 0.7
    
    def test_obter_parametros_manual(self):
        """Testa obtenção de estrutura padrão para configuração manual"""
        config = obter_parametros_dispositivo(None)
        
        assert 'erro_estimativa_canal' in config
        assert 'velocidade_max_kmh' in config
        assert 'guard_band_sigma' in config
    
    def test_obter_parametros_invalido(self):
        """Testa comportamento com dispositivo inválido"""
        with pytest.raises(ValueError):
            obter_parametros_dispositivo('dispositivo_inexistente')


class TestTempoCoerencia:
    """Testes para cálculo de tempo de coerência"""
    
    def test_tempo_coerencia_sensor_estatico(self):
        """Testa tempo de coerência para sensor estático"""
        tc = calcular_tempo_coerencia(0.0, 2.4e9)
        
        assert tc == np.inf  # Canal estático tem tempo infinito
    
    def test_tempo_coerencia_pessoa_andando(self):
        """Testa tempo de coerência para pessoa andando"""
        # v = 5 km/h = 1.39 m/s, fc = 2.4 GHz
        # fD = 1.39 * 2.4e9 / 3e8 = 11.1 Hz
        # Tc = 9/(16*π*11.1) ≈ 16.2 ms
        tc = calcular_tempo_coerencia(5.0, 2.4e9)
        
        assert 0.015 < tc < 0.018  # Aproximadamente 16.2 ms
    
    def test_tempo_coerencia_veiculo(self):
        """Testa tempo de coerência para veículo"""
        # v = 60 km/h = 16.67 m/s, fc = 5.9 GHz
        # fD = 16.67 * 5.9e9 / 3e8 = 328 Hz
        # Tc ≈ 0.55 ms
        tc = calcular_tempo_coerencia(60.0, 5.9e9)
        
        assert 0.0004 < tc < 0.0007  # Aproximadamente 0.55 ms


class TestCorrelacaoTemporal:
    """Testes para cálculo de correlação temporal"""
    
    def test_correlacao_temporal_alta(self):
        """Testa correlação para atraso pequeno"""
        # Tc = 16 ms, atraso = 1 ms
        # ρ = exp(-1/16) ≈ 0.94
        rho = calcular_correlacao_temporal(1.0, 0.016)
        
        assert 0.93 < rho < 0.95
    
    def test_correlacao_temporal_baixa(self):
        """Testa correlação para atraso grande"""
        # Tc = 1 ms, atraso = 5 ms
        # ρ = exp(-5/1) ≈ 0.007
        rho = calcular_correlacao_temporal(5.0, 0.001)
        
        assert rho < 0.01
    
    def test_correlacao_temporal_moderada(self):
        """Testa correlação para atraso moderado"""
        # Tc = 5 ms, atraso = 2 ms
        # ρ = exp(-2/5) ≈ 0.67
        rho = calcular_correlacao_temporal(2.0, 0.005)
        
        assert 0.65 < rho < 0.70


class TestCalcularParametrosCanal:
    """Testes para cálculo completo de parâmetros de canal"""
    
    def test_parametros_canal_pessoa_andando(self):
        """Testa cálculo de parâmetros para pessoa andando"""
        config = obter_parametros_dispositivo('pessoa_andando')
        parametros = calcular_parametros_canal(config, atraso_medicao_ms=1.0)
        
        assert 'tempo_coerencia_s' in parametros
        assert 'freq_doppler_hz' in parametros
        assert 'correlacao_temporal' in parametros
        
        # Correlação deve ser alta para pessoa andando
        assert parametros['correlacao_temporal'] > 0.9
    
    def test_parametros_canal_veiculo(self):
        """Testa cálculo de parâmetros para veículo"""
        config = obter_parametros_dispositivo('veiculo_urbano')
        parametros = calcular_parametros_canal(config, atraso_medicao_ms=1.0)
        
        # Correlação deve ser baixa para veículo rápido
        assert parametros['correlacao_temporal'] < 0.5
        
        # Frequência Doppler deve ser alta
        assert parametros['freq_doppler_hz'] > 100
    
    def test_parametros_canal_sensor_estatico(self):
        """Testa cálculo de parâmetros para sensor estático"""
        config = obter_parametros_dispositivo('sensor_estatico')
        parametros = calcular_parametros_canal(config, atraso_medicao_ms=1.0)
        
        # Correlação deve ser perfeita (1.0)
        assert parametros['correlacao_temporal'] == 1.0
        
        # Frequência Doppler deve ser zero
        assert parametros['freq_doppler_hz'] == 0.0
        
        # Tempo de coerência deve ser infinito
        assert parametros['tempo_coerencia_s'] == np.inf


class TestConsistenciaParametros:
    """Testes de consistência entre parâmetros"""
    
    def test_todos_perfis_validos(self):
        """Testa se todos os perfis têm parâmetros válidos"""
        perfis = listar_dispositivos()
        
        for nome in perfis.keys():
            config = obter_parametros_dispositivo(nome)
            
            # Verifica campos obrigatórios
            assert 'erro_estimativa_canal' in config
            assert 'velocidade_max_kmh' in config
            assert 'frequencia_portadora_hz' in config
            assert 'guard_band_sigma' in config
            
            # Verifica valores válidos
            assert 0.0 <= config['erro_estimativa_canal'] <= 1.0
            assert config['velocidade_max_kmh'] >= 0.0
            assert config['frequencia_portadora_hz'] > 0
            assert 0.0 <= config['guard_band_sigma'] <= 2.0
    
    def test_parametros_calculados_consistentes(self):
        """Testa consistência de parâmetros calculados"""
        perfis = listar_dispositivos()
        
        for nome in perfis.keys():
            config = obter_parametros_dispositivo(nome)
            parametros = calcular_parametros_canal(config)
            
            # Correlação deve estar entre 0 e 1
            assert 0.0 <= parametros['correlacao_temporal'] <= 1.0
            
            # Frequência Doppler deve ser não-negativa
            assert parametros['freq_doppler_hz'] >= 0.0
            
            # Tempo de coerência deve ser positivo ou infinito
            assert parametros['tempo_coerencia_s'] > 0 or parametros['tempo_coerencia_s'] == np.inf
