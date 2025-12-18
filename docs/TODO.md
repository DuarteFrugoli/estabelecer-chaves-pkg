# Objetivo principal atual
Chegar a um estado em que seja possível simular a distância (frequência) entre dispositivos e um invasor tentando acessar a chave gerada entre eles. Plot de chaves geradas, reconciliadas e descobertas pelo invasor no final.

## Progresso da Implementação Realista

### 🔄 Próximos Passos
2. ⏳ **Path loss** - Atenuação dependente de distância e frequência
3. ⏳ **Fading temporal** - Modelo de Jakes para fading correlacionado
4. ⏳ **Correlação espacial** - Diferentes canais para Alice-Bob e Alice-Eva
5. ⏳ **Simulador de invasor (Eve)** - Terceiro agente tentando interceptar

## Importante
- simular invasor
- simular distância
- estudar mais termos de bpsk e qpsk e implementá-los no código
- estudar como a quantidade de erros que o bch pode corrigir afeta os resultados
- escrever o começo do relatório

## Paper
1. introdução: importancia da segurança, importancia da confidencialidade, porque nós usamos pkg
2. background teórico: contextualização geral dos processos de como que tudo funciona sem ser específico sobre nosso sistema
3. modelo de sistema: definição específica teórica do nosso processo sem falar sobre a prática da simulação
4. materiais e métodos: como que o nosso sistema funciona e explicações de código e simulação
5. conclusão: resultados obtidos a partir dos nossos trabalhos

- usar poucos bullets e ser mais técnico
- colocar imagens principalmente no tópico 2 e 3
- colocar imagens do código no tópico 4
- imagens de resultados na 5 obviamente
- prestar atenção na contextualização sempre, do porque aquilo é importante ser mencionado

rodar a bateria completa de testes:
poetry run python experimentos/executar_todos.py --modo completo