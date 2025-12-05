# Parâmetros de Frequência e Impacto no KDR

## Relação Fundamental

### Frequência e Comprimento de Onda
```
λ = c / f
```
- **λ**: Comprimento de onda (m)
- **c**: Velocidade da luz (~3×10⁸ m/s)
- **f**: Frequência da portadora (Hz)

**Exemplo**: fc = 1 MHz → λ = 300 m

## Banda de Coerência

### Definição
Faixa de frequências sobre a qual o canal possui resposta aproximadamente constante.

```
Bc ≈ 1 / (2π·τrms)
```
- **Bc**: Banda de coerência (Hz)
- **τrms**: Delay spread RMS (dispersão temporal)

### Classificação
- **Bc > B**: Canal de faixa estreita (flat fading)
- **Bc < B**: Canal de faixa larga (frequency-selective fading)

## Correlação de Canais

### Separação Espacial
Para canais descorrelacionados (independentes):
```
d ≥ λ/2
```
- **d**: Distância entre antenas
- **λ/2**: Meia comprimento de onda

### Coeficiente de Correlação Espacial
```
ρ(d) ≈ J₀(2π·d/λ)
```
- **J₀**: Função de Bessel de primeira espécie, ordem zero
- Para d = λ/2: ρ ≈ 0 (descorrelacionados)
- Para d < λ/2: ρ > 0.5 (correlacionados)

## Impacto na Modulação

### BPSK
- **Taxa de símbolos**: Rs = Rb (1 bit/símbolo)
- **Largura de banda**: B ≈ 2·Rb
- **Exemplo**: Rb = 100 kbps → B ≈ 200 kHz

### QPSK
- **Taxa de símbolos**: Rs = Rb/2 (2 bits/símbolo)
- **Largura de banda**: B ≈ Rb (metade do BPSK)
- **Exemplo**: Rb = 100 kbps → B ≈ 100 kHz

## Efeito no KDR

### Correlação Alta (ρ ≈ 0.95)
- Canais de Alice e Bob são **similares**
- Desvanecimento afeta ambos igualmente
- Símbolos recebidos tendem a ser **iguais**
- **KDR baixo** (menos erros)

### Correlação Baixa (ρ ≈ 0.1)
- Canais de Alice e Bob são **independentes**
- Desvanecimento afeta cada um diferentemente
- Símbolos recebidos tendem a **diferir**
- **KDR alto** (mais erros)

### Fórmula do KDR
```
KDR = (100 × N_erros) / N_total
```
- **N_erros**: Bits diferentes entre Alice e Bob
- **N_total**: Total de bits comparados

## Configuração no Sistema

### Parâmetros Implementados
```python
fc = 1e6          # 1 MHz (frequência portadora)
fs = 20e6         # 20 MHz (taxa de amostragem)
bit_rate = 100e3  # 100 kbps
```

### Relações
- **λ = 300 m** (comprimento de onda)
- **d ≥ 150 m** para descorrelação (λ/2)
- **Oversampling**: fs/fc = 20 (20 amostras por ciclo)

## Diretrizes Práticas

### Para Reduzir KDR (Melhorar)
1. Aumentar correlação do canal (ρ → 1)
2. Reduzir distância entre antenas (d < λ/2)
3. Reduzir ruído AWGN (maior SNR)
4. Usar QPSK (menor banda, mais robusta)

### Para Aumentar Realismo
1. Usar frequências típicas de comunicação (GHz)
2. Modelar delay spread realista
3. Considerar mobilidade (efeito Doppler)
4. Incluir interferência multi-percurso

## Referências Teóricas

- **Rayleigh Fading**: Modelo para ambientes sem linha de visada
- **AWGN**: Ruído aditivo branco gaussiano
- **Flat Fading**: B << Bc (modulação de faixa estreita)
- **Bessel J₀**: Aproximação de Clarke para correlação espacial
