# Arquitetura

## Limites dos módulos

`radio` modela o canal físico e as observações específicas de cada tecnologia.
O CSI permanece complexo e futuramente poderá incluir subportadoras, antenas,
OFDM e estimação por pilotos. O RSSI representa uma medição escalar de potência
com ruído, resolução e limitações do receptor.

`protocol` contém as etapas que não precisam conhecer se a origem foi CSI ou
RSSI. Novos quantizadores, métodos de reconciliação e amplificadores de
privacidade devem implementar os contratos declarados em
`plkg.core.protocols`.

`security` contém limites de entropia e métricas de segurança. Modelos de
ataque devem consumir o mesmo transcript público disponibilizado a Bob.

`simulation` conecta implementações concretas em execuções reproduzíveis.
Toda aleatoriedade é fornecida explicitamente por um
`numpy.random.Generator`.

`experiments` importa o pacote `plkg` instalado. Os módulos de produção nunca
devem importar scripts de experimento.

Os perfis de rádio são recursos TOML empacotados em
`plkg.radio.profile_data`. O módulo `plkg.radio.profiles` valida e carrega
esses arquivos com `tomllib`. Os experimentos podem selecionar um perfil pelo
nome, mas não podem definir um segundo catálogo de perfis.

## Direção das dependências

```text
core <- radio
core <- protocol
core <- security
radio + protocol + security <- simulation <- experiments
```

Regras práticas:

- `core` não depende dos modelos concretos de rádio ou protocolo;
- `radio`, `protocol` e `security` não dependem de `simulation`;
- `simulation` é responsável pela composição dos componentes;
- `experiments` é a camada mais externa;
- nenhum módulo do pacote importa código de `experiments`.

## Fluxo do protocolo

```text
canal físico
  -> observação CSI ou RSSI
  -> extração de características
  -> quantização e seleção de índices
  -> reconciliação com transcript público
  -> estimação da entropia restante
  -> amplificação de privacidade
  -> métricas de confiabilidade e segurança
```

Limiar, índices aceitos, helper data e seed da amplificação são informações
públicas. Bob e Eve devem observar exatamente o mesmo transcript.

## Regras de extensão

1. Adicionar um componente somente quando existir implementação concreta e
   teste correspondente.
2. Manter waveforms e modulações na camada de rádio, fora das etapas genéricas
   do protocolo PLKG.
3. Publicar limiares, índices, helper data e seeds por modelos explícitos de
   transcript.
4. Comparar métodos com seeds explícitas e o mesmo orçamento de observações.
5. Reportar separadamente BMR, FER, retenção, abortos, vazamento e comprimento
   extraível da chave.
6. Não descrever experimentos RSSI como CSI.
7. Não inferir 256 bits de segurança somente a partir de um digest de 256
   bits.
8. Não criar diretórios ou interfaces vazias para funcionalidades futuras.

## Perfis de rádio

Os arquivos em `src/plkg/radio/profile_data/*.toml` são a única fonte oficial
dos perfis.

Cada perfil declara:

- tipo de medição, CSI ou RSSI;
- frequência da portadora;
- velocidade;
- intervalo entre amostras;
- correlação Alice-Bob e Alice-Eve;
- erro de estimação para CSI;
- potência de referência, ruído e resolução para RSSI.

O carregador rejeita campos desconhecidos, valores inválidos, campos
obrigatórios ausentes e nomes que não correspondam ao arquivo.

## Escopo atual

O modelo de rádio atual usa um canal Rayleigh plano e correlacionado. O CSI
utiliza a amplitude como característica. O RSSI deriva potência recebida
quantizada a partir do mesmo canal latente.

Ainda não estão implementados:

- canal multipercurso seletivo em frequência;
- OFDM, pilotos e estimação de canal;
- MIMO e beamforming;
- fading Rician;
- ataques ativos;
- calibração com datasets medidos.

Esses recursos devem entrar conforme as fases do `ROADMAP.md`, acompanhados de
testes e referências.

A dependência `galois` é utilizada como backend de pesquisa para simulações
BCH. Ela não é constant-time e não deve ser tratada como implementação
criptográfica de produção.

## Artefatos dos experimentos

Cada execução é armazenada em:

```text
results/<experimento>/<identificador UTC>/
  results.csv
  manifest.json
```

`results.csv` contém as medições tabulares. `manifest.json` contém parâmetros
resolvidos, seed, commit, plataforma e versões dos pacotes.

`results/` é ignorada pelo Git porque resultados Monte Carlo comuns são dados
gerados. Resultados destinados a publicação devem ser congelados e associados
a uma release, configuração e commit específicos.

## Testes e integração contínua

Os testes são separados em:

- `tests/unit`: comportamento local dos componentes;
- `tests/integration`: composição CSI/RSSI e protocolo;
- `tests/statistical`: propriedades que dependem de amostragem.

O GitHub Actions valida Python 3.12 e 3.13, executa Ruff, mypy, pytest, a
bateria rápida de experimentos, o build e uma instalação limpa do wheel. O
smoke test do wheel também confirma que os perfis TOML foram empacotados.
