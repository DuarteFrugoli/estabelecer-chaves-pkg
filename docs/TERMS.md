# Glossário de Termos - Estabelecimento de Chaves por Canal Físico

> **Objetivo:** Este documento define e explica todos os termos técnicos utilizados no projeto de estabelecimento de chaves baseado em características do canal físico (PKG - Physical Key Generation).

---

## 📡 MODULAÇÃO DIGITAL

### BPSK (Binary Phase Shift Keying)
**Definição:** Modulação digital que transmite 1 bit por símbolo.

**Mapeamento:**
- Bit `0` → Símbolo `-1`
- Bit `1` → Símbolo `+1`

**Características:**
- Eficiência espectral: 1 bit/símbolo
- Mais robusta a ruído que QPSK
- Demodulação por limiar em 0

**Uso no projeto:** Modo de modulação básico para comparação de desempenho.

---

### QPSK (Quadrature Phase Shift Keying)
**Definição:** Modulação digital que transmite 2 bits por símbolo usando componentes I (In-phase) e Q (Quadrature).

**Mapeamento (Gray Coding):**
- `00` → `-1-1j` (Quadrante III)
- `01` → `-1+1j` (Quadrante II)
- `10` → `+1-1j` (Quadrante IV)
- `11` → `+1+1j` (Quadrante I)

**Características:**
- Eficiência espectral: 2 bits/símbolo
- Dobro da taxa de transmissão comparado ao BPSK
- Mesma BER que BPSK (com Gray coding) para mesmo Eb/N0
- Demodulação separada de I e Q

**Uso no projeto:** Modo de modulação avançado para maior eficiência.

---

### Frequência de Portadora
**Definição:** Frequência da onda senoidal usada para transportar informação.

**No projeto:**
- **NÃO é explicitamente simulada** (trabalhamos em banda base)
- Banda base = representação equivalente passa-baixas do sinal
- Evita necessidade de simular frequências altas (GHz)
- Mantém todas as propriedades estatísticas relevantes

**Conceito:** `s(t) = A·cos(2πf_c·t + φ(t))` onde `f_c` é a portadora.

**Por que banda base?** Simplifica simulação mantendo características de BER, ruído e fading.

---

### Taxa de Transmissão
**Definição:** Velocidade de transmissão de informação pelo canal.

**Medidas:**
- **Taxa de bits (bit rate):** bits/segundo
- **Taxa de símbolos (symbol rate):** símbolos/segundo

**Relação:**
```
Taxa_de_bits = Taxa_de_símbolos × bits_por_símbolo

BPSK: R_b = R_s × 1
QPSK: R_b = R_s × 2
```

**No projeto:** Não simulamos em tempo real, mas contamos bits e símbolos transmitidos.

---

### Taxa de Bits (Bit Rate)
**Definição:** Número de bits transmitidos por unidade de tempo.

**Símbolo:** `R_b` (bits/s ou bps)

**Exemplo:**
- 1000 bits em 100 testes = 10 bits/teste
- Com BPSK: 10 símbolos/teste
- Com QPSK: 5 símbolos/teste

---

### Taxa de Símbolos (Symbol Rate)
**Definição:** Número de símbolos transmitidos por unidade de tempo.

**Símbolo:** `R_s` (símbolos/s ou baud)

**Relação com largura de banda:**
```
Largura_de_banda ≥ R_s
```

**Eficiência espectral:**
```
η = R_b / BW (bits/s/Hz)

BPSK: η ≈ 1 bit/s/Hz
QPSK: η ≈ 2 bits/s/Hz
```

---

## CANAL DE COMUNICAÇÃO

### Canal Rayleigh
**Definição:** Modelo estatístico para canal com desvanecimento (fading) quando não há componente de linha de visada (NLOS - Non-Line-Of-Sight).

**Características:**
- Amplitude do ganho `|h|` segue distribuição Rayleigh
- Potência `|h|²` segue distribuição exponencial
- Modela reflexões múltiplas (multipaths)

**Distribuição:**
```
f(r) = (r/σ²)·exp(-r²/(2σ²))   para r ≥ 0

Onde:
  r = amplitude do ganho
  σ = parâmetro de escala
```

**Parâmetro σ no projeto:**
- `σ = 1/√2 ≈ 0.707`: Canal normalizado (E[|h|²] = 1) - **PADRÃO**
- `σ = 0.5`: Canal fraco (E[|h|²] = 0.5, -3 dB)
- `σ = 1.0`: Canal moderado (E[|h|²] = 2.0, +3 dB)
- `σ = 2.0`: Canal forte (E[|h|²] = 8.0, +9 dB)

**Uso no projeto:** Simula canal sem linha de visada entre AP e estações.

---

### Tempo de Coerência (Coherence Time)
**Definição:** Intervalo de tempo durante o qual o canal pode ser considerado aproximadamente constante.

**Símbolo:** `T_c`

**Relação com velocidade:**
```
T_c ≈ 1 / (2·f_d)

Onde f_d = v·f_c / c (deslocamento Doppler)
  v = velocidade relativa
  f_c = frequência de portadora
  c = velocidade da luz
```

**Interpretação:**
- `T_c` grande: Canal varia lentamente (slow fading)
- `T_c` pequeno: Canal varia rapidamente (fast fading)

**No projeto:** Assumimos slow fading (canal muda entre transmissões, não durante).

---

### Banda de Coerência (Coherence Bandwidth)
**Definição:** Faixa de frequências sobre a qual o canal apresenta resposta aproximadamente constante.

**Símbolo:** `B_c`

**Relação com delay spread:**
```
B_c ≈ 1 / (5·τ_rms)

Onde τ_rms = delay spread RMS
```

**Classificação:**
- Se `B_s << B_c`: **Flat fading** (desvanecimento plano)
- Se `B_s >> B_c`: **Frequency-selective fading**

**No projeto:** 
- Assumimos **flat fading** (B_c > largura de banda do sinal)
- Ganho do canal é único por símbolo
- Não há interferência intersimbólica (ISI) devido ao canal

---

### Desvanecimento Plano (Flat Fading)
**Definição:** Desvanecimento onde toda a largura de banda do sinal sofre atenuação uniforme.

**Condição:** `B_c > B_s` (banda de coerência > banda do sinal)

**Modelo:** `y = h·x + n` onde `h` é escalar complexo.

**No projeto:** Modelo utilizado - ganho Rayleigh único por símbolo.

---

### Reciprocidade do Canal
**Definição:** Propriedade onde o canal de Alice→Bob é similar ao canal Bob→Alice.

**Coeficiente de correlação (ρ):**
```
h_Bob = ρ·h_Alice + √(1-ρ²)·h_indep

Onde:
  ρ = correlação (0 ≤ ρ ≤ 1)
  h_indep = componente independente
```

**Valores típicos:**
- `ρ = 1.0`: Reciprocidade perfeita (TDD ideal)
- `ρ = 0.9`: Reciprocidade alta (valor usado no projeto)
- `ρ = 0.8`: Reciprocidade moderada
- `ρ = 0.0`: Canais independentes

**Importância:** Base do PKG - Alice e Bob observam canal similar, Eva não.

---

## 📊 MÉTRICAS DE DESEMPENHO

### SNR (Signal-to-Noise Ratio)
**Definição:** Relação entre potência do sinal e potência do ruído.

**Fórmulas:**
```
SNR = P_sinal / P_ruído = E_s / N_0

Em dB: SNR_dB = 10·log₁₀(SNR)

Relação com variância do ruído:
σ² = E_s / (2·SNR)
```

**Interpretação:**
- SNR alto: Pouco ruído, BER baixa
- SNR baixo: Muito ruído, BER alta

**No projeto:** Varia de -10 dB a 30 dB (18 pontos) para análise.

---

### Eb/N0 (Energy per Bit to Noise Power Spectral Density)
**Definição:** Energia por bit dividida pela densidade espectral de potência do ruído.

**Relação com SNR:**
```
Eb/N0 = SNR / log₂(M)

Onde M = tamanho da constelação
  BPSK: M=2, log₂(M)=1 → Eb/N0 = SNR
  QPSK: M=4, log₂(M)=2 → Eb/N0 = SNR/2
```

**Uso:** Métrica universal para comparar modulações diferentes.

---

### BER (Bit Error Rate)
**Definição:** Taxa de erro de bit - probabilidade de um bit ser recebido incorretamente.

**Fórmula:**
```
BER = Erros_de_bits / Total_de_bits
```

**BER Teórica (Rayleigh):**
```
BER = 0.5 × (1 - √(γ/(1+γ)))

Onde γ = SNR_médio = E[|h|²]·Eb/N0
```

**Faixas típicas:**
- BER < 10⁻⁶: Excelente
- BER ≈ 10⁻³: Aceitável (com correção de erros)
- BER > 10⁻²: Ruim

**No projeto:** Comparamos BER simulada vs teórica para validação.

---

### KDR (Key Disagreement Rate)
**Definição:** Taxa de discrepância entre chaves de Alice e Bob.

**Fórmula:**
```
KDR = (Bits_diferentes / Total_de_bits) × 100%
```

**Três medições no projeto:**

1. **KDR Inicial:**
   - Erros entre sinal_Alice e sinal_Bob
   - Antes de qualquer correção
   - Baseline do canal

2. **KDR Pós-Reconciliação:**
   - Erros após correção BCH
   - Deve ser ~0% se correção funcionou
   - Mede eficácia do código corretor

3. **KDR Pós-Amplificação:**
   - Erros após SHA-256
   - Comparação de 256 bits finais
   - Chave final do sistema

**Objetivo:** KDR pós-amplificação = 0% (chaves idênticas).

---

## 🔐 PILARES DO PKG

### 1. Quantização
**Definição:** Processo de converter sinal analógico (ganho do canal) em bits.

**No projeto:**
- Recepção do sinal: `y = h·x + n`
- Demodulação BPSK: `bit = 1 se y ≥ 0, senão 0`
- Demodulação QPSK: separada em I e Q

**Resultado:** Sequência de bits baseada no canal observado.

---

### 2. Reconciliação de Chaves
**Definição:** Processo onde Alice e Bob corrigem diferenças em suas observações do canal.

**Método usado:** Códigos BCH (Bose-Chaudhuri-Hocquenghem)

**Processo:**
1. Alice gera síndrome: `s = XOR(chave_Alice, erro_estimado)`
2. Alice envia síndrome para Bob (público)
3. Bob decodifica: `chave_Bob = decodificar_BCH(síndrome)`
4. Resultado: chaves quase idênticas

**Vazamento de informação:** Síndrome revela ~(n-k) bits para Eva.

---

### 3. Amplificação de Privacidade
**Definição:** Processo que reduz informação de Eva sobre a chave final.

**Método usado:** SHA-256

**Processo:**
```python
chave_final = SHA256(chave_pós_reconciliação)
```

**Propriedades:**
- Entrada: N bits (variável)
- Saída: 256 bits (fixo)
- Determinístico: mesma entrada → mesma saída
- Efeito avalanche: 1 bit muda → ~50% dos bits mudam
- Irreversível: não há como calcular entrada a partir da saída

**Segurança:** Eva precisa de informação completa da entrada para prever saída.

---

## 🛠️ CÓDIGOS CORRETORES DE ERROS

### BCH (Bose-Chaudhuri-Hocquenghem)
**Definição:** Família de códigos cíclicos para correção de erros.

**Parâmetros:**
- `n`: Comprimento da palavra código (7, 15, 127, 255)
- `k`: Comprimento da mensagem (bits de informação)
- `t`: Capacidade de correção (erros corrigíveis)

**Propriedade sistemática:**
- Primeiros k bits = mensagem original
- Últimos (n-k) bits = paridade

**No projeto:**
| n   | k   | t  |
|-----|-----|----|
| 7   | 4   | 1  |
| 15  | 11  | 1  |
| 127 | 120 | 1  |
| 255 | 247 | 1  |

**Uso:** Corrige erros causados por ruído no canal.

---

## 🎯 CONCEITOS DE SISTEMA

### PKG (Physical Key Generation)
**Definição:** Geração de chaves criptográficas baseada em características físicas do canal de comunicação.

**Princípio fundamental:**
1. Alice e Bob observam canal similar (reciprocidade)
2. Eva observa canal independente (decorrelação espacial)
3. Chaves geradas são secretas e idênticas

**Vantagens:**
- Não requer infraestrutura de chave pública (PKI)
- Segurança baseada em física, não apenas computação
- Renovação de chaves simples (nova observação do canal)

---

### TDD (Time Division Duplex)
**Definição:** Método de comunicação bidirecional onde transmissão e recepção usam mesma frequência em tempos diferentes.

**Relevância para PKG:**
- Garante reciprocidade do canal
- Alice e Bob usam mesma frequência
- Medições feitas em intervalo < tempo de coerência

**Alternativa:** FDD (Frequency Division Duplex) - canais diferentes, sem reciprocidade.

---

### AWGN (Additive White Gaussian Noise)
**Definição:** Modelo de ruído onde ruído aditivo tem distribuição gaussiana e espectro uniforme (branco).

**Propriedades:**
- **Aditivo:** `y = x + n`
- **Gaussiano:** `n ~ N(μ, σ²)`
- **Branco:** Densidade espectral constante

**Parâmetros no projeto:**
- Média: `μ = 0` (ruído centrado)
- Variância: `σ² = E_s / (2·SNR)` (depende do SNR)

---

### Banda Base (Baseband)
**Definição:** Representação equivalente passa-baixas de um sinal modulado em portadora.

**Vantagem para simulação:**
- Evita simular frequências de portadora (GHz)
- Mantém todas as características estatísticas
- Simplifica implementação
- Resultados de BER idênticos

**Modelo:**
```
Real (com portadora):
  s(t) = Re{x(t)·exp(j2πf_c·t)}

Banda base (equivalente):
  s(t) = x(t)  (complexo)
```

**No projeto:** BPSK usa símbolos reais {-1,+1}, QPSK usa símbolos complexos.

---

## 🔬 CONCEITOS AVANÇADOS

### Deslocamento Doppler (Doppler Shift)
**Definição:** Mudança na frequência devido ao movimento relativo.

**Fórmula:**
```
f_d = v·f_c / c

Onde:
  v = velocidade relativa (m/s)
  f_c = frequência de portadora (Hz)
  c = velocidade da luz (3×10⁸ m/s)
```

**Efeito:** Causa variação temporal do canal (fading rate).

---

### Delay Spread (Dispersão de Atraso)
**Definição:** Diferença de tempo entre primeiro e último caminho de multipercurso.

**Símbolo:** `τ_rms` (RMS delay spread)

**Efeito:**
- Determina banda de coerência: `B_c ≈ 1/(5·τ_rms)`
- Causa interferência intersimbólica (ISI)

**No projeto:** Assumimos τ_rms pequeno (flat fading).

---

### Gray Coding
**Definição:** Codificação onde símbolos adjacentes diferem por apenas 1 bit.

**Benefício:** Minimiza BER pois erro de símbolo causa erro de apenas 1 bit.

**Uso em QPSK:**
```
00 → -1-1j    01 → -1+1j
   ↓ 1 bit       ↓ 1 bit
10 → +1-1j    11 → +1+1j
```

**Resultado:** BER_QPSK ≈ BER_BPSK (para mesmo Eb/N0).

---

### Teorema de Nyquist
**Definição:** Taxa mínima de amostragem para reconstrução perfeita de sinal.

**Fórmula:**
```
f_s ≥ 2·B

Onde:
  f_s = frequência de amostragem
  B = largura de banda do sinal
```

**No projeto:** Implicitamente respeitado (1 amostra/símbolo).

---

### Capacidade de Shannon
**Definição:** Taxa máxima de transmissão confiável em canal com ruído.

**Fórmula:**
```
C = B·log₂(1 + SNR) bits/s

Onde:
  B = largura de banda (Hz)
  SNR = relação sinal-ruído
```

**Interpretação:** Limite teórico - taxas acima de C têm BER inevitável.

---

## 📐 FÓRMULAS IMPORTANTES

### Relação SNR e Variância do Ruído
```
SNR = E_s / N_0
N_0 = 2·σ²
σ² = E_s / (2·SNR)
```

### Potência Média Canal Rayleigh
```
E[|h|²] = 2·σ²

Valores comuns:
  σ = 1/√2 → E[|h|²] = 1 (normalizado)
  σ = 0.5  → E[|h|²] = 0.5 (-3 dB)
  σ = 1.0  → E[|h|²] = 2.0 (+3 dB)
  σ = 2.0  → E[|h|²] = 8.0 (+9 dB)
```

### BER Teórica Canal Rayleigh
```
BPSK/QPSK: BER = 0.5 × (1 - √(γ̄/(1+γ̄)))

Onde γ̄ = E[|h|²]·SNR
```

### Reciprocidade do Canal
```
h_Bob = ρ·h_Alice + √(1-ρ²)·h_indep

|ρ| = coeficiente de correlação
```

---

## 🎓 REFERÊNCIAS

### Livros
1. **Proakis, J. G., & Salehi, M.** (2008). *Digital Communications*. McGraw-Hill, 5th edition.
   - Capítulo 14: Fading Channels

2. **Goldsmith, A.** (2005). *Wireless Communications*. Cambridge University Press.
   - Capítulo 3: Channel Models

3. **Tse, D., & Viswanath, P.** (2005). *Fundamentals of Wireless Communication*. Cambridge University Press.
   - Capítulo 2: The Wireless Channel

### Papers PKG
1. Mathur et al. (2008). "Radio-telepathy: extracting a secret key from an unauthenticated wireless channel"
2. Azimi-Sadjadi et al. (2007). "Robust key generation from signal envelopes in wireless networks"

---

## 📝 NOTAS FINAIS

### Simplificações do Projeto
1. **Banda base:** Não simula frequência de portadora explicitamente
2. **Flat fading:** Assume banda de coerência > largura do sinal
3. **Slow fading:** Canal muda entre transmissões, não durante
4. **Reciprocidade ideal:** Ignora assimetrias de hardware
5. **Sincronização perfeita:** Assume Alice e Bob sincronizados

### Por que essas simplificações são válidas?
- Mantêm propriedades estatísticas essenciais
- BER simulada corresponde à teoria
- Foco no problema principal: extração de chaves do canal
- Sistema mais simples de entender e implementar
- Resultados generalizáveis para sistemas reais

---

*Última atualização: 6 de novembro de 2025*