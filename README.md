# Segurança em Camada Física: Estabelecimento de Chaves Criptográficas para Comunicações Móveis de Próxima Geração

Este projeto faz parte da Iniciação Científica (IC) **"Segurança em Camada Física: Estabelecimento de Chaves Criptográficas para Comunicações Móveis de Próxima Geração"**.

- **Autores:** Pedro Henrique Duarte Frugoli e Henrique Rodrigues Mendonça
- **Baseado em código anterior de:** João Gabriel Ferreira Ribeiro

## 🎯 Objetivo

O objetivo deste projeto é simular o sucesso no estabelecimento de chaves criptográficas em relação ao SNR (relação sinal-ruído) em um cenário de geração de chaves na camada física (PKG - *Physical-layer Key Generation*), antes e depois da aplicação do código corretor de erros BCH.

A simulação permite analisar como diferentes condições de ruído e parâmetros do código BCH afetam a taxa de sucesso na geração de chaves seguras.

## 🛠️ Dependências

Certifique-se de ter o **Python 3.x** instalado. Instale as dependências necessárias com:

```sh
pip install numpy matplotlib galois
```

## ▶️ Como Executar

Execute o script principal com:

```sh
python Main.py
```

## 📝 Entradas do Usuário

Durante a execução, o usuário deverá fornecer:

- **Quantidade de testes:** Número de simulações a serem realizadas.
- **Tamanho da cadeia de bits:** Escolha entre `7, 15, 127, 255`.
- **Tamanho do espaço amostral:** (Opcional, para cadeias muito grandes) Define o número de amostras a serem consideradas.

## 📈 Saída

O código exibe um gráfico de estabelecimento da chave versus SNR, comparando os resultados antes e depois do processamento com o código BCH.

## 🧩 Estrutura do Código

```
C:.
│   main.py
│   NOTES.md
│   plotkar.py
│   README.md
│   TODO.md
│
├───canal
│   │   canal.py
│   │   __init__.py
│
├───codigos_corretores
│   │   bch.py
│   │   __init__.py
│
├───pilares
│       amplificacao_privacidade.py
│       reconciliacao.py
│       __init__.py
│
├───util
│   │   binario_util.py
│   │   util.py
│   │   __init__.py
```

## ⏱️ Tempo de Execução

O tempo total de execução é medido e exibido ao final da simulação no terminal.

🚀 **Este projeto integra pesquisa sobre segurança em canais sem fio e técnicas de correção de erros para comunicações móveis de próxima geração.**
