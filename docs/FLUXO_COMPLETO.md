# Fluxo Completo do Sistema de Distribuição Quântica de Chaves

## Visão Geral

Este documento descreve passo a passo o funcionamento completo do sistema de distribuição de chaves baseado em canal sem fio com desvanecimento Rayleigh, incluindo todos os cálculos, parâmetros e processos envolvidos.

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
ganho_i = np.random.normal(0, sigma, tamanho)
ganho_q = np.random.normal(0, sigma, tamanho)

# BPSK (real)
ganho = np.sqrt(ganho_i**2 + ganho_q**2)

# QPSK (complexo)
ganho = ganho_i + 1j * ganho_q
```

### 3.2 Correlação entre Canais Alice-Bob

Alice e Bob estão próximos, então seus canais de desvanecimento são correlacionados:

```
h_Bob = ρ * h_Alice + √(1-ρ²) * h_independente
```

onde:
- ρ = 0.9 (coeficiente de correlação, valor típico 0.8-0.99)
- h_Alice: ganho do canal de Alice
- h_independente: componente independente

**Cálculo:**
```python
correlacao = 0.9
ganho_bob = correlacao * ganho_alice + \
            np.sqrt(1 - correlacao**2) * ganho_independente
```

Isso simula a reciprocidade do canal sem fio.

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

#### Detecção por Limiar
Decide o bit baseado no sinal de y:

```
y > 0  →  bit = 0
y < 0  →  bit = 1
```

**Implementação:**
```python
bits_recebidos = (sinal_recebido >= 0).astype(int)
```

### 4.2 QPSK

#### Separação de Componentes
Demodula I e Q independentemente:

```
I = Re(y)  (parte real)
Q = Im(y)  (parte imaginária)
```

#### Decisão
```
I > 0  →  bit_I = 0
I < 0  →  bit_I = 1

Q > 0  →  bit_Q = 0
Q < 0  →  bit_Q = 1
```

**Implementação:**
```python
for simbolo in sinal_recebido:
    bit_i = 0 if simbolo.real >= 0 else 1
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

## 14. Exemplo Numérico Completo

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

## Referências

1. **Proakis, J. G., & Salehi, M.** (2008). Digital Communications. McGraw-Hill.
2. **Rappaport, T. S.** (2002). Wireless Communications: Principles and Practice.
3. **Goldsmith, A.** (2005). Wireless Communications. Cambridge University Press.
4. **Lin, S., & Costello, D. J.** (2004). Error Control Coding. Prentice Hall.

---

**Arquivos relacionados:**
- `src/canal/canal.py` - Implementação do canal e modulação
- `src/codigos_corretores/bch.py` - Código BCH
- `src/pilares/reconciliacao.py` - Processo de reconciliação
- `src/pilares/amplificacao_privacidade.py` - SHA-256
- `interfaces/basic/main.py` - Script principal
