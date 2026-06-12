# Estado da Auditoria

## Objetivo

Este documento registra o estado técnico após a remoção do código legado e a
migração para a arquitetura `plkg`.

O projeto passou de uma coleção de módulos, interfaces e demonstrações
misturadas para uma biblioteca de simulação voltada exclusivamente a
Physical-Layer Key Generation por CSI e RSSI.

## Correções concluídas

- O pacote importável agora é `plkg`, e não `src`.
- Pastas, módulos, APIs e experimentos novos utilizam nomes em inglês.
- CSI e RSSI possuem modelos de observação distintos.
- O canal físico foi separado da tecnologia de medição.
- Quantização, reconciliação e amplificação de privacidade são componentes
  reutilizáveis.
- Bob e Eve recebem o mesmo transcript público de reconciliação.
- Toda aleatoriedade do núcleo usa `numpy.random.Generator` explícito.
- O código não utiliza mais o estado global de `random` ou `numpy.random`.
- SHA-256 deixou de ser apresentado como garantia automática de 256 bits de
  segurança.
- A amplificação de privacidade usa universal hashing com matriz Toeplitz.
- O cálculo de comprimento extraível considera entropia, vazamento e margem de
  segurança.
- O caso crítico de correlação `rho = -1` com quantização de amplitude possui
  teste de regressão.
- Os experimentos registram seed, commit, versões, plataforma e parâmetros.
- A comparação BCH usa orçamento explícito de observações.
- Os perfis possuem uma única fonte TOML validada e empacotada.
- O wheel inclui e consegue carregar todos os perfis.
- O GitHub Actions valida Python 3.12 e 3.13.
- Interfaces gráficas, demonstrações de modulação, visualizações antigas,
  resultados obsoletos e testes do fluxo legado foram removidos.

## Ambiente e qualidade

O ambiente foi reconstruído com dependências explícitas no `pyproject.toml` e
versões resolvidas no `poetry.lock`.

Validações atualmente disponíveis:

- `poetry check`;
- Ruff;
- mypy em modo estrito;
- pytest com cobertura;
- testes unitários, de integração e estatísticos;
- bateria rápida de experimentos;
- build de sdist e wheel;
- smoke test de instalação do wheel.

O arquivo `poetry.toml` mantém a virtualenv dentro do projeto. A faixa oficial
é definida em `requires-python`; por isso não existe dependência de
`.python-version`.

## Resultados experimentais

Os experimentos escrevem em:

```text
results/<experimento>/<run_id>/
  results.csv
  manifest.json
```

Os resultados são ignorados pelo Git. Isso evita versionar saídas Monte Carlo
ocasionais e permite repetir as execuções com seeds conhecidas.

Para publicação, os resultados escolhidos deverão ser congelados como
artefatos de release e vinculados ao commit, lockfile e configuração que os
produziram.

## Limitações científicas atuais

Apesar da renovação estrutural, os resultados ainda representam uma base de
pesquisa, não uma validação completa de segurança ou implantação real.

### Segurança e entropia

- A min-entropia condicional ainda não é estimada diretamente a partir das
  observações de Eve.
- Ainda faltam intervalos de confiança para as métricas agregadas.
- Mutual information e guessing probability ainda não são reportadas.
- O vazamento total precisa incorporar formalmente toda comunicação pública.

### CSI 5G/6G

- O canal atual é Rayleigh plano.
- Ainda não existem OFDM, pilotos, subportadoras ou estimação por waveform.
- Ainda não existem multipercurso seletivo, MIMO, beamforming ou Rician.
- Os perfis atuais são parâmetros experimentais iniciais, não modelos 3GPP
  completos.

### RSSI IoT

- Ainda faltam path loss, shadowing e sensibilidade do receptor.
- Ainda faltam bias entre dispositivos, saturação e perda de pacotes.
- Os perfis precisam ser calibrados com literatura ou traces medidos.
- Ainda não há dataset real versionado para regressão.

### Eve

- Eve atualmente é passiva e representada por correlação com o canal.
- Ainda faltam posição, antena, hardware e SNR próprios.
- Ainda não existem pilot contamination, jamming, replay ou signal injection.
- Ainda não existem defesas ou autenticação do transcript.

## Próximas prioridades

1. Criar resultados por repetição e intervalos de confiança.
2. Registrar amostras aceitas, descartadas, blocos e abortos.
3. Implementar estimativa de min-entropia condicional.
4. Integrar o comprimento extraível automaticamente ao pipeline.
5. Completar o modelo RSSI IoT com dados medidos.
6. Evoluir CSI para OFDM, pilotos e canal seletivo em frequência.
7. Implementar o framework de ataques ativos de Eve.

A ordem detalhada, os critérios de aceite e as melhorias futuras estão em
`docs/ROADMAP.md`.

## Conclusão

A base estrutural agora é coerente com o objetivo do projeto: simular um
sistema PLKG modular, reproduzível e testável contra Eve.

O maior risco restante não é mais código legado, mas avançar para modelos
complexos sem antes concluir métricas estatísticas e de entropia. As próximas
fases devem seguir os Gates definidos no roadmap.
