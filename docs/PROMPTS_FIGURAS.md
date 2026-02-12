# Prompts para Geração de Figuras do Artigo - Sistema PKG

**Data:** 12/02/2026  
**Objetivo:** Prompts para geração de figuras conceituais usando IA (DALL-E, Midjourney, etc.) ou ferramentas manuais (PowerPoint, draw.io)

**RESUMO:** Este documento contém prompts para **2 figuras conceituais** da Seção II que devem ser geradas por IA ou manualmente.

> 📝 **Nota:** Figuras geradas por Python estão em arquivo separado: `FIGURAS_PYTHON.md`

---

## FIGURA 1: Diagrama do Modelo de Sistema (Seção II)

**Tipo:** Diagrama técnico/esquemático  
**Onde usar:** Seção II (Fundamentos Teóricos) - Modelo de Sistema para PKG  
**Label LaTeX:** `\label{fig:modelo_sistema}`  
**Arquivo:** `paper/overleaf/figuras/fig01_modelo_sistema.png`

### Prompt MELHORADO para IA:

```
Create a professional technical diagram for an IEEE academic paper on physical-layer key generation. White background, publication-quality style.

LAYOUT STRUCTURE:
- TOP CENTER: 5G cellular tower (gNodeB/base station) with visible antenna
  * Label: "gNodeB"
  * Downward arrow labeled "x" (transmitted signal)
  
- MIDDLE SECTION: Two small devices (smartphone/IoT icons) very close together (<0.5m):
  * LEFT device: labeled "Alice" 
  * RIGHT device: labeled "Bob"
  * Visual indication of proximity: bracket showing "d_AB < 0.5m"
  * Arrow from gNodeB to Alice: labeled "h_A"
  * Arrow from gNodeB to Bob: labeled "h_B"
  * Double-headed arrow between them: labeled "ρ = 0.9" (high spatial correlation)
  
- BOTTOM RIGHT: Third device positioned farther away:
  * Label: "Eve" (use RED color to indicate eavesdropper)
  * Arrow from gNodeB labeled "h_E"
  * Distance annotation: "d_E > 20cm"
  * Correlation annotation: "ρ_E ≈ 0" (decorrelated)

MATHEMATICAL ANNOTATIONS (small, professional font):
- Top or side corner: Mathematical box with "ρ = J₀(2πd/λ)" (Clarke model)
- Near Alice/Bob: "Spatial correlation"
- Near Eve: "Decorrelated"

VISUAL STYLE:
- Clean engineering schematic (not photo-realistic)
- Blue/gray tones for Alice/Bob (legitimate users)
- Red tone for Eve (threat/eavesdropper)
- Dashed security perimeter circle at 20cm radius around Alice/Bob
- Professional IEEE publication quality
- High contrast for black & white printing compatibility
- Grid background optional (very subtle if used)

The diagram must clearly convey: Alice and Bob are spatially correlated (close proximity) while Eve is decorrelated (far away), forming the physical security basis for key generation.
```

**Alternativa se IA não funcionar:** 
- Procure no Google Images: "5G downlink communication diagram" ou "spatial correlation wireless channel"
- Use PowerPoint/Google Slides para criar com formas básicas e anotações
- Ferramentas recomendadas: draw.io, Lucidchart, TikZ (LaTeX)

---

## FIGURA 2: Fluxograma do Processo PKG (Seção II)

**Tipo:** Fluxograma vertical (4 etapas sequenciais)  
**Onde usar:** Seção II (Fundamentos Teóricos) - Processo de Geração de Chaves em Camada Física  
**Label LaTeX:** `\label{fig:Processo_Geração}`  
**Arquivo:** `paper/overleaf/figuras/fig02_fluxograma_pkg.png`

### Prompt para IA:
```
Create a professional vertical flowchart for an IEEE academic paper showing the Physical-Layer Key Generation protocol. White background, clean technical style.

STRUCTURE (4 sequential stages, top to bottom):

╔════════════════════════════════════════╗
║    STAGE 1: CHANNEL PROBING           ║
╠════════════════════════════════════════╣
║ Box title: "Sondagem e Amostragem"    ║
║ Formula: y_i = h_i · x + n_i          ║
║ Icon: Antenna/tower symbol            ║
║ Description: "Observações              ║
║              correlacionadas"          ║
╚════════════════════════════════════════╝
           ↓ (arrow down)
╔════════════════════════════════════════╗
║    STAGE 2: QUANTIZATION              ║
╠════════════════════════════════════════╣
║ Box title: "Quantização"              ║
║ Formula: b_i = Q(z_i)                 ║
║ Icon: Digital waveform/binary         ║
║ Description: "BPSK/QPSK               ║
║              Guard-band opcional"      ║
╚════════════════════════════════════════╝
           ↓ (arrow down)
╔════════════════════════════════════════╗
║    STAGE 3: RECONCILIATION            ║
╠════════════════════════════════════════╣
║ Box title: "Reconciliação"            ║
║ Formula: σ = b_B ⊕ c                  ║
║ Icon: Error correction symbol         ║
║ Description: "Código BCH(127,64,10)   ║
║              Canal público"            ║
╚════════════════════════════════════════╝
           ↓ (arrow down)
╔════════════════════════════════════════╗
║    STAGE 4: PRIVACY AMPLIFICATION     ║
╠════════════════════════════════════════╣
║ Box title: "Amplificação Privacidade" ║
║ Formula: k_final = H(k)               ║
║ Icon: Lock/padlock symbol             ║
║ Description: "SHA-256                 ║
║              Chave 256 bits"           ║
╚════════════════════════════════════════╝

VISUAL SPECIFICATIONS:
- Box style: Light blue fill (#E3F2FD), dark blue border (#1976D2), rounded corners
- Box dimensions: Approximately same width, height adjust to content
- Arrows: Solid dark blue, medium thickness, with arrowhead
- Formula text: Mathematical font, clear and readable
- Icons: Simple, minimalist, monochrome (blue/gray)
- Spacing: Equal vertical spacing between boxes
- Title text: Bold, 14pt
- Formula text: 12pt
- Description text: Regular, 10pt
- Overall dimensions: Portrait orientation, suitable for IEEE column

STYLE GUIDELINES:
- Professional engineering diagram
- Clean, minimalist design
- High contrast for printing
- IEEE publication quality
- No shadows or 3D effects
- White/light gray background
- Grid lines optional (very subtle if included)

The flowchart must clearly show the sequential nature of the PKG process, from correlated channel observations to final secure key generation.
```

**Alternativa manual (PowerPoint/Google Slides):**
1. Criar 4 retângulos arredondados verticalmente alinhados
2. Preencher com azul claro (#E3F2FD), borda azul escuro (#1976D2)
3. Inserir texto em cada caixa:
   - Título em negrito (ex: "Sondagem e Amostragem")
   - Fórmula matemática (usar Inserir → Equação)
   - Descrição breve abaixo
4. Adicionar setas verticais entre as caixas
5. Inserir ícones simples ao lado de cada título:
   - Etapa 1: 📡 antena
   - Etapa 2: 💠 sinal digital
   - Etapa 3: ⚙️ engrenagem/correção
   - Etapa 4: 🔒 cadeado
6. Exportar como PNG 300 DPI (Arquivo → Salvar Como → PNG, opções de alta qualidade)

**Ferramentas alternativas:**
- **draw.io** (diagrams.net) - gratuito, online, templates prontos
- **Lucidchart** - profissional, tem versão gratuita
- **Dia Diagram Editor** - código aberto, Windows/Linux
- **TikZ (LaTeX)** - para quem domina LaTeX, resultado perfeito

---

## RESUMO DAS FIGURAS

**Figuras conceituais para geração por IA ou manualmente:**

1. **fig:modelo_sistema** - Diagrama Alice/Bob/Eve com correlação espacial
   - 📍 Seção II (Modelo de Sistema)
   - 📄 Arquivo: `fig01_modelo_sistema.png`
   - ⚠️ **PRECISA GERAR** - Usar IA (DALL-E, Midjourney) ou PowerPoint
   
2. **fig:Processo_Geração** - Fluxograma das 4 etapas do protocolo PKG
   - 📍 Seção II (Processo de Geração de Chaves)
   - 📄 Arquivo: `fig02_fluxograma_pkg.png`
   - ⚠️ **PRECISA GERAR** - Usar IA ou draw.io/PowerPoint

### 🔧 AÇÕES NECESSÁRIAS:

1. ⚠️ **Gerar fig01_modelo_sistema.png** 
   - **Opção 1 (Recomendada):** IA generativa (DALL-E, Midjourney, Stable Diffusion)
     * Copiar prompt completo da seção "FIGURA 1" acima
     * Gerar imagem
     * Salvar como PNG 300 DPI mínimo
   - **Opção 2:** PowerPoint/Google Slides
     * Criar manualmente com formas e setas
     * Adicionar anotações matemáticas
     * Exportar como PNG alta qualidade
   - **Opção 3:** draw.io, Lucidchart, ou TikZ (LaTeX)
   
2. ⚠️ **Gerar fig02_fluxograma_pkg.png**
   - **Opção 1 (Recomendada):** IA generativa
     * Copiar prompt completo da seção "FIGURA 2" acima
     * Gerar fluxograma vertical com 4 etapas
   - **Opção 2:** PowerPoint/Google Slides
     * Seguir instruções manuais fornecidas
     * Usar retângulos arredondados + setas
     * Adicionar ícones (antena, binário, engrenagem, cadeado)
   - **Opção 3:** draw.io (tem templates de fluxograma prontos)

### 📋 FERRAMENTAS RECOMENDADAS:

**Para IA Generativa:**
- DALL-E 3 (OpenAI) - excelente para diagramas técnicos
- Midjourney - resultados artísticos de alta qualidade
- Stable Diffusion - código aberto, customizável

**Para Criação Manual:**
- draw.io (diagrams.net) - gratuito, templates prontos
- PowerPoint/Google Slides - fácil, universal
- Lucidchart - profissional, colaborativo
- TikZ (LaTeX) - perfeito para publicações acadêmicas

---

## INSTRUÇÕES FINAIS DE USO

### Para gerar as 2 figuras conceituais:

**1. Figura 1 (Diagrama Modelo de Sistema):**
```bash
# Opção A: Usar IA (DALL-E, Midjourney, Stable Diffusion, etc.)
# 1. Copiar prompt completo da seção "FIGURA 1" acima
# 2. Colar na IA geradora de imagens
# 3. Ajustar se necessário (pode gerar múltiplas versões e escolher a melhor)
# 4. Salvar em: paper/overleaf/figuras/fig01_modelo_sistema.png

# Opção B: Criar manualmente (PowerPoint/Google Slides)
# 1. Abrir PowerPoint/Slides em branco
# 2. Inserir formas: retângulos (Alice, Bob, Eve), triângulo (gNodeB)
# 3. Adicionar setas com rótulos (h_A, h_B, h_E, x)
# 4. Inserir fórmula matemática (Inserir → Equação): ρ = J₀(2πd/λ)
# 5. Colorir: azul/cinza para Alice/Bob, vermelho para Eve
# 6. Exportar: Arquivo → Salvar Como → PNG, configurar DPI alto (300)
# 7. Salvar em: paper/overleaf/figuras/fig01_modelo_sistema.png
```

**2. Figura 2 (Fluxograma PKG):**
```bash
# Opção A: Usar IA (recomendada para fluxogramas)
# 1. Copiar prompt completo da seção "FIGURA 2" acima
# 2. Colar na IA geradora de imagens
# 3. Verificar se as 4 etapas estão corretas e legíveis
# 4. Salvar em: paper/overleaf/figuras/fig02_fluxograma_pkg.png

# Opção B: Usar draw.io (diagrams.net) - MUITO FÁCIL
# 1. Acessar https://app.diagrams.net/
# 2. Novo diagrama → Flowchart template
# 3. Arrastar 4 retângulos arredondados verticalmente
# 4. Conectar com setas
# 5. Adicionar texto conforme especificado no prompt
# 6. Exportar: File → Export as → PNG (300 DPI)
# 7. Salvar em: paper/overleaf/figuras/fig02_fluxograma_pkg.png

# Opção C: PowerPoint/Slides (mesma lógica da Figura 1)
```

---

**Documento atualizado:** 12/02/2026  
**Status:** ✅ Pronto para geração das 2 figuras conceituais com IA  
**Próximo passo:**
1. Copiar prompts acima
2. Gerar fig01_modelo_sistema.png usando IA ou PowerPoint
3. Gerar fig02_fluxograma_pkg.png usando IA ou draw.io
4. Salvar arquivos em `paper/overleaf/figuras/`
5. Compilar LaTeX para verificar resultado
