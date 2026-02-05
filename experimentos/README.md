# 🧪 Experimentos Sistemáticos - PKG

Este diretório contém os scripts para executar experimentos sistemáticos que gerarão os resultados para o artigo científico.

## 📋 Estrutura

```
experimentos/
├── util_experimentos.py          # Utilitários para salvar resultados
├── exp01_variacao_snr.py         # ✅ Experimento 1: Variação de SNR
├── exp02_comparacao_modulacao.py # ✅ Experimento 2: BPSK vs QPSK
├── exp03_variacao_bch.py         # ✅ Experimento 3: Diferentes códigos BCH
├── exp04_analise_complexidade.py # ✅ Experimento 4: Complexidade computacional
├── exp05_perfis_dispositivos.py  # ✅ Experimento 5: Perfis IoT (aplicação prática)
├── exp06_analise_eve.py          # ✅ Experimento 6: Segurança contra Eve
├── exp07_impacto_guard_band.py   # ✅ Experimento 7: Trade-off guard-band (NOVO!)
└── executar_todos.py             # Script master que roda todos

resultados/
├── dados/                         # JSON e CSV dos resultados
└── figuras/                       # Gráficos PNG de alta resolução
```

**EXPERIMENTOS ESSENCIAIS PARA O ARTIGO:**
1. **exp01** - KDR vs SNR (fundamental)
2. **exp04** - Complexidade (viabilidade IoT)
3. **exp05** - Perfis dispositivos (aplicação prática)
4. **exp06** - Segurança Eve (validação PKG)
5. **exp07** - Guard-band (DIFERENCIAL do sistema!)

## 🚀 Como Executar

### Opção 1: Execução Individual

Execute cada experimento separadamente:

```bash
# Experimento 1: Variação de SNR
python experimentos/exp01_variacao_snr.py

# Experimento 2: Comparação Modulação
python experimentos/exp02_comparacao_modulacao.py

# Experimento 3: Variação de BCH
python experimentos/exp03_variacao_bch.py

# Experimento 4: Análise de Complexidade
python experimentos/exp04_analise_complexidade.py

# Experimento 5: Perfis de Dispositivos
python experimentos/exp05_perfis_dispositivos.py

# Experimento 6: Análise de Segurança (Eve)
python experimentos/exp06_analise_eve.py

# Experimento 7: Impacto Guard-Band (NOVO!)
python experimentos/exp07_impacto_guard_band.py
```

### Opção 2: Bateria Rápida (Recomendado para teste)

```bash
python experimentos/executar_todos.py --modo rapido
```

**Duração:** ~5-10 minutos  
**Uso:** Testar se tudo funciona antes de rodar completo

### Opção 3: Bateria Completa (Para resultados finais)

```bash
python experimentos/executar_todos.py --modo completo
```

**Duração:** ~2-4 horas (depende do computador)  
**Uso:** Gerar todos os resultados para o artigo

## 📊 Experimentos Disponíveis

### Experimento 1: Variação de SNR
**Objetivo:** Analisar como a relação sinal-ruído afeta o KDR

**Parâmetros fixos:**
- BCH(127,64) - t=10
- σ = 1/√2 (canal normalizado)
- Modulação: BPSK
- ρ = 0.9
- 1000 testes

**Parâmetro variável:**
- SNR: -10 a 30 dB (18 pontos)

**Resultados gerados:**
- JSON com todos os dados
- CSV com tabela SNR vs KDR
- Gráfico PNG comparativo

---

### Experimento 2: Variação do Parâmetro Rayleigh (σ)
**Objetivo:** Analisar como a intensidade do desvanecimento afeta o KDR

**Parâmetros fixos:**
- BCH(127,64) - t=10
- Modulação: BPSK
- ρ = 0.9
- 1000 testes

**Parâmetro variável:**
- σ: [0.5, 1/√2, 1.0, 2.0]
  - 0.5 → canal fraco (-3 dB)
  - 1/√2 → canal normalizado (0 dB)
  - 1.0 → canal moderado (+3 dB)
  - 2.0 → canal forte (+9 dB)

**Resultados gerados:**
- Gráficos comparativos para cada σ
- CSV com dados consolidados

---

### Experimento 3: Comparação BPSK vs QPSK
**Objetivo:** Comparar desempenho das duas modulações

**Parâmetros fixos:**
- BCH(127,64) - t=10
- σ = 1/√2
- ρ = 0.9
- 1000 testes

**Parâmetro variável:**
- Modulação: BPSK e QPSK

**Análise:**
- Comparar KDR antes/pós reconciliação
- Eficiência espectral vs taxa de erro
- Mesmo Eb/N0 para comparação justa

---

### Experimento 4: Variação da Correlação (ρ)
**Objetivo:** Analisar impacto da reciprocidade do canal

**Parâmetros fixos:**
- BCH(127,64) - t=10
- σ = 1/√2
- Modulação: BPSK
- 1000 testes

**Parâmetro variável:**
- ρ: [0.7, 0.8, 0.9, 0.95, 0.99]

**Importância:**
- ρ ≈ 1: Alice e Bob muito próximos (ideal)
- ρ < 0.7: Reciprocidade degradada
- Simula efeito da distância/movimento

---

### Experimento 5: Variação do Código BCH
**Objetivo:** Comparar diferentes códigos BCH

**Parâmetros fixos:**
- σ = 1/√2
- Modulação: BPSK
- ρ = 0.9
- 500 testes (reduzido por código grande)

**Parâmetro variável:**
- Códigos: BCH(7,4), BCH(15,7), BCH(127,64), [BCH(255,139)]

**Análise:**
| Código | k | t | Taxa | Aplicação |
|--------|---|---|------|-----------|
| (7,4) | 4 | 1 | 0.57 | Teste rápido |
| (15,7) | 7 | 2 | 0.47 | Baixo overhead |
| (127,64) | 64 | 10 | 0.50 | Balanceado |
| (255,139) | 139 | 15 | 0.55 | Alta correção |

---

## 💾 Formato dos Resultados

### JSON
```json
{
  "experimento": "exp01_variacao_snr",
  "descricao": "Análise do impacto da SNR no KDR",
  "timestamp": "20231218_143022",
  "data_hora": "2023-12-18 14:30:22",
  "dados": {
    "parametros": {...},
    "snr_db": [...],
    "kdr_rates": [...],
    "kdr_pos_rates": [...],
    "kdr_amplificacao_rates": [...]
  }
}
```

### CSV
```
SNR_dB,KDR_antes,KDR_pos_rec,KDR_pos_amp
-10.00,45.2341,23.1234,12.3456
-7.36,42.1234,20.5678,10.2345
...
```

### Gráficos PNG
- Resolução: 300 DPI (qualidade publicação)
- Formato: PNG com transparência
- Tamanho: Otimizado para artigo (18×5 ou 10×6)

---

## 📈 Usando os Resultados no Artigo

### 1. Carregar Dados

```python
import json

# Carregar resultados
with open('resultados/dados/exp01_variacao_snr_20231218_143022.json') as f:
    dados = json.load(f)

# Acessar resultados
snr = dados['dados']['snr_db']
kdr = dados['dados']['kdr_rates']
```

### 2. Inserir Gráficos no LaTeX

```latex
\begin{figure}[h]
  \centering
  \includegraphics[width=0.9\textwidth]{../resultados/graficos/exp01_variacao_snr_20231218_143022.png}
  \caption{Impacto da SNR no Key Disagreement Rate.}
  \label{fig:exp01_snr}
\end{figure}
```

### 3. Criar Tabelas

Use os arquivos CSV ou a função `gerar_tabela_latex()`:

```python
from experimentos.util_experimentos import gerar_tabela_latex

tabela_tex = gerar_tabela_latex(dados, "exp01_variacao_snr")
```

---

## ⚙️ Configuração Personalizada

Você pode modificar os parâmetros diretamente nos scripts:

```python
# Em exp01_variacao_snr.py
resultados = experimento_variacao_snr(
    tamanho_cadeia_bits=255,      # Mudar código BCH
    quantidade_de_testes=5000,    # Mais testes = mais precisão
    rayleigh_param=1.0,           # Mudar intensidade canal
    modulacao='qpsk',             # Testar QPSK
    correlacao_canal=0.95,        # Maior reciprocidade
    snr_min=-15,                  # Expandir range SNR
    snr_max=35,
    snr_pontos=25                 # Mais pontos = gráfico mais suave
)
```

---

## 🔍 Interpretação dos Resultados

### KDR (Key Disagreement Rate)

- **KDR antes:** Taxa de discrepância após canal
  - Alta SNR → KDR baixo
  - Baixa SNR → KDR alto

- **KDR pós reconciliação:** Após correção BCH
  - Deve reduzir significativamente
  - Se t erros ≤ capacidade BCH → KDR ≈ 0

- **KDR pós amplificação:** Após SHA-256
  - Compara chaves de 256 bits
  - Pode ser maior que pós-rec devido ao efeito avalanche

### Convergência

**SNR de Convergência:** Ponto onde KDR → 0%

- Ideal: SNR ≥ 4 dB
- σ maior → convergência em SNR menor (canal forte)
- ρ maior → convergência em SNR menor (reciprocidade)

---

## 📝 Checklist para o Artigo

- [ ] Executar bateria completa de experimentos
- [ ] Verificar convergência dos resultados
- [ ] Selecionar gráficos mais relevantes
- [ ] Criar tabelas resumo
- [ ] Analisar tendências e padrões
- [ ] Escrever Seção III (Modelo de Sistema)
- [ ] Escrever Seção IV (Materiais e Métodos)
- [ ] Escrever Seção V (Resultados)
- [ ] Adicionar citações apropriadas
- [ ] Revisar consistência entre texto e figuras

---

## 🐛 Troubleshooting

### Erro de memória
- Reduzir `quantidade_de_testes`
- Usar códigos BCH menores
- Executar experimentos separadamente

### Execução muito lenta
- Usar bateria rápida primeiro
- Reduzir `snr_pontos`
- Usar `tamanho_cadeia_bits=15` ou `7`

### Resultados inconsistentes
- Verificar `random.seed(42)` está fixo
- Aumentar `quantidade_de_testes`
- Conferir parâmetros do canal

---

## 📧 Suporte

Se tiver dúvidas sobre os experimentos ou resultados, consulte:
- `docs/FLUXO_COMPLETO.md` - Detalhes do sistema
- `docs/TERMS.md` - Glossário técnico
- Código fonte em `src/` - Implementação

**Boa sorte com o artigo! 📄🎓**
