# Prompts para Geração de Figuras do Artigo - Sistema PKG

**Data:** 06/02/2026  
**Objetivo:** Prompts detalhados para IA geradora de imagens (DALL-E, Midjourney, Stable Diffusion)

---

## FIGURA 1: Diagrama do Modelo de Sistema (Seção III)

**Tipo:** Diagrama técnico/esquemático  
**Onde usar:** Seção III (Modelo de Sistema) - após equação $y_A = h_A x + n_A$  
**Label LaTeX:** `\label{fig:modelo_sistema}`

### Prompt para IA:

```
Create a clean technical diagram showing a 5G/IoT physical-layer key generation system with spatial correlation. The image should have a white background and include:

1. TOP CENTER: A cellular tower (gNodeB/base station) labeled "gNodeB" transmitting downlink signal "x"
2. MIDDLE: Two small IoT devices (smartphones/sensors) positioned close together (< 0.5 meters apart):
   - Left device labeled "Alice" 
   - Right device labeled "Bob"
   - Arrow from gNodeB to Alice labeled "h_A" (channel coefficient)
   - Arrow from gNodeB to Bob labeled "h_B" (channel coefficient)
   - Double-headed arrow between Alice and Bob labeled "ρ = 0.9" indicating high spatial correlation
3. BOTTOM RIGHT: A third device farther away (> 20cm) labeled "Eve" (eavesdropper)
   - Arrow from gNodeB to Eve labeled "h_E"
   - Text near Eve: "d_E > 20cm" and "ρ_E ≈ 0" indicating decorrelation
4. Style: Clean engineering diagram with simple icons, blue/gray color scheme for professional look
5. Include mathematical notation: spatial correlation formula ρ = J₀(2πd/λ) in small text

The diagram should clearly show that Alice and Bob are spatially correlated (close proximity) while Eve is decorrelated (far away).
```

**Alternativa simples:** Procure no Google por "5G downlink communication diagram" ou "spatial correlation wireless channel" e adapte com anotações.

---

## FIGURA 2: Fluxograma do Protocolo PKG Completo (Seção IV)

**Tipo:** Fluxograma vertical  
**Onde usar:** Seção IV (Metodologia Experimental) - após Fluxo de Processamento  
**Label LaTeX:** `\label{fig:fluxograma_protocolo}`

### Prompt para IA:

```
Create a vertical flowchart showing the complete flow of a physical-layer key generation protocol with 7 steps. White background, professional style:

1. Top box: "1. Channel Generation" with formula "h_A, h_B (ρ = 0.9)"
2. Second box: "2. Downlink Reception" with formula "y_A = h_A·x + n_A"
3. Third box: "3. Channel Estimation" with text "Error 10-30%"
4. Fourth box: "4. BPSK/QPSK Quantization" with text "Guard-band optional"
5. Fifth box: "5. Code-Offset BCH(127,64,10)" with formula "σ = b_B ⊕ c"
6. Sixth box: "6. SHA-256 Privacy Amplification" with text "256-bit key"
7. Bottom box: "7. Metrics" with text "BER, KDR"

Connect boxes with downward arrows. Use light blue boxes with dark blue borders. Add small icons (antenna, lock, hash symbol) where appropriate. Keep it clean and technical.
```

**IMPORTANTE:** Você já tem a figura **ProcessoGer.png** na pasta `paper/overleaf/figuras/`. Verifique se essa figura serve! Se servir, use ela e não precisa gerar nova.

---

## FIGURA 3: Curva de Correlação Espacial de Clarke (Seção III)

**Tipo:** Gráfico técnico/científico  
**Onde usar:** Seção III (Modelo de Sistema) - após equação $\rho = J_0(2\pi d/\lambda)$  
**Label LaTeX:** `\label{fig:clarke_correlacao}`

### Prompt para IA:

```
Create a technical graph showing the Clarke spatial correlation model. Clean scientific style with white background:

X-axis: Distance (meters) from 0 to 1.0 m
Y-axis: Spatial Correlation ρ from -0.4 to 1.0
Plot: Bessel function J₀(2πd/λ) curve showing:
- Starting at ρ=1.0 when d=0
- Decreasing to ρ≈0.7 at d=0.1m
- Crossing zero at d≈0.0625m (λ/2 for 2.4 GHz)
- Oscillating with decreasing amplitude for d > 0.2m

Add annotations:
- Vertical dashed line at d=0.2m labeled "Security threshold (20cm)"
- Horizontal dashed line at ρ=0 
- Text box: "f = 2.4 GHz, λ = 12.5 cm"
- Title: "Spatial Correlation vs Distance (Clarke Model)"

Use blue line, grid background, professional scientific plotting style similar to matplotlib.
```

**Alternativa:** Gere a curva real usando Python/Matplotlib e salve como PNG. Mais fácil e preciso do que IA.

**Código Python para gerar:**
```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import jv

freq = 2.4e9  # 2.4 GHz
lambda_m = 3e8 / freq
d = np.linspace(0, 1.0, 500)
rho = jv(0, 2*np.pi*d/lambda_m)

plt.figure(figsize=(8, 5))
plt.plot(d, rho, 'b-', linewidth=2)
plt.axhline(0, color='k', linestyle='--', linewidth=0.8)
plt.axvline(0.2, color='r', linestyle='--', linewidth=1.5, label='Limiar segurança (20cm)')
plt.xlabel('Distância (m)', fontsize=12)
plt.ylabel('Correlação Espacial ρ', fontsize=12)
plt.title('Modelo de Clarke: ρ = J₀(2πd/λ)', fontsize=14)
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig('clarke_correlacao.png', dpi=300)
```

---

## FIGURA 4: Diagrama Guard-Band (Quantização) (Seção II ou VII)

**Tipo:** Diagrama técnico/ilustrativo  
**Onde usar:** Seção II (Fundamentação) ou Seção V (Exp07)  
**Label LaTeX:** `\label{fig:guardband_quantizacao}`

### Prompt para IA:

```
Create a technical diagram illustrating the guard-band concept in signal quantization. White background, clean style:

Show a vertical amplitude axis with symmetric zones:
- Top region (+σ): Light green zone labeled "Bit = 1"
- Upper middle (+GB to +σ): Yellow zone labeled "Guard-band (discard)"
- Center (-GB to +GB): Yellow zone labeled "Dead zone (discard)"
- Lower middle (-σ to -GB): Yellow zone labeled "Guard-band (discard)"
- Bottom region (below -σ): Light red zone labeled "Bit = 0"

Add:
- Horizontal dashed lines at +σ, +GB, 0, -GB, -σ
- Small signal points scattered in each region
- Arrow pointing to discarded samples in guard-band with text "30-50% discarded for GB=0.5σ"
- Title: "Guard-Band Effect on Quantization"
- Annotation: "Trade-off: Security vs Efficiency"

Use engineering diagram style with clear labels and professional color scheme.
```

**MUITO SIMPLES:** Procure por "quantization threshold diagram" ou "guard band signal processing" no Google Images. Fácil de encontrar e adaptar com anotações.

---

## FIGURA 5: Comparação Reciprocidade Temporal vs Correlação Espacial (Seção III)

**Tipo:** Diagrama comparativo lado a lado  
**Onde usar:** Seção III (Modelo de Sistema) - Justificativa  
**Label LaTeX:** `\label{fig:temporal_vs_espacial}`

### Prompt para IA:

```
Create a side-by-side comparison diagram showing two wireless channel models. Clean technical style, white background:

LEFT PANEL - "Temporal Reciprocity (TDD)":
- Alice device with upward arrow labeled "Pilot (t₁)"
- Bob device with downward arrow labeled "Pilot (t₂)"
- Double-headed arrow between them labeled "h_AB(t₁) ≈ h_BA(t₂)"
- Text below: "Requires TDD mode"
- Text below: "Time synchronization needed"

RIGHT PANEL - "Spatial Correlation (FDD/TDD)":
- Base station (tower) at top
- Two devices (Alice and Bob) close together below
- Downward arrows from tower to both devices labeled "h_A" and "h_B"
- Arrow between devices labeled "ρ = J₀(2πd/λ)"
- Text below: "Works in FDD/TDD"
- Text below: "No synchronization needed"

Add central label "vs" between panels. Use blue/green color scheme for professional look.
```

**SIMPLES:** Procure "TDD reciprocity vs FDD correlation" ou desenhe manualmente no PowerPoint/Google Slides.

---

## FIGURAS DOS RESULTADOS (Seção V) - JÁ EXISTEM!

Essas figuras já foram geradas pelos experimentos Python. Apenas copie para pasta `paper/overleaf/figuras/`:

### Exp01: SNR vs KDR
- **Arquivo:** `resultados/figuras/exp01_variacao_snr_YYYYMMDD_HHMMSS.png`
- **Label:** `\label{fig:exp01_snr}`
- **Legenda:** "Taxa de Desacordo de Chaves (KDR) em função da Relação Sinal-Ruído (SNR). A curva mostra decaimento exponencial, atingindo KDR nula a partir de 13--15~dB."

### Exp02: BPSK vs QPSK (opcional - dados na tabela)
- **Arquivo:** `resultados/figuras/exp02_comparacao_modulacao_YYYYMMDD_HHMMSS.png`
- **Label:** `\label{fig:exp02_modulacao}`

### Exp03: Códigos BCH (opcional - dados na tabela)
- **Arquivo:** `resultados/figuras/exp03_variacao_bch_YYYYMMDD_HHMMSS.png`
- **Label:** `\label{fig:exp03_bch}`

### Exp04: Complexidade Computacional (opcional - dados na tabela)
- **Arquivo:** `resultados/figuras/exp04_analise_complexidade_YYYYMMDD_HHMMSS.png`
- **Label:** `\label{fig:exp04_complexidade}`

### Exp05: Perfis IoT
- **Arquivo:** `resultados/figuras/exp05_perfis_dispositivos_YYYYMMDD_HHMMSS.png`
- **Label:** `\label{fig:exp05_perfis}`
- **Legenda:** "Desempenho do sistema em cinco perfis de dispositivos IoT. Todos os perfis atingem KDR nula em SNR entre 13--15~dB, demonstrando ampla aplicabilidade."

### Exp06: Segurança Eve (Descorrelação Espacial)
- **Arquivo:** `resultados/figuras/exp06_analise_eve_YYYYMMDD_HHMMSS.png`
- **Label:** `\label{fig:exp06_eve}`
- **Legenda:** "Correlação espacial e BER de Eve em função da distância lateral. Descorrelação espacial superior a 20~cm garante segurança equivalente a chute aleatório (BER $\approx 50\%$)."

### Exp07: Guard-Band
- **Arquivo:** `resultados/figuras/exp07_impacto_guard_band_YYYYMMDD_HHMMSS.png`
- **Label:** `\label{fig:exp07_guardband}`
- **Legenda:** "Trade-off entre eficiência e segurança em função do parâmetro de guard-band. O sistema é naturalmente seguro sem guard-band (BER Eve $\approx 50\%$), e valores elevados (GB $> 0.5$) são contraproducentes."

---

## RESUMO DE PRIORIDADES

### ESSENCIAIS (precisam ser criadas/encontradas):
1. ✅ **FIGURA 1:** Diagrama Modelo Sistema (IA ou Google "5G downlink diagram")
2. ✅ **FIGURA 2:** Fluxograma PKG (verificar se ProcessoGer.png serve!)
3. ✅ **FIGURA 3:** Curva Clarke (GERAR COM PYTHON - código fornecido acima)

### IMPORTANTES (melhoram o artigo):
4. **FIGURA 4:** Guard-band (Google "quantization threshold" - fácil)
5. **FIGURA 5:** Temporal vs Espacial (PowerPoint/Google Slides - simples)

### JÁ EXISTEM (copiar da pasta resultados/figuras/):
6. **Exp01:** SNR vs KDR (gráfico principal)
7. **Exp05:** 5 perfis IoT
8. **Exp06:** Eve descorrelação espacial
9. **Exp07:** Guard-band trade-off

---

## INSTRUÇÕES DE USO

1. **Para IA (DALL-E, Midjourney, etc.):**
   - Copie o prompt completo da seção correspondente
   - Cole na IA geradora de imagens
   - Ajuste se necessário (adicione "engineering style", "technical diagram", etc.)
   - Salve a imagem em alta resolução (300 DPI mínimo)

2. **Para Google Images:**
   - Use termos de busca mencionados em cada seção
   - Procure imagens com licença livre ou Creative Commons
   - Adapte com anotações no PowerPoint/GIMP se necessário

3. **Para gerar com Python:**
   - Execute o código Python fornecido (Figura 3 - Clarke)
   - Ajuste estilo/cores conforme necessário
   - Salve como PNG 300 DPI

4. **Organização final:**
   - Salve todas as figuras em: `paper/overleaf/figuras/`
   - Nomes sugeridos:
     - `fig01_modelo_sistema.png`
     - `fig02_fluxograma_pkg.png`
     - `fig03_clarke_correlacao.png`
     - `fig04_guardband.png`
     - `fig05_temporal_vs_espacial.png`
     - `exp01_snr_kdr.png`
     - `exp05_perfis_iot.png`
     - `exp06_eve_seguranca.png`
     - `exp07_guardband_tradeoff.png`

---

**Documento criado:** 06/02/2026  
**Status:** Pronto para geração de imagens  
**Próximo passo:** Gerar figuras e inserir no LaTeX descomentando os comandos `\includegraphics`
