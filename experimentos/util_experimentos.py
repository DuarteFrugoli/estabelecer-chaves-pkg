"""
Utilitários para salvar e carregar resultados de experimentos
"""

import json
import csv
import os
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np


def salvar_resultado_json(dados, nome_experimento, descricao=""):
    """
    Salva resultados em formato JSON
    
    Args:
        dados: Dicionário com os resultados
        nome_experimento: Nome do experimento (ex: "teste_snr")
        descricao: Descrição do experimento
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{nome_experimento}_{timestamp}.json"
    filepath = os.path.join("resultados", "dados", filename)
    
    resultado_completo = {
        "experimento": nome_experimento,
        "descricao": descricao,
        "timestamp": timestamp,
        "data_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "dados": dados
    }
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(resultado_completo, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Resultados salvos em: {filepath}")
    return filepath


def salvar_resultado_csv(dados, nome_experimento, colunas):
    """
    Salva resultados em formato CSV
    
    Args:
        dados: Lista de dicionários com os resultados
        nome_experimento: Nome do experimento
        colunas: Lista com nomes das colunas
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{nome_experimento}_{timestamp}.csv"
    filepath = os.path.join("resultados", "dados", filename)
    
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=colunas)
        writer.writeheader()
        writer.writerows(dados)
    
    print(f"✓ CSV salvo em: {filepath}")
    return filepath


def salvar_grafico(fig, nome_experimento, nome_grafico=""):
    """
    Salva gráfico em formato PNG de alta resolução
    
    Args:
        fig: Figura matplotlib
        nome_experimento: Nome do experimento
        nome_grafico: Nome específico do gráfico
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if nome_grafico:
        filename = f"{nome_experimento}_{nome_grafico}_{timestamp}.png"
    else:
        filename = f"{nome_experimento}_{timestamp}.png"
    
    filepath = os.path.join("resultados", "graficos", filename)
    fig.savefig(filepath, dpi=300, bbox_inches='tight')
    print(f"✓ Gráfico salvo em: {filepath}")
    return filepath


def criar_grafico_comparativo_kdr(snr_db, dados_variacoes, 
                                   titulo, xlabel, 
                                   nome_arquivo, 
                                   legenda_template=None):
    """
    Cria gráfico comparativo de KDR para diferentes variações de parâmetro
    
    Args:
        snr_db: Array com valores de SNR
        dados_variacoes: Dict com dados para cada variação
        titulo: Título do gráfico
        xlabel: Label do eixo X
        nome_arquivo: Nome do arquivo para salvar
        legenda_template: Template para legendas (ex: "σ = {}")
    """
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    fig.suptitle(titulo, fontsize=14, fontweight='bold')
    
    cores = plt.cm.tab10(np.linspace(0, 1, len(dados_variacoes)))
    
    titulos_subplots = [
        'KDR Antes da Reconciliação',
        'KDR Pós Reconciliação',
        'KDR Pós Amplificação (SHA-256)'
    ]
    
    metricas = ['kdr_rates', 'kdr_pos_rates', 'kdr_amplificacao_rates']
    
    for i, (metrica, titulo_sub) in enumerate(zip(metricas, titulos_subplots)):
        ax = axes[i]
        
        for j, (variacao, dados) in enumerate(sorted(dados_variacoes.items())):
            if legenda_template:
                label = legenda_template.format(variacao)
            else:
                label = str(variacao)
            
            ax.plot(snr_db, dados[metrica], 
                   marker='o', linestyle='-', linewidth=2,
                   color=cores[j], label=label)
        
        ax.set_xlabel(xlabel)
        ax.set_ylabel('KDR (%)')
        ax.set_title(titulo_sub)
        ax.grid(True, alpha=0.3)
        ax.legend()
    
    plt.tight_layout()
    
    filepath = salvar_grafico(fig, nome_arquivo)
    plt.close()
    
    return filepath


def gerar_tabela_latex(dados, nome_experimento):
    """
    Gera código LaTeX para tabela de resultados
    
    Args:
        dados: Lista de dicionários com resultados
        nome_experimento: Nome do experimento
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"tabela_{nome_experimento}_{timestamp}.tex"
    filepath = os.path.join("resultados", "dados", filename)
    
    if not dados:
        return None
    
    # Pega as chaves do primeiro item como colunas
    colunas = list(dados[0].keys())
    
    latex = "\\begin{table}[h]\n"
    latex += "\\centering\n"
    latex += "\\begin{tabular}{" + "c" * len(colunas) + "}\n"
    latex += "\\hline\n"
    
    # Cabeçalho
    latex += " & ".join(colunas) + " \\\\\n"
    latex += "\\hline\n"
    
    # Linhas de dados
    for linha in dados:
        valores = [str(linha[col]) for col in colunas]
        latex += " & ".join(valores) + " \\\\\n"
    
    latex += "\\hline\n"
    latex += "\\end{tabular}\n"
    latex += f"\\caption{{Resultados do experimento: {nome_experimento}}}\n"
    latex += f"\\label{{tab:{nome_experimento}}}\n"
    latex += "\\end{table}\n"
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(latex)
    
    print(f"✓ Tabela LaTeX salva em: {filepath}")
    return filepath


def imprimir_sumario_resultados(dados):
    """
    Imprime um sumário dos resultados na tela
    """
    print("\n" + "="*70)
    print("SUMÁRIO DOS RESULTADOS")
    print("="*70)
    
    if isinstance(dados, dict):
        for chave, valor in dados.items():
            if isinstance(valor, (list, np.ndarray)):
                print(f"{chave}:")
                print(f"  Mín: {np.min(valor):.4f}")
                print(f"  Máx: {np.max(valor):.4f}")
                print(f"  Média: {np.mean(valor):.4f}")
                print(f"  Desvio: {np.std(valor):.4f}")
            else:
                print(f"{chave}: {valor}")
    
    print("="*70 + "\n")
