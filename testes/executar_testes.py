#!/usr/bin/env python
"""
Script principal para executar todos os testes do sistema PKG

Este script executa uma suíte completa de testes incluindo:
- Testes individuais de componentes
- Testes de integração
- Validação do sistema completo

Uso:
    python executar_testes.py [--test=nome_do_teste] [--quick] [--verbose]
"""

import sys
import os
import argparse
import time

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def executar_teste_amplificacao():
    """Executa teste da amplificação de privacidade"""
    print("EXECUTANDO: Teste de Amplificação de Privacidade")
    print("-" * 50)
    
    try:
        from teste_amplificacao import teste_amplificacao_privacidade
        return teste_amplificacao_privacidade()
    except Exception as e:
        print(f"ERRO no teste de amplificação: {e}")
        return False

def executar_teste_melhorias():
    """Executa teste automatizado das melhorias"""
    print("\nEXECUTANDO: Teste das Melhorias Implementadas")
    print("-" * 50)
    
    try:
        from teste_melhorias import teste_automatizado
        return teste_automatizado()
    except Exception as e:
        print(f"ERRO no teste de melhorias: {e}")
        return False

def executar_teste_completo():
    """Executa teste do sistema PKG completo"""
    print("\nEXECUTANDO: Teste Sistema PKG Completo (3 Pilares)")
    print("-" * 50)
    
    try:
        from teste_pkg_completo import teste_pkg_completo, teste_individual_amplificacao
        teste_pkg_completo()
        teste_individual_amplificacao()
        return True
    except Exception as e:
        print(f"ERRO no teste completo: {e}")
        return False

def executar_todos_os_testes(quick_mode=False, verbose=False):
    """Executa toda a suíte de testes"""
    print("INICIANDO SUÍTE COMPLETA DE TESTES PKG")
    print("=" * 60)
    
    start_time = time.time()
    resultados = {}
    
    # Lista de testes a executar
    testes = [
        ("amplificacao", "Amplificação de Privacidade", executar_teste_amplificacao),
        ("melhorias", "Melhorias Implementadas", executar_teste_melhorias),
        ("completo", "Sistema PKG Completo", executar_teste_completo),
    ]
    
    # Executa cada teste
    for teste_id, nome, funcao in testes:
        try:
            print(f"\nIniciando: {nome}")
            resultado = funcao()
            resultados[teste_id] = resultado
            status = "PASSOU" if resultado else "FALHOU"
            print(f"Resultado: {status}")
        except Exception as e:
            print(f"ERRO CRÍTICO em {nome}: {e}")
            resultados[teste_id] = False
    
    # Relatório final
    execution_time = time.time() - start_time
    print("\n" + "=" * 60)
    print("RELATÓRIO FINAL DOS TESTES")
    print("=" * 60)
    
    sucessos = sum(1 for r in resultados.values() if r)
    total = len(resultados)
    
    for teste_id, nome, _ in testes:
        status = "PASSOU" if resultados.get(teste_id, False) else "FALHOU"
        print(f"  {nome:<35} {status}")
    
    print("-" * 60)
    print(f"Taxa de Sucesso: {sucessos}/{total} ({100*sucessos/total:.0f}%)")
    print(f"Tempo Total: {execution_time:.1f}s")
    
    if sucessos == total:
        print("TODOS OS TESTES PASSARAM! Sistema PKG está funcionando perfeitamente.")
    else:
        print("ALGUNS TESTES FALHARAM. Verifique os logs acima.")
    
    return sucessos == total

def main():
    """Função principal do script"""
    parser = argparse.ArgumentParser(description='Executar testes do sistema PKG')
    parser.add_argument('--test', choices=['amplificacao', 'melhorias', 'completo'], 
                       help='Executar um teste específico')
    parser.add_argument('--quick', action='store_true', 
                       help='Modo rápido (menos iterações)')
    parser.add_argument('--verbose', action='store_true',
                       help='Saída verbosa')
    
    args = parser.parse_args()
    
    if args.test:
        # Executa teste específico
        testes_disponiveis = {
            'amplificacao': executar_teste_amplificacao,
            'melhorias': executar_teste_melhorias, 
            'completo': executar_teste_completo
        }
        
        if args.test in testes_disponiveis:
            print(f"EXECUTANDO TESTE ESPECÍFICO: {args.test}")
            resultado = testes_disponiveis[args.test]()
            sys.exit(0 if resultado else 1)
        else:
            print(f"Teste '{args.test}' não encontrado")
            sys.exit(1)
    else:
        # Executa todos os testes
        sucesso = executar_todos_os_testes(quick_mode=args.quick, verbose=args.verbose)
        sys.exit(0 if sucesso else 1)

if __name__ == "__main__":
    main()
