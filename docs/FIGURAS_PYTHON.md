# Figuras Geradas com Python para o Artigo - Sistema PKG

**Data:** 12/02/2026  
**Objetivo:** Scripts Python para geração de figuras científicas do artigo

---

## FIGURA 3: Curva de Correlação Espacial de Clarke (Seção II)

**Tipo:** Gráfico científico quantitativo  
**Onde usar:** Seção II (Fundamentos Teóricos) - O Canal Sem Fio e Suas Propriedades  
**Label LaTeX:** `\label{fig:clarke_correlacao}`  
**Arquivo de saída:** `paper/overleaf/figuras/fig03_clarke_correlacao.png`

### Script Python Completo

```python
"""
Gera a curva de correlação espacial de Clarke para o artigo.
Frequência: 2.4 GHz (λ ≈ 12.5 cm)
Arquivo de saída: fig03_clarke_correlacao.png
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import jv
import os

# Criar diretório de saída se não existir
output_dir = 'paper/overleaf/figuras'
os.makedirs(output_dir, exist_ok=True)

# Parâmetros do sistema
freq = 2.4e9  # 2.4 GHz
c = 3e8  # Velocidade da luz (m/s)
lambda_m = c / freq  # Comprimento de onda (≈ 12.5 cm)

# Vetor de distâncias (0 a 1 m)
d = np.linspace(0, 1.0, 1000)

# Função de Bessel J₀ - Modelo de Clarke
rho = jv(0, 2*np.pi*d/lambda_m)

# Configuração da figura (tamanho IEEE padrão)
plt.figure(figsize=(10, 6))

# Plot principal
plt.plot(d, rho, 'b-', linewidth=2.5, label='Modelo de Clarke: $\\rho = J_0(2\\pi d/\\lambda)$')

# Linhas de referência
plt.axhline(0, color='gray', linestyle='--', linewidth=1, alpha=0.7)
plt.axvline(0.2, color='red', linestyle='--', linewidth=2.0, 
            label='Limiar de segurança (20 cm)', zorder=10)

# Zonas de segurança (opcional - visual)
plt.fill_between(d, -0.5, 1.0, where=(d <= 0.2), alpha=0.08, color='green')
plt.fill_between(d, -0.5, 1.0, where=(d > 0.2), alpha=0.08, color='red')

# Anotações
plt.text(0.05, 0.85, f'$f = 2.4$ GHz\n$\\lambda \\approx {lambda_m*100:.1f}$ cm', 
         fontsize=12, bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
plt.text(0.21, 0.15, 'Zona segura\n(Eve decorrelacionado)', fontsize=10, color='red')

# Formatação dos eixos
plt.xlabel('Distância $d$ (m)', fontsize=14, fontweight='bold')
plt.ylabel('Correlação Espacial $\\rho$', fontsize=14, fontweight='bold')
plt.title('Correlação Espacial segundo Modelo de Clarke', 
          fontsize=16, fontweight='bold', pad=15)

# Grade e legenda
plt.grid(True, alpha=0.3, linestyle=':', linewidth=0.8)
plt.legend(fontsize=11, loc='upper right', framealpha=0.95)

# Limites dos eixos
plt.xlim(0, 1.0)
plt.ylim(-0.5, 1.05)

# Ajuste do layout
plt.tight_layout()

# Salvar em alta resolução (300 DPI para publicação)
output_path = os.path.join(output_dir, 'fig03_clarke_correlacao.png')
plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
print(f"✅ Figura salva em: {output_path}")

# Opcional: mostrar figura
# plt.show()
```

### Instruções de Uso

**Opção 1: Executar diretamente**
```powershell
python -c "import numpy as np; import matplotlib.pyplot as plt; from scipy.special import jv; import os; output_dir = 'paper/overleaf/figuras'; os.makedirs(output_dir, exist_ok=True); freq = 2.4e9; c = 3e8; lambda_m = c / freq; d = np.linspace(0, 1.0, 1000); rho = jv(0, 2*np.pi*d/lambda_m); plt.figure(figsize=(10, 6)); plt.plot(d, rho, 'b-', linewidth=2.5, label='Modelo de Clarke: \$\\rho = J_0(2\\pi d/\\lambda)\$'); plt.axhline(0, color='gray', linestyle='--', linewidth=1, alpha=0.7); plt.axvline(0.2, color='red', linestyle='--', linewidth=2.0, label='Limiar de segurança (20 cm)', zorder=10); plt.fill_between(d, -0.5, 1.0, where=(d <= 0.2), alpha=0.08, color='green'); plt.fill_between(d, -0.5, 1.0, where=(d > 0.2), alpha=0.08, color='red'); plt.text(0.05, 0.85, f'\$f = 2.4\$ GHz\\n\$\\lambda \\approx {lambda_m*100:.1f}\$ cm', fontsize=12, bbox=dict(boxstyle='round', facecolor='white', alpha=0.8)); plt.text(0.21, 0.15, 'Zona segura\\n(Eve decorrelacionado)', fontsize=10, color='red'); plt.xlabel('Distância \$d\$ (m)', fontsize=14, fontweight='bold'); plt.ylabel('Correlação Espacial \$\\rho\$', fontsize=14, fontweight='bold'); plt.title('Correlação Espacial segundo Modelo de Clarke', fontsize=16, fontweight='bold', pad=15); plt.grid(True, alpha=0.3, linestyle=':', linewidth=0.8); plt.legend(fontsize=11, loc='upper right', framealpha=0.95); plt.xlim(0, 1.0); plt.ylim(-0.5, 1.05); plt.tight_layout(); output_path = os.path.join(output_dir, 'fig03_clarke_correlacao.png'); plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white'); print(f'✅ Figura salva em: {output_path}')"
```

**Opção 2: Salvar como arquivo e executar**
1. Copie o código acima para um arquivo `gerar_fig03_clarke.py`
2. Execute: `python gerar_fig03_clarke.py`
3. A figura será salva automaticamente em `paper/overleaf/figuras/fig03_clarke_correlacao.png`

### Dependências Necessárias

```powershell
pip install numpy matplotlib scipy
```

### Especificações Técnicas

- **Resolução:** 300 DPI (padrão IEEE para publicação)
- **Formato:** PNG com fundo branco
- **Dimensões:** 10×6 polegadas (2400×1440 pixels @ 300 DPI)
- **Modelo matemático:** Função de Bessel de primeira espécie $J_0(2\pi d/\lambda)$
- **Parâmetros:** 
  - Frequência: 2.4 GHz (banda ISM)
  - Comprimento de onda: ~12.5 cm
  - Distância de segurança: 20 cm (limiar de descorrelação)

### Validação Visual

A figura gerada deve apresentar:
- ✅ Curva azul iniciando em ρ=1.0 (d=0m) e decaindo com oscilações
- ✅ Linha vermelha vertical tracejada em d=0.2m
- ✅ Zona verde clara (d < 20cm) e zona vermelha clara (d > 20cm)
- ✅ Anotações com parâmetros do sistema no canto superior esquerdo
- ✅ Grade de fundo sutil
- ✅ Legenda no canto superior direito

---

**Documento atualizado:** 12/02/2026  
**Status:** ✅ Script pronto para execução  
**Próximo passo:** Executar o script Python para gerar fig03_clarke_correlacao.png
