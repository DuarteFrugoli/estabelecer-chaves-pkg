# PLKG Simulator Roadmap

Este documento define a ordem de implementacao do projeto. A prioridade nao e
acumular modelos, mas construir resultados reproduziveis e cientificamente
defensaveis para:

- CSI em sistemas 5G/6G;
- RSS/RSSI em dispositivos IoT;
- avaliacao de seguranca contra Eve passiva e ativa;
- comparacao modular de quantizacao, reconciliacao e privacy amplification.

## Status Legend

- `[x]` concluido;
- `[~]` implementado parcialmente;
- `[ ]` pendente;
- `Gate` criterio obrigatorio para iniciar a fase seguinte.

## Current Baseline

- [x] Pacote importavel `plkg` usando o layout `src/`.
- [x] Separacao entre canal fisico, CSI, RSSI e protocolo PLKG.
- [x] Quantizacao por mediana com guard band.
- [x] Reconciliacao BCH code-offset.
- [x] Transcript publico unico para Bob e Eve.
- [x] Privacy amplification com Toeplitz universal hashing.
- [x] RNG explicito com `numpy.random.Generator`.
- [x] Testes unitarios, de integracao e estatisticos.
- [x] Experimentos com seed, commit, versoes e parametros.
- [x] Ambiente local funcional com Python 3.13.
- [~] Metricas de seguranca basicas.
- [~] Perfis de radio para CSI e RSSI.
- [ ] Modelos realistas de 5G/6G e IoT.
- [ ] Estimativa condicional de entropia.
- [ ] Ataques ativos de Eve.

## Phase 0 - Repository And Environment

Objetivo: garantir que qualquer colaborador consiga instalar, testar e repetir
um experimento sem depender do estado local da maquina.

### Tasks

- [x] Remover `.python-version`, pois o projeto nao usa pyenv ou mise.
- [x] Manter a faixa oficial de Python em `requires-python`.
- [x] Documentar a instalacao do Poetry, preferencialmente via `pipx`.
- [x] Documentar `poetry env use` para selecionar Python 3.12 ou 3.13.
- [x] Escolher uma unica fonte para perfis de radio.
- [x] Implementar carregamento dos perfis TOML com `tomllib`.
- [x] Remover `PROFILES` hardcoded quando os TOMLs forem a fonte oficial.
- [x] Validar schema e unidades de todos os arquivos de configuracao.
- [x] Adicionar CI para Python 3.12 e 3.13.
- [x] Executar no CI: `poetry check`, pytest, Ruff e mypy.
- [x] Adicionar teste de instalacao e import do pacote empacotado.
- [ ] Definir uma politica de versao e changelog.

### Deliverables

- Workflow de CI.
- Guia de instalacao testado em ambiente limpo.
- Carregador tipado de configuracao.
- Um unico catalogo de perfis.

### Gate

Uma nova maquina deve conseguir instalar o projeto pelo lockfile, executar
todos os testes e reproduzir um experimento rapido sem edicao manual.

## Phase 1 - Experimental Foundations

Objetivo: tornar comparacoes estatisticamente validas antes de aumentar o
realismo do radio.

### Tasks

- [ ] Criar `ExperimentConfig` e `ExperimentResult` tipados.
- [ ] Registrar a configuracao completa resolvida no manifesto.
- [ ] Registrar numero de amostras geradas, aceitas e descartadas.
- [ ] Registrar numero de blocos processados e abortados.
- [ ] Adicionar intervalos de confianca para todas as taxas.
- [ ] Salvar resultados por repeticao, nao apenas medias agregadas.
- [ ] Introduzir common random numbers para comparar metodos.
- [ ] Separar seeds de canal, ruido, reconciliacao e privacy amplification.
- [ ] Adicionar FER, taxa de aborto e bits finais por observacao.
- [ ] Medir tempo ponta a ponta com p50, p95 e p99.
- [ ] Definir unidades explicitamente nos nomes e metadados.
- [ ] Criar teste de reproducibilidade byte a byte para uma seed fixa.
- [ ] Criar um comando unico para validar todos os experimentos.

### Metrics Required

- Raw Bit Mismatch Rate.
- Reconciled Bit Mismatch Rate.
- Frame Error Rate.
- Abort Rate.
- Retention Rate.
- Public Leakage.
- Extractable Key Length.
- Secret Bits Per Observation.
- End-to-end Runtime.

### Gate

Toda curva deve conter quantidade efetiva de amostras, intervalo de confianca,
seed e configuracao completa.

## Phase 2 - Security And Entropy

Objetivo: substituir indicadores isolados de BER por uma avaliacao explicita
da informacao restante apos Eve e o transcript publico.

### Tasks

- [ ] Definir formalmente o modelo de conhecimento de Eve.
- [ ] Representar toda comunicacao publica no `PublicTranscript`.
- [ ] Incluir limiar, indices, helper data, seed e abortos no vazamento.
- [ ] Implementar estimadores de min-entropia.
- [ ] Implementar min-entropia condicional dada a observacao de Eve.
- [ ] Calcular o comprimento final pelo leftover hash lemma.
- [ ] Integrar automaticamente o comprimento extraivel ao pipeline.
- [ ] Impedir extracao quando a entropia estimada for insuficiente.
- [ ] Reportar mutual information Alice-Bob e Alice-Eve.
- [ ] Reportar guessing probability de Eve.
- [ ] Comparar Eve antes e depois do transcript publico.
- [ ] Adicionar testes para correlacao `-1`, `0` e `1`.
- [ ] Adicionar testes para Eve com observacao melhor que Bob.
- [ ] Documentar hipoteses e limitacoes de cada estimador.

### Gate

Nenhum resultado deve ser chamado de seguro apenas porque a BER de Eve esta
proxima de 50%. O pipeline deve reportar entropia, vazamento e comprimento
final extraivel.

## Phase 3 - Realistic RSSI For IoT

Objetivo: construir primeiro um modelo IoT completo e validavel, por ser mais
simples do que CSI MIMO/OFDM.

### Channel And Hardware

- [ ] Adicionar path loss com distancia e frequencia.
- [ ] Adicionar log-normal shadowing.
- [ ] Adicionar fading temporal correlacionado.
- [ ] Modelar piso de ruido e sensibilidade do receptor.
- [ ] Modelar saturacao, clipping e resolucao do RSSI.
- [ ] Modelar offset e bias especificos por dispositivo.
- [ ] Modelar perda de pacotes e amostragem irregular.
- [ ] Modelar atraso entre as medicoes de Alice e Bob.
- [ ] Separar RSS de valor RSSI reportado pelo hardware.

### Profiles

- [ ] Criar perfis calibrados para IEEE 802.15.4.
- [ ] Criar perfis calibrados para BLE.
- [ ] Criar perfis calibrados para LoRa/LoRaWAN.
- [ ] Criar perfis calibrados para NB-IoT.
- [ ] Citar a origem de cada parametro.

### Validation

- [ ] Importar traces reais em CSV ou formato documentado.
- [ ] Comparar distribuicoes simuladas e medidas.
- [ ] Validar autocorrelacao, variancia e taxa de perda.
- [ ] Criar testes de regressao com um pequeno dataset versionado.

### Gate

Os perfis IoT devem ser rastreaveis a literatura ou dados medidos, e as
metricas simuladas devem reproduzir propriedades estatisticas desses dados.

## Phase 4 - Realistic CSI For 5G/6G

Objetivo: evoluir do fading plano para uma cadeia de estimacao de CSI baseada
em waveform.

### Waveform

- [ ] Criar contratos para waveform, modulation e pilot pattern.
- [ ] Implementar OFDM com FFT/IFFT e cyclic prefix.
- [ ] Implementar BPSK, QPSK e QAM como componentes de waveform.
- [ ] Configurar subcarrier spacing e numerologia.
- [ ] Modelar pilotos e estimacao de canal.
- [ ] Modelar interpolacao no tempo e frequencia.

### Channel

- [ ] Implementar canal multipath frequency-selective.
- [ ] Implementar Rician fading e componente LoS.
- [ ] Implementar Doppler e mobilidade temporal.
- [ ] Implementar correlacao entre subportadoras.
- [ ] Implementar correlacao espacial entre antenas.
- [ ] Implementar MIMO e beamforming.
- [ ] Adicionar modelos de phase noise e carrier frequency offset.
- [ ] Adicionar quantizacao de ADC e imperfeicoes de RF quando necessario.

### Profiles

- [ ] Criar perfil 5G NR FR1.
- [ ] Criar perfil 5G NR FR2/mmWave.
- [ ] Criar perfil 6G sub-THz de pesquisa.
- [ ] Separar parametros normativos de hipoteses experimentais.
- [ ] Citar 3GPP ou literatura para cada perfil.

### Features

- [ ] CSI amplitude.
- [ ] CSI phase after sanitization.
- [ ] Phase differences.
- [ ] Subcarrier selection.
- [ ] Temporal differences.
- [ ] Spatial/MIMO features.
- [ ] Feature fusion with leakage analysis.

### Gate

Os experimentos 5G/6G devem derivar CSI de pilotos recebidos por uma waveform,
nao de coeficientes perfeitos entregues diretamente ao quantizador.

## Phase 5 - Quantization Research

Objetivo: comparar quantizadores sob o mesmo canal, observacoes e orcamento.

### Methods

- [x] Median threshold with guard band.
- [ ] Mean and adaptive threshold.
- [ ] CDF/equiprobable quantization.
- [ ] Multi-bit quantization.
- [ ] Level crossing.
- [ ] Differential quantization.
- [ ] Vector quantization.
- [ ] Learned quantization, somente apos baselines solidos.

### Evaluation

- [ ] Usar as mesmas realizacoes para todos os metodos.
- [ ] Medir bias e autocorrelacao dos bits.
- [ ] Medir retencao e taxa de aborto.
- [ ] Medir entropia e informacao de Eve.
- [ ] Comparar custo computacional.
- [ ] Testar sensibilidade aos parametros.

### Gate

Um novo quantizador deve superar ou complementar o baseline em uma metrica
predefinida sem reduzir silenciosamente entropia ou taxa de geracao.

## Phase 6 - Reconciliation Research

Objetivo: avaliar confiabilidade, vazamento e custo de metodos alternativos.

### Methods

- [x] BCH code-offset baseline.
- [ ] BCH com escolha automatica de parametros.
- [ ] LDPC syndrome reconciliation.
- [ ] Polar-code reconciliation.
- [ ] Cascade como baseline interativo.
- [ ] Rate adaptation.

### Evaluation

- [ ] FER em funcao do BMR.
- [ ] Vazamento publico real.
- [ ] Numero de mensagens e bytes transmitidos.
- [ ] Tempo, memoria e energia estimada.
- [ ] Capacidade de abortar falhas nao corrigiveis.
- [ ] Comparacao com igual comprimento de chave e igual orcamento de amostras.

### Gate

O pipeline deve distinguir sucesso de decodificacao, chave incorreta e aborto.
O vazamento de cada reconciliador deve ser explicitamente contabilizado.

## Phase 7 - Eve Attack Framework

Objetivo: transformar Eve em um componente extensivel com capacidades e
restricoes declaradas.

### Passive Eve

- [~] Observacao correlacionada do mesmo canal.
- [ ] Posicao e distancia explicitas.
- [ ] Antenas e hardware proprios.
- [ ] SNR e taxa de amostragem proprios.
- [ ] Multiplas Eves colaborativas.
- [ ] Eve com observacoes temporais acumuladas.

### Active Eve

- [ ] Pilot contamination.
- [ ] Jamming.
- [ ] Replay.
- [ ] Signal injection.
- [ ] Man-in-the-middle durante probing.
- [ ] Manipulacao do transcript publico.
- [ ] Selective denial-of-service.

### Defenses

- [ ] Autenticacao do transcript.
- [ ] Deteccao de anomalias no canal.
- [ ] Testes de reciprocidade antes da quantizacao.
- [ ] Deteccao de pilot contamination.
- [ ] Politicas de aborto.

### Gate

Cada ataque deve declarar o que Eve conhece, controla e observa. Experimentos
devem comparar ataque e baseline usando as mesmas realizacoes.

## Phase 8 - Protocol Composition

Objetivo: permitir montar cenarios sem editar o codigo do runner.

### Tasks

- [ ] Criar factories/registry para componentes.
- [ ] Montar pipelines inteiros por TOML.
- [ ] Validar compatibilidade entre observacao e feature extractor.
- [ ] Permitir selecao de quantizer, reconciler e amplifier.
- [ ] Permitir selecao de Eve e attack model.
- [ ] Criar sweep declarativo de parametros.
- [ ] Criar resume de execucoes interrompidas.
- [ ] Evitar plugins dinamicos ate haver necessidade concreta.

### Gate

Um experimento novo deve ser configuravel sem duplicar runners ou modificar o
nucleo do pacote.

## Phase 9 - Performance And Scale

Objetivo: aumentar o volume de simulacao sem comprometer reprodutibilidade.

### Tasks

- [ ] Medir hotspots antes de otimizar.
- [ ] Vetorizar Monte Carlo onde for seguro.
- [ ] Adicionar paralelismo com streams RNG independentes.
- [ ] Criar checkpoints e retomada.
- [ ] Adicionar batches e limites de memoria.
- [ ] Avaliar Numba apenas nos hotspots medidos.
- [ ] Adicionar benchmark de regressao.
- [ ] Avaliar GPU somente para cenarios que justifiquem a complexidade.

### Gate

Resultados paralelos devem permanecer reproduziveis e estatisticamente
equivalentes ao runner de referencia.

## Phase 10 - Publication And Reproducibility

Objetivo: produzir artefatos adequados para artigos e revisao externa.

### Tasks

- [ ] Congelar configs dos experimentos publicados.
- [ ] Gerar tabelas e figuras a partir dos dados salvos.
- [ ] Nunca recalcular resultados dentro do codigo de plot.
- [ ] Registrar commit, lockfile e ambiente de cada figura.
- [ ] Exportar dataset processado e manifesto.
- [ ] Criar scripts de reproducao por figura/tabela.
- [ ] Documentar hipoteses, ameacas a validade e limitacoes.
- [ ] Adicionar referencias bibliograficas aos modelos.
- [ ] Criar release versionada para cada submissao.

### Gate

Cada numero publicado deve ser rastreavel a um manifesto, configuracao, seed,
commit e arquivo de resultado.

## Future Improvements

Estas ideias devem entrar somente depois das fases das quais dependem.

- Measurement campaigns com SDRs, smartphones e dispositivos IoT.
- Digital twins de ambientes indoor, industrial e veicular.
- Ray tracing ou channel datasets externos.
- Secret-key capacity bounds.
- Estimadores de entropia baseados em modelos nao parametricos.
- Multi-party group key generation.
- Cooperative relays.
- Cross-layer authentication.
- Adaptive probing.
- Hardware energy profiling.
- Federated calibration entre dispositivos heterogeneos.
- ML para selecao de features e parametros.
- Adversarial ML contra classificadores de ataque.
- Reconciliacao e quantizacao adaptativas em tempo real.
- Suporte a outros observaveis, como CIR, AoA, ToF e Doppler.

## Recommended Immediate Order

1. Concluir Phase 0.
2. Implementar Phase 1.
3. Implementar Phase 2.
4. Completar RSSI IoT na Phase 3.
5. Completar CSI 5G/6G na Phase 4.
6. Comparar quantizadores e reconciliadores nas Phases 5 e 6.
7. Implementar Eve ativa na Phase 7.
8. Declarar pipelines e escalar experimentos nas Phases 8 e 9.
9. Congelar resultados publicaveis na Phase 10.

As fases podem ter pequenas sobreposicoes, mas seus Gates nao devem ser
ignorados. Em especial, modelos mais sofisticados de radio nao compensam
metricas de seguranca incompletas ou experimentos sem rastreabilidade.
