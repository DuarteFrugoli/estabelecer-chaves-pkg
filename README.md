# Physical Key Generation (PKG) - Sistema de Criptografia em Camada Física

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Stable-brightgreen)
![Research](https://img.shields.io/badge/Research-IC%20Project-orange)

**Sistema completo de estabelecimento de chaves criptográficas usando características físicas do canal de comunicação**

[Funcionalidades](#funcionalidades) • [Instalação](#instalação) • [Como Usar](#como-usar) • [Arquitetura](#arquitetura) • [Resultados](#resultados)

</div>

---

## Sobre o Projeto

Este projeto implementa um sistema completo de **Physical Key Generation (PKG)** desenvolvido como parte da Iniciação Científica *"Segurança em Camada Física: Estabelecimento de Chaves Criptográficas para Comunicações Móveis de Próxima Geração"*.

### O que é PKG?

Physical Key Generation é uma técnica de segurança que utiliza as características naturais e aleatórias do canal de comunicação sem fio para gerar chaves criptográficas idênticas entre dois dispositivos (Alice e Bob), sem necessidade de troca prévia de segredos.

### Os Três Pilares Implementados

1. **Estimativa de Canal** - Simulação realística usando canal Rayleigh com modulação BPSK
2. **Reconciliação de Chave** - Correção de erros usando códigos BCH com algoritmo code-offset
3. **Amplificação de Privacidade** - Aplicação de SHA-256 para garantir segurança criptográfica

---

## Funcionalidades

### Sistema PKG Completo
- **Redução média KDR**: ~22 pontos percentuais
- **Convergência**: SNR ≥ 4dB → KDR = 0%
- **Segurança**: Chaves de 256 bits (SHA-256)
- **Reciprocidade**: Correlação ρ=0.9 entre canais

### Implementação Robusta
- **Canal Rayleigh** com ruído gaussiano e BPSK
- **Códigos BCH** para múltiplos tamanhos (7, 15, 127, 255 bits)
- **Detecção otimizada** com limiarização simétrica
- **Validação experimental** com análise estatística

### Interface Amigável
- **Menu interativo** para configuração de parâmetros
- **Gráficos automáticos** comparando KDR vs SNR
- **Logs detalhados** do processo de execução
- **Suite de testes** automatizada

---

## Instalação

### Pré-requisitos
- Python 3.8 ou superior
- Poetry (gerenciador de dependências moderno)

### Opção 1: Instalação com Poetry (Recomendada)

```bash
# Instale o Poetry (se não tiver)
curl -sSL https://install.python-poetry.org | python3 -
# ou no Windows:
# (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -

# Clone o repositório
git clone https://github.com/DuarteFrugoli/estabelecer-chaves-pkg.git
cd Criptografia

# Instale as dependências
poetry install

# Ative o ambiente virtual
poetry shell
```

### Opção 2: Instalação com pip (Alternativa)

```bash
# Clone o repositório
git clone https://github.com/DuarteFrugoli/estabelecer-chaves-pkg.git
cd Criptografia

# Instale as dependências principais
pip install numpy>=1.21.0 matplotlib>=3.5.0 galois>=0.3.7

# Para desenvolvimento (opcional)
pip install pytest>=7.0.0 pytest-cov>=4.0.0
```

### Opção 3: Ambiente Virtual Manual

```bash
# Windows
python -m venv venv
venv\Scripts\activate
pip install numpy>=1.21.0 matplotlib>=3.5.0 galois>=0.3.7

# Linux/Mac
python -m venv venv
source venv/bin/activate
pip install numpy>=1.21.0 matplotlib>=3.5.0 galois>=0.3.7
```

---

## Como Usar

### Execução Principal

```bash
python main.py
```

### Fluxo de Execução Passo a Passo

#### 1. **Configuração de Parâmetros**
```
Entre com a quantidade de testes: 100
Entre com o tamanho da cadeia de Bits (7, 15, 127, 255): 15
```

#### 2. **Escolha da Amplificação**
```
AMPLIFICAÇÃO DE PRIVACIDADE
A amplificação de privacidade aplica função hash SHA-256 para gerar chaves de 256 bits com segurança criptográfica.
Deseja usar amplificação de privacidade? (s/n): s
```

#### 3. **Processamento Automático**
O sistema executa automaticamente:
- **Geração de códigos BCH** para o tamanho especificado
- **Simulação de canais Rayleigh correlacionados** (ρ=0.9)
- **Aplicação de ruído gaussiano** com diferentes SNRs
- **Reconciliação usando code-offset** para corrigir erros
- **Amplificação com SHA-256** (se habilitada)
- **Análise estatística** dos resultados

#### 4. **Visualização dos Resultados**
- Gráficos KDR vs SNR são gerados automaticamente
- Comparação entre diferentes parâmetros Rayleigh (σ = 0.5, 1.0, 2.0)
- Análise com e sem amplificação de privacidade

### Executar Testes

```bash
python -m pytest tests/ -v
```

---

## Arquitetura

### Estrutura de Diretórios

```
Criptografia/
├── main.py                    # Script principal
├── plotkdr.py                 # Geração de gráficos
├── pyproject.toml            # Configuração Poetry e dependências
├── LICENSE                   # Licença MIT
├── canal/                     # Simulação de canal
│   ├── canal.py                  # Implementação Rayleigh + BPSK
│   └── __init__.py
├── codigos_corretores/        # Códigos de correção
│   ├── bch.py                    # Implementação BCH
│   └── __init__.py
├── pilares/                   # Três pilares do PKG
│   ├── reconciliacao.py         # Code-offset algorithm
│   ├── amplificacao_privacidade.py # SHA-256
│   └── __init__.py
├── util/                      # Utilitários
│   ├── binario_util.py          # Operações binárias
│   ├── util.py                  # Funções auxiliares
│   └── __init__.py
├── tests/                     # Suite de testes
│   ├── test_binario_util.py     # Testes unitários utilitários
│   ├── test_bch.py              # Testes códigos BCH
│   ├── test_reconciliacao.py    # Testes reconciliação
│   ├── test_amplificacao_privacidade.py # Testes amplificação
│   ├── test_canal.py            # Testes simulação canal
│   └── test_sistema_completo.py # Testes integração
└── docs/                      # Documentação
    ├── RELATORIO_FINAL.md       # Relatório executivo
    ├── MELHORIAS_IMPLEMENTADAS.md
    └── NOTES.md
```

### Fluxo de Dados do Sistema

O sistema PKG funciona seguindo este fluxo:

1. **Configuração**: Usuário define parâmetros (quantidade de testes, tamanho da cadeia)
2. **Geração BCH**: Sistema gera tabela de códigos para correção de erros
3. **Simulação de Canal**: 
   - Alice e Bob observam canais Rayleigh correlacionados (ρ=0.9)
   - Modulação BPSK com símbolos {-1, +1}
   - Adição de ruído gaussiano com variância σ² = Es/(2·SNR)
4. **Reconciliação**: Algoritmo code-offset corrige discrepâncias usando BCH
5. **Amplificação**: SHA-256 gera chave final de 256 bits (opcional)
6. **Análise**: Cálculo de KDR e geração de gráficos comparativos

---

## Resultados

### Performance do Sistema

| Métrica | Valor |
|---------|-------|
| **Redução média KDR** | ~22 pontos percentuais |
| **Máxima melhoria** | 41.5 pontos (SNR baixo) |
| **Convergência** | SNR ≥ 4dB → KDR = 0% |
| **Segurança** | 256 bits (2^256 operações) |
| **Tempo execução** | 0.5-2s (configuração típica) |
| **Performance amplificação** | < 0.2ms por operação |

### Comparação Antes/Depois das Melhorias

| SNR | KDR Original | KDR Melhorado | Melhoria |
|-----|-------------|---------------|----------|
| 0.0dB | 43.2% | 10.4% | -32.8 pts |
| 2.1dB | 33.6% | 8.1% | -25.5 pts |
| 8.6dB | 19.9% | 1.1% | -18.8 pts |
| 15.0dB | 7.7% | 0.0% | -7.7 pts |

### Interpretação dos Gráficos

Os gráficos gerados mostram:
- **Linha vermelha**: KDR antes da reconciliação (erro bruto do canal)
- **Linha azul**: KDR pós reconciliação BCH (após correção de erros)
- **Linha verde**: KDR pós amplificação SHA-256 (chave final)

---

## Como Funciona (Detalhes Técnicos)

### 1. Estimativa de Canal
```python
# Canal Rayleigh com correlação entre Alice e Bob
ganho_canal_alice = np.random.rayleigh(sigma, n_bits)
ganho_canal_bob = (ρ * ganho_canal_alice + 
                   √(1-ρ²) * ganho_independente)
```

### 2. Modulação BPSK
```python
# Mapeia bits {0,1} → símbolos {-1,+1}
simbolos_bpsk = 2 * bits - 1
sinal_recebido = ganho * simbolos_bpsk + ruido
bits_recebidos = (sinal_recebido >= 0).astype(int)
```

### 3. Reconciliação BCH (Code-Offset)
```python
# Alice calcula syndrome S = Ka ⊕ C
syndrome = alice_key XOR codigo_aleatorio

# Bob decodifica Cb = S ⊕ Kb para encontrar C
codigo_bob = bob_key XOR syndrome  
codigo_corrigido = decodificar_bch(codigo_bob)

# Chave final K = S ⊕ C_corrigido
chave_final = syndrome XOR codigo_corrigido
```

### 4. Amplificação SHA-256
```python
# Converte bits → bytes → SHA-256 → 256 bits finais
chave_bytes = bits_to_bytes(chave_reconciliada)
hash_digest = hashlib.sha256(chave_bytes).digest()
chave_final_256bits = bytes_to_bits(hash_digest)
```

---

## Testes e Validação

### Executar Suite Completa
```bash
python -m pytest tests/ -v
```

### Testes Disponíveis
- **test_binario_util.py**: Validação operações binárias
- **test_bch.py**: Validação códigos BCH e correção de erros
- **test_reconciliacao.py**: Validação algoritmo code-offset
- **test_amplificacao_privacidade.py**: Validação SHA-256
- **test_canal.py**: Validação simulação canal Rayleigh
- **test_sistema_completo.py**: Validação sistema end-to-end

### Análise Estatística
- **Centenas de iterações** para cada ponto SNR
- **Múltiplos parâmetros** Rayleigh (σ = 0.5, 1.0, 2.0)
- **Intervalos de confiança** para todas as métricas

---

## Testes

### Executar Suite Completa de Testes
```bash
# Com Poetry
poetry run pytest tests/ -v

# Com pip
python -m pytest tests/ -v

# Com cobertura
python -m pytest tests/ --cov=. --cov-report=html
```

---

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

## Equipe de Desenvolvimento

### Discentes
- **Pedro Henrique Duarte Frugoli** - pedro.frugoli@ges.inatel.br
- **Henrique Rodrigues Mendonça** - henrique.mendonca@ges.inatel.br

### Orientação
- **Prof.ª Vanessa Mendes Rennó** - Orientadora
- **Prof. Guilherme Pedro Aquino** - Coorientador  
- **Prof. Luciano Leonel Mendes** - Coorientador

**Projeto de Iniciação Científica (IC)**  
*"Segurança em Camada Física: Estabelecimento de Chaves Criptográficas para Comunicações Móveis de Próxima Geração"*

