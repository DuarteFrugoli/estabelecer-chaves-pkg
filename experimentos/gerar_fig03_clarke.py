"""
Gera a figura 3: Curva de Correlação Espacial de Clarke
Frequência: 2.4 GHz (λ ≈ 12.5 cm)
Arquivo de saída: ../paper/overleaf/figuras/fig03_clarke_correlacao.png
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import jv
import os

def gerar_figura_clarke():
    """
    Gera o gráfico da correlação espacial segundo o modelo de Clarke.
    """
    # Criar diretório de saída se não existir (caminho absoluto)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    output_dir = os.path.join(project_root, 'paper', 'overleaf', 'figuras')
    os.makedirs(output_dir, exist_ok=True)
    
    # Parâmetros do sistema
    freq = 2.4e9  # 2.4 GHz
    c = 3e8  # Velocidade da luz (m/s)
    lambda_m = c / freq  # Comprimento de onda (≈ 12.5 cm)
    
    print(f"Frequência: {freq/1e9:.1f} GHz")
    print(f"Comprimento de onda: {lambda_m*100:.2f} cm")
    
    # Vetor de distâncias (0 a 1 m)
    d = np.linspace(0, 1.0, 1000)
    
    # Função de Bessel J₀ - Modelo de Clarke
    rho = jv(0, 2*np.pi*d/lambda_m)
    
    # Configuração da figura (tamanho IEEE padrão)
    plt.figure(figsize=(10, 6))
    
    # Plot principal
    plt.plot(d, rho, 'b-', linewidth=2.5, 
             label=r'Modelo de Clarke: $\rho = J_0(2\pi d/\lambda)$')
    
    # Linhas de referência
    plt.axhline(0, color='gray', linestyle='--', linewidth=1, alpha=0.7)
    plt.axvline(0.2, color='red', linestyle='--', linewidth=2.0, 
                label='Limiar de segurança (20 cm)', zorder=10)
    
    # Zonas de segurança (visual)
    plt.fill_between(d, -0.5, 1.0, where=(d <= 0.2), 
                     alpha=0.08, color='green', label='Zona correlacionada')
    plt.fill_between(d, -0.5, 1.0, where=(d > 0.2), 
                     alpha=0.08, color='red', label='Zona descorrelacionada')
    
    # Anotações
    plt.text(0.05, 0.85, f'$f = 2.4$ GHz\n$\\lambda \\approx {lambda_m*100:.1f}$ cm', 
             fontsize=12, bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    plt.text(0.21, 0.15, 'Zona segura\n(Eve decorrelacionado)', 
             fontsize=10, color='red')
    
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
    
    # Mostrar figura (opcional - comentar para execução em batch)
    # plt.show()
    
    return output_path


if __name__ == '__main__':
    print("=" * 60)
    print("Gerando Figura 3: Curva de Correlação Espacial de Clarke")
    print("=" * 60)
    
    caminho_figura = gerar_figura_clarke()
    
    print("\n" + "=" * 60)
    print("Geração concluída com sucesso!")
    print(f"Arquivo: {caminho_figura}")
    print("=" * 60)
