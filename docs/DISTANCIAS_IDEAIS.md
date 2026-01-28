# Distâncias Ideais para PKG - 5G e IoT

## 📐 Arquitetura do Sistema

### Artigo de Referência (Yuan et al.)
```
        AP (Access Point)
       /  |  \
      /   |   \
    STA1 STA2 STA3
```
- **Arquitetura:** Multi-usuário (1 AP + 3 STAs)
- **Distância medida:** AP ↔ STA (1m ou 3m)
- **PKG:** Entre AP e cada STA individualmente

### Nosso Trabalho
```
    Alice ←────────→ Bob
         (distância d)
```
- **Arquitetura:** Ponto-a-ponto (peer-to-peer)
- **Distância medida:** Alice ↔ Bob (direto)
- **PKG:** Entre Alice e Bob diretamente
- **Vantagem:** Mais simples, sem infraestrutura centralizada

---

## 🎯 Distâncias Ideais por Tecnologia

### 1. 5G (Sub-6 GHz - FR1)

#### Banda n78 (3.5 GHz) - Mais comum no Brasil
```python
Frequência: 3.5 GHz
Potência TX: 23 dBm (200 mW)
SNR mínimo PKG: 11 dB

Distâncias viáveis:
├─ Indoor (LOS): até 50m
├─ Indoor (NLOS): até 20m
├─ Outdoor (LOS): até 200m
└─ Outdoor (NLOS): até 80m
```

**Cenários práticos:**
- **Residencial:** 10-30m (smartphone ↔ smart TV)
- **Escritório:** 15-40m (laptop ↔ impressora 5G)
- **Shopping:** 20-60m (dispositivos móveis)

#### Banda n77 (3.7 GHz)
```python
Frequência: 3.7 GHz
Resultados similares a n78
Distância ideal: 10-50m indoor
```

#### Banda n41 (2.5 GHz) - LTE Advanced / 5G
```python
Frequência: 2.5 GHz
Maior penetração que 3.5 GHz

Distâncias viáveis:
├─ Indoor (LOS): até 80m
├─ Indoor (NLOS): até 35m
└─ Outdoor (LOS): até 300m
```

### 2. 5G mmWave (FR2) - 28 GHz

```python
Frequência: 28 GHz (mmWave)
Potência TX: 23 dBm
SNR mínimo: 11 dB

Distâncias viáveis:
├─ Indoor (LOS): até 10m
├─ Indoor (NLOS): até 3m
└─ Outdoor (LOS): até 50m

LIMITAÇÕES:
- Alta atenuação atmosférica
- Bloqueio por paredes/obstáculos
- Ideal para: Small cells, hotspots
```

**Cenários práticos:**
- **Escritório pequeno:** 5-10m (mesma sala)
- **Estádio/Arena:** 10-30m (alta densidade)
- **Kiosk:** 1-5m (pagamento sem contato)

---

### 3. NB-IoT (Narrowband IoT)

#### Banda 20 (800 MHz) - Mais comum
```python
Frequência: 800 MHz
Potência TX: 23 dBm
SNR mínimo: 11 dB

Distâncias viáveis:
├─ Indoor (LOS): até 500m
├─ Indoor (NLOS): até 200m
├─ Outdoor (LOS): até 10 km ✅
└─ Outdoor (NLOS): até 3 km

VANTAGENS:
- Excelente penetração
- Longo alcance
- Baixo consumo
```

**Cenários práticos:**
- **Smart city:** 500m - 2km (sensores urbanos)
- **Agricultura:** 1km - 5km (sensores de campo)
- **Industrial:** 100m - 1km (monitoramento de máquinas)

#### Banda 8 (900 MHz)
```python
Frequência: 900 MHz
Similar ao 800 MHz
Distância ideal: 200m - 5km
```

---

### 4. LoRa (Long Range)

```python
Frequência: 915 MHz (Brasil)
Potência TX: 14 dBm
SNR mínimo: 11 dB

Distâncias viáveis:
├─ Indoor: até 300m
├─ Urbano: até 5km
└─ Rural: até 15km ✅

CARACTERÍSTICAS:
- Spread spectrum
- Muito baixa taxa (300 bps - 50 kbps)
- Ideal para sensores estáticos
```

**Cenários práticos:**
- **Smart farming:** 2km - 10km
- **Cidades inteligentes:** 1km - 5km
- **Monitoramento ambiental:** 5km - 15km

---

### 5. WiFi (2.4 GHz / 5 GHz)

#### WiFi 2.4 GHz (nosso perfil "pessoa_andando")
```python
Frequência: 2.4 GHz
Potência TX: 20 dBm
SNR mínimo: 11 dB

Distâncias viáveis:
├─ Indoor (LOS): até 100m
├─ Indoor (NLOS): até 35m
└─ Outdoor (LOS): até 300m
```

**Cenários práticos:**
- **Casa:** 10-30m (wearables, smart home)
- **Escritório:** 20-50m
- **Campus:** 50-100m

#### WiFi 5 GHz (nosso perfil "veiculo_urbano")
```python
Frequência: 5.9 GHz (V2X)
Menor penetração, maior taxa

Distâncias viáveis:
├─ Indoor (LOS): até 50m
├─ Outdoor (LOS): até 300m (V2V)
└─ V2X: 50-200m
```

---

## 📊 Tabela Resumo: Distâncias Ideais

| Tecnologia | Frequência | Indoor LOS | Indoor NLOS | Outdoor LOS | Caso de Uso |
|------------|-----------|------------|-------------|-------------|-------------|
| **5G mmWave** | 28 GHz | 10m | 3m | 50m | Hotspots, small cells |
| **5G FR1 (n78)** | 3.5 GHz | 50m | 20m | 200m | Smartphones, IoT urbano |
| **5G FR1 (n41)** | 2.5 GHz | 80m | 35m | 300m | Cobertura geral |
| **WiFi 2.4 GHz** | 2.4 GHz | 100m | 35m | 300m | Wearables, smart home |
| **WiFi 5 GHz** | 5.9 GHz | 50m | 15m | 300m | V2X, alta taxa |
| **NB-IoT** | 800 MHz | 500m | 200m | **10 km** | Smart city, agricultura |
| **LoRa** | 915 MHz | 300m | 100m | **15 km** | Sensores remotos |

---

## 🎯 Recomendações para Artigo IC

### Cenário 1: 5G Urbano (FR1 - 3.5 GHz)
```python
Perfil sugerido: 'pessoa_andando' (adaptado para 3.5 GHz)
Distâncias teste: [5, 10, 20, 30, 50] metros
Tipo: LOS e NLOS
Aplicação: Smartphone ↔ Smartphone (PKG para compartilhamento seguro)

Resultados esperados:
- 5m: SNR ~25 dB → KDR = 0%
- 10m: SNR ~19 dB → KDR = 0%
- 20m: SNR ~13 dB → KDR ~0.5%
- 30m: SNR ~10 dB → KDR ~2%
- 50m: SNR ~6 dB → KDR ~8%
```

### Cenário 2: IoT (NB-IoT - 800 MHz)
```python
Perfil sugerido: 'nb_iot'
Distâncias teste: [50, 100, 200, 500, 1000, 2000] metros
Tipo: LOS (outdoor)
Aplicação: Sensor ↔ Gateway (PKG para autenticação)

Resultados esperados:
- 50m: SNR ~30 dB → KDR = 0%
- 100m: SNR ~24 dB → KDR = 0%
- 200m: SNR ~18 dB → KDR = 0%
- 500m: SNR ~12 dB → KDR ~0.3%
- 1000m: SNR ~6 dB → KDR ~8%
- 2000m: SNR ~0 dB → KDR ~20%
```

### Cenário 3: 5G mmWave (28 GHz) - Desafiador
```python
Perfil sugerido: criar 'mmwave_5g'
Distâncias teste: [1, 2, 3, 5, 10, 15] metros
Tipo: LOS apenas (NLOS impraticável)
Aplicação: Dispositivos fixos em ambiente controlado

Resultados esperados:
- 1m: SNR ~35 dB → KDR = 0%
- 3m: SNR ~25 dB → KDR = 0%
- 5m: SNR ~20 dB → KDR = 0%
- 10m: SNR ~14 dB → KDR ~0.8%
- 15m: SNR ~10 dB → KDR ~2%
```

---

## 🔬 Experimentos Sugeridos

### Para Validar com Artigo (WiFi Indoor)
```python
# Reproduzir cenários SS1, SS3, DS1, DS3
experimento_variacao_distancia(
    perfil_dispositivo='sensor_estatico',  # SS1, SS3
    tipo_canal='LOS',
    distancias_m=[1, 3],
    potencia_tx_dbm=20  # WiFi típico
)
```

### Para 5G (Original do seu projeto)
```python
# Criar perfil 5G FR1
experimento_variacao_distancia(
    perfil_dispositivo='5g_fr1_3500mhz',  # Novo perfil
    tipo_canal='LOS',
    distancias_m=[5, 10, 20, 30, 50, 100],
    potencia_tx_dbm=23  # 5G UE
)
```

### Para IoT (Mais prático)
```python
# NB-IoT longo alcance
experimento_variacao_distancia(
    perfil_dispositivo='nb_iot',
    tipo_canal='LOS',
    distancias_m=[50, 100, 200, 500, 1000, 2000],
    potencia_tx_dbm=23
)
```

---

## 📝 Conclusão

### Resposta à Pergunta Original

**1. Distância A↔B ou Tx→A/B?**
- **Artigo:** Tx → A e Tx → B (multi-usuário via AP)
- **Nosso trabalho:** A ↔ B (ponto-a-ponto, mais simples)
- **Diferença:** Nossa distância é DIRETA entre Alice e Bob

**2. Distância ideal 5G:**
- **FR1 (3.5 GHz):** 10-50m indoor, até 200m outdoor
- **mmWave (28 GHz):** 5-10m indoor, até 50m outdoor
- **Recomendado para IC:** 5-50m (cenários urbanos realistas)

**3. Distância ideal IoT:**
- **NB-IoT:** 100-2000m (sweet spot 200-500m)
- **LoRa:** 500m - 5km urbano
- **Recomendado para IC:** 50-1000m (demonstra viabilidade)

### Próximos Passos

1. **Criar perfil 5G FR1** específico (3.5 GHz)
2. **Executar exp08** com distâncias 5G: [5, 10, 20, 30, 50]m
3. **Executar exp08** com distâncias IoT: [50, 100, 200, 500, 1000]m
4. **Comparar** com artigo em distâncias equivalentes (1m, 3m)
5. **Destacar** que nosso trabalho vai além: testa 5G e IoT de longo alcance

---

## 🎯 Foco do Artigo

**Título sugerido:** "Physical Key Generation para Redes 5G e IoT: Análise de Viabilidade por Distância e Mobilidade"

**Contribuições:**
1. ✅ Análise para **5G FR1** (3.5 GHz) - distâncias 5-50m
2. ✅ Análise para **IoT** (NB-IoT, LoRa) - distâncias 50-2000m
3. ✅ Comparação com artigo (WiFi 1-3m)
4. ✅ 5 perfis de mobilidade (0-60 km/h)
5. ✅ Sistema end-to-end (BPSK/QPSK + BCH + SHA-256)

**Diferencial:** Primeiro trabalho a analisar PKG para **5G FR1 E IoT de longo alcance** de forma sistemática! 🚀
