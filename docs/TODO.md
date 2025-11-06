# Objetivo principal atual
Chegar a um estado em que seja possível simular a distância (frequência) entre dispositivos e um invasor tentando acessar a chave gerada entre eles. Plot de chaves geradas, reconciliadas e descobertas pelo invasor no final.

1. aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
2. arrumar bpsk (ver como ele está sendo implementado com a sua frequência)
3. bpsk modulado * frenquencia de portadora (banda de coerência)
4. implementar qpsk para testar sua eficiência na geração de chaves (comparar kdr com o bpsk)
5. colocar explicação dos termos no terms e no readme
6. criar modo avançado (main_advanced.py e gui_advanced.py) com parâmetros configuráveis

## Importante
- simular invasor
- simular distância
- estudar mais termos de bpsk e qpsk e implementá-los no código
- estudar como a quantidade de erros que o bch pode corrigir afeta os resultados
- escrever o começo do relatório


## daqui 3 semanas
- comparar taxa de erro de bit (BER) teórica e simulada (bpsk e qpsk)
- plots das fases dos processsos da modulação, geração da sequencia binaria, sequencia binaria antipodal (1 e -1), sequencia modulada (onda eletromagnética). Tudo para observar a variação da frenquência.