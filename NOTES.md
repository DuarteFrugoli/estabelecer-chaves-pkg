# Anotações aleatórias

y = h * x + n

o artigo do método 2 usa o CSI e não o ganho, além disso a quantização é feita utilizando o block-gray. A reconciliação é com BCH mesmo.

O KDR é a taxa de erro entre as chaves extraídas, ou seja, a quantidade de vezes (em percentual) que as chaves geradas são diferentes. Podemos fazer o kdr pós-processamento para ver a eficácia dos códigos de correção de erros.



# sobre PKG

PKG = Physical-layer Key Generation

a) Comunicação clássica (não PKG)
Você transmite o código BCH inteiro (informação + paridade).
Exemplo: pega 4 bits info, gera 3 bits paridade, envia os 7 bits.

b) PKG com reconciliação
Você não transmite a palavra código inteira — porque o objetivo é não revelar a chave toda.

Alice calcula os bits de paridade a partir dos bits dela.

Ela envia somente os bits de paridade.

Bob pega a sequência dele (que é quase igual à de Alice) e aplica o algoritmo BCH usando os bits de paridade recebidos para corrigir erros.

Assim, Bob chega exatamente na sequência de Alice.

O espião Eve pode ouvir os bits de paridade, mas isso não é suficiente para reconstruir a chave inteira, desde que a reconciliação seja bem projetada.



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
| (255, 131) | 131           | 124              | 15        |

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