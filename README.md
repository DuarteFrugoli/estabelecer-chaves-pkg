# Estabelicimento de chave criptografica

## 📌 Estrutura do Código

- **`CodeGenerator`**: Classe responsável pela geração das tabelas de código.
- **`Cenário1 - Cenário5`**: Classes que modelam diferentes cenários de ruído.
- **`Plotagem`**: Classe que gerencia a visualização gráfica dos resultados.
- **`main.py`**: Script principal que executa a simulação.

---

## 🚀 Como Usar

### 1️⃣ Instalação

Certifique-se de ter o **Python 3.x** instalado e instale as dependências necessárias:

```sh
pip install numpy matplotlib
```

### 2️⃣ Execução

Execute o script principal com:

```sh
python Main.py
```

### 3️⃣ Entradas do Usuário

Durante a execução, o usuário deve fornecer as seguintes informações:

- **Quantidade de testes**: Número de simulações a serem realizadas.
- **Tamanho da cadeia de bits**: Para códigos diferentes de `Golay`, escolha entre `7, 15, 127, 255`.
- **Plotagem de resultados**: Opção de visualizar gráficos (`y` para sim, `n` para não).

### 4️⃣ Saída

O código exibe as porcentagens de acerto nos diferentes cenários de ruído e gera gráficos representando os resultados da simulação.

---

## 🔧 Estrutura dos Canais

Os seguintes canais são simulados:

- **Ruído Nulo Canal Unitário**
- **Baixo Ruído Canal Unitário**
- **Baixo Ruído Canal Rayleigh**
- **Alto Ruído Canal Unitário**
- **Alto Ruído Canal Rayleigh**

Cada um desses canais afeta a transmissão dos bits e influencia a taxa de erro na recuperação da informação.

---

## ⏳ Tempo de Execução

O código mede o tempo total de execução e exibe o tempo decorrido ao final da simulação.

---

## 📊 Visualização de Dados

Os resultados são apresentados graficamente usando a classe **Plotagem**.

---
🚀 **Este projeto faz parte de uma iniciativa de pesquisa sobre segurança em canais sem fio e técnicas de correção de erros.**
