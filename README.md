# Segurança em Camada Física: Estabelecimento de Chaves Crip## Estrutura do Projeto

```
Criptografia/
├── main.py                       # Script principal
├── plotkdr.py                    # Geração de gráficos
├── README.md                     # Este arquivo
├── canal/                        # Simulação de canal
│   ├── canal.py                  # Implementação Rayleigh + BPSK
│   └── __init__.py
├── codigos_corretores/           # Códigos de correção
│   ├── bch.py                    # Implementação BCH
│   └── __init__.py
├── pilares/                      # Três pilares do PKG
│   ├── reconciliacao.py         # Code-offset algorithm
│   ├── amplificacao_privacidade.py # SHA-256
│   └── __init__.py
├── util/                         # Utilitários
│   ├── binario_util.py          # Operações binárias
│   ├── util.py                  # Funções auxiliaresnicações Móveis de Próxima Geração

Este projeto faz parte da Iniciação Científica (IC) **"Segurança em Camada Física: Estabelecimento de Chaves Criptográficas para Comunicações Móveis de Próxima Geração"**.

- **Autores:** Pedro Henrique Duarte Frugoli e Henrique Rodrigues Mendonça
- **Baseado em código anterior de:** João Gabriel Ferreira Ribeiro

## Objetivo

O objetivo deste projeto é implementar um sistema completo de **Physical-layer Key Generation (PKG)** com os três pilares fundamentais:

1. **Estimativa de Canal** - Simulação Rayleigh com BPSK e reciprocidade
2. **Reconciliação de Chave** - Códigos BCH com algoritmo code-offset
3. **Amplificação de Privacidade** - SHA-256 para segurança criptográfica

O sistema simula o estabelecimento de chaves criptográficas em relação ao SNR, validando a eficácia das correções implementadas para cenários realísticos.

## Dependências

Certifique-se de ter o **Python 3.x** instalado. Instale as dependências necessárias com:

```sh
pip install numpy matplotlib galois
```

## Como Executar

### Execução Principal
```sh
python main.py
```

### Executar Testes Automatizados
```sh
# Suíte completa de testes
cd testes
python executar_testes.py

# Teste específico do sistema completo
python executar_testes.py --test=completo

# Modo rápido
python executar_testes.py --quick
```

## Entradas do Usuário

Durante a execução, o usuário deverá fornecer:

- **Quantidade de testes:** Número de simulações a serem realizadas
- **Tamanho da cadeia de bits:** Escolha entre `7, 15, 127, 255`
- **Tamanho do espaço amostral:** (Opcional, para cadeias > 15 bits)

## Saída

O sistema gera gráficos comparativos mostrando:
- **KDR antes da reconciliação** (linha vermelha)
- **KDR pós reconciliação** (linha azul) 
- **KDR pós amplificação** (linha verde) - quando habilitado

## 🧩 Estrutura do Projeto

```
📁 Criptografia/
├── 📄 main.py                    # Script principal
├── 📄 plotkdr.py                 # Geração de gráficos
├── 📄 README.md                  # Este arquivo
├── 📁 canal/                     # Simulação de canal
│   ├── canal.py                  # Implementação Rayleigh + BPSK
│   └── __init__.py
├── 📁 codigos_corretores/        # Códigos de correção
│   ├── bch.py                    # Implementação BCH
│   └── __init__.py
├── 📁 pilares/                   # Três pilares do PKG
│   ├── reconciliacao.py         # Code-offset algorithm
│   ├── amplificacao_privacidade.py # SHA-256
│   └── __init__.py
├── 📁 util/                      # Utilitários
│   ├── binario_util.py          # Operações binárias
│   ├── util.py                  # Funções auxiliares
│   └── __init__.py
├── testes/                       # Suíte de testes
│   ├── executar_testes.py       # Runner principal
│   ├── teste_pkg_completo.py    # Teste completo
│   ├── teste_melhorias.py       # Validação melhorias
│   ├── teste_amplificacao.py    # Teste amplificação
│   ├── comparacao_melhorias.py  # Comparação A/B
│   ├── README.md               # Documentação dos testes
│   └── __init__.py
└── docs/                        # Documentação
    ├── README.md               # Índice da documentação
    ├── RELATORIO_FINAL.md      # Relatório executivo
    ├── MELHORIAS_IMPLEMENTADAS.md # Detalhes técnicos
    ├── ANALISE_AMPLIFICACAO_PRIVACIDADE.md
    ├── NOTES.md               # Notas de desenvolvimento
    └── TODO.md               # Tarefas pendentes
```

## Resultados Principais

### Sistema PKG Completo Implementado
- **Redução média KDR**: ~22 pontos percentuais
- **Máxima melhoria**: 41.5 pontos (SNR baixo)
- **Convergência**: SNR ≥ 4dB → KDR = 0%
- **Segurança**: 256 bits (2^256 operações para quebra)

### Melhorias Técnicas Realizadas
1. **Reciprocidade de Canal**: Correlação ρ=0.9 entre Alice e Bob
2. **Migração OOK→BPSK**: Modulação simétrica otimizada
3. **SNR-Variância Corrigida**: Fórmula adequada para BPSK
4. **Amplificação SHA-256**: Implementação robusta
5. **Documentação Completa**: Sistema totalmente documentado

## Performance

- **Tempo de execução**: 0.5-2s (dependendo dos parâmetros)
- **Performance amplificação**: < 0.2ms por operação
- **Memória**: Otimizada para códigos BCH grandes
- **Escalabilidade**: Suporta cadeias de 7 a 255 bits

## Validação

O sistema foi extensivamente testado com:
- **Suíte automatizada** de 4+ testes diferentes
- **Comparações A/B** entre versões
- **Análises estatísticas** com centenas de iterações
- **Validação criptográfica** das propriedades de segurança

Para executar a validação completa:
```sh
cd testes && python executar_testes.py
```

---

**Este projeto implementa um sistema PKG de qualidade industrial com os três pilares fundamentais para comunicações móveis seguras de próxima geração.**
