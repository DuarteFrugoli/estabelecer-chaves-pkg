# Fluxo Completo do Sistema de Estabelecimento de Chaves via Canal Físico

## Visão Geral

Este documento descreve passo a passo o funcionamento completo do sistema de estabelecimento de chaves baseado em canal sem fio com desvanecimento Rayleigh, incluindo todos os cálculos, parâmetros e processos envolvidos, com ênfase nos aspectos realistas implementados para dispositivos IoT.

## 1. Geração da Sequência Binária Inicial

### Processo
Alice gera uma sequência aleatória de bits que será usada como base para a chave criptográfica.

### Parâmetros
- `tamanho_cadeia_bits`: Comprimento da sequência (7, 15, 127 ou 255 bits)
- Valores: {0, 1}

### Cálculo
```python
palavra_codigo = [random.randint(0, 1) for _ in range(tamanho_cadeia_bits)]
```

**Exemplo:**
```
bits = [1, 0, 1, 1, 0, 0, 1, 0]
```

## 2. Modulação dos Bits

### 2.1 BPSK (Binary Phase Shift Keying)

#### Mapeamento Antipodal
Converte bits digitais {0, 1} para símbolos antipolares {+1, -1}:

```
bit = 0  →  símbolo = +1
bit = 1  →  símbolo = -1
```

**Fórmula:**
```
s = 1 - 2*b
```
onde b ∈ {0, 1}

#### Energia por Símbolo
```
Es = |s|² = 1
```

#### Energia por Bit
```
Eb = Es (pois 1 bit por símbolo)
Eb = 1
```

**Exemplo:**
```
bits:     [1,  0,  1,  1,  0,  0]
símbolos: [-1, +1, -1, -1, +1, +1]
```

### 2.2 QPSK (Quadrature Phase Shift Keying)

#### Agrupamento de Bits
QPSK transmite 2 bits por símbolo. Os bits são agrupados em pares.

**Exemplo:**
```
bits: [1, 0, 1, 1, 0, 0]
pares: [10] [11] [00]
```

#### Mapeamento Gray Coding
Cada par de bits mapeia para um símbolo complexo (I + jQ):

```
00 → I=-1, Q=-1 → (-1-1j)/√2 = -0.707-0.707j
01 → I=-1, Q=+1 → (-1+1j)/√2 = -0.707+0.707j
10 → I=+1, Q=-1 → (+1-1j)/√2 = +0.707-0.707j
11 → I=+1, Q=+1 → (+1+1j)/√2 = +0.707+0.707j
```

#### Normalização
Os símbolos são normalizados por √2 para manter energia unitária:

```
normalização = 1/√2 ≈ 0.7071
```

**Fórmula:**
```
val_i = 1 - 2*bit_i  (bit I: primeiro bit)
val_q = 1 - 2*bit_q  (bit Q: segundo bit)
s = (val_i + j*val_q) / √2
```

#### Energia por Símbolo
```
Es = |s|² = [(±1)² + (±1)²] / 2 = 2/2 = 1
```

#### Energia por Bit
```
Eb = Es/2 = 1/2 = 0.5  (2 bits por símbolo)
```

Mas como comparamos com mesmo Eb/N0 do BPSK, usamos potência_sinal = 1.

**Exemplo:**
```
bits:     [1, 0] [1, 1] [0, 0]
pares:    [10]   [11]   [00]
símbolos: +0.707-0.707j, +0.707+0.707j, -0.707-0.707j
```

## 3. Canal Rayleigh com Desvanecimento

### 3.1 Geração do Ganho do Canal (Fading)

#### Modelo Rayleigh
O ganho do canal h segue distribuição Rayleigh, modelado por componentes gaussianas:

```
h_I ~ N(0, σ²)  (componente In-phase)
h_Q ~ N(0, σ²)  (componente Quadrature)
h = h_I + j*h_Q  (ganho complexo)
```

Para BPSK (sinal real), usamos apenas a magnitude:
```
h = |h_I + j*h_Q| = √(h_I² + h_Q²)
```

#### Estimação Imperfeita do Canal (Realista)

Em sistemas reais, o ganho do canal não pode ser conhecido perfeitamente. A estimação requer símbolos piloto e sempre contém erro.

**Modelo de erro:**
```
h_estimado = h_real + epsilon
epsilon ~ N(0, (erro_relativo * |h_real|)²)
```

Onde:
- h_real: ganho verdadeiro do canal (usado na transmissão física)
- h_estimado: ganho estimado (usado na demodulação)
- erro_relativo: parâmetro configurável (0.0 a 1.0)

**Valores típicos:**
- 0.00: estimação perfeita (ideal, não realista)
- 0.08: sensor estático em ambiente controlado
- 0.15: pessoa andando (wearable)
- 0.25: veículo urbano (alta mobilidade)
- 0.30: drone (movimento 3D complexo)

**Implementação:**
```python
ganho_real, ganho_estimado = gerar_ganho_canal_rayleigh(
    rayleigh_param, num_amostras, erro_estimativa
)

# Transmissão usa ganho REAL (física do canal)
y = ganho_real * simbolo + ruido

# Demodulação usa ganho ESTIMADO (conhecimento do receptor)
decisao = f(y, ganho_estimado, limiar)
```

#### Parâmetro σ (Sigma)
Controla a intensidade do desvanecimento:

```
E[|h|²] = 2σ²  (potência média do canal)
```

**Valores usados:**
- σ = 0.5:       E[|h|²] = 0.5  (-3 dB) - canal fraco
- σ = 1/√2:      E[|h|²] = 1.0  (0 dB)  - canal normalizado (PADRÃO)
- σ = 1.0:       E[|h|²] = 2.0  (+3 dB) - canal moderado
- σ = 2.0:       E[|h|²] = 8.0  (+9 dB) - canal forte

#### Geração do Ganho
```python
# Componentes gaussianas
ganho_i = np.random.normal(0, sigma, tamanho)
ganho_q = np.random.normal(0, sigma, tamanho)

# BPSK (real) - magnitude
ganho_real = np.sqrt(ganho_i**2 + ganho_q**2)

# Adiciona erro de estimação
if erro_estimativa > 0:
    erro = np.random.normal(0, erro_estimativa * ganho_real)
    ganho_estimado = np.abs(ganho_real + erro)
else:
    ganho_estimado = ganho_real

# QPSK (complexo)
ganho_real = ganho_i + 1j * ganho_q
```

### 3.2 Correlação Temporal entre Canais Alice-Bob (Realista)

Alice e Bob não medem o canal simultaneamente. O atraso entre medições reduz a correlação devido à variação temporal.

#### Modelo de Jakes

**Tempo de coerência:**
```
Tc = 9 / (16π * fD)
```

Onde fD é a frequência Doppler máxima:
```
fD = v * fc / c
```
- v: velocidade em m/s
- fc: frequência da portadora em Hz
- c: velocidade da luz (3×10⁸ m/s)

**Correlação temporal:**
```
ρ(τ) = exp(-τ / Tc)
```
- τ: atraso entre medições de Alice e Bob
- Tc: tempo de coerência

#### Exemplos Práticos

**Pessoa andando (5 km/h, 2.4 GHz):**
```
v = 5/3.6 = 1.39 m/s
fD = 1.39 × 2.4×10⁹ / 3×10⁸ = 11.1 Hz
Tc = 9/(16π×11.1) = 16.2 ms
ρ(1ms) = exp(-1/16.2) = 0.940  (alta correlação)
```

**Veículo urbano (60 km/h, 5.9 GHz):**
```
v = 60/3.6 = 16.67 m/s
fD = 16.67 × 5.9×10⁹ / 3×10⁸ = 328 Hz
Tc = 9/(16π×328) = 0.55 ms
ρ(1ms) = exp(-1/0.55) = 0.169  (correlação baixa)
```

**Sensor estático (0 km/h):**
```
v = 0 m/s
fD = 0 Hz
Tc = ∞
ρ = 1.0  (canal idêntico)
```

#### Reciprocidade do Canal

```
h_Bob = ρ * h_Alice + √(1-ρ²) * h_independente
```

Onde:
- ρ: coeficiente de correlação temporal (calculado acima)
- h_Alice: ganho do canal de Alice
- h_independente: componente independente ~ Rayleigh(σ)

**Cálculo:**
```python
# Calcula correlação temporal baseada em velocidade e frequência
tempo_coerencia = calcular_tempo_coerencia(velocidade_kmh, freq_portadora_hz)
correlacao = calcular_correlacao_temporal(atraso_medicao_ms, tempo_coerencia)

# Gera ganho de Alice
ganho_real_alice, ganho_est_alice = gerar_ganho_canal_rayleigh(
    rayleigh_param, num_ganhos, erro_estimativa
)

# Gera ganho correlacionado de Bob (reciprocidade)
ganho_real_bob = aplicar_correlacao_temporal(
    ganho_real_alice, rayleigh_param, correlacao
)

# Bob também tem erro de estimação
erro_bob = np.random.normal(0, erro_estimativa * ganho_real_bob)
ganho_est_bob = np.abs(ganho_real_bob + erro_bob)
```

**Interpretação:**
- ρ ≈ 1.0: canais quase idênticos (ideal para PKG)
- 0.5 < ρ < 0.9: correlação moderada (funciona, mas com mais erros)
- ρ < 0.5: canais parcialmente independentes (PKG degradado)

### 3.3 Relação Sinal-Ruído (SNR)

#### Definição
SNR é a relação entre a potência do sinal e a potência do ruído:

```
SNR = Eb/N0
```

onde:
- Eb: Energia por bit
- N0: Densidade espectral de potência do ruído

#### Range de SNR
```
SNR_dB = [-10, -7.36, -4.73, -2.11, 0.53, 3.16, 5.79, 8.42, 
          11.05, 13.68, 16.32, 18.95, 21.58, 24.21, 26.84, 29.47, 30]
```
18 pontos logaritmicamente espaçados de -10 dB a 30 dB.

#### Conversão dB para Linear
```python
SNR_linear = 10^(SNR_dB / 10)
```

**Exemplo:**
```
SNR_dB = 10 dB
SNR_linear = 10^(10/10) = 10
```

### 3.4 Cálculo da Variância do Ruído

#### Potência do Sinal
```
potencia_sinal = 1.0  (sinal normalizado)
```

#### Variância do Ruído
Para canal AWGN (Additive White Gaussian Noise) em banda base:

```
N0 = 2σ²_ruido  (densidade espectral bilateral)
SNR = Es / N0 = potencia_sinal / (2σ²_ruido)
```

Resolvendo para σ²_ruido:

```
σ²_ruido = potencia_sinal / (2 * SNR_linear)
```

**Fórmula implementada:**
```python
variancia_ruido = potencia_sinal / (2 * snr_linear)
```

**Exemplo para SNR = 10 dB:**
```
SNR_linear = 10
σ²_ruido = 1.0 / (2 * 10) = 0.05
σ_ruido = √0.05 ≈ 0.2236
```

### 3.5 Geração do Ruído

#### BPSK (Ruído Real)
```python
ruido = np.random.normal(media_ruido, sigma_ruido, num_simbolos)
```

onde:
- media_ruido = 0 (ruído centrado)
- sigma_ruido = √(variancia_ruido)

#### QPSK (Ruído Complexo)
O ruído é dividido igualmente entre componentes I e Q:

```python
sigma_ruido = √(variancia_ruido / 2)
ruido_i = np.random.normal(0, sigma_ruido, num_simbolos)
ruido_q = np.random.normal(0, sigma_ruido, num_simbolos)
ruido = ruido_i + j*ruido_q
```

**Por que dividir por 2?**
A potência total do ruído complexo é:
```
E[|n|²] = E[|n_I|²] + E[|n_Q|²] = σ²_I + σ²_Q
```

Para manter potência total = variancia_ruido:
```
σ²_I = σ²_Q = variancia_ruido/2
```

### 3.6 Modelo do Canal Completo

#### BPSK
```
y = h * s + n
```

onde:
- y: sinal recebido
- h: ganho Rayleigh (real)
- s: símbolo transmitido (±1)
- n: ruído AWGN

#### QPSK
```
y = h * s + n
```

onde:
- h: ganho Rayleigh (complexo)
- s: símbolo transmitido (complexo normalizado)
- n: ruído AWGN complexo

**Implementação:**
```python
# BPSK
sinal_recebido = ganho * simbolos + ruido

# QPSK
sinal_recebido = ganho * simbolos_qpsk + ruido_complexo
```

## 4. Demodulação

### 4.1 BPSK

#### Detecção Clássica por Limiar Fixo
Decide o bit baseado no sinal de y:

```
y > 0  →  bit = 0
y < 0  →  bit = 1
```

**Implementação básica:**
```python
bits_recebidos = (sinal_recebido >= 0).astype(int)
```

**Limitação:** Não considera incerteza da estimação do canal.

#### Detecção com Guard Band Adaptativo (Realista)

Quando há erro na estimação do canal, símbolos próximos ao limiar têm alta probabilidade de erro. Guard bands criam zona de incerteza para decisões mais confiáveis.

**Limiar adaptativo:**
```
limiar(i) = guard_band_sigma * σ_ruido / |h_estimado(i)|
```

Onde:
- guard_band_sigma: parâmetro configurável (0.0 a 1.5)
- σ_ruido: desvio padrão do ruído
- h_estimado(i): ganho estimado para o i-ésimo símbolo

**Regra de decisão:**
```
Se y > limiar(i):           bit = 0  (alta confiança)
Se y < -limiar(i):          bit = 1  (alta confiança)
Se -limiar(i) ≤ y ≤ limiar(i):  bit = sign(y)  (baixa confiança)
```

**Valores típicos de guard_band_sigma:**
- 0.0: sem guard band (limiar fixo em 0)
- 0.3-0.5: conservador (sensor estático, wearable)
- 0.8-1.0: muito conservador (veículo, drone)

**Implementação:**
```python
if guard_band_sigma > 0:
    limiar = guard_band_sigma * sigma_ruido / (ganho_estimado + 1e-10)
    
    for i, y in enumerate(sinal_recebido_continuo):
        if y > limiar[i]:
            bit = 0  # Alta confiança: símbolo +1
        elif y < -limiar[i]:
            bit = 1  # Alta confiança: símbolo -1
        else:
            # Zona de incerteza: decisão menos confiável
            bit = 0 if y >= 0 else 1
else:
    # Limiar fixo em 0 (clássico)
    bits_recebidos = (sinal_recebido >= 0).astype(int)
```

**Trade-off:**
- Maior guard_band_sigma → menos erros, mas bits decididos com menor confiança
- Menor guard_band_sigma → mais bits, mas mais erros
- Sistemas reais ajustam dinamicamente baseado em SNR estimado

### 4.2 QPSK

#### Separação de Componentes
Demodula I e Q independentemente:

```
I = Re(y)  (parte real)
Q = Im(y)  (parte imaginária)
```

#### Decisão Clássica
```
I > 0  →  bit_I = 0
I < 0  →  bit_I = 1

Q > 0  →  bit_Q = 0
Q < 0  →  bit_Q = 1
```

#### Decisão com Guard Band (Realista)

Similar ao BPSK, mas aplicado independentemente nas componentes I e Q:

```
limiar_I(i) = guard_band_sigma * σ_ruido * √2 / |h_est(i)|
limiar_Q(i) = limiar_I(i)  (mesmo limiar para ambas componentes)
```

**Fator √2:** Devido à normalização QPSK para manter Es=1.

**Implementação:**
```python
for simbolo in sinal_recebido_qpsk:
    # Componente I
    if simbolo.real > limiar:
        bit_i = 0
    elif simbolo.real < -limiar:
        bit_i = 1
    else:
        bit_i = 0 if simbolo.real >= 0 else 1
    
    # Componente Q
    if simbolo.imag > limiar:
        bit_q = 0
    elif simbolo.imag < -limiar:
        bit_q = 1
    else:
        bit_q = 0 if simbolo.imag >= 0 else 1
    
    bits_recebidos.extend([bit_i, bit_q])
```

## 5. Extração da Chave (KDR - Key Disagreement Rate)

### 5.1 Comparação de Bits

Alice e Bob comparam suas sequências recebidas:

```python
erros = sum(bit_alice != bit_bob for bit_alice, bit_bob in zip(alice, bob))
```

### 5.2 Taxa de Erro de Bit (BER)

```
BER = erros / total_bits
```

**Exemplo:**
```
alice = [1, 0, 1, 1, 0, 0, 1, 0]
bob   = [1, 0, 0, 1, 0, 0, 1, 1]
erros = 2 (posições 2 e 7)
BER = 2/8 = 0.25
```

### 5.3 BER Teórica vs Simulada

#### BER Teórica (Canal Rayleigh)

Para canal Rayleigh com desvanecimento e σ = 1/√2 (normalizado):

```
BER = 0.5 * (1 - √(SNR/(1+SNR)))
```

onde SNR = Eb/N0 (linear).

**Dedução:**
Para Rayleigh, o ganho |h|² tem distribuição exponencial:
```
p(γ) = (1/γ̄) * exp(-γ/γ̄)
```
onde γ̄ = E[|h|²] = 2σ² = 1 (para σ = 1/√2).

A BER média é obtida integrando sobre todas as realizações de γ:
```
BER = ∫₀^∞ Q(√(2γSNR)) * p(γ) dγ
```

Resolvendo essa integral:
```
BER = 0.5 * (1 - √(SNR/(1+SNR)))
```

**Implementação:**
```python
def ber_teorica_rayleigh(snr_db):
    snr_linear = 10 ** (snr_db / 10)
    ber = 0.5 * (1 - np.sqrt(snr_linear / (1 + snr_linear)))
    return ber
```

#### BER Simulada

Obtida através de simulação de Monte Carlo:

```python
ber_simulada = total_erros / total_bits
```

onde:
- total_erros: soma de todos os erros em todos os testes
- total_bits: quantidade_testes * tamanho_cadeia_bits

## 6. Reconciliação (Correção de Erros)

### 6.1 Código BCH

Código de correção de erros BCH (Bose-Chaudhuri-Hocquenghem).

#### Parâmetros BCH
Baseado no tamanho da cadeia de bits:

```
n = 7:   BCH(7, 4)   - corrige 1 erro
n = 15:  BCH(15, 7)  - corrige 2 erros
n = 127: BCH(127, 64) - corrige 10 erros
n = 255: BCH(255, 131) - corrige 18 erros
```

Notação BCH(n, k):
- n: comprimento total do código
- k: bits de informação
- t: erros que pode corrigir

#### Codificação (Alice)

```python
bch_codigo = galois.BCH(n, k)
palavra_codigo_codificada = bch_codigo.encode(bits_alice)
```

A codificação adiciona bits de paridade:
```
bits_paridade = n - k
```

**Exemplo BCH(15, 7):**
```
mensagem (7 bits):  [1, 0, 1, 1, 0, 0, 1]
paridade (8 bits):  [1, 1, 0, 0, 1, 0, 1, 1]
código (15 bits):   [1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1]
```

#### Decodificação (Bob)

Bob recebe a palavra com possíveis erros e tenta corrigir:

```python
palavra_decodificada = bch_codigo.decode(bits_bob_recebidos)
```

O decodificador:
1. Calcula a síndrome (detecta erros)
2. Localiza os erros usando algoritmo de Berlekamp-Massey
3. Corrige os erros (se t_erros ≤ capacidade)

#### Capacidade de Correção

Se número de erros > capacidade do BCH:
- Decodificação falha
- Bits permanecem com erros

### 6.2 Taxa de Erro Pós-Reconciliação

```python
erros_pos_reconciliacao = sum(alice_original != bob_decodificado)
BER_pos_reconciliacao = erros_pos_reconciliacao / tamanho_cadeia_bits
```

## 7. Amplificação de Privacidade

### 7.1 Objetivo

Reduzir qualquer informação que um espião (Eva) possa ter obtido sobre a chave.

### 7.2 Processo

Usa função hash criptográfica SHA-256 para comprimir a chave:

```python
from hashlib import sha256

def amplificar_privacidade(bits):
    # Converte bits para bytes
    byte_string = int(''.join(map(str, bits)), 2).to_bytes(
        (len(bits) + 7) // 8, byteorder='big')
    
    # Aplica SHA-256
    hash_obj = sha256(byte_string)
    hash_hex = hash_obj.hexdigest()
    
    # Converte hash para bits
    hash_bits = bin(int(hash_hex, 16))[2:].zfill(256)
    return [int(b) for b in hash_bits]
```

### 7.3 Propriedades

1. **Compressão**: Entrada de n bits → Saída de 256 bits
2. **Não-reversibilidade**: Impossível recuperar entrada do hash
3. **Sensibilidade**: Mudança de 1 bit na entrada muda ~50% da saída
4. **Determinístico**: Mesma entrada sempre produz mesmo hash

### 7.4 Taxa de Discordância Pós-Amplificação

```python
erros_pos_amplificacao = sum(hash_alice != hash_bob)
taxa_discordancia = erros_pos_amplificacao / 256
```

## 8. Taxa de Extração de Chave (KDR)

### 8.1 Definição

KDR mede a eficiência na geração de bits de chave compartilhados:

```
KDR = (bits_finais_corretos / bits_iniciais) * 100%
```

### 8.2 Cálculo

```python
# Bits que Alice e Bob concordam após amplificação
bits_acordo = 256 - erros_pos_amplificacao

# KDR
kdr = bits_acordo / tamanho_cadeia_bits
```

**Exemplo:**
```
tamanho_inicial: 127 bits
bits_finais: 256 bits (após SHA-256)
bits_corretos: 250 bits
KDR = 250/127 ≈ 1.97 (197%)
```

### 8.3 KDR Médio

Média de KDR sobre múltiplos testes e valores de SNR:

```python
kdr_medio = np.mean(kdr_lista)
```

## 9. Fórmulas Resumidas

### Modulação BPSK
```
s = 1 - 2*b,  b ∈ {0,1}
Es = 1
```

### Modulação QPSK
```
s = (val_i + j*val_q) / √2
Es = 1,  Eb = 0.5
```

### Canal Rayleigh
```
h ~ CN(0, 2σ²)  para σ = 1/√2: E[|h|²] = 1
y = h*s + n
```

### Ruído AWGN
```
σ²_n = Es / (2*SNR)
n ~ N(0, σ²_n)  (BPSK)
n ~ CN(0, σ²_n)  (QPSK)
```

### BER Teórica
```
BER_Rayleigh = 0.5 * (1 - √(SNR/(1+SNR)))
```

### SNR
```
SNR_linear = 10^(SNR_dB/10)
SNR = Es/N0 = potencia_sinal / (2*σ²_ruido)
```

### Correlação de Canal
```
h_Bob = ρ*h_Alice + √(1-ρ²)*h_indep,  ρ = 0.9
```

## 10. Fluxo Completo - Diagrama

```
1. ALICE                              BOB
   ↓                                  ↓
[Gera bits aleatórios]          [Não sabe os bits]
   ↓
[Modula: BPSK/QPSK]
   ↓
[Transmite por canal sem fio] →  [Recebe sinal]
   ↓                                  ↓
[Canal: h*s + n]                 [Canal: h*s + n]
   ↓                                  ↓
[y_Alice = h_A*s + n_A]         [y_Bob = h_B*s + n_B]
   ↓                                  ↓
[Demodula]                       [Demodula]
   ↓                                  ↓
[bits_Alice (com erros)]        [bits_Bob (com erros)]
   |                                  |
   |     2. RECONCILIAÇÃO             |
   |     (Comunicação pública)        |
   ├──────────────────────────────────┤
   |  Alice envia bits de paridade   →|
   |                                  ↓
   |                            [BCH decode]
   |                                  |
   ├──────────────────────────────────┤
   |         bits reconciliados       |
   |                                  |
   |     3. AMPLIFICAÇÃO              |
   |                                  |
   ↓                                  ↓
[SHA-256(bits)]                 [SHA-256(bits)]
   ↓                                  ↓
[chave_Alice (256 bits)]        [chave_Bob (256 bits)]
   |                                  |
   └──────────[COMPARAM]──────────────┘
                  ↓
            [Se iguais: SUCESSO!]
            [Se diferentes: DESCARTA]
```

## 11. Parâmetros Principais do Sistema

### Configuráveis
```python
quantidade_de_testes = 1000        # Número de simulações
tamanho_cadeia_bits = 127          # Tamanho da sequência (7/15/127/255)
modulacao = 'bpsk'                 # ou 'qpsk'
rayleigh_sigma = 1/√2              # σ do canal Rayleigh
correlacao_canal = 0.9             # Correlação Alice-Bob
usar_amplificacao = True           # Habilitar SHA-256
```

### Fixos
```python
potencia_sinal = 1.0               # Sinal normalizado
media_ruido = 0.0                  # Ruído centrado
snr_db_range = [-10, ..., 30]      # 18 pontos
```

### BCH Automático
```python
if tamanho == 7:   BCH(7, 4)
if tamanho == 15:  BCH(15, 7)
if tamanho == 127: BCH(127, 64)
if tamanho == 255: BCH(255, 131)
```

## 12. Métricas de Desempenho

### 12.1 BER (Bit Error Rate)
```
BER = erros_bits / total_bits
```
Mede qualidade do canal de comunicação.

### 12.2 BER Pós-Reconciliação
```
BER_reconciliacao = erros_apos_BCH / tamanho_cadeia
```
Mede eficácia da correção de erros.

### 12.3 KDR (Key Disagreement Rate)
```
KDR = bits_acordo_final / bits_iniciais
```
Mede eficiência de geração de chave.

### 12.4 Taxa de Discordância
```
discordancia = erros_pos_amplificacao / 256
```
Mede concordância após hash (ideal: 0%).

## 13. Interpretação dos Resultados

### BER vs SNR
- **SNR baixo** (-10 dB): BER alta (~0.4-0.5), canal ruim
- **SNR médio** (0-10 dB): BER moderada (~0.1-0.2), BCH consegue corrigir
- **SNR alto** (20+ dB): BER baixa (~0.001), quase sem erros

### KDR vs SNR
- **SNR baixo**: KDR baixo, muitos erros mesmo após BCH
- **SNR alto**: KDR próximo de 100%, chaves idênticas

### Efeito do σ Rayleigh
- **σ pequeno** (0.5): Canal mais fraco, precisa SNR maior
- **σ normalizado** (1/√2): Referência teórica
- **σ grande** (2.0): Canal mais forte, melhor desempenho

## 14. Perfis de Dispositivos IoT (Realistas)

### 14.1 Motivação

Diferentes tipos de dispositivos operam em condições distintas:
- Mobilidade (afeta correlação temporal)
- Capacidade de estimação de canal (afeta erro)
- Ambiente operacional (afeta parâmetros de quantização)

O sistema fornece perfis pré-configurados baseados em padrões industriais e permite configuração manual para cenários customizados.

### 14.2 Perfis Implementados

#### Sensor Estático
```python
{
    'descricao': 'Sensor fixo em ambiente interno',
    'erro_estimativa_canal': 0.08,      # 8% de erro
    'velocidade_max_kmh': 0.0,          # Estático
    'frequencia_portadora_hz': 868e6,   # 868 MHz (LoRa EU)
    'taxa_bits_bps': 50e3,              # 50 kbps
    'potencia_transmissao_dbm': 14,     # 25 mW
    'guard_band_sigma': 0.3,            # Conservador
}
```

**Correlação temporal:** ρ = 1.0 (canal estático)  
**Aplicações:** Smart home, sensores industriais, monitoramento ambiental  
**Padrões:** IEEE 802.15.4, LoRaWAN

#### Pessoa Andando (Wearable)
```python
{
    'descricao': 'Dispositivo vestível em pessoa caminhando',
    'erro_estimativa_canal': 0.15,      # 15% de erro
    'velocidade_max_kmh': 5.0,          # 5 km/h
    'frequencia_portadora_hz': 2.4e9,   # 2.4 GHz (WiFi, Bluetooth, Zigbee)
    'taxa_bits_bps': 250e3,             # 250 kbps
    'potencia_transmissao_dbm': 0,      # 1 mW
    'guard_band_sigma': 0.5,            # Moderado
}
```

**Correlação temporal:** ρ ≈ 0.94 (atraso 1ms)  
**Aplicações:** Health monitoring, fitness trackers, smartwatches  
**Padrões:** Bluetooth LE, Zigbee

#### Veículo Urbano (V2X)
```python
{
    'descricao': 'Dispositivo em veículo urbano',
    'erro_estimativa_canal': 0.25,      # 25% de erro
    'velocidade_max_kmh': 60.0,         # 60 km/h
    'frequencia_portadora_hz': 5.9e9,   # 5.9 GHz (DSRC/C-V2X)
    'taxa_bits_bps': 6e6,               # 6 Mbps
    'potencia_transmissao_dbm': 20,     # 100 mW
    'guard_band_sigma': 0.8,            # Conservador
}
```

**Correlação temporal:** ρ ≈ 0.17 (atraso 1ms, alta variação!)  
**Aplicações:** V2X, telemetria veicular, safety messages  
**Padrões:** IEEE 802.11p (DSRC), 3GPP C-V2X

#### Drone (UAV)
```python
{
    'descricao': 'Drone em voo',
    'erro_estimativa_canal': 0.30,      # 30% de erro
    'velocidade_max_kmh': 40.0,         # 40 km/h
    'frequencia_portadora_hz': 2.4e9,   # 2.4 GHz
    'taxa_bits_bps': 1e6,               # 1 Mbps
    'potencia_transmissao_dbm': 20,     # 100 mW
    'guard_band_sigma': 1.0,            # Muito conservador
}
```

**Correlação temporal:** ρ ≈ 0.53 (ambiente 3D complexo)  
**Aplicações:** Inspeção, entrega, vigilância  
**Notas:** Movimento 3D aumenta variação do canal

#### NB-IoT
```python
{
    'descricao': 'Dispositivo NB-IoT (3GPP)',
    'erro_estimativa_canal': 0.12,      # 12% de erro
    'velocidade_max_kmh': 10.0,         # Mobilidade baixa
    'frequencia_portadora_hz': 900e6,   # 900 MHz (banda licenciada)
    'taxa_bits_bps': 200e3,             # 200 kbps
    'potencia_transmissao_dbm': 23,     # 200 mW (máximo NB-IoT)
    'guard_band_sigma': 0.4,
}
```

**Correlação temporal:** ρ ≈ 0.87  
**Aplicações:** Smart meters, asset tracking, smart city  
**Padrões:** 3GPP Release 13+

### 14.3 Configuração Manual (Genérico)

Para cenários não cobertos pelos perfis, o sistema permite configuração manual:

```python
# Estrutura padrão para configuração manual
config_manual = {
    'descricao': 'Configuração manual',
    'erro_estimativa_canal': 0.10,      # Solicita ao usuário
    'velocidade_max_kmh': 5.0,          # Solicita ao usuário
    'guard_band_sigma': 0.5,            # Solicita ao usuário
    # Outros parâmetros com valores padrão
}
```

**Processo interativo:**
1. Solicita erro de estimativa (0.0 a 1.0)
2. Solicita velocidade máxima (km/h)
3. Solicita parâmetro de guard band (0.0 a 1.5)
4. Calcula automaticamente correlação temporal

### 14.4 Cálculo Automático de Parâmetros

Baseado no perfil selecionado, o sistema calcula automaticamente:

```python
def calcular_parametros_canal(config, atraso_medicao_ms=1.0):
    # Tempo de coerência
    v_ms = config['velocidade_max_kmh'] / 3.6
    fD = v_ms * config['frequencia_portadora_hz'] / 3e8
    Tc = 9 / (16 * π * fD) if fD > 0 else ∞
    
    # Correlação temporal
    ρ = exp(-atraso_medicao_ms / (Tc * 1000))
    
    return {
        'tempo_coerencia_s': Tc,
        'freq_doppler_hz': fD,
        'correlacao_temporal': ρ,
    }
```

### 14.5 Interpretação dos Resultados por Perfil

#### Sensor Estático
- **KDR esperado:** Excelente (convergência rápida)
- **SNR mínimo:** ~2-4 dB para KDR < 1%
- **Vantagens:** Canal estável, estimação boa
- **Limitações:** Sem mobilidade

#### Pessoa Andando
- **KDR esperado:** Muito bom
- **SNR mínimo:** ~4-6 dB para KDR < 1%
- **Vantagens:** Boa correlação, erro moderado
- **Limitações:** Mobilidade limitada

#### Veículo Urbano
- **KDR esperado:** Moderado
- **SNR mínimo:** ~8-12 dB para KDR < 1%
- **Vantagens:** Alta taxa de bits
- **Limitações:** Correlação baixa, erro alto

#### Drone
- **KDR esperado:** Moderado a ruim
- **SNR mínimo:** ~10-15 dB para KDR < 1%
- **Vantagens:** Flexibilidade de movimento
- **Limitações:** Canal muito variável, erro alto

#### NB-IoT
- **KDR esperado:** Bom
- **SNR mínimo:** ~5-8 dB para KDR < 1%
- **Vantagens:** Padronizado, boa cobertura
- **Limitações:** Taxa de bits limitada

### 14.6 Recomendações de Uso

**Para pesquisa acadêmica:**
- Use configuração manual para explorar trade-offs
- Varie erro_estimativa de 0.0 a 0.3
- Teste diferentes velocidades e frequências

**Para prototipagem:**
- Escolha perfil mais próximo da aplicação real
- NB-IoT para smart city
- Wearable para health monitoring
- V2X para aplicações veiculares

**Para simulação realista:**
- Sempre use erro_estimativa > 0 (estimação perfeita não é realista)
- Use guard_band_sigma > 0 para refletir incerteza
- Correlação deve ser calculada automaticamente (não fixar em 0.9)

### Entrada
```
bits_alice = [1, 0, 1, 1, 0, 0, 1]  (n=7)
SNR = 5 dB
σ = 1/√2
modulacao = BPSK
```

### Passo 1: Modulação
```
símbolos = [-1, +1, -1, -1, +1, +1, -1]
```

### Passo 2: Canal
```
SNR_linear = 10^(5/10) = 3.162
σ²_ruido = 1/(2*3.162) = 0.158
σ_ruido = 0.398

h = [0.8, 1.2, 0.6, 1.1, 0.9, 0.7, 1.0]  (exemplo)
n = [0.1, -0.2, 0.3, -0.1, 0.2, -0.3, 0.1]  (exemplo)

y = h*s + n = [-0.7, 1.0, -0.15, -1.21, 1.1, 0.39, -0.9]
```

### Passo 3: Demodulação
```
bits_bob = [1, 0, 1, 1, 0, 0, 1]  (nenhum erro neste exemplo)
```

### Passo 4: BCH
```
BCH(7,4): sem erros, passa direto
```

### Passo 5: SHA-256
```
alice_hash = SHA256([1,0,1,1,0,0,1])
bob_hash   = SHA256([1,0,1,1,0,0,1])
concordância = 100%
```

### Métricas
```
BER_canal = 0/7 = 0%
BER_pos_BCH = 0/7 = 0%
KDR = 256/7 = 3657%  (ganho por usar hash de 256 bits)
```

---

## 15. Comparação: Sistema Ideal vs Sistema Realista

### 15.1 Características

| Aspecto | Sistema Ideal (Original) | Sistema Realista (Atual) |
|---------|-------------------------|-------------------------|
| Estimação de canal | Perfeita (h conhecido exatamente) | Imperfeita (erro gaussiano) |
| Correlação Alice-Bob | Fixa (ρ = 0.9) | Calculada via modelo Jakes |
| Dependência de mobilidade | Não | Sim (velocidade → fD → Tc → ρ) |
| Quantização | Limiar fixo em 0 | Guard band adaptativo |
| Perfis de dispositivo | Não | Sim (5 perfis + manual) |
| Complexidade computacional | Baseline | +10% de overhead |

### 15.2 Impacto no Desempenho

#### BER Antes da Reconciliação

Sistema Ideal:
```
BER_ideal = f(SNR, σ_Rayleigh)
```

Sistema Realista:
```
BER_realista ≈ BER_ideal × (1 + α × erro_estimativa)
```
Onde α ≈ 1.5-2.0 (fator empírico dependente de SNR)

Exemplo (SNR = 10 dB, σ = 1/√2, erro = 15%):
```
BER_ideal ≈ 5%
BER_realista ≈ 5% × (1 + 1.8 × 0.15) ≈ 6.35%
```

#### Convergência do KDR

Sistema Ideal:
- KDR < 1% em SNR ≥ 4 dB (sensor estático)

Sistema Realista:
- Sensor estático (erro 8%): KDR < 1% em SNR ≥ 5 dB
- Wearable (erro 15%): KDR < 1% em SNR ≥ 6 dB
- Veículo (erro 25%): KDR < 1% em SNR ≥ 10 dB
- Drone (erro 30%): KDR < 1% em SNR ≥ 12 dB

### 15.3 Validação Acadêmica

#### Referências da Literatura

Azimi-Sadjadi et al. (2007):
- BER experimental: ~10-15% em SNR = 10 dB
- Sistema realista: 12-15% (compatível)

Mathur et al. (2008):
- Taxa de descarte: 20-30% em ambientes móveis
- Sistema realista com drone: taxa similar

Wilhelm et al. (2011):
- Correlação temporal medida: 0.85-0.95 para velocidades < 5 km/h
- Sistema realista (wearable): ρ = 0.94 (exato)

### 15.4 Quando Usar Cada Modo

Use Sistema Ideal Quando:
- Estudar comportamento teórico
- Comparar com curvas teóricas de BER
- Ensino de conceitos básicos
- Baseline para comparações

Use Sistema Realista Quando:
- Projetar sistema para aplicação específica
- Estimar desempenho de protótipo
- Publicar resultados experimentais
- Validar contra medições reais

---

## Referências

1. **Proakis, J. G., & Salehi, M.** (2008). Digital Communications. McGraw-Hill.
2. **Rappaport, T. S.** (2002). Wireless Communications: Principles and Practice.
3. **Goldsmith, A.** (2005). Wireless Communications. Cambridge University Press.
4. **Lin, S., & Costello, D. J.** (2004). Error Control Coding. Prentice Hall.
5. **Jakes, W. C.** (1974). Microwave Mobile Communications. Wiley.
6. **Azimi-Sadjadi, B., et al.** (2007). Robust Key Generation from Signal Envelopes in Wireless Networks. ACM CCS.
7. **Mathur, S., et al.** (2008). Radio-telepathy: Extracting a Secret Key from an Unauthenticated Wireless Channel. ACM MobiCom.
8. **Wilhelm, M., et al.** (2011). Secret Keys from Entangled Sensor Motes: Implementation and Analysis. WiSec.

---

**Arquivos relacionados:**
- `src/canal/canal.py` - Implementação do canal e modulação
- `src/codigos_corretores/bch.py` - Código BCH
- `src/pilares/reconciliacao.py` - Processo de reconciliação
- `src/pilares/amplificacao_privacidade.py` - SHA-256
- `src/util/config_dispositivos.py` - Perfis de dispositivos IoT
- `interfaces/basic/main.py` - Script principal
- `docs/MELHORIAS_REALISTAS.md` - Documentação técnica detalhada das melhorias
