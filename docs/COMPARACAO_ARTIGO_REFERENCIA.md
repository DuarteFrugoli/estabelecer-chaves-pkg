# Comparação: Artigo de Referência vs. Nosso Trabalho

## Informações do Artigo de Referência

**Título:** Wireless Channel Key Generation for Multi-User Access Scenarios  
**Autores:** Xiaowei Yuan, Yu Jiang, Aiqun Hu, Cheng Guo  
**Instituição:** Southeast University, China  
**Conferência:** IEEE ICCC 2022  
**DOI:** 10.1109/ICCC55456.2022.9880811

---

## 1. RESUMO COMPARATIVO

### 1.1 Artigo de Referência (IEEE ICCC 2022)

**Objetivo Principal:**
- Implementar ferramenta CSI para cenários **multi-usuário** (1 AP + 3 STAs)
- Usar ESP32 para geração de chaves em IoT
- Propor ferramenta "numbered CSI tool" baseada em ESP CSI

**Características:**
- ✅ Arquitetura **multi-usuário** (1 AP, 3 STAs)
- ✅ ESP32 com ferramenta CSI modificada
- ✅ Extração CSI com numeração sequencial
- ✅ 6 cenários experimentais (estático/dinâmico, LOS/NLOS, 1m/3m)
- ✅ Quantização Block-Gray
- ✅ Código corretor BCH
- ❌ Modulação não especificada
- ❌ Modelo de canal não detalhado
- ✅ Testes NIST de aleatoriedade

### 1.2 Nosso Trabalho

**Objetivo Principal:**
- Implementar sistema completo de PKG para **comunicação ponto-a-ponto**
- Usar simulação matemática com canal Rayleigh
- Criar sistema modular educacional com perfis de dispositivos IoT

**Características:**
- ✅ Arquitetura **peer-to-peer** (Alice ↔ Bob)
- ✅ Simulação completa em Python
- ✅ Modulação **BPSK/QPSK** explícita
- ✅ Canal **Rayleigh fading** com correlação temporal
- ✅ Perfis de dispositivos IoT realistas (velocidade, distância, frequência)
- ✅ Quantização limiarizada
- ✅ Código corretor BCH
- ✅ Amplificação de privacidade SHA-256
- ✅ Visualização gráfica (KDR vs SNR)
- ✅ Experimentos automatizados (variação SNR, sigma, modulação, etc.)

---

## 2. COMPARAÇÃO DETALHADA POR COMPONENTE

### 2.1 Arquitetura do Sistema

| Aspecto | Artigo de Referência | Nosso Trabalho |
|---------|---------------------|----------------|
| **Topologia** | 1 AP + 3 STAs (multi-usuário) | Alice ↔ Bob (ponto-a-ponto) |
| **Tipo** | Cenário real com ESP32 | Simulação matemática |
| **Hardware** | ESP32 development boards | Software Python (numpy, matplotlib) |
| **Escalabilidade** | Limitada (capacidade do AP) | Ilimitada (simulação) |
| **Polling** | Group polling para 3 STAs | Não aplicável |
| **Reciprocidade** | Bidirecional (AP ↔ STA) | Bidirecional (Alice ↔ Bob) |

**Análise:**
- **Diferença fundamental:** Artigo foca em **multi-acesso WiFi** (cenário prático IoT), enquanto nosso trabalho foca em **comunicação segura ponto-a-ponto** (modelo teórico).
- **Vantagem do artigo:** Implementação prática com hardware real.
- **Vantagem nossa:** Controle total de parâmetros, reprodutibilidade, educacional.

---

### 2.2 Extração de Características do Canal

| Aspecto | Artigo de Referência | Nosso Trabalho |
|---------|---------------------|----------------|
| **Ferramenta CSI** | ESP32 CSI tool modificado | Modelo matemático Rayleigh |
| **Subportadoras** | 52 efetivas (802.11n) | Não aplicável (simulação) |
| **Informação extraída** | Magnitude CSI (amplitude) | Coeficiente de canal complexo h = α·e^(jθ) |
| **Taxa de amostragem** | 7 pacotes/segundo | Configurável (simulação) |
| **Resolução** | 8 bits (real/imag) | float64 (precisão dupla) |
| **Numeração** | Sequential numbering tool | Não necessário |
| **Estabilidade** | Testado (Fig. 2 do artigo) | Perfeita (simulação determinística) |

**Análise:**
- **Artigo:** Utiliza CSI real extraído de hardware WiFi 802.11n (52 subportadoras OFDM).
- **Nosso trabalho:** Simula canal sem fio Rayleigh com parâmetros físicos realistas.
- **Equivalência:** Magnitude CSI (artigo) ≈ Amplitude do canal |h| (nosso).

---

### 2.3 Modelo de Canal

| Aspecto | Artigo de Referência | Nosso Trabalho |
|---------|---------------------|----------------|
| **Modelo** | Canal WiFi real (não especificado) | Rayleigh fading explícito |
| **Desvanecimento** | Implícito (ambiente indoor) | Rayleigh (h ~ CN(0,σ²)) |
| **Correlação temporal** | Não modelada | Modelo Jakes: ρ(Δt) = exp(-Δt/Tc) |
| **Ruído** | AWGN implícito | AWGN explícito (σ_n² = 1/(2·SNR)) |
| **Doppler** | Não calculado | fD = v·fc/c, Tc = 9/(16π·fD) |
| **Reciprocidade** | Experimental (ρ > 0.95) | Perfeita (h_AB = h_BA) |
| **Cenários** | LOS/NLOS, estático/dinâmico, 1m/3m | Configurable (velocidade, distância) |

**Análise:**
- **Artigo:** Canal real WiFi indoor com reflexões, multipercurso não modelado matematicamente.
- **Nosso trabalho:** Modelo matemático Rayleigh com correlação temporal de Jakes.
- **Vantagem nossa:** Controle completo de parâmetros (SNR, σ, velocidade, Doppler).

---

### 2.4 Modulação

| Aspecto | Artigo de Referência | Nosso Trabalho |
|---------|---------------------|----------------|
| **Modulação digital** | **Não especificada** | BPSK / QPSK |
| **Mapeamento BPSK** | - | 0→+1, 1→-1 |
| **Mapeamento QPSK** | - | Gray coding (00→-1-1j, 01→-1+1j, etc.) |
| **Normalização** | - | QPSK: 1/√2 para Es=1 |
| **Energia por símbolo** | - | Es = 1 (ambas modulações) |
| **Bits por símbolo** | - | BPSK: 1, QPSK: 2 |

**Análise:**
- **Artigo:** Não detalha modulação (provavelmente OFDM 802.11n padrão).
- **Nosso trabalho:** Implementa BPSK e QPSK com mapeamento explícito e normalização de energia.
- **Diferença crítica:** Nossa implementação permite comparar eficiência espectral (BPSK vs QPSK).

---

### 2.5 Quantização

| Aspecto | Artigo de Referência | Nosso Trabalho |
|---------|---------------------|----------------|
| **Algoritmo** | Block-Gray quantization | Quantização limiarizada com histograma |
| **Entrada** | Magnitude CSI (52 subportadoras) | Amplitude do canal \|h\| |
| **Número de bits** | 104 bits (52 × 2 bits) | 1 bit por amostra |
| **Método** | 4 blocos ordenados + Gray coding | Limiar adaptativo (threshold) |
| **Saída** | Chave de 104 bits | Cadeia binária variável |

**Análise:**
- **Block-Gray (artigo):**
  1. Ordena 52 magnitudes CSI
  2. Divide em 4 blocos iguais (13 amostras cada)
  3. Codifica Gray: bloco 1→00, bloco 2→01, bloco 3→11, bloco 4→10
  4. Gera 2 bits por subportadora = 104 bits

- **Limiarizada (nossa):**
  1. Calcula histograma de |h|
  2. Define threshold (ex: mediana, percentil)
  3. |h| > threshold → 1, |h| ≤ threshold → 0
  4. Gera 1 bit por amostra

- **Vantagem do artigo:** Maior taxa de bits (2 bits/amostra).
- **Vantagem nossa:** Simplicidade, ajustável (threshold configurável).

---

### 2.6 Reconciliação de Informação

| Aspecto | Artigo de Referência | Nosso Trabalho |
|---------|---------------------|----------------|
| **Código corretor** | BCH | BCH |
| **Mecanismo** | Alice: c ⊕ K_A → s<br>Bob: s ⊕ K_B → c'<br>Decodifica c' → c | Mesmo princípio |
| **Re-codificação** | Sim (evitar 0s/1s consecutivos) | Não especificada |
| **Parâmetros BCH** | Não especificados | (n=127, k=106, t=3) ou (n=255, k=231, t=3) |
| **KDR antes/depois** | 4.07%-10.61% → ~0% | Variável (depende SNR, sigma) |

**Análise:**
- **Ambos:** Usam código BCH para correção de erros.
- **Artigo:** KDR médio 4.07% (SS1) a 10.61% (DS3).
- **Nosso trabalho:** KDR depende de SNR e sigma (resultados experimentais: convergência para 0% em SNR 11-13dB). KDR @ 9dB: 3.18%-4.70% (compatível com artigo).

---

### 2.7 Amplificação de Privacidade

| Aspecto | Artigo de Referência | Nosso Trabalho |
|---------|---------------------|----------------|
| **Implementado?** | ❌ Não (futuro) | ✅ Sim |
| **Algoritmo** | - | SHA-256 |
| **Entrada** | - | Chave reconciliada (bits) |
| **Saída** | - | Hash 256 bits (32 bytes hex) |
| **Objetivo** | - | Reduzir informação vazada, uniformizar entropia |

**Análise:**
- **Artigo:** Menciona privacy amplification como trabalho futuro.
- **Nosso trabalho:** Implementa SHA-256 completo para gerar chave final criptográfica.

---

### 2.8 Métricas de Avaliação

#### Reciprocidade

| Métrica | Artigo de Referência | Nosso Trabalho |
|---------|---------------------|----------------|
| **Coeficiente** | Pearson: ρ(CSI_AP, CSI_STA) | Implícita (h_AB = h_BA) |
| **Fórmula** | ![Pearson formula](eq1 artigo) | ρ = 1 (simulação perfeita) |
| **Resultados** | ρ ∈ [0.953, 0.994] | ρ = 1.0 (reciprocidade perfeita) |
| **Cenários** | SS1: 0.993, SNS1: 0.983, DS3: 0.965 | Todos: 1.0 |

#### KDR (Key Disagreement Rate)

| Métrica | Artigo de Referência | Nosso Trabalho |
|---------|---------------------|----------------|
| **Definição** | KDR = Σ(K_A[i] ⊕ K_S[i]) / L | Mesma definição |
| **Resultados** | 4.07% (SS1) a 10.61% (DS3) | Depende de SNR/sigma |
| **Após BCH** | ~0% (chaves idênticas) | ~0% (SNR suficiente) |

#### Aleatoriedade

| Métrica | Artigo de Referência | Nosso Trabalho |
|---------|---------------------|----------------|
| **Testes NIST** | ✅ 6 testes (Frequency, Runs, etc.) | ❌ Não implementado |
| **P-value** | > 0.01 (aprovado) | - |
| **Comprimento** | 1000 bits (10 chaves × 100 bits) | - |

#### Anti-Eavesdropping

| Métrica | Artigo de Referência | Nosso Trabalho |
|---------|---------------------|----------------|
| **Teste** | ✅ Eve a 30cm de STA | ❌ Não implementado |
| **Reciprocidade** | ρ(AP,STA)=0.942, ρ(Eve,STA)=0.560 | - |
| **Distância mínima** | λ/2 (meio comprimento de onda) | - |

**Análise:**
- **Artigo:** Validação experimental robusta (NIST + eavesdropping).
- **Nosso trabalho:** Foco em simulação e parametrização, sem validação NIST.

---

### 2.9 Cenários Experimentais

#### Artigo de Referência

| Cenário | Descrição | Distância | ρ médio | KDR médio |
|---------|-----------|-----------|---------|-----------|
| **SS1** | Static Sight 1m | 1m | 0.993 | 4.07% |
| **SNS1** | Static Non-Sight 1m | 1m | 0.983 | - |
| **DS1** | Dynamic Sight 1m | 1m | 0.976 | - |
| **SS3** | Static Sight 3m | 3m | 0.986 | - |
| **SNS3** | Static Non-Sight 3m | 3m | 0.983 | - |
| **DS3** | Dynamic Sight 3m | 3m | 0.965 | 10.61% |

**Configuração:**
- Sala 5m × 4m com mesas/cadeiras
- Dinâmico: pessoa caminhando em "8"
- NLOS: bloqueio por parede

#### Nosso Trabalho

**Perfis de Dispositivos:**

| Perfil | Dispositivo | Velocidade | Distância | Frequência | fc (GHz) | λ (cm) | fD (Hz) | Tc (s) |
|--------|-------------|------------|-----------|------------|----------|--------|---------|--------|
| 1 | Smartphone estático | 0 m/s | 10m | 2.4 GHz | 2.4 | 12.5 | 0 | ∞ |
| 2 | Smartphone movimento lento | 1.5 m/s | 5m | 2.4 GHz | 2.4 | 12.5 | 12 | 0.0149s |
| 3 | Notebook WiFi | 0.5 m/s | 8m | 5 GHz | 5.0 | 6.0 | 8.33 | 0.0214s |
| 4 | Wearable próximo | 2 m/s | 2m | 2.4 GHz | 2.4 | 12.5 | 16 | 0.0112s |
| 5 | Sensor IoT remoto | 0.1 m/s | 50m | 915 MHz | 0.915 | 32.8 | 0.305 | 0.5865s |
| 6 | Manual | Configurável | Configurável | Configurável | - | - | - | - |

**Experimentos Automatizados:**
- `exp01_variacao_snr.py`: SNR de -10 a 30 dB
- `exp02_variacao_sigma.py`: σ de 0.1 a 2.0
- `exp03_comparacao_modulacao.py`: BPSK vs QPSK
- `exp04_variacao_correlacao.py`: Impacto de velocidade/Doppler
- `exp05_variacao_bch.py`: BCH (127,106) vs (255,231)
- `exp06_analise_complexidade.py`: Tempo computacional

---

## 3. CONTRIBUIÇÕES ORIGINAIS

### 3.1 Artigo de Referência

**Inovações:**
1. ✅ **Numbered CSI Tool:** Ferramenta ESP32 modificada para multi-usuário com numeração sequencial
2. ✅ **Multi-user scheme:** Polling de 1 AP + 3 STAs simultâneas
3. ✅ **ESP32 para PKG:** Primeiro trabalho usando ESP CSI tool para geração de chaves
4. ✅ **Block-Gray quantization:** 104 bits/chave (2 bits/subportadora)
5. ✅ **Validação experimental:** 6 cenários (LOS/NLOS, estático/dinâmico, 1m/3m)

**Limitações reconhecidas:**
- Capacidade de processamento limitada do AP
- Necessidade de melhorar privacy amplification

### 3.2 Nosso Trabalho

**Inovações:**
1. ✅ **Modulação explícita:** Implementação completa BPSK/QPSK com mapeamento Gray
2. ✅ **Canal Rayleigh parametrizável:** Modelo matemático com correlação temporal de Jakes
3. ✅ **Perfis de dispositivos IoT:** 5 perfis realistas + configuração manual
4. ✅ **Cálculo Doppler/Tc:** fD = v·fc/c, Tc = 9/(16π·fD), ρ = exp(-Δt/Tc)
5. ✅ **Sistema completo:** Modulação → Canal → Reconciliação → SHA-256
6. ✅ **Visualização gráfica:** Plots KDR vs SNR, BER teórico vs prático
7. ✅ **Experimentos automatizados:** 6 scripts para análise paramétrica
8. ✅ **Interfaces duplas:** CLI básica + GUI avançada
9. ✅ **Educacional:** Documentação completa (FLUXO_COMPLETO.md, TERMS.md, etc.)

---

## 4. SEMELHANÇAS E DIFERENÇAS CHAVE

### 4.1 Semelhanças

| Aspecto | Ambos os trabalhos |
|---------|-------------------|
| **Objetivo** | Geração de chaves criptográficas via canal sem fio |
| **Fundamento** | Reciprocidade do canal (h_AB = h_BA) |
| **Código corretor** | BCH para reconciliação |
| **Métrica KDR** | Key Disagreement Rate |
| **Cenário** | IoT / dispositivos sem fio |

### 4.2 Diferenças Fundamentais

| Aspecto | Artigo de Referência | Nosso Trabalho |
|---------|---------------------|----------------|
| **Abordagem** | Experimental (hardware ESP32) | Simulação (Python) |
| **Cenário** | Multi-usuário (1 AP + 3 STAs) | Ponto-a-ponto (Alice ↔ Bob) |
| **CSI** | Real (52 subportadoras WiFi) | Simulado (canal Rayleigh) |
| **Modulação** | Não especificada | BPSK/QPSK explícito |
| **Canal** | WiFi indoor real | Rayleigh fading matemático |
| **Correlação temporal** | Não modelada | Jakes: ρ = exp(-Δt/Tc) |
| **Doppler** | Não calculado | Calculado (fD = v·fc/c) |
| **Privacy Amplification** | Futuro | SHA-256 implementado |
| **Testes NIST** | Sim | Não |
| **Anti-eavesdropping** | Sim (Eve a 30cm) | Não |
| **Visualização** | Não | Sim (plots KDR, BER) |
| **Perfis IoT** | Não | Sim (5 perfis + manual) |

---

## 5. ANÁLISE CRÍTICA

### 5.1 Vantagens do Artigo de Referência

1. ✅ **Implementação prática:** Hardware real (ESP32) em cenário IoT
2. ✅ **Multi-usuário:** Escalável para 1 AP + múltiplos STAs
3. ✅ **Validação robusta:** NIST randomness + anti-eavesdropping experimental
4. ✅ **Cenários realistas:** LOS/NLOS, estático/dinâmico, paredes
5. ✅ **Numbered CSI tool:** Inovação técnica para sincronização multi-usuário

### 5.2 Vantagens do Nosso Trabalho

1. ✅ **Controle total:** Parâmetros configuráveis (SNR, σ, v, fc, d)
2. ✅ **Reprodutibilidade:** Simulação determinística
3. ✅ **Educacional:** Documentação completa, interfaces gráficas
4. ✅ **Modulação explícita:** BPSK/QPSK com mapeamento detalhado
5. ✅ **Sistema completo:** Modulação → Canal → Reconciliação → SHA-256
6. ✅ **Experimentos automatizados:** 6 scripts parametrizados
7. ✅ **Visualização:** Plots KDR vs SNR, BER teórico vs simulado
8. ✅ **Flexibilidade:** Fácil modificar algoritmos (quantização, BCH, hash)

### 5.3 Limitações Comparativas

#### Artigo de Referência

❌ **Modulação não detalhada:** Não especifica esquema de modulação  
❌ **Canal não modelado:** Não apresenta equações do canal WiFi  
❌ **Privacy amplification:** Não implementado (trabalho futuro)  
❌ **Sem visualização:** Não há plots de desempenho paramétrico  
❌ **Limitado a ESP32:** Dependência de hardware específico  

#### Nosso Trabalho

❌ **Apenas simulação:** Não valida com hardware real  
❌ **Ponto-a-ponto:** Não suporta multi-usuário (1 AP + N STAs)  
❌ **Sem NIST:** Não implementa testes de aleatoriedade  
❌ **Sem anti-eavesdropping:** Não testa segurança contra Eve  
❌ **Canal simplificado:** Rayleigh puro (sem multipercurso OFDM)  

---

## 6. COMPLEMENTARIDADE DOS TRABALHOS

### 6.1 Artigo como Base Prática

O artigo de referência fornece:
- **Validação experimental** de que PKG funciona em hardware IoT real
- **Cenários práticos** (LOS/NLOS, estático/dinâmico)
- **Multi-usuário** para escalabilidade WiFi

### 6.2 Nosso Trabalho como Base Teórica/Educacional

Nosso trabalho fornece:
- **Fundamentos matemáticos** (modulação, canal Rayleigh, Doppler)
- **Simulação parametrizável** para estudo de sensibilidade
- **Sistema completo** (incluindo privacy amplification)
- **Ferramenta educacional** com interfaces e documentação

### 6.3 Integração Possível

**Cenário ideal:**
1. Usar nosso **modelo teórico** para prever desempenho (SNR, KDR)
2. Implementar em **ESP32** seguindo numbered CSI tool do artigo
3. Validar com **NIST** e **anti-eavesdropping** do artigo
4. Adicionar **SHA-256** e **visualização** do nosso trabalho

---

## 7. CONTRIBUIÇÃO PARA ARTIGO DE IC

### 7.1 Elementos do Artigo de Referência a Citar

- **Numbered CSI tool:** Técnica de sincronização multi-usuário
- **Validação NIST:** Metodologia de teste de aleatoriedade
- **Anti-eavesdropping:** Distância mínima λ/2, correlação Eve vs STA
- **Block-Gray quantization:** Algoritmo de 2 bits/amostra
- **Cenários experimentais:** LOS/NLOS, estático/dinâmico

### 7.2 Diferenciação do Nosso Trabalho

**Seção de Metodologia:**
- Apresentar modelo Rayleigh com correlação temporal de Jakes
- Detalhar modulação BPSK/QPSK (não presente no artigo)
- Explicar cálculo Doppler (fD = v·fc/c) e tempo de coerência (Tc)

**Seção de Resultados:**
- Comparar KDR nosso vs artigo (SNR 11-13dB → KDR = 0%, @ 9dB: 3-5% ≈ artigo 4-10%)
- Apresentar experimentos parametrizados (variação SNR, σ, modulação)
- Mostrar visualizações gráficas (KDR vs SNR)

**Seção de Discussão:**
- Contrastar **simulação teórica** (nosso) vs **implementação prática** (artigo)
- Argumentar complementaridade: simulação prevê → implementação valida
- Destacar SHA-256 como contribuição original

### 7.3 Estrutura Sugerida para Artigo IC

```
I. INTRODUÇÃO
   - Contexto: IoT e segurança (citar artigo referência)
   - Problema: Distribuição de chaves em escala (ambos)
   - Solução: PKG via reciprocidade do canal

II. TRABALHOS RELACIONADOS
   - Artigo de referência: ESP32 multi-usuário
   - Outros trabalhos: Linux 802.11n, Atheros CSI
   - Nossa contribuição: Modelo teórico + simulação

III. FUNDAMENTOS TEÓRICOS
   - Modulação BPSK/QPSK (NOSSO)
   - Canal Rayleigh fading (NOSSO)
   - Correlação temporal Jakes (NOSSO)
   - Doppler e Tc (NOSSO)

IV. METODOLOGIA
   A. Modelo de Sistema (NOSSO)
      - Alice ↔ Bob ponto-a-ponto
      - Parâmetros: SNR, σ, v, fc, d
   
   B. Extração de Características
      - Artigo: CSI real (52 subportadoras)
      - Nosso: Amplitude |h| Rayleigh
   
   C. Quantização
      - Artigo: Block-Gray (2 bits/amostra)
      - Nosso: Limiarizada (1 bit/amostra)
   
   D. Reconciliação
      - BCH (ambos)
   
   E. Privacy Amplification
      - Artigo: não implementado
      - Nosso: SHA-256

V. EXPERIMENTOS E RESULTADOS
   A. Variação de SNR (NOSSO)
   B. Variação de σ (NOSSO)
   C. Comparação BPSK vs QPSK (NOSSO)
   D. Impacto de velocidade/Doppler (NOSSO)
   E. Comparação com artigo referência
      - KDR: nosso (SNR 11dB → 0%, @ 9dB: 3-5%) vs artigo (4.07%-10.61% hardware real)
      - Cenários: simulação vs experimental

VI. DISCUSSÃO
   - Simulação vs Hardware
   - Ponto-a-ponto vs Multi-usuário
   - Complementaridade dos trabalhos

VII. CONCLUSÃO
   - Contribuições: modelo teórico, SHA-256, visualização
   - Limitações: sem validação NIST/eavesdropping
   - Trabalho futuro: integrar simulação + ESP32
```

---

## 8. CONCLUSÃO DA COMPARAÇÃO

### 8.1 Resumo Executivo

| Aspecto | Artigo (IEEE ICCC 2022) | Nosso Trabalho |
|---------|------------------------|----------------|
| **Tipo** | Experimental (ESP32) | Simulação (Python) |
| **Topologia** | Multi-usuário (1 AP + 3 STAs) | Ponto-a-ponto (Alice ↔ Bob) |
| **Modulação** | Não especificada | BPSK/QPSK detalhado |
| **Canal** | WiFi real | Rayleigh matemático |
| **Quantização** | Block-Gray (104 bits) | Limiarizada (N bits) |
| **Reconciliação** | BCH | BCH |
| **Privacy Amp.** | Não | SHA-256 |
| **Validação** | NIST + anti-eavesdropping | KDR vs SNR plots |
| **Contribuição** | Numbered CSI tool multi-user | Modelo teórico completo |

### 8.2 Síntese Final

**Artigo de Referência:**
- Foco em **implementação prática** multi-usuário
- Validação experimental robusta
- Limitado em modelagem teórica

**Nosso Trabalho:**
- Foco em **simulação teórica** educacional
- Controle total de parâmetros
- Limitado em validação experimental

**Complementaridade:**
- Artigo fornece **validação de viabilidade prática**
- Nosso trabalho fornece **fundamentos matemáticos e ferramentas de análise**
- Juntos formam base completa: **teoria + prática**

### 8.3 Recomendações para Artigo IC

1. **Citar artigo de referência** para validação experimental de PKG em IoT
2. **Diferenciar contribuição:** modelo teórico Rayleigh + modulação explícita + SHA-256
3. **Argumentar complementaridade:** simulação (nosso) → implementação (futuro, inspirado no artigo)
4. **Destacar originalidade:** perfis IoT, experimentos parametrizados, visualização
5. **Reconhecer limitações:** sem validação NIST/eavesdropping (trabalho futuro)

---

**Documento gerado em:** 2025  
**Autor:** Análise comparativa para IC (Iniciação Científica)  
**Referência:** Yuan et al., "Wireless Channel Key Generation for Multi-User Access Scenarios", IEEE ICCC 2022
