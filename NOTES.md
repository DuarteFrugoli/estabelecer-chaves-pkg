eu estou tentando muito simplificar as coisas, não precisam ser classes, João pelo amor de Deus cara.

vou primeiro tirar as funções de inicializar pq n precisa.

depois de ajeitar tudo que for necessário vou ter certeza de que nenhuma variável está sendo criada 2 vezes ou se perdendo no meio do caminho.

eu encontrei variáveis sendo inicializadas em chamada de função, isso é um ultraje. Eu estou ficando maluco.

Qual o caminho atual de informações do código:
1. Main
    1. variáveis iniciais
    2. entradas
    3. cria instância de CodeGenerator com o parâmetro "tamanho_cadeia_bits"
    4. cria uma tabela (nome pouco intuitivo) usando o método "generate_code_table" da classe CodeGenerator
    5. cria uma instância de AltoRuidoCanalRayleigh com os parâmetros media_ruido, variancia_ruido e quantidade_de_testes e guarda em canais
        1. AltoRuidoCanalRayleigh cria uma instância de CenárioBase e uma instância de Plotagem
    6. chama o método "cenario" de AltoRuidoCanalRayleigh
        1.

a última coisa que eu fiz em 28/07 foi adicionar os TODOS em comentário de onde eu vou mudar mais tarde.