# Geração de Chaves em Camada Física (PKG) - Sistema Completo para Redes 5G/IoT

<div align="center">

![Python](https://img.shields.io/badge/Python-3.12%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Production-brightgreen)
![Research](https://img.shields.io/badge/Research-IEEE%20Paper-orange)
![Tests](https://img.shields.io/badge/Coverage-95%25-success)

**Sistema completo de estabelecimento de chaves criptográficas usando correlação espacial de canais sem fio**

[Sobre](#sobre-o-projeto) • [Artigo](#publicações) • [Instalação](#instalação) • [Como Usar](#como-usar) • [Resultados](#resultados) • [Arquitetura](#arquitetura)

</div>

---

## 📋 Sobre o Projeto

Este repositório implementa um **sistema completo de Physical Layer Key Generation (PKG)** para redes 5G e Internet das Coisas (IoT), desenvolvido como projeto de Iniciação Científica no Instituto Nacional de Telecomunicações (Inatel).

### 🎯 O que é PKG?

Physical Layer Key Generation é uma técnica de segurança que utiliza as características aleatórias e recíprocas do canal de comunicação sem fio para gerar chaves criptográficas idênticas entre dispositivos legítimos (Alice e Bob), sem necessidade de:
- ✅ Infraestrutura de chave pública (PKI)
- ✅ Troca prévia de segredos
- ✅ Hardware especializado (FPGA/USRP)

### 🔬 Modelo de Sistema

O sistema explora **correlação espacial** entre canais *downlink* de dispositivos próximos conectados à mesma estação base:
- **Alice e Bob**: Dispositivos espacialmente próximos (d < 0.5m) com correlação ρ ≈ 0.9
- **Segurança**: Descorrelação espacial garante que atacantes distantes (d > 20cm) observem BER ≈ 50%
- **Aplicações**: Sensores IoT, wearables, veículos conectados, dispositivos NB-IoT

### 🏗️ Arquitetura do Sistema (4 Etapas)

1. **🔍 Sondagem de Canal** - Observação de sinais de referência *downlink* (BPSK/QPSK)
2. **📊 Quantização** - Conversão para bits usando limiar τ=0 (antipodal, otimizado estatisticamente)
3. **🔧 Reconciliação** - Correção de erros via código BCH(127,64,10) com protocolo *code-offset*
4. **🔐 Amplificação** - Aplicação de SHA-256 para chave final de 256 bits

---

## 📄 Publicações

### Artigo IEEE (Finalizado - Pronto para Submissão)

**Título**: *"Geração de Chaves Criptográficas em Camada Física para Redes 5G e Internet das Coisas: Implementação e Validação Experimental"*

**Status**: ✅ Finalizado (Fevereiro 2026)

**Principais Contribuições**:
- ✨ **Demonstração inédita**: Guard-band não é necessário em sistemas baseados em correlação espacial
- 📊 **Validação abrangente**: 7 experimentos sistemáticos com 1000 realizações Monte Carlo
- 💻 **Implementação prática**: Sistema completo em Python (vs hardware especializado da literatura)
- 🌐 **Múltiplos cenários IoT**: 5 perfis validados (sensor estático, wearable, veículo 60km/h, drone, NB-IoT)

**Resultados Chave**:
- ✅ SNR mínimo operacional: **13-15 dB** (compatível com redes 5G/NB-IoT)
- ⚡ Baixa complexidade: **0.489 ms** de processamento (2000+ operações/segundo)
- 🔒 Segurança física: BER Eve ≈ **50%** para d ≥ 20cm
- 🚀 Robustez: Opera em alta mobilidade (60km/h, ρ_temporal = 0.16)

**Arquivo**: [`paper/overleaf/`](paper/overleaf/)

---

## ✨ Funcionalidades

### Sistema PKG de Alto Desempenho

**Validação Experimental** (7 Experimentos Sistemáticos):
- ✅ **Exp 1**: Impacto da SNR → SNR_mín = 13-15dB para KDR = 0%
- ✅ **Exp 2**: BPSK vs QPSK → Desempenho equivalente (segurança idêntica)
- ✅ **Exp 3**: Códigos BCH → BCH(127,64,10) ideal para IoT
- ✅ **Exp 4**: Complexidade → 0.489ms (codificação + decodificação + SHA-256)
- ✅ **Exp 5**: Perfis IoT → 5 cenários validados (0-60 km/h)
- ✅ **Exp 6**: Segurança → BER_Eve ≈ 50% para d ≥ 20cm
- ✅ **Exp 7**: Guard-band → GB=0 suficiente (contribuição original)

**Métricas de Performance**:
- 🎯 **Taxa de sucesso**: KDR = 0% para SNR ≥ 13dB (maioria dos perfis)
- ⚡ **Processamento**: <0.5ms por operação completa
- 🔐 **Segurança**: 256 bits (2^256 ≈ 10^77 tentativas de força bruta)
- 📊 **Correlação**: Suporta ρ = 0.16 a 1.0 (temporal) e ρ ≥ 0.7 (espacial)
- 🌐 **Escalabilidade**: Funciona em cenários estáticos e alta mobilidade (60km/h)

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

### 🔬 Reproduzindo Experimentos do Artigo

Para reproduzir os **7 experimentos sistemáticos** descritos no artigo IEEE:

```bash
# 1. Navegue até o diretório de experimentos
cd experimentos

# 2. Execute experimentos individuais
python exp01_variacao_snr.py           # Exp 1: Impacto da SNR
python exp02_variacao_sigma.py         # Exp 2: Comparação BPSK/QPSK
python exp03_comparacao_modulacao.py   # Exp 3: Diferentes códigos BCH
python exp04_variacao_correlacao.py    # Exp 4: Análise de complexidade
python exp05_variacao_bch.py           # Exp 5: Perfis IoT
python exp06_analise_complexidade.py   # Exp 6: Análise de segurança (Eve)
# exp07 implementado em exp01 (variação de guard-band)

# 3. OU execute todos de uma vez (⚠️ ~15-30 minutos)
bash quickstart.sh  # Linux/macOS
# Windows: execute cada script manualmente

# 4. Resultados salvos em:
cd ../resultados/dados/
ls -lh  # exp01_*.csv, exp01_*.json, ...
```

**Configurações dos Experimentos** (1000 Monte Carlo realizations cada):

| Experimento | Parâmetros Variados | SNR Range | Modulation | BCH Code | Outputs |
|-------------|---------------------|-----------|-----------|----------|---------|
| **Exp 1** | SNR (1-20 dB) | 1-20 dB | BPSK | BCH(127,64,10) | KDR, BMR vs SNR |
| **Exp 2** | Modulação | 11 dB | BPSK/QPSK | BCH(127,64,10) | KDR comparison |
| **Exp 3** | Código BCH | 11 dB | BPSK | (7,4), (15,7), (127,64) | KDR vs t |
| **Exp 4** | Correlação ρ | 11 dB | BPSK | BCH(127,64,10) | KDR vs ρ_temporal |
| **Exp 5** | Perfil IoT | Variável | BPSK | BCH(127,64,10) | 5 IoT scenarios |
| **Exp 6** | Tempo exec. | 11 dB | BPSK | 3 códigos | Complexity (ms) |
| **Exp 7** | Guard-band σ | 11 dB | BPSK | BCH(127,64,10) | KDR vs GB |

**Nota**: Os arquivos CSV/JSON gerados contém dados brutos para reprodução das tabelas e figuras do artigo (Seção V).

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

## 📊 Resultados Experimentais

### Performance Global do Sistema

| Métrica | Valor | Observação |
|---------|-------|------------|
| **SNR mínimo operacional** | 13-15 dB | KDR = 0% (chaves idênticas) |
| **Complexidade computacional** | 0.489 ms | BCH + SHA-256 (software Python) |
| **Capacidade teórica** | >2000 ops/s | Geração de chaves por segundo |
| **Segurança física** | BER_Eve ≈ 50% | Atacante a d ≥ 20cm |
| **Comprimento da chave** | 256 bits | SHA-256 (2^256 espaço de busca) |
| **Código corretor** | BCH(127,64,10) | Corrige até 10 erros/bloco |
| **Modulação** | BPSK/QPSK | Desempenho equivalente |
| **Quantização** | τ = 0 | Antipodal {+1, -1} otimizada |

### Resultados por Perfil IoT (Experimento 5)

| Perfil | Velocidade | Frequência | ρ_temporal | ρ_espacial | SNR_mín (KDR=0%) | KDR @ 11dB |
|--------|-----------|------------|------------|-----------|------------------|----------|
| **Sensor Estático** | 0 km/h | 870 MHz | 1.000 | 0.900 | 11 dB | 0.0% |
| **Wearable/Pessoa** | 5 km/h | 2.4 GHz | 0.940 | 0.900 | 11 dB | 0.03% |
| **Veículo Urbano** | 60 km/h | 5.9 GHz | 0.160 | 0.900 | 13 dB | 3.91% |
| **Drone** | 40 km/h | 2.4 GHz | 0.609 | 0.900 | 11 dB | 0.0% |
| **Dispositivo NB-IoT** | 10 km/h | 900 MHz | 0.955 | 0.900 | 11 dB | 0.0% |

**Insight Principal**: Sistema opera adequadamente mesmo em alta mobilidade (veículo 60km/h) com ρ_temporal = 0.16, demonstrando que **qualidade da estimação de canal** é mais crítica que correlação temporal.

### Comparação BPSK vs QPSK (Experimento 2)

| SNR (dB) | BMR BPSK | BMR QPSK | KDR BPSK | KDR QPSK | Diferença |
|----------|----------|----------|----------|----------|-----------|
| 8.82 | 5.55% | 5.47% | 2.93% | 3.37% | Desprezível |
| 11.18 | 3.38% | 3.35% | 0.03% | 0.03% | Idêntico |
| 15.88 | 1.27% | 1.26% | 0.0% | 0.0% | Idêntico |

**Conclusão**: Escolha entre BPSK/QPSK não afeta segurança ou eficiência para PKG (pode guiar-se por eficiência espectral).

### Análise de Complexidade (Experimento 4)

| Código BCH | Codificação | Decodificação | Total | Capacidade/s |
|------------|-------------|---------------|-------|--------------|
| BCH(7,4,1) | 0.015 ms | 0.022 ms | 0.037 ms | 27,027 ops/s |
| BCH(15,7,2) | 0.035 ms | 0.058 ms | 0.093 ms | 10,753 ops/s |
| **BCH(127,64,10)** | **0.189 ms** | **0.300 ms** | **0.489 ms** | **2,045 ops/s** |

**Observação**: BCH(127,64,10) oferece melhor balanço entre robustez (t=10 erros) e performance para aplicações IoT.

### Segurança contra Espionagem Passiva (Experimento 6)

| Distância Eve | Correlação ρ_Eve | BER Alice-Eve | BER Bob-Eve | Segurança |
|--------------|------------------|---------------|-------------|-----------|
| d = 0.5 cm | 0.98 | 2.1% | 2.0% | ⚠️ Muito próximo |
| d = 5.0 cm | 0.76 | 12.5% | 12.3% | ⚠️ Comprometida |
| **d = 20 cm** | **0.02** | **49.8%** | **49.9%** | ✅ **Seguro** |
| d = 50 cm | 0.00 | 50.1% | 50.0% | ✅ Ideal |
| d = 100 cm | 0.00 | 50.0% | 50.0% | ✅ Ideal |

**Modelo de Clarke Validado**: ρ_espacial(d) = J₀(2πd/λ) → Para d ≥ λ/2 (20cm @ 2.4GHz), ρ ≈ 0 e BER ≈ 50%.

### Impacto do Guard-Band (Experimento 7) - **Contribuição Original**

| Guard-Band (GB) | Descarte de Bits | KDR Alice-Bob | BER Eve | Recomendação |
|-----------------|------------------|---------------|---------|--------------|
| GB = 0.0σ | 0% | 0.03% | 49.9% | ✅ **Recomendado** |
| GB = 0.1σ | 8% | 0.02% | 49.8% | ✅ Aceitável |
| GB = 0.5σ | 31% | 0.01% | 49.7% | ⚠️ Ineficiente |
| GB = 1.0σ | 63% | 0.0% | 49.5% | ❌ Contraproducente |

**Descoberta**: Ao contrário da literatura tradicional (sistemas de reciprocidade temporal), sistemas baseados em **correlação espacial** não necessitam guard-band. GB=0 maximiza taxa de geração sem comprometer segurança.

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

## 📖 Como Citar

Se você usar este código ou referências deste projeto em sua pesquisa, por favor cite:

```bibtex
@unpublished{frugoli2026pkg,
  author = {Frugoli, Pedro H. D. and Mendonça, Henrique R. and Rennó, Vanessa M. and Aquino, Guilherme P. and Mendes, Luciano L.},
  title = {Geração de Chaves Criptográficas em Camada Física para Redes 5G e Internet das Coisas: Implementação e Validação Experimental},
  year = {2026},
  note = {Artigo em preparação para submissão em conferência IEEE},
  institution = {Instituto Nacional de Telecomunicações (Inatel)},
  url = {https://github.com/DuarteFrugoli/estabelecer-chaves-pkg}
}
```

---

## 🔬 Fundamentos Técnicos

### Modelo de Canal (Rayleigh + AWGN)

O sistema simula canal Rayleigh plano com desvanecimento multiplicativo:

```python
# Coeficiente de canal complexo gaussiano: h ~ CN(0,1)
h = np.random.rayleigh(scale=1.0, size=n_bits) * np.exp(1j * np.random.uniform(0, 2*np.pi, n_bits))

# Correlação espacial (modelo de Clarke)
ρ_espacial = scipy.special.j0(2 * np.pi * d / λ)
h_Bob = ρ * h_Alice + np.sqrt(1 - ρ²) * h_independente

# Sinal recebido: y = h·x + n (eq. canal_basico)
y_Alice = h_Alice * x + n_Alice  # n ~ CN(0, σ²_n)
y_Bob = h_Bob * x + n_Bob
```

**PDF Rayleigh**: $f_{|h|}(r) = r \cdot e^{-r^2/2}, \quad r \geq 0$ (eq. pdf_rayleigh)

**SNR**: Para potência de canal $\mathbb{E}[|h|^2] = 1$ e potência de sinal $E_s$:
$$\text{SNR} = \frac{E_s \cdot \mathbb{E}[|h|^2]}{\sigma_n^2} = \frac{E_s}{\sigma_n^2}$$

### Quantização Antipodal (τ = 0)

Conversão de sinal contínuo para bits usando limiar zero-crossing:

```python
# BPSK: Símbolos {-1, +1} → Bits {0, 1}
símbolos_BPSK = 2 * bits - 1  
y_recebido = h * símbolos_BPSK + ruído

# Quantização com limiar τ = 0
bits_quantizados = (y_recebido.real >= 0).astype(int)
```

**Justificativa para τ=0**:
1. **Otimalidade estatística**: Maximiza entropia para distribuições simétricas (Rayleigh de média zero)
2. **Simplicidade**: Não requer estimação de parâmetros ou ajuste adaptativo
3. **Robustez**: Evita viés sistemático introduzido por limiares fixos não-nulos

### Reconciliação BCH (Code-Offset Protocol)

Algoritmo de reconciliação assimétrico baseado em síndromes:

```python
# Bob: Gera palavra-código aleatória
r_Bob = np.random.randint(0, 2, k)  # k=64 bits de informação
c_Bob = BCH_encode(r_Bob)           # n=127 bits codificados

# Bob: Transmite síndrome pública σ = b_Bob ⊕ c
σ = b_Bob XOR c_Bob                 # eq. sindrome

# Alice: Recebe σ e decodifica c' = σ ⊕ b_Alice
c_prime = σ XOR b_Alice
c_hat = BCH_decode(c_prime)         # eq. decod_bch (Berlekamp-Massey + Chien)

# Alice: Reconcilia chave: k_reconciliada = σ ⊕ ĉ
k_reconciliada = σ XOR c_hat        # eq. reconciliada
```

**Algoritmos BCH Implementados**:
- **Codificação**: Multiplicação polinomial em GF(2) - O(n·k)
- **Síndrome**: Avaliação polinomial com potências de α - O(n·t)
- **Berlekamp-Massey**: Cálculo do polinômio localizador de erros - O(t²)
- **Chien Search**: Busca das raízes do polinômio localizador - O(n·t)

**Complexidade Total**: O(n·t²) vs O(2^k) força bruta → Para BCH(127,64,10): ~1,270 operações vs 1.84×10^19

### Amplificação de Privacidade (SHA-256)

Eliminação de vazamento de informação causado pela síndrome pública:

```python
# Converte bits reconciliados → bytes → SHA-256 → 256 bits finais
def amplify_privacy(reconciled_bits):
    # Converte bits para bytes (padding se necessário)
    byte_array = np.packbits(reconciled_bits)
    
    # Aplica SHA-256
    hash_object = hashlib.sha256(byte_array)
    hash_bytes = hash_object.digest()  # 32 bytes = 256 bits
    
    # Converte hash de volta para bits
    final_key = np.unpackbits(np.frombuffer(hash_bytes, dtype=np.uint8))
    
    return final_key  # Chave de 256 bits (eq. amplificada)
```

**Propriedades do SHA-256**:
- ✅ Função one-way: Computacionalmente inviável reverter k_final → k_reconciliada
- ✅ Difusão: Mudança de 1 bit →  média 128 bits alterados no hash
- ✅ Resistência a colisões: ~2^128 tentativas necessárias
- ✅ Padronização: NIST FIPS 180-4 (recomendado para aplicações criptográficas)

---

## 🏗️ Arquitetura do Projeto

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

## 📄 Licença

Este projeto está licenciado sob a **Licença MIT** - veja o arquivo [LICENSE](LICENSE) para detalhes.

**Uso Acadêmico**: Este código fonte é fornecido para fins de reproducibilidade e validação dos resultados apresentados no artigo IEEE. Se você usar ou adaptar este código em sua pesquisa, por favor cite nossa publicação (veja seção [Como Citar](#📖-como-citar)).

---

## 👥 Equipe

**Autores**:
- **Pedro Henrique Duarte Frugoli** - [pedro.frugoli@ges.inatel.br](mailto:pedro.frugoli@ges.inatel.br)  
  *Desenvolvedor principal, Implementação da arquitetura PKG, Simulações e experimentos*

- **Henrique Rodrigues Mendonça** - [henrique.mendonca@ges.inatel.br](mailto:henrique.mendonca@ges.inatel.br)  
  *Co-desenvolvedor, Análise teórica, Validação experimental*

**Orientação Acadêmica**:
- **Prof.ª Vanessa Mendes Rennó** (Instituto Nacional de Telecomunicações - Inatel)  
  *Orientadora Principal - Especialista em Segurança em Comunicações*

- **Prof. Guilherme Pedro Aquino** (Inatel)  
  *Coorientador - Especialista em Processamento de Sinais*

- **Prof. Luciano Leonel Mendes** (Inatel)  
  *Coorientador - Especialista em Redes Móveis e IoT*

**Instituição**: [Instituto Nacional de Telecomunicações (Inatel)](https://inatel.br/)

**Projeto**: Originado de Iniciação Científica (IC) "Segurança em Camada Física: Estabelecimento de Chaves Criptográficas para Comunicações Móveis de Próxima Geração" - Concluído com publicação de artigo completo.

---

## 🤝 Contribuições

Este repositório contém a implementação oficial do artigo IEEE e está **fechado para contribuições externas** no momento (código finalizado para publicação). 

**Para questões ou sugestões**:
- 📧 Contate os autores via e-mail (endereços acima)
- 🐛 Reporte bugs via [GitHub Issues](https://github.com/DuarteFrugoli/estabelecer-chaves-pkg/issues)
- 💡 Para discussões técnicas, inclua referência ao artigo e experimento específico

**Trabalhos Futuros** (potenciais extensões):
- ✨ Implementação em hardware (FPGA/SDR) para validação em tempo real
- 📡 Extensão para canais MIMO e massive MIMO
- 🔐 Integração com protocolos de autenticação 5G (AKA, SUPI/SUCI)
- 🌐 Validação em cenários D2D (Device-to-Device) reais

---

## 📞 Contato & Links

- 📂 **Repositório**: [github.com/DuarteFrugoli/estabelecer-chaves-pkg](https://github.com/DuarteFrugoli/estabelecer-chaves-pkg)
- 📧 **E-mail**: pedro.frugoli@ges.inatel.br
- 🏢 **Instituição**: [Instituto Nacional de Telecomunicações (Inatel)](https://inatel.br/)
- 📄 **Artigo**: `paper/overleaf/main.tex` (LaTeX source disponível neste repositório)

---

<div align="center">

**⭐ Se este projeto foi útil para sua pesquisa, considere deixar uma estrela no GitHub! ⭐**

Desenvolvido com 💻 e ☕ no [Inatel](https://inatel.br/)  
© 2024-2026 Pedro Frugoli & Henrique Mendonça

</div>

