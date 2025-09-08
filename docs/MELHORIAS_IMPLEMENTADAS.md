# Melhorias Implementadas no Código de PKG (Physical Key Generation)

## 1. Correção da Reciprocidade do Canal

**Problema**: Canais independentes (não correlacionados) entre Alice e Bob geravam alta discrepância de chaves.

**Solução**: 
- Implementado canal parcialmente correlacionado com coeficiente ρ = 0.9
- Alice e Bob agora observam canais correlacionados que simulam reciprocidade TDD
- Fórmula: `hB = ρ * hA + √(1-ρ²) * componente_independente`

## 2. Migração para BPSK (Binary Phase Shift Keying)

**Problema**: Modelo OOK (On-Off Keying) com limiar fixo 0.5 não era simétrico e gerava BER enviesado.

**Solução**:
- Mapeamento de bits: 0 → -1, 1 → +1
- Detecção por sinal: `bit_hat = (y >= 0)`
- Modelo mais realista e usado na literatura de PKG

## 3. Correção da Relação SNR-Variância

**Problema**: Relação incorreta entre SNR e variância do ruído.

**Solução**:
- Para BPSK: `SNR = Es/N0` onde `σ² = N0/2`
- Nova fórmula: `σ² = Es / (2·SNR) = 1 / (2·SNR_linear)`
- Mapeamento consistente entre SNR e potência de ruído

## 4. Melhorias na Reconciliação

**Algoritmo Code-Offset (Secure Sketch)**:
1. Alice escolhe código aleatório C
2. Alice calcula S = Ka ⊕ C (syndrome)
3. Bob calcula Cb = S ⊕ Kb = C ⊕ e
4. Bob decodifica Cb para palavra-código mais próxima
5. Chave reconciliada: K̂ = S ⊕ Ĉ

**Observação**: Sucesso depende de peso(e) ≤ t (capacidade de correção BCH)

## 5. Correções Menores

- **Typo corrigido**: `total_erros_pos_reconcilicao` → `total_erros_pos_reconciliacao`
- **Documentação melhorada**: Comentários detalhados na função de reconciliação
- **Título do gráfico**: Indica uso de BPSK com reciprocidade

## Parâmetros Recomendados

- **Correlação canal**: ρ = 0.9 (típico: 0.8 ≤ ρ ≤ 0.99)
- **Código BCH**: Escolher (n,k,t) tal que t ≳ 1.5·n·BER
- **SNR range**: -10 a 30 dB (adequado para análise)

## Resultados Esperados

- **KDR antes**: Redução significativa devido à reciprocidade
- **KDR pós-reconciliação**: Melhora na correção de erros
- **Convergência**: KDR → 0 para SNRs altos com códigos adequados

## Possíveis Extensões Futuras

1. **Decodificador algorítmico**: Para códigos BCH grandes (n > 31)
2. **Códigos adaptativos**: Ajuste de (n,k,t) baseado no SNR estimado
3. **Amplificação de privacidade**: Implementação do pilar restante
4. **Análise de segurança**: Cálculo da informação vazada para Eva
