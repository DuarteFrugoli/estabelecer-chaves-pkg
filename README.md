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

### Funcionalidades

#### Modo Básico (Atual)
- **Amplificação sempre ativa**: SHA-256 aplicado automaticamente
- **Parâmetros otimizados**: σ = 0.5, 1.0, 2.0 (cientificamente relevantes)
- **Visualização em grid 2x2**: Layout otimizado para comparação
- **Interface simplificada**: Foco na facilidade de uso

#### Modo Avançado (Planejado)
- **Parâmetros configuráveis**: Range de valores Rayleigh personalizável
- **Amplificação opcional**: Controle total sobre o processo
- **Exportação de dados**: Gráficos e dados em múltiplos formatos
- **Interface profissional**: Para usuários experientes

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

### Interfaces Disponíveis

#### Modo Básico (Recomendado)
Interface simplificada com parâmetros otimizados:

```bash
# Interface CLI
cd interfaces/basic && python main.py

# Interface Gráfica
cd interfaces/basic && python gui.py
```

#### Modo Avançado (Em Desenvolvimento)
Interface com parâmetros totalmente configuráveis:

```bash
# Interface CLI Avançada
cd interfaces/advanced && python main_advanced.py

# Interface Gráfica Avançada  
cd interfaces/advanced && python gui_advanced.py
```

### Fluxo de Execução (Modo Básico)

#### 1. **Configuração de Parâmetros**
```
Entre com a quantidade de testes: 100
Entre com o tamanho da cadeia de Bits (7, 15, 127, 255): 15
```

#### 2. **Processamento Automático**
O sistema executa automaticamente:
- **Amplificação sempre habilitada**: SHA-256 aplicado automaticamente
- **Parâmetros Rayleigh fixos**: σ = 0.5, 1.0, 2.0 (otimizados)
- **Simulação de canais correlacionados** (ρ=0.9)
- **Reconciliação usando códigos BCH**
- **Análise estatística** dos resultados

#### 3. **Visualização dos Resultados**
- **Grid 2x2**: Três gráficos em layout otimizado
- **Comparação simultânea**: Todos os parâmetros Rayleigh visíveis
- **Análise completa**: Original → Reconciliado → Amplificado

### Executar Testes

```bash
python -m pytest tests/ -v
```

---

## Arquitetura do Projeto

### Estrutura de Diretórios

```
Criptografia/
├── README.md                   # Documentação principal
├── LICENSE                     # Licença MIT
├── pyproject.toml             # Configuração e dependências
├── .gitignore                 # Arquivos ignorados
│
├── docs/                      # Documentação técnica
│   ├── NOTES.md              # Notas de desenvolvimento
│   ├── TERMS.md              # Glossário técnico
│   └── TODO.md               # Lista de tarefas
│
├── src/                       # Código fonte principal
│   ├── __init__.py
│   ├── canal/                # Simulação de canal Rayleigh
│   │   ├── __init__.py
│   │   └── canal.py
│   ├── codigos_corretores/   # Implementação códigos BCH
│   │   ├── __init__.py
│   │   └── bch.py
│   ├── pilares/              # Três pilares do PKG
│   │   ├── __init__.py
│   │   ├── reconciliacao.py  # Code-offset BCH
│   │   └── amplificacao_privacidade.py  # SHA-256
│   ├── util/                 # Utilitários e funções auxiliares
│   │   ├── __init__.py
│   │   ├── util.py
│   │   └── binario_util.py
│   └── visualization/        # Geração de gráficos
│       ├── __init__.py
│       └── plotkdr.py
│
├── interfaces/               # Interfaces de usuário
│   ├── __init__.py
│   ├── basic/               # Interface simplificada
│   │   ├── __init__.py
│   │   ├── main.py          # CLI principal
│   │   └── gui.py           # Interface gráfica
│   └── advanced/            # Interface avançada (futuro)
│       ├── __init__.py
│       ├── main_advanced.py
│       └── gui_advanced.py
│
└── tests/                   # Suite de testes
    ├── __init__.py
    ├── test_*.py           # Testes unitários
    └── executar_testes.py  # Runner de testes
```

### Fluxo de Dados do Sistema

O sistema PKG funciona seguindo este fluxo:

1. **Configuração**: Usuário define parâmetros via `interfaces/basic/main.py`
2. **Geração BCH**: Sistema gera tabela de códigos usando `src/codigos_corretores/bch.py`
3. **Simulação de Canal**: 
   - Alice e Bob observam canais Rayleigh correlacionados via `src/canal/canal.py`
   - Modulação BPSK com símbolos {-1, +1}
   - Adição de ruído gaussiano com variância σ² = Es/(2·SNR)
4. **Reconciliação**: Algoritmo code-offset em `src/pilares/reconciliacao.py`
5. **Amplificação**: SHA-256 via `src/pilares/amplificacao_privacidade.py`
6. **Visualização**: Gráficos gerados por `src/visualization/plotkdr.py`

### Princípios de Design

- **Separação de responsabilidades**: Cada módulo tem função específica
- **Interfaces organizadas**: Básica vs avançada em diretórios separados
- **Código reutilizável**: Lógica core em `src/` independente das interfaces
- **Testes abrangentes**: Cobertura completa em `tests/`
- **Documentação centralizada**: Guias técnicos em `docs/`

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

O sistema gera **3 gráficos em layout 2x2** mostrando:
- **Superior esquerdo**: Rayleigh σ = 0.5 (baixa variância)
- **Superior direito**: Rayleigh σ = 1.0 (variância padrão)
- **Inferior esquerdo**: Rayleigh σ = 2.0 (alta variância)

Cada gráfico contém três linhas:
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

### Executar Suite Completa de Testes

```bash
# Na raiz do projeto
python -m pytest tests/ -v

# Com Poetry
poetry run pytest tests/ -v

# Com cobertura
python -m pytest tests/ --cov=src --cov-report=html
```

### Executar Testes Específicos

```bash
# Testes de um módulo específico
python -m pytest tests/test_canal.py -v

# Executar runner personalizado
cd tests && python executar_testes.py
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

