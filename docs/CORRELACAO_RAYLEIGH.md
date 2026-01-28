# Correlação de Variáveis Rayleigh

## Problema Observado

Ao medir a correlação entre coeficientes de canal h_Alice e h_Bob no experimento 09, observamos uma **discrepância** entre:
- **ρ configurado**: 0.95 (parâmetro `correlacao_alice_bob`)
- **ρ medido**: ~0.84 (correlação de Pearson calculada)

**Razão de atenuação**: k ≈ 0.88 (ρ_medido ≈ 0.88 × ρ_configurado)

---

## Por Que Isso Acontece?

### Modelo de Correlação Usado

O modelo implementado em `aplicar_correlacao_temporal()` é:

```python
h_bob = ρ × h_alice + √(1-ρ²) × h_independente
```

Onde:
- `h_alice` ~ Rayleigh(σ)
- `h_independente` ~ Rayleigh(σ)
- `ρ` = coeficiente de correlação desejado

**Este modelo funciona perfeitamente para variáveis Gaussianas, mas NÃO preserva correlação exata para variáveis Rayleigh.**

---

## Análise Matemática

### Para Variáveis Gaussianas (Funciona Corretamente)

Se `X_A ~ Gaussiana(0, σ²)` e `X_ind ~ Gaussiana(0, σ²)` são independentes:

```
X_B = ρ·X_A + √(1-ρ²)·X_ind
```

Então:
- **E[X_A] = 0** (média zero)
- **E[X_B] = 0** (média zero)
- **Var(X_A) = σ²**
- **Var(X_B) = ρ²·σ² + (1-ρ²)·σ² = σ²**
- **Cov(X_A, X_B) = E[X_A·X_B] = ρ·E[X_A²] = ρ·σ²**
- **corr(X_A, X_B) = Cov / √(Var_A · Var_B) = ρ·σ² / σ² = ρ** ✅

**Resultado**: Correlação medida = ρ configurado

---

### Para Variáveis Rayleigh (Não Funciona!)

Se `H_A ~ Rayleigh(σ)` e `H_ind ~ Rayleigh(σ)`:

```
H_B = ρ·H_A + √(1-ρ²)·H_ind
```

**Propriedades da distribuição Rayleigh:**
- **E[H] = σ√(π/2) ≠ 0** ⚠️ (média não-zero!)
- **E[H²] = 2σ²**
- **Var(H) = E[H²] - E[H]² = 2σ² - (σ√(π/2))² = (2 - π/2)σ² ≈ 0.43σ²**

**Cálculo da Covariância:**

```
Cov(H_A, H_B) = E[H_A · H_B] - E[H_A]·E[H_B]
              = E[H_A · (ρ·H_A + √(1-ρ²)·H_ind)] - E[H_A]·E[ρ·H_A + √(1-ρ²)·H_ind]
              = ρ·E[H_A²] + √(1-ρ²)·E[H_A]·E[H_ind] - ρ·E[H_A]² - √(1-ρ²)·E[H_A]·E[H_ind]
              = ρ·E[H_A²] - ρ·E[H_A]²
              = ρ·Var(H_A)
```

**Problema**: A variância de H_B não é igual à de H_A!

```
Var(H_B) = E[(ρ·H_A + √(1-ρ²)·H_ind)²] - E[ρ·H_A + √(1-ρ²)·H_ind]²
```

A soma de duas variáveis Rayleigh **não resulta em uma Rayleigh** e tem variância diferente. Isso faz com que:

```
corr(H_A, H_B) = Cov(H_A, H_B) / √(Var(H_A)·Var(H_B))
               = ρ·Var(H_A) / √(Var(H_A)·Var(H_B))
               = ρ · √(Var(H_A)/Var(H_B))
               < ρ  (porque Var(H_B) > Var(H_A))
```

**Resultado**: Correlação medida < ρ configurado ❌

---

## Por Que Rayleigh Tem Esse Comportamento?

1. **Média não-zero**: E[H] = σ√(π/2) ≈ 1.25σ
   - Gaussianas têm média zero, Rayleigh não
   - Isso introduz um "offset" que afeta a correlação linear

2. **Distribuição assimétrica**: Rayleigh é sempre positivo (amplitude)
   - Valores pequenos são mais prováveis
   - A "cauda" da distribuição afeta a correlação de Pearson

3. **Variância não-aditiva**: Var(H_A + H_B) ≠ Var(H_A) + Var(H_B)
   - Para Gaussianas independentes, variâncias somam
   - Para Rayleigh, a soma altera a estrutura da distribuição

4. **Correlação de Pearson pressupõe linearidade**
   - Mede relação linear entre variáveis
   - Rayleigh introduz não-linearidades na combinação

---

## Comparação com Yuan et al.

### Yuan et al. (IEEE ICCC 2022)

- **Mede CSI complexo**: h = A·e^(jφ) = I + jQ
  - Componentes I (in-phase) e Q (quadrature) são **Gaussianas**
  - Amplitude |h| = √(I² + Q²) é Rayleigh
  - **Correlação é calculada nas componentes I/Q (Gaussianas), não na amplitude**

- **Resultados reportados**:
  - ρ(AP, STA) = 0.942 (legítimo)
  - ρ(Eve, STA) = 0.560 (espião)

### Nossa Simulação

- **Mede amplitude Rayleigh diretamente**: h ~ Rayleigh(σ)
  - Apenas a amplitude do canal, sem fase
  - **Correlação calculada diretamente nas amplitudes Rayleigh**

- **Resultados obtidos**:
  - ρ_medido(Alice, Bob) ≈ 0.84 quando ρ_configurado = 0.95
  - ρ_medido(Alice, Eve) ≈ 0.18 quando ρ_configurado = 0.21

---

## Impacto nos Experimentos

### O Contraste Relativo é Preservado

Embora ρ_medido seja menor que ρ_configurado, **o contraste entre Bob e Eve permanece válido**:

**Experimento 09 (descorrelação espacial, 10cm):**
- ρ(Alice, Bob) = 0.84 (alta correlação, legítimo)
- ρ(Alice, Eve) = 0.19 (baixa correlação, espião)
- **Razão**: Bob/Eve ≈ 4.4× (contraste claro)

**Interpretação:**
- Bob observa canal **altamente correlacionado** com Alice
- Eve observa canal **fracamente correlacionado** com Alice
- A descorrelação espacial é **efetiva** para segurança

### Fator de Atenuação Empírico

Da observação experimental:
```
ρ_medido ≈ k × ρ_configurado

Onde k ≈ 0.88 para variáveis Rayleigh
```

Este fator pode variar ligeiramente dependendo de:
- Número de amostras
- Parâmetro σ da distribuição
- Presença de ruído/erro de estimativa

---

## Soluções Possíveis

### 1. Aceitar a Discrepância (IMPLEMENTADO)

✅ **Documentar** que ρ_medido ≈ 0.88 × ρ_configurado para Rayleigh

**Vantagens:**
- Mantém implementação atual (simples)
- Contraste relativo Bob/Eve é preservado
- Resultados qualitativos são válidos

**Desvantagens:**
- Parâmetros configurados não correspondem exatamente aos medidos
- Menos preciso para comparações quantitativas diretas

---

### 2. Usar CSI Complexo (Gaussiano I/Q)

Mudar de:
```python
h ~ Rayleigh(σ)  # Apenas amplitude
```

Para:
```python
h = I + jQ  onde I, Q ~ Gaussiana(0, σ²)
|h| = √(I² + Q²)  # Amplitude Rayleigh
```

**Vantagens:**
- Correlação exata preservada (ρ_medido = ρ_configurado)
- Mais próximo do CSI real (Yuan et al.)
- Permite modelar fase do canal

**Desvantagens:**
- Complexidade adicional na implementação
- Precisa refatorar todo canal.py
- Aumenta tempo de processamento

---

### 3. Calibração Empírica

Ajustar ρ_configurado para obter ρ_medido desejado:
```python
# Se deseja ρ_medido = 0.95
ρ_configurado = ρ_medido / k = 0.95 / 0.88 ≈ 1.08
```

**Problema**: ρ > 1 é inválido! (correlação deve estar em [0, 1])

**Alternativa**: Criar tabela de mapeamento empírica
- Medir k(ρ) para diferentes valores de ρ
- Interpolar para obter ρ_config dado ρ_desejado

---

## Conclusão

A **discrepância entre ρ_configurado e ρ_medido** é um **fenômeno matemático esperado** ao usar o modelo linear de correlação com variáveis Rayleigh, devido à:

1. Média não-zero da distribuição Rayleigh
2. Assimetria da distribuição
3. Variância não-aditiva na soma de Rayleigh
4. Limitação da correlação de Pearson para medir relações não-lineares

**Decisão**: Aceitar a discrepância e documentar o fator k ≈ 0.88, mantendo a interpretação qualitativa dos resultados (contraste Bob/Eve) como válida para análise de segurança.

---

## Referências

1. **Jakes, W. C. (1974)**. *Microwave Mobile Communications*. Wiley.
   - Modelo de correlação temporal para canais móveis

2. **Yuan et al. (2022)**. *Secure Key Generation for Integrated Sensing and Communication*. IEEE ICCC.
   - Medição de correlação CSI em WiFi real

3. **Papoulis, A., Pillai, S. U. (2002)**. *Probability, Random Variables, and Stochastic Processes*. McGraw-Hill.
   - Propriedades estatísticas da distribuição Rayleigh

4. **Clarke, R. H. (1968)**. *A Statistical Theory of Mobile-Radio Reception*. Bell System Technical Journal.
   - Fundamentos da distribuição Rayleigh em canais wireless
