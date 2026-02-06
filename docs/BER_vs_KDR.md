# BER vs KDR: Diferença Fundamental

## Definições ✅

### BER (Bit Error Rate)
**Taxa de erro de bits ANTES da reconciliação BCH**

- **Quando**: Após quantização do canal, antes do BCH corrigir
- **Comparação**: Alice vs Bob (bits brutos do canal)
- **Causa**: Ruído AWGN + erro de estimação + descorrelação temporal
- **Valor típico**: 2-10% (dependente de SNR e correlação ρ)

**Fórmula:**
```
BER = (número de bits diferentes entre Alice e Bob) / total de bits × 100%
```

**Código (canal.py linha 411):**
```python
# Conta erros bit a bit ANTES da reconciliação (BER)
erros_raw = contar_erros_bits(sinal_recebido_1, sinal_recebido_2)
total_erros_raw += erros_raw
```

---

### KDR (Key Disagreement Rate)
**Taxa de erro de bits APÓS a reconciliação BCH**

- **Quando**: Após Bob corrigir erros usando BCH
- **Comparação**: Alice (original) vs Bob (corrigido por BCH)
- **Causa**: Erros residuais que BCH não conseguiu corrigir
- **Valor típico**: <0.01% (SNR adequado) ou 0% (SNR alto)

**Fórmula:**
```
KDR = (número de bits diferentes após BCH) / total de bits × 100%
```

**Código (canal.py linha 418-420):**
```python
# Reconciliação de chaves usando BCH
chave = reconciliar_chaves(sinal_recebido_1, sinal_recebido_2, bch_codigo)

# Conta erros APÓS reconciliação (KDR)
erros_pos_reconciliacao = contar_erros_bits(sinal_recebido_1, chave)
total_erros_pos_reconciliacao += erros_pos_reconciliacao
```

**Retorno (canal.py linha 435-436):**
```python
ber = 100.0 * total_erros_raw / total_bits  # BER: antes reconciliação
kdr = 100.0 * total_erros_pos_reconciliacao / total_bits  # KDR: após reconciliação
```

---

## Fluxo do Sistema

```
┌─────────────────┐
│  Canal Alice    │ ──┐
│  h_A, ruído n_A │   │
└─────────────────┘   │
                      │  Correlação ρ
┌─────────────────┐   │  (temporal ou espacial)
│  Canal Bob      │ ──┘
│  h_B, ruído n_B │
└─────────────────┘
         │
         ↓ Quantização
         │
    ┌────────────┐
    │ Bits brutos│
    │  Alice: b_A│
    │  Bob:   b_B│
    └────────────┘
         │
         ↓ Compara (BER)
         │
    BER = |b_A ⊕ b_B| / n × 100%
         │
         ↓ Reconciliação BCH
         │
    ┌────────────┐
    │Bob corrige:│
    │  c = BCH(b_B) │
    └────────────┘
         │
         ↓ Compara (KDR)
         │
    KDR = |b_A ⊕ c| / n × 100%
```

---

## Exemplo Numérico

### Cenário: SNR = 15 dB, ρ = 0.94 (pessoa andando)

**Alice quantiza:**
```
b_A = [1, 0, 1, 1, 0, 1, 0, 0, ...]  (127 bits)
```

**Bob quantiza (com erros):**
```
b_B = [1, 0, 0, 1, 0, 1, 1, 0, ...]  (127 bits)
      ✓  ✓  ✗  ✓  ✓  ✓  ✗  ✓
```

**BER:**
```
Erros = 2 bits diferentes (posições 2 e 6)
BER = 2/127 × 100% ≈ 1.57%
```

**Bob aplica BCH(127,64,10):**
- Capacidade de correção: t = 10 erros
- Bob corrige os 2 erros ✅

**Chave corrigida:**
```
c = [1, 0, 1, 1, 0, 1, 0, 0, ...]  (idêntica a Alice!)
    ✓  ✓  ✓  ✓  ✓  ✓  ✓  ✓
```

**KDR:**
```
Erros = 0 bits diferentes
KDR = 0/127 × 100% = 0.00%
```

---

## Relação BCH: BER → KDR

### BCH(127, 64, 10)
- **n = 127**: Total de bits
- **k = 64**: Bits de informação
- **t = 10**: Capacidade de correção

**Cenários:**

| BER (%) | Erros médios | BCH consegue? | KDR esperado (%) |
|---------|--------------|---------------|------------------|
| 0.79    | 1 erro       | ✅ Sempre     | 0.00             |
| 1.57    | 2 erros      | ✅ Sempre     | 0.00             |
| 5.51    | 7 erros      | ✅ Sempre     | 0.00             |
| 7.87    | 10 erros     | ✅ Limite     | 0.00-0.03        |
| 11.02   | 14 erros     | ❌ Falha      | 3.15 (residual)  |

---

## Por que BER ≠ KDR?

### 1. **BCH corrige erros:**
   - Se BER = 5% e BCH(127,64,10) consegue corrigir → KDR = 0%
   - BCH reduz drasticamente KDR quando BER < 7.87%

### 2. **SNR mínimo diferente:**
   - **BER < 10%**: Requer SNR ≈ 5-8 dB (modulação BPSK)
   - **KDR < 1%**: Requer SNR ≈ 13-15 dB (BCH precisa de menos erros)

### 3. **Guard-band afeta ambos:**
   - Aumentar guard-band → Reduz BER (descarta bits incertos)
   - Mas também → Reduz taxa efetiva (bits por segundo)

---

## Experimentos: Valores Reais

### Experimento 1: Variação SNR (BPSK, ρ=0.9)

| SNR (dB) | BER (%) | KDR (%) | Interpretação             |
|----------|---------|---------|---------------------------|
| 8.82     | 5.55    | 2.93    | BCH corrige ~50% (5→3)    |
| 11.18    | 3.40    | 0.15    | BCH corrige ~95% (3→0.15) |
| 13.53    | 2.00    | 0.00    | BCH corrige 100% ✅       |
| 30.00    | 0.06    | 0.00    | Poucos erros, BCH trivial |

**Insight:** KDR cai muito mais rápido que BER porque BCH amplifica o efeito do SNR.

---

### Experimento 5: Perfis Dispositivos (SNR = 15 dB)

| Perfil          | ρ     | Erro (%) | BER (%) | KDR (%) |
|-----------------|-------|----------|---------|---------|
| Sensor estático | 1.00  | 8.0      | 1.80    | 0.00    |
| Pessoa andando  | 0.94  | 15.0     | 2.10    | 0.00    |
| Drone           | 0.61  | 30.0     | 3.50    | 0.02    |
| Veículo urbano  | 0.16  | 25.0     | 5.20    | 0.15    |

**Insight:** 
- Menor ρ → Maior BER (canais mais diferentes)
- Maior erro estimação → Maior BER (h̃ ≠ h)
- Mas KDR permanece baixo (BCH compensa)

---

## Conclusão ✅

### **BER**: Métrica de qualidade do **canal**
- Mede capacidade de Alice e Bob observarem canais correlacionados
- Dependente de SNR, correlação ρ, erro de estimação

### **KDR**: Métrica de qualidade da **chave**
- Mede probabilidade de Alice e Bob terem chaves diferentes
- Dependente de BER + capacidade de correção do BCH
- **Métrica final** para segurança (KDR < 10⁻⁶ ideal)

### **Relação:**
```
BER mede problema → KDR mede solução após BCH
```

---

## Referências

**Código:**
- [src/canal/canal.py](../src/canal/canal.py#L435-L436) - Cálculo BER e KDR
- [src/pilares/reconciliacao.py](../src/pilares/reconciliacao.py) - Protocolo code-offset

**Artigos:**
- Yuan et al. (2013) - "Key Generation from Wireless Channels"
- Ren et al. (2011) - "The Secrecy of Channel-Based Authentication"

**Experimentos:**
- [exp01_variacao_snr.py](../experimentos/exp01_variacao_snr.py) - BER vs SNR
- [exp02_variacao_sigma.py](../experimentos/exp02_variacao_sigma.py) - BER vs σ
- [exp05_perfis_dispositivos.py](../experimentos/exp05_perfis_dispositivos.py) - BER/KDR por perfil

---

**Atualizado:** 2026-02-06  
**Autor:** Sistema PKG - Geração de Chaves por Camada Física
