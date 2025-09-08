# Testes do Sistema PKG

Esta pasta contém todos os testes automatizados para validar o funcionamento do sistema PKG (Physical Key Generation).

## 🧪 Suíte de Testes Disponível

### 📊 Testes Principais

#### `executar_testes.py` - **Script Principal** ⭐
Runner principal que executa toda a suíte de testes
```bash
# Executar todos os testes
python executar_testes.py

# Executar teste específico
python executar_testes.py --test=completo

# Modo rápido (pula comparações longas)
python executar_testes.py --quick
```

#### `teste_pkg_completo.py` - **Sistema Completo**
Testa os três pilares integrados do PKG
- ✅ Estimativa de canal (Rayleigh + BPSK)
- ✅ Reconciliação (BCH + Code-offset)
- ✅ Amplificação (SHA-256)

#### `teste_melhorias.py` - **Melhorias Implementadas**
Validação das correções realizadas
- ✅ Reciprocidade de canal
- ✅ Modulação BPSK
- ✅ SNR-variância corrigida

#### `teste_amplificacao.py` - **Amplificação Individual**
Teste específico do terceiro pilar
- ✅ Propriedades criptográficas
- ✅ Efeito avalanche
- ✅ Performance

#### `comparacao_melhorias.py` - **Comparação A/B**
Compara versão original vs melhorada
- ✅ Gráficos comparativos
- ✅ Análise estatística
- ✅ Métricas de melhoria

## 🚀 Como Executar

### Execução Rápida
```bash
cd testes
python executar_testes.py --quick
```

### Execução Completa
```bash
cd testes  
python executar_testes.py
```

### Testes Individuais
```bash
# Teste específico
python teste_pkg_completo.py

# Ou via runner
python executar_testes.py --test=completo
```

## 📈 Resultados Esperados

### ✅ Cenário de Sucesso
```
📊 Taxa de Sucesso: 4/4 (100%)
⏱️  Tempo Total: 2.1s
🎉 TODOS OS TESTES PASSARAM!
```

### 📊 Métricas Validadas
- **KDR inicial**: ~10% (SNR baixo) → ~0.1% (SNR alto)
- **KDR pós-reconciliação**: ~4% (SNR baixo) → 0% (SNR ≥4dB)
- **KDR pós-amplificação**: ~3% (SNR baixo) → 0% (SNR ≥4dB)
- **Convergência**: SNR ≥ 4dB
- **Performance**: < 0.2ms por amplificação

## 🔧 Estrutura dos Testes

### Configuração Padrão
```python
quantidade_de_testes = 100        # Iterações por ponto
tamanho_cadeia_bits = 15         # BCH(15,7)  
correlacao_canal = 0.9           # Reciprocidade
snr_range = 0 a 20 dB           # Faixa de teste
```

### Parâmetros Testados
- **Códigos BCH**: (15,7), (127,64), (255,139)
- **SNR Range**: -10 a 30 dB
- **Parâmetros Rayleigh**: σ = 0.5, 1.0, 2.0
- **Correlação Canal**: ρ = 0.8 a 0.99

## 🐛 Solução de Problemas

### Erro de Import
```python
# Se houver erro de import, verifique se está na pasta correta
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
```

### Dependências Ausentes
```bash
# Instalar dependências necessárias
pip install numpy matplotlib galois
```

### Erro de Matplotlib (Gráficos)
```python
# Para ambiente sem GUI, use backend não-interativo
import matplotlib
matplotlib.use('Agg')  # Backend para salvar arquivos
```

## 📋 Checklist de Validação

Antes de considerar o sistema aprovado, verifique:

- [ ] ✅ Todos os testes passam (100% sucesso)
- [ ] ✅ KDR converge para 0% em SNRs adequados (≥4dB)
- [ ] ✅ Amplificação gera sempre 256 bits
- [ ] ✅ Efeito avalanche > 40% (típico ~50%)
- [ ] ✅ Performance < 1ms por operação
- [ ] ✅ Sistema suporta códigos BCH diversos
- [ ] ✅ Reciprocidade implementada (ρ ≥ 0.8)
- [ ] ✅ BPSK funcionando corretamente

## 🎯 Interpretação dos Resultados

### 🟢 **Resultados Excelentes**
- KDR final < 1% para SNR ≥ 6dB
- Convergência rápida (SNR ≥ 4dB)
- Performance < 0.5ms

### 🟡 **Resultados Aceitáveis**  
- KDR final < 5% para SNR ≥ 3dB
- Convergência em SNR ≥ 6dB
- Performance < 1ms

### 🔴 **Resultados Inadequados**
- KDR > 10% em SNRs altos (> 10dB)
- Não convergência em SNRs adequados
- Erros de importação ou execução

---

💡 **Dica**: Execute `python executar_testes.py --quick` para validação rápida durante desenvolvimento!
