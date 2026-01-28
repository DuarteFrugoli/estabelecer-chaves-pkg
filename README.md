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
- **Convergência**: SNR ≥ 11dB → KDR = 0% (maioria dos perfis)
- **Segurança**: Chaves de 256 bits (SHA-256)
- **Reciprocidade**: Correlação ρ até 1.0 (sensor estático)
- **Perfis IoT**: 5 cenários testados (pessoa, sensor, veículo, drone, NB-IoT)

### Implementação Robusta
- **Canal Rayleigh** com ruído gaussiano e BPSK
- **Códigos BCH** com algoritmos eficientes de codificação/decodificação
- **Algoritmos otimizados** - Síndromes, Berlekamp-Massey e busca de Chien
- **Escalabilidade** para códigos grandes (até 255 bits) com alta performance
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
- pip (gerenciador de pacotes Python)
- Bibliotecas gráficas para matplotlib

---

## 🐧 **Linux (Ubuntu/Debian)**

### Opção 1: Instalação Completa com Poetry (Recomendada)

```bash
# 1. Instale dependências do sistema
sudo apt update
sudo apt install python3-pip python3-venv python3-tk git

# 2. Clone o repositório
git clone https://github.com/DuarteFrugoli/estabelecer-chaves-pkg.git
cd estabelecer-chaves-pkg

# 3. Crie um ambiente virtual
python3 -m venv .venv

# 4. Ative o ambiente virtual
source .venv/bin/activate

# 5. Instale o Poetry
pip install poetry

# 6. Instale as dependências do projeto
poetry install

# 7. Execute o programa
python interfaces/basic/main.py
```

### Opção 2: Instalação Simples com pip

```bash
# 1. Instale dependências do sistema
sudo apt update
sudo apt install python3-pip python3-venv python3-tk git

# 2. Clone e configure
git clone https://github.com/DuarteFrugoli/estabelecer-chaves-pkg.git
cd estabelecer-chaves-pkg
python3 -m venv .venv
source .venv/bin/activate

# 3. Instale dependências Python
pip install numpy matplotlib galois scipy tqdm pytest pytest-cov

# 4. Execute o programa
python interfaces/basic/main.py
```

---

## 🍎 **macOS**

### Opção 1: Instalação Completa com Poetry (Recomendada)

```bash
# 1. Instale Homebrew (se não tiver)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. Instale Python e dependências
brew install python python-tk git

# 3. Clone o repositório
git clone https://github.com/DuarteFrugoli/estabelecer-chaves-pkg.git
cd estabelecer-chaves-pkg

# 4. Crie um ambiente virtual
python3 -m venv .venv

# 5. Ative o ambiente virtual
source .venv/bin/activate

# 6. Instale o Poetry
pip install poetry

# 7. Instale as dependências do projeto
poetry install

# 8. Execute o programa
python interfaces/basic/main.py
```

### Opção 2: Instalação Simples com pip

```bash
# 1. Instale dependências (se não tiver Homebrew)
# Python já vem no macOS, mas recomenda-se instalar via Homebrew
brew install python python-tk git

# 2. Clone e configure
git clone https://github.com/DuarteFrugoli/estabelecer-chaves-pkg.git
cd estabelecer-chaves-pkg
python3 -m venv .venv
source .venv/bin/activate

# 3. Instale dependências Python
pip install numpy matplotlib galois scipy tqdm pytest pytest-cov

# 4. Execute o programa
python interfaces/basic/main.py
```

---

## 🪟 **Windows**

### Opção 1: Instalação Completa com Poetry (Recomendada)

```powershell
# 1. Instale Python do site oficial: https://www.python.org/downloads/
# Certifique-se de marcar "Add Python to PATH" durante a instalação

# 2. Abra PowerShell ou Command Prompt

# 3. Clone o repositório (instale Git se necessário: https://git-scm.com/)
git clone https://github.com/DuarteFrugoli/estabelecer-chaves-pkg.git
cd estabelecer-chaves-pkg

# 4. Crie um ambiente virtual
python -m venv .venv

# 5. Ative o ambiente virtual
.venv\Scripts\activate

# 6. Instale o Poetry
pip install poetry

# 7. Instale as dependências do projeto
poetry install

# 8. Execute o programa
python interfaces/basic/main.py
```

### Opção 2: Instalação Simples com pip

```powershell
# 1. Certifique-se que Python está instalado e no PATH

# 2. Clone e configure
git clone https://github.com/DuarteFrugoli/estabelecer-chaves-pkg.git
cd estabelecer-chaves-pkg
python -m venv .venv
.venv\Scripts\activate

# 3. Instale dependências Python
pip install numpy matplotlib galois scipy tqdm pytest pytest-cov

# 4. Execute o programa
python interfaces/basic/main.py
```

---

### ⚠️ Solução de Problemas Comuns

| Problema | Solução |
|----------|---------|
| **Linux**: `ModuleNotFoundError: No module named '_tkinter'` | `sudo apt install python3-tk` |
| **macOS**: Gráficos não aparecem | `brew install python-tk` |
| **Windows**: `'python' não é reconhecido` | Reinstale Python marcando "Add to PATH" |
| **Qualquer OS**: `poetry: command not found` | Use a Opção 2 (pip) em vez do Poetry |

---

## Como Usar

### Interfaces Disponíveis

⚠️ **IMPORTANTE**: Sempre execute os programas a partir da **raiz do projeto** com o ambiente virtual ativado.

#### Modo Básico (Recomendado)
Interface simplificada com parâmetros otimizados:

```bash
# 1. Navegue até a RAIZ do projeto

# 2. Ative o ambiente virtual
# Linux/macOS:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate

# 3. Execute os programas (sempre da raiz do projeto)

# Interface CLI (Terminal)
python interfaces/basic/main.py

# Interface Gráfica (GUI)
python interfaces/basic/gui.py
```

#### Modo Avançado (Em Desenvolvimento)
Interface com parâmetros totalmente configuráveis:

```bash
# 1. Navegue até a RAIZ do projeto
cd estabelecer-chaves-pkg

# 2. Ative o ambiente virtual
# Linux/macOS:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate

# 3. Execute os programas (sempre da raiz do projeto)

# Interface CLI Avançada
python interfaces/advanced/main_advanced.py

# Interface Gráfica Avançada  
python interfaces/advanced/gui_advanced.py
```

**💡 Dica**: Se você receber erros como `ModuleNotFoundError` ou `Arquivo ou diretório inexistente`, certifique-se de que:
1. Você está na **raiz do projeto** (pasta `estabelecer-chaves-pkg`), não em subpastas
2. O ambiente virtual está ativado (você deve ver `(.venv)` no prompt do terminal)
3. As dependências estão instaladas (`poetry install` ou use a instalação manual com pip)

**Exemplo de erro comum**: 
```bash
# ❌ ERRADO - tentando ativar de dentro de uma subpasta
cd interfaces/basic
source .venv/bin/activate  # ERRO: .venv não está aqui!

# ✅ CORRETO - sempre ative da raiz do projeto
cd estabelecer-chaves-pkg
source .venv/bin/activate
python interfaces/basic/main.py
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
2. **Instanciação BCH**: Sistema instancia código BCH usando `src/codigos_corretores/bch.py`
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
| **Convergência** | SNR ≥ 11dB → KDR = 0% |
| **Segurança** | 256 bits (2^256 operações) |
| **Performance BCH** | Algoritmos eficientes O(n²) vs O(2^k) força bruta |
| **Escalabilidade** | Suporte eficiente para códigos de 255 bits |
| **Tempo execução** | 0.5-2s (configuração típica) |
| **Performance amplificação** | < 0.2ms por operação |

### Resultados por Perfil IoT

| Perfil | Velocidade | Correlação (ρ) | SNR mín. (KDR=0%) | KDR @ 9dB |
|--------|-----------|----------------|------------------|----------|
| **Pessoa Andando** | 5 km/h | 0.940 | 11 dB | 3.18% |
| **Sensor Estático** | 0 km/h | 1.000 | 11 dB | 4.70% |
| **Veículo Urbano** | 60 km/h | 0.160 | 13 dB | 3.91% |
| **Drone** | 40 km/h | 0.609 | 11 dB | 3.13% |
| **NB-IoT** | 10 km/h | 0.955 | 11 dB | 3.37% |

### Comparação Antes/Depois das Melhorias

| SNR | KDR Original | KDR Pós-Reconciliação | KDR Pós-Amplificação | Melhoria Total |
|-----|-------------|----------------------|---------------------|----------------|
| -5.0dB | 33.4% | 41.7% | 49.9% | -16.5 pts |
| 1.0dB | 16.5% | 32.9% | 49.8% | -33.3 pts |
| 5.0dB | 7.7% | 12.4% | 20.6% | -12.9 pts |
| 9.0dB | 3.2% | 0.03% | 0.05% | -3.2 pts |
| 11.0dB | 2.0% | 0.0% | 0.0% | -2.0 pts |

**Observação:** Dados do perfil "Pessoa Andando" (ρ=0.94, v=5km/h)

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

# Bob decodifica Cb = S ⊕ Kb usando algoritmos BCH
codigo_bob = bob_key XOR syndrome  
codigo_corrigido = bch_decode(codigo_bob)  # Síndromes + Berlekamp-Massey + Chien

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

