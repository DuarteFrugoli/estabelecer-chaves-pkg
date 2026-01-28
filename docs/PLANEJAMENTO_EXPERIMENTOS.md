# Planejamento de Experimentos - Análise Estatística para Artigo IC

## Data: Janeiro 2026

---

## 1. PERFIS DE DISPOSITIVOS IMPLEMENTADOS

### Resumo dos Perfis Existentes

| # | Perfil | Velocidade | Frequência | Aplicação | Tc | ρ (1ms) |
|---|--------|------------|------------|-----------|-----|---------|
| 1 | **pessoa_andando** | 5 km/h | 2.4 GHz | Wearables | 16.2 ms | 0.940 |
| 2 | **sensor_estatico** | 0 km/h | 868 MHz | Smart home | ∞ | 1.000 |
| 3 | **veiculo_urbano** | 60 km/h | 5.9 GHz | V2X | 0.55 ms | 0.169 |
| 4 | **drone** | 40 km/h | 2.4 GHz | UAV | 2.25 ms | 0.640 |
| 5 | **nb_iot** | 10 km/h | 900 MHz | Smart city | 40.5 ms | 0.975 |

### Detalhamento dos Perfis

#### 1. Pessoa Andando (Wearable)
```python
{
    'descricao': 'Dispositivo vestível em pessoa caminhando (wearable)',
    'erro_estimativa_canal': 0.15,  # 15%
    'velocidade_max_kmh': 5.0,      # Caminhada típica
    'frequencia_portadora_hz': 2.4e9,  # WiFi/Bluetooth/Zigbee
    'taxa_bits_bps': 250e3,         # 250 kbps (IEEE 802.15.4)
    'potencia_transmissao_dbm': 0,  # 1 mW
    'guard_band_sigma': 0.5,
}
```
**Cálculos:**
- fD = (5/3.6) × 2.4e9 / 3e8 = 11.1 Hz
- Tc = 9/(16π × 11.1) ≈ 16.2 ms
- ρ(1ms) = exp(-1/16.2) ≈ 0.940

**Cenário ideal:**
- Distância: 2-10 metros
- Ambiente: Indoor LOS/NLOS
- SNR esperado: 5-15 dB

---

#### 2. Sensor Estático ⭐ (Dispositivo Parado)
```python
{
    'descricao': 'Sensor fixo em ambiente interno (smart home, industrial)',
    'erro_estimativa_canal': 0.08,  # 8% (ambiente controlado)
    'velocidade_max_kmh': 0.0,      # ESTÁTICO
    'frequencia_portadora_hz': 868e6,  # LoRa EU
    'taxa_bits_bps': 50e3,          # 50 kbps
    'potencia_transmissao_dbm': 14, # 25 mW
    'guard_band_sigma': 0.3,
}
```
**Cálculos:**
- fD = 0 Hz (sem Doppler)
- Tc = ∞ (canal estático)
- ρ(τ) = 1.0 para qualquer τ

**Cenário ideal:**
- Distância: 10-100 metros
- Ambiente: Indoor/outdoor estático
- SNR esperado: 3-12 dB
- **Melhor desempenho PKG esperado** (canal constante)

---

#### 3. Veículo Urbano (V2X)
```python
{
    'descricao': 'Dispositivo em veículo urbano (V2X, telemetria)',
    'erro_estimativa_canal': 0.25,  # 25%
    'velocidade_max_kmh': 60.0,     # Velocidade urbana
    'frequencia_portadora_hz': 5.9e9,  # DSRC/C-V2X
    'taxa_bits_bps': 6e6,           # 6 Mbps
    'potencia_transmissao_dbm': 20, # 100 mW
    'guard_band_sigma': 0.8,
}
```
**Cálculos:**
- fD = (60/3.6) × 5.9e9 / 3e8 ≈ 328 Hz
- Tc = 9/(16π × 328) ≈ 0.55 ms
- ρ(1ms) = exp(-1/0.55) ≈ 0.169

**Cenário ideal:**
- Distância: 50-300 metros
- Ambiente: Outdoor urbano
- SNR esperado: 10-25 dB
- **Desempenho PKG desafiador** (canal variável)

---

#### 4. Drone (UAV)
```python
{
    'descricao': 'Drone em voo (UAV)',
    'erro_estimativa_canal': 0.30,  # 30%
    'velocidade_max_kmh': 40.0,     # Velocidade típica
    'frequencia_portadora_hz': 2.4e9,
    'taxa_bits_bps': 1e6,           # 1 Mbps
    'potencia_transmissao_dbm': 20, # 100 mW
    'guard_band_sigma': 1.0,
}
```
**Cálculos:**
- fD = (40/3.6) × 2.4e9 / 3e8 ≈ 88.9 Hz
- Tc = 9/(16π × 88.9) ≈ 2.02 ms
- ρ(1ms) = exp(-1/2.02) ≈ 0.605

**Cenário ideal:**
- Distância: 100-500 metros
- Ambiente: 3D, linha de visada variável
- SNR esperado: 8-20 dB

---

#### 5. NB-IoT (Narrowband IoT)
```python
{
    'descricao': 'Dispositivo NB-IoT (Narrowband IoT, 3GPP)',
    'erro_estimativa_canal': 0.12,  # 12%
    'velocidade_max_kmh': 10.0,     # Mobilidade baixa
    'frequencia_portadora_hz': 900e6,  # 900 MHz
    'taxa_bits_bps': 200e3,         # 200 kbps
    'potencia_transmissao_dbm': 23, # 200 mW
    'guard_band_sigma': 0.4,
}
```
**Cálculos:**
- fD = (10/3.6) × 900e6 / 3e8 ≈ 8.33 Hz
- Tc = 9/(16π × 8.33) ≈ 21.5 ms
- ρ(1ms) = exp(-1/21.5) ≈ 0.954

**Cenário ideal:**
- Distância: 1-10 km
- Ambiente: Urbano/suburbano
- SNR esperado: 0-10 dB

---

## 2. ANÁLISE DOS DOCUMENTOS EXISTENTES

### ✅ Documentos Consistentes

#### COMPARACAO_ARTIGO_REFERENCIA.md
**Status:** ✅ Completo e atualizado
- Comparação detalhada com IEEE ICCC 2022
- Tabelas de diferenças e semelhanças
- Seção de contribuições originais bem definida

#### FLUXO_COMPLETO.md
**Status:** ✅ Completo e preciso
- Descreve todo o sistema passo a passo
- Fórmulas matemáticas corretas
- Exemplos numéricos validados

#### TERMS.md
**Status:** ✅ Glossário completo
- Definições técnicas precisas
- Exemplos práticos
- Alinhado com implementação

#### REFERENCIAS_BIBLIOGRAFICAS.md
**Status:** ✅ Referências acadêmicas sólidas
- Livros clássicos (Goldsmith, Proakis, etc.)
- Artigos seminais (Wyner, Maurer, etc.)
- Adequado para artigo IC

### ⚠️ Documentos que Precisam Revisão

#### ATUALIZACOES_FINAIS.md
**Status:** ⚠️ Parcialmente desatualizado
- Menciona tarefas pendentes (gui_advanced.py)
- Não documenta comparação com artigo de referência
- **Ação:** Atualizar seção de status

#### MELHORIAS_REALISTAS.md
**Status:** ✅ Bem documentado
- Explica erro de estimação, correlação temporal, guard band
- Perfis de dispositivos documentados
- **Ação:** Adicionar seção de resultados esperados

#### PARAMETROS_FREQUENCIA.md
**Status:** ✅ Correto mas incompleto
- Fórmulas de Doppler e Tc corretas
- Falta exemplos com os 5 perfis implementados
- **Ação:** Adicionar tabela com cálculos dos perfis

---

## 3. EXPERIMENTOS IMPLEMENTADOS (1-6)

### Experimentos Existentes

#### EXP01: Variação de SNR
**Arquivo:** `exp01_variacao_snr.py`

**Objetivo:** Testar impacto do SNR no KDR

**Parâmetros fixos:**
- Rayleigh σ = 1/√2
- Correlação ρ = 0.9
- Modulação: BPSK ou QPSK
- BCH: (127, 106, 3)

**Parâmetros variados:**
- SNR: -10 a 30 dB (18 pontos)

**Saída esperada:**
- Gráfico: KDR vs SNR
- Curvas: Antes reconciliação, após reconciliação, após amplificação
- **Resultado chave:** SNR mínimo para KDR < 1%

---

#### EXP02: Variação de σ (Rayleigh)
**Arquivo:** `exp02_variacao_sigma.py`

**Objetivo:** Testar impacto do parâmetro Rayleigh no KDR

**Parâmetros fixos:**
- SNR = 10 dB
- Correlação ρ = 0.9
- Modulação: BPSK

**Parâmetros variados:**
- σ: 0.1 a 2.0 (20 pontos)

**Saída esperada:**
- Gráfico: KDR vs σ
- **Resultado chave:** Valor ótimo de σ (normalizado: 1/√2)

---

#### EXP03: Comparação BPSK vs QPSK
**Arquivo:** `exp03_comparacao_modulacao.py`

**Objetivo:** Comparar desempenho das duas modulações

**Parâmetros fixos:**
- Rayleigh σ = 1/√2
- Correlação ρ = 0.9
- SNR: -10 a 30 dB

**Parâmetros variados:**
- Modulação: BPSK vs QPSK

**Saída esperada:**
- Gráfico: KDR vs SNR (ambas modulações)
- **Resultado chave:** BER similar (Gray coding), eficiência espectral dobrada (QPSK)

---

#### EXP04: Variação de Correlação
**Arquivo:** `exp04_variacao_correlacao.py`

**Objetivo:** Testar impacto da correlação temporal no KDR

**Parâmetros fixos:**
- SNR = 10 dB
- Rayleigh σ = 1/√2
- Modulação: BPSK

**Parâmetros variados:**
- Correlação ρ: 0.0 a 1.0 (21 pontos)

**Saída esperada:**
- Gráfico: KDR vs ρ
- **Resultado chave:** Correlação mínima para PKG viável (ρ > 0.7?)

---

#### EXP05: Variação de BCH
**Arquivo:** `exp05_variacao_bch.py`

**Objetivo:** Comparar diferentes códigos BCH

**Parâmetros fixos:**
- SNR = 10 dB
- Rayleigh σ = 1/√2
- Correlação ρ = 0.9

**Parâmetros variados:**
- BCH: (127, 106, 3) vs (255, 231, 3)

**Saída esperada:**
- Comparação de KDR e taxa de correção
- **Resultado chave:** Trade-off entre overhead e capacidade de correção

---

#### EXP06: Análise de Complexidade
**Arquivo:** `exp06_analise_complexidade.py`

**Objetivo:** Medir tempo computacional vs tamanho da chave

**Parâmetros fixos:**
- SNR = 10 dB
- Rayleigh σ = 1/√2

**Parâmetros variados:**
- Tamanho cadeia: 15, 31, 63, 127, 255, 511 bits

**Saída esperada:**
- Gráfico: Tempo vs tamanho
- Complexidade linear esperada: O(N)

---

## 4. NOVO EXPERIMENTO NECESSÁRIO

### EXP07: Perfis de Dispositivos ⭐

**Objetivo:** Analisar desempenho PKG para cada perfil IoT em diferentes condições

**Arquivo a criar:** `exp07_perfis_dispositivos.py`

#### Estrutura do Experimento

```python
# Para cada perfil de dispositivo:
perfis = ['pessoa_andando', 'sensor_estatico', 'veiculo_urbano', 'drone', 'nb_iot']

# Testar em diferentes condições:
snr_range = np.linspace(-5, 25, 16)  # 16 pontos SNR

# Para cada perfil:
# 1. Extrair parâmetros (erro_estimativa, velocidade, fc, guard_band)
# 2. Calcular Tc, fD, ρ
# 3. Simular PKG com parâmetros realistas
# 4. Medir KDR antes/após reconciliação
```

#### Saídas Esperadas

1. **Gráfico 1:** KDR vs SNR (5 curvas, uma por perfil)
   - Identificar qual perfil tem melhor desempenho
   - Esperado: sensor_estatico > nb_iot > pessoa_andando > drone > veiculo_urbano

2. **Tabela 1:** SNR mínimo para KDR < 1% por perfil

| Perfil | SNR mín (dB) | Tc (ms) | ρ (1ms) | Erro (%) |
|--------|--------------|---------|---------|----------|
| Sensor estático | 3-4 | ∞ | 1.00 | 8% |
| NB-IoT | 4-5 | 21.5 | 0.95 | 12% |
| Pessoa andando | 5-6 | 16.2 | 0.94 | 15% |
| Drone | 7-9 | 2.02 | 0.61 | 30% |
| Veículo urbano | 10-12 | 0.55 | 0.17 | 25% |

3. **Gráfico 2:** Impacto do erro de estimação
   - KDR vs erro_estimativa (0% a 30%)
   - Para SNR fixo (10 dB)

4. **Gráfico 3:** Impacto do guard band
   - KDR vs guard_band_sigma (0.0 a 1.5)
   - Para cada perfil

---

## 5. DESCOBRINDO CONDIÇÕES SATISFATÓRIAS

### Objetivo
**"Descobrir em qual distância e outras condições conseguimos um resultado satisfatório"**

### Definição de "Resultado Satisfatório"
- KDR após reconciliação < 1% (99% de acerto)
- KDR após amplificação ≈ 0% (chave idêntica)
- Taxa de bits adequada (>100 bits por tentativa)

### Análise por Perfil

#### Sensor Estático (Melhor caso)
**Condições para sucesso:**
- SNR ≥ 3 dB
- Distância: 10-100 metros (depende de fc=868MHz)
- Ambiente: Indoor/outdoor sem obstáculos móveis
- **Path loss:** PL(d) = PL(d0) + 10·n·log10(d/d0) + Xσ
  - n ≈ 2-3 (path loss exponent)
  - Para 868 MHz, indoor: ~70-90 dB a 50m

**Relação SNR vs Distância:**
```
SNR(d) = Ptx - PL(d) - N0·B

Para Ptx=14dBm, B=50kHz:
- d=10m: SNR ≈ 12 dB → KDR < 0.1%
- d=50m: SNR ≈ 5 dB → KDR ≈ 7-10% (pré-reconciliação)
- d=100m: SNR ≈ 0 dB → KDR ≈ 16-20% (pré-reconciliação)
- **SNR 11-13 dB necessário para KDR=0% pós-reconciliação**
```

---

#### Pessoa Andando (Wearable)
**Condições para sucesso:**
- SNR ≥ 5 dB
- Distância: 2-10 metros (fc=2.4GHz, indoor)
- Velocidade ≤ 5 km/h (caminhada)
- Ambiente: Indoor com LOS/NLOS misto

**Cenário típico:**
- Smartwatch ↔ Smartphone
- Distância: 2-5 metros
- SNR esperado: 8-15 dB
- **KDR esperado: < 0.5%**

---

#### Veículo Urbano (Pior caso)
**Condições para sucesso:**
- SNR ≥ 10 dB
- Distância: 50-200 metros
- Velocidade ≤ 60 km/h
- Ambiente: Outdoor urbano, LOS

**Desafios:**
- Correlação baixa (ρ=0.17)
- Erro de estimação alto (25%)
- Guard band conservador necessário (0.8σ)

**KDR esperado:**
- SNR=10dB: ~8-12%
- SNR=15dB: ~3-5%
- SNR=20dB: ~1-2%

---

## 6. ROTEIRO DE EXECUÇÃO DOS EXPERIMENTOS

### Fase 1: Preparação (Completa)
- [x] Verificar perfis de dispositivos
- [x] Analisar documentação
- [x] Planejar experimentos

### Fase 2: Criação do EXP07
- [ ] Criar `exp07_perfis_dispositivos.py`
- [ ] Testar localmente com poucos pontos
- [ ] Validar saídas (CSV, JSON, gráficos)

### Fase 3: Execução de Todos os Experimentos
- [ ] Executar exp01 (variação SNR)
- [ ] Executar exp02 (variação sigma)
- [ ] Executar exp03 (BPSK vs QPSK)
- [ ] Executar exp04 (correlação)
- [ ] Executar exp05 (BCH)
- [ ] Executar exp06 (complexidade)
- [ ] Executar exp07 (perfis dispositivos) ⭐

### Fase 4: Análise de Dados
- [ ] Compilar todos os CSVs
- [ ] Gerar gráficos comparativos
- [ ] Criar tabelas estatísticas
- [ ] Calcular intervalos de confiança

### Fase 5: Documentação Final
- [ ] Criar `RESULTADOS_EXPERIMENTAIS.md`
- [ ] Atualizar `ATUALIZACOES_FINAIS.md`
- [ ] Adicionar seção de resultados em `COMPARACAO_ARTIGO_REFERENCIA.md`

---

## 7. MÉTRICAS ESTATÍSTICAS PARA O ARTIGO

### Dados a Coletar

#### Para cada experimento:
1. **KDR médio** (média de N testes)
2. **Desvio padrão do KDR** (variabilidade)
3. **KDR mínimo e máximo** (range)
4. **Taxa de sucesso** (% de casos com KDR<1%)
5. **Tempo de execução** (para análise de complexidade)

#### Formato de saída (CSV):
```csv
experimento,perfil,snr_db,sigma,correlacao,kdr_antes,kdr_pos,kdr_amp,std_kdr,tempo_s
exp07,sensor_estatico,5.0,0.707,1.0,0.023,0.001,0.000,0.005,2.34
exp07,pessoa_andando,5.0,0.707,0.94,0.045,0.008,0.000,0.012,2.41
...
```

### Análise Estatística

#### Teste de Hipóteses
- **H0:** KDR é independente do perfil de dispositivo
- **H1:** Perfis diferentes produzem KDR significativamente diferentes
- **Método:** ANOVA ou Kruskal-Wallis (dependendo da normalidade)

#### Intervalos de Confiança (95%)
```
IC(KDR) = KDR_médio ± 1.96 × (σ_KDR / √N)
```

#### Comparação com Artigo de Referência
| Métrica | Artigo IEEE | Nosso (Simulação) |
|---------|-------------|-------------------|
| KDR (SS1, 1m) | 4.07% | ~3-5% (sensor estático, SNR=10dB) |
| KDR (DS3, 3m) | 10.61% | ~8-12% (pessoa andando, SNR=5dB) |
| Reciprocidade | ρ=0.965-0.993 | ρ=0.94-1.0 (calculado) |

---

## 8. ESTRUTURA DOS RESULTADOS PARA O ARTIGO

### Seção IV: Resultados Experimentais

#### A. Configuração Experimental
- Parâmetros da simulação
- Perfis de dispositivos testados
- Número de testes Monte Carlo (N=1000)

#### B. Impacto do SNR (EXP01)
- **Figura 1:** KDR vs SNR para BPSK
- **Tabela 1:** SNR mínimo para KDR<1% por modulação
- **Análise:** Convergência em SNR ≥ 5dB

#### C. Impacto do Parâmetro Rayleigh (EXP02)
- **Figura 2:** KDR vs σ
- **Resultado:** σ=1/√2 ótimo (normalizado)

#### D. Comparação BPSK vs QPSK (EXP03)
- **Figura 3:** KDR vs SNR (ambas modulações)
- **Conclusão:** Desempenho equivalente, QPSK com 2x eficiência espectral

#### E. Impacto da Correlação Temporal (EXP04)
- **Figura 4:** KDR vs ρ
- **Limite viável:** ρ > 0.7 para KDR<5%

#### F. Análise de Perfis IoT (EXP07) ⭐
- **Figura 5:** KDR vs SNR (5 perfis)
- **Tabela 2:** Comparação de perfis
- **Análise:** Sensor estático tem melhor desempenho

#### G. Complexidade Computacional (EXP06)
- **Figura 6:** Tempo vs tamanho de chave
- **Resultado:** Complexidade O(N) confirmada

---

## 9. PRÓXIMOS PASSOS

### Imediatos
1. ✅ Verificar perfil estático (sensor_estatico já existe com v=0)
2. 🔄 Criar exp07_perfis_dispositivos.py
3. 🔄 Executar todos os 7 experimentos
4. 🔄 Gerar dados CSV/JSON

### Análise
5. Compilar resultados em tabelas
6. Gerar todos os gráficos
7. Calcular estatísticas (média, std, IC)
8. Comparar com artigo de referência

### Documentação
9. Criar RESULTADOS_EXPERIMENTAIS.md
10. Atualizar documentação existente
11. Preparar figuras e tabelas para artigo IC

---

## 10. CONCLUSÃO

### Perfil Estático Existe? ✅
**Sim!** O perfil `sensor_estatico` já implementado tem:
- Velocidade: 0 km/h
- Tc = ∞
- ρ = 1.0
- Erro estimação: 8% (melhor caso)

### Documentação em Ordem? ✅
- FLUXO_COMPLETO.md: ✅ Completo
- TERMS.md: ✅ Preciso
- REFERENCIAS_BIBLIOGRAFICAS.md: ✅ Adequado
- COMPARACAO_ARTIGO_REFERENCIA.md: ✅ Detalhado
- MELHORIAS_REALISTAS.md: ✅ Bem documentado
- PARAMETROS_FREQUENCIA.md: ✅ Correto

### Experimentos Prontos? 🔄
- EXP01-06: ✅ Implementados e atualizados
- EXP07: ❌ **Precisa ser criado**

### Dados Estatísticos? ❌
- Nenhum experimento executado ainda
- Necessário rodar todos e gerar CSVs/JSONs
- **Próximo passo crítico para o artigo**
