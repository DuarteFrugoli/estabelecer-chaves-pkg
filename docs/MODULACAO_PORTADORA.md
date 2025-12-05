# Modulação com Frequência de Portadora

## Visão Geral

Este documento explica a implementação realista de modulação BPSK e QPSK com frequência de portadora, simulando o comportamento real de sistemas de comunicação sem fio.

## Conceitos Fundamentais

### 1. Por que usar portadora?

Na prática, sinais digitais não podem ser transmitidos diretamente pelo ar. É necessário:

- **Modular** o sinal em uma frequência de rádio (RF)
- **Transmitir** pela antena
- **Demodular** no receptor para recuperar os bits

**Exemplo:**
- WiFi: 2.4 GHz ou 5 GHz
- 4G/5G: 700 MHz - 6 GHz
- Bluetooth: 2.4 GHz

### 2. Banda Base vs Passabanda

| Característica | Banda Base | Passabanda |
|---------------|------------|------------|
| **Frequência** | Próxima de 0 Hz | Centrada em fc (portadora) |
| **Sinal** | Símbolos: ±1, ±1±j | Onda senoidal modulada |
| **Uso** | Teoria, simulações | Prática, transmissão real |
| **Largura de banda** | B Hz | B Hz centrada em fc |

## Implementação BPSK

### Modulação

Para BPSK, a modulação é:

$$s(t) = A \cdot m(t) \cdot \cos(2\pi f_c t)$$

onde:
- $A = \sqrt{2E_b/T_b}$ é a amplitude da portadora
- $m(t) \in \{-1, +1\}$ é o sinal banda base (antipodal)
- $f_c$ é a frequência da portadora
- $T_b$ é a duração de um bit

**Mapeamento de bits:**
- Bit 0 → $m(t) = +1$ → $s(t) = A\cos(2\pi f_c t)$ (fase 0°)
- Bit 1 → $m(t) = -1$ → $s(t) = -A\cos(2\pi f_c t)$ (fase 180°)

### Demodulação Coerente

1. **Multiplica** o sinal recebido pela portadora local: 
   $$r(t) \times 2\cos(2\pi f_c t)$$

2. **Integra** sobre o período de bit:
   $$z = \int_0^{T_b} r(t) \cdot 2\cos(2\pi f_c t) \, dt$$

3. **Decide**:
   - Se $z > 0$ → Bit 0
   - Se $z < 0$ → Bit 1

**Por que funciona?**

Usando identidade trigonométrica:
$$\cos(A)\cos(B) = \frac{1}{2}[\cos(A-B) + \cos(A+B)]$$

O termo em $2f_c$ é filtrado pela integração, restando apenas o sinal banda base.

## Implementação QPSK

### Modulação

QPSK usa duas portadoras em **quadratura** (90° defasadas):

$$s(t) = A \cdot [I(t)\cos(2\pi f_c t) - Q(t)\sin(2\pi f_c t)]$$

onde:
- $I(t)$ = componente In-phase
- $Q(t)$ = componente Quadrature
- Ambos $\in \{-1/\sqrt{2}, +1/\sqrt{2}\}$ (normalizado para $E_s = 1$)

**Mapeamento Gray Coding:**

| Bits | I | Q | Fase |
|------|---|---|------|
| 00 | -1/√2 | -1/√2 | 225° |
| 01 | -1/√2 | +1/√2 | 135° |
| 10 | +1/√2 | -1/√2 | 315° |
| 11 | +1/√2 | +1/√2 | 45° |

### Demodulação Coerente

Para recuperar componentes I e Q:

1. **Demodula I**: 
   $$z_I = \int_0^{T_s} r(t) \cdot 2\cos(2\pi f_c t) \, dt$$

2. **Demodula Q**: 
   $$z_Q = \int_0^{T_s} r(t) \cdot (-2\sin(2\pi f_c t)) \, dt$$

3. **Decide** cada componente:
   - $z_I > 0$ → bit I = 0, caso contrário = 1
   - $z_Q > 0$ → bit Q = 0, caso contrário = 1

## Parâmetros da Implementação

### Escolha de Parâmetros

```python
fc = 1e6        # 1 MHz - frequência portadora
fs = 20e6       # 20 MHz - frequência amostragem (20x fc)
bit_rate = 100e3  # 100 kbps
```

**Critérios:**

1. **Nyquist**: $f_s \geq 2f_c$ (aqui: $20 \text{ MHz} > 2 \text{ MHz}$ ✓)

2. **Amostras por bit (BPSK)**: 
   $$N_{bit} = \frac{f_s}{R_b} = \frac{20 \times 10^6}{100 \times 10^3} = 200$$

3. **Amostras por símbolo (QPSK)**: 
   $$N_{sym} = \frac{f_s}{R_s} = \frac{f_s}{R_b/2} = 400$$
   (QPSK transmite 2 bits/símbolo)

## Vantagens da Implementação com Portadora

### 1. Realismo
- Simula transmissão real via antena
- Considera limitações de largura de banda
- Permite estudar efeitos de frequência

### 2. Visualização
- Mostra forma de onda real transmitida
- Permite observar variação temporal
- Facilita entendimento físico

### 3. Extensibilidade
- Permite adicionar **path loss** dependente de frequência
- Permite modelar **Doppler shift** (movimento)
- Facilita adicionar **filtros** (raised cosine, etc.)

### 4. Compatibilidade
- Pode integrar com simuladores RF
- Permite comparação com padrões (WiFi, LTE)
- Facilita validação experimental

## Diferença da Implementação Anterior

### Banda Base (anterior)
```python
# Símbolos diretos
simbolos = [+1, -1, +1, +1, ...]

# Canal: y = h*x + n
y = ganho * simbolos + ruido

# Demodula: threshold
bits = (y > 0)
```

### Passabanda (nova)
```python
# Modula para RF
sinal_rf = A * simbolos * cos(2πfct)

# Canal temporal
sinal_recebido = canal(sinal_rf)

# Demodula coerentemente
sinal_bb = sinal_recebido * 2*cos(2πfct)
bits = integrate_and_dump(sinal_bb)
```

## Próximos Passos

### 1. Path Loss
Adicionar atenuação dependente de distância:

$$P_r = P_t \cdot \left(\frac{\lambda}{4\pi d}\right)^2$$

onde $\lambda = c/f_c$ depende da frequência da portadora.

### 2. Fading Temporal
Implementar modelo de Jakes para fading correlacionado no tempo:

$$h(t) = \sum_{n=1}^{N} \alpha_n e^{j(2\pi f_d \cos\theta_n t + \phi_n)}$$

### 3. Doppler Shift
Para transmissor/receptor em movimento:

$$f_{\text{recebida}} = f_c \left(1 + \frac{v}{c}\cos\theta\right)$$

### 4. Filtros Formatadores
Implementar filtro raised cosine para limitar largura de banda.

## Referências

1. **Proakis, J. G., & Salehi, M.** (2008). *Digital Communications*. McGraw-Hill, 5th ed.
   - Capítulo 4: Modulação em Passabanda
   - Capítulo 6: Demodulação Coerente

2. **Haykin, S.** (2001). *Communication Systems*. Wiley, 4th ed.
   - Capítulo 3: Modulação em Amplitude e Ângulo

3. **Rappaport, T. S.** (2002). *Wireless Communications: Principles and Practice*. Prentice Hall.
   - Capítulo 5: Propagação e Path Loss

4. **Goldsmith, A.** (2005). *Wireless Communications*. Cambridge University Press.
   - Capítulo 3: Canais com Fading

## Arquivos Relacionados

- `src/canal/modulacao.py` - Classes ModuladorBPSK e ModuladorQPSK
- `interfaces/teoria/demo_portadora.py` - Demonstração e visualização
- `interfaces/teoria/plots/modulacao_portadora.png` - Formas de onda
- `interfaces/teoria/plots/constelacao_qpsk.png` - Diagrama de constelação
