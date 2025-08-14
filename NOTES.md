# Sobre BCH

O BCH é definido como (n, k, t):

n → tamanho total da palavra código (bits de informação + bits de paridade)

k → número de bits de informação

n − k → número de bits de paridade (fixo para aquele código)

t → número máximo de erros que podem ser corrigidos

## Para BCH binário padrão:

𝑛 = 2^𝑚 − 1

onde 𝑚 é um inteiro ≥ 3.
Alguns exemplos:

𝑚 = 3 → 𝑛 = 7  
𝑚 = 4 → 𝑛 = 15  
𝑚 = 5 → 𝑛 = 31  
𝑚 = 6 → 𝑛 = 63  
𝑚 = 7 → 𝑛 = 127  
𝑚 = 8 → 𝑛 = 255  

(Existem BCH encurtados, mas a base é essa.)

## Valores possíveis de k e bits de paridade

| Código BCH | k (bits info) | Paridade (n − k) | t (erros) |
| ---------- | ------------- | ---------------- | --------- |
| (7, 4)     | 4             | 3                | 1         |
| (15, 11)   | 11            | 4                | 1         |
| (15, 7)    | 7             | 8                | 2         |
| (31, 26)   | 26            | 5                | 1         |
| (31, 16)   | 16            | 15               | 3         |
| (63, 57)   | 57            | 6                | 1         |
| (63, 45)   | 45            | 18               | 3         |
| (127, 120) | 120           | 7                | 1         |
| (127, 64)  | 64            | 63               | 10        |
| (255, 247) | 247           | 8                | 1         |
| (255, 139) | 139           | 116              | 15        |

Repare: para o mesmo n, se você escolher um 𝑡 diferente, o número de bits de paridade muda, mas para um BCH específico (n,k) ele é sempre fixo.

## Como funciona a reconciliação entre A e B
    
###### Alice
1. Gera Ka por quantização assim como bob com Kb
2. Escolhe uma palavra código aleatória C da tabela de códigos
3. calcula S = Ka ⊕ C e envia S para Bob
###### Bob
1. Bob calcula Cb = S ⊕ Kb → versão corrompida de C
2. Bob compara Cb com todos os códigos na tabela e encontra o código válido mais próximo
3. Bob reconstrói a chave → Ka = S ⊕ Cb

# Dúvidas
    eu tenho quase certeza que algo está errado, não sei se é no método de reconciliação proposto no artigo 2, não sei se é no meu código, não sei de nada, estou ficando maluco. BCH não foi feito para ser usado desse jeito.

    pelo menos agora dá para saber quais métodos de reconciliação estão funcionando ou não e também testar outros tipos de quantização. creio que estas partes estejam corretas.