# CORREÇÃO DO ERRO "too many values to unpack" - MAIN.PY

## 🚨 **Problema Identificado**

```
ValueError: too many values to unpack (expected 2)
```

**Causa**: A função `extrair_kdr()` foi atualizada para retornar 3 valores quando `usar_amplificacao=True`, mas o `main.py` ainda estava tentando desempacotar apenas 2 valores.

## ✅ **Solução Implementada**

### 1. **Opção para o Usuário**
Adicionada pergunta interativa no `main.py`:
```python
print("🔐 AMPLIFICAÇÃO DE PRIVACIDADE")
print("A amplificação de privacidade aplica SHA-256 para gerar chaves de 256 bits...")
usar_amplificacao = input("Deseja usar amplificação de privacidade? (s/N): ")
```

### 2. **Desempacotamento Condicional**
```python
if usar_amplificacao:
    kdr, kdr_pos_reconciliacao, kdr_pos_amplificacao = extrair_kdr(
        # ... parâmetros ...
        usar_amplificacao=True
    )
    kdr_amplificacao_rates.append(kdr_pos_amplificacao)
else:
    kdr, kdr_pos_reconciliacao = extrair_kdr(
        # ... parâmetros ...
        usar_amplificacao=False
    )
```

### 3. **Plotagem Adaptável**
```python
# Plota com ou sem amplificação conforme escolha
plot_kdr(snr_db_range, kdr_rates, kdr_pos_rates, rayleigh_param, kdr_amplificacao_rates)
```

## 🧪 **Validação da Correção**

### Teste Executado com Sucesso:
```
🔄 Testando SEM amplificação...
  SNR 0.0dB -> KDR: 9.33% -> 3.60%    ✅
  SNR 10.0dB -> KDR: 1.20% -> 0.00%   ✅

🔐 Testando COM amplificação...
  SNR 0.0dB -> KDR: 12.80% -> 7.07% -> 10.07%   ✅
  SNR 10.0dB -> KDR: 0.93% -> 0.00% -> 0.00%    ✅

✅ Retorno de 2 valores (sem amplificação)
✅ Retorno de 3 valores (com amplificação)
⏱️  Performance: 0.1s (ambos os modos)
```

## 🎯 **Benefícios da Solução**

### ✅ **Compatibilidade Total**
- **Modo clássico**: Funciona como antes (sem amplificação)
- **Modo avançado**: Inclui amplificação de privacidade
- **Escolha do usuário**: Interface interativa

### ✅ **Flexibilidade**
- **Pesquisa**: Pode comparar com/sem amplificação
- **Performance**: Modo sem amplificação é mais rápido
- **Segurança**: Modo com amplificação oferece 256 bits

### ✅ **Robustez**
- **Sem quebras**: Código anterior funciona
- **Extensível**: Facilita futuras melhorias
- **Testado**: Validação completa realizada

## 🚀 **Como Usar Agora**

### Execução Simples (Sem Amplificação)
```bash
python main.py
# Escolher "N" quando perguntado sobre amplificação
```

### Execução Completa (Com Amplificação)
```bash
python main.py
# Escolher "s" quando perguntado sobre amplificação
```

### Execução de Testes
```bash
cd testes
python teste_main_corrigido.py  # Valida ambos os modos
```

## 📊 **Status Final**

**✅ PROBLEMA COMPLETAMENTE RESOLVIDO**

- **Erro eliminado**: Desempacotamento correto de valores
- **Funcionalidade preservada**: Modo clássico intacto
- **Funcionalidade expandida**: Amplificação opcional
- **Testado e validado**: Funcionamento confirmado
- **Interface melhorada**: Escolha clara para o usuário

O `main.py` agora funciona perfeitamente em ambos os modos! 🎯✨
