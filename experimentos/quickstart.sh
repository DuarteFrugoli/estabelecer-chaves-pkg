#!/bin/bash

# Script de inicialização rápida dos experimentos
# Execute com: bash experimentos/quickstart.sh

echo "=============================================="
echo "  GUIA RÁPIDO - EXPERIMENTOS PKG"
echo "=============================================="
echo ""

echo "📋 OPÇÕES DISPONÍVEIS:"
echo ""
echo "1. Bateria Rápida (5-10 min) - Para testar"
echo "2. Bateria Completa (2-4 horas) - Para artigo"
echo "3. Experimento Individual"
echo "4. Sair"
echo ""

read -p "Escolha uma opção (1-4): " opcao

case $opcao in
    1)
        echo ""
        echo "🚀 Executando Bateria Rápida..."
        python3 experimentos/executar_todos.py --modo rapido
        ;;
    2)
        echo ""
        echo "⚠️  ATENÇÃO: Isso pode levar 2-4 horas!"
        read -p "Deseja continuar? (s/n): " confirma
        if [ "$confirma" = "s" ] || [ "$confirma" = "S" ]; then
            echo ""
            echo "🚀 Executando Bateria Completa..."
            python3 experimentos/executar_todos.py --modo completo
        else
            echo "❌ Cancelado."
        fi
        ;;
    3)
        echo ""
        echo "📊 EXPERIMENTOS DISPONÍVEIS:"
        echo ""
        echo "1. Variação de SNR"
        echo "2. Variação de Sigma (Rayleigh)"
        echo "3. Comparação BPSK vs QPSK"
        echo "4. Variação de Correlação"
        echo "5. Variação de Código BCH"
        echo ""
        read -p "Escolha o experimento (1-5): " exp
        
        case $exp in
            1)
                echo "🧪 Executando Experimento 1: Variação de SNR..."
                python3 experimentos/exp01_variacao_snr.py
                ;;
            2)
                echo "🧪 Executando Experimento 2: Variação de Sigma..."
                python3 experimentos/exp02_variacao_sigma.py
                ;;
            3)
                echo "🧪 Executando Experimento 3: Comparação Modulação..."
                python3 experimentos/exp03_comparacao_modulacao.py
                ;;
            4)
                echo "🧪 Executando Experimento 4: Variação de Correlação..."
                python3 experimentos/exp04_variacao_correlacao.py
                ;;
            5)
                echo "🧪 Executando Experimento 5: Variação de BCH..."
                echo "⚠️  Este experimento pode demorar mais..."
                python3 experimentos/exp05_variacao_bch.py
                ;;
            *)
                echo "❌ Opção inválida!"
                ;;
        esac
        ;;
    4)
        echo "👋 Até logo!"
        exit 0
        ;;
    *)
        echo "❌ Opção inválida!"
        ;;
esac

echo ""
echo "=============================================="
echo "✓ CONCLUÍDO!"
echo "=============================================="
echo ""
echo "📁 Resultados salvos em:"
echo "   - resultados/dados/ (JSON e CSV)"
echo "   - resultados/graficos/ (PNG)"
echo ""
echo "📖 Veja experimentos/README.md para mais detalhes"
echo ""
