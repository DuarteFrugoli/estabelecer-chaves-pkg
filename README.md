# PLKG Simulator

Simulador reproduzivel de Physical-Layer Key Generation com duas familias de
observacao:

- CSI complexo para cenarios celulares 5G/6G;
- RSSI para dispositivos IoT com medicao de potencia limitada pelo hardware.

O canal fisico e independente da tecnologia de medicao. Quantizacao,
reconciliacao, amplificacao de privacidade, metricas e ataques sao componentes
reutilizaveis.

## Pipeline

```text
physical channel
  -> CSI or RSSI observation
  -> feature extraction
  -> quantization with public indices
  -> BCH code-offset reconciliation
  -> entropy bound
  -> universal-hash privacy amplification
  -> reliability and Eve metrics
```

Bob e Eve recebem exatamente o mesmo transcript publico. O hash universal nao
define sozinho o tamanho seguro da chave: o comprimento deve respeitar a
min-entropia restante e o vazamento da reconciliacao.

## Setup

O projeto usa Python 3.12 ou 3.13 e mantem a virtualenv em `.venv`.

```powershell
pipx install poetry==2.2.1
poetry env use python
poetry install --with dev
poetry run pytest
poetry run ruff check .
poetry run mypy
```

O Poetry deve estar instalado separadamente. `poetry.toml` configura o
ambiente virtual dentro do projeto; `pyproject.toml` define as versoes de
Python aceitas e `poetry.lock` fixa as dependencias.

## Experiments

Execucao rapida:

```powershell
poetry run python -m experiments.run_all
```

Execucao completa:

```powershell
poetry run python -m experiments.run_all --full
```

Cada experimento grava `results.csv` e `manifest.json` sob `results/`, com
seed, commit, versoes, plataforma e parametros.

```text
results/
  csi_snr_sweep/
    20260612T120000000000Z/
      results.csv
      manifest.json
```

A pasta `results/` e criada na primeira execucao e esta no `.gitignore`.
Resultados destinados a publicacao devem ser congelados e versionados como
artefatos de uma release, nao adicionados informalmente ao repositorio.

Os perfis usados pelos experimentos ficam em
`src/plkg/radio/profile_data/*.toml`. Eles sao a unica fonte de configuracao
dos perfis e tambem sao incluidos no wheel.

## Layout

```text
src/plkg/
  core/
  radio/
    channels/
    measurements/csi/
    measurements/rssi/
    profile_data/
  protocol/
    quantization/
    reconciliation/
    privacy_amplification/
  security/
  simulation/
experiments/
tests/
  unit/
  integration/
  statistical/
```

Veja:

- `docs/ARCHITECTURE.md` para as regras de dependencia e extensao;
- `docs/ROADMAP.md` para a ordem de implementacao;
- `docs/AUDIT.md` para o estado da auditoria estrutural.

## Continuous Integration

O workflow `.github/workflows/ci.yml` executa em Python 3.12 e 3.13:

- validacao do projeto com Poetry;
- Ruff e mypy;
- testes e cobertura;
- experimentos rapidos;
- build e instalacao de teste do wheel;
- verificacao dos perfis TOML empacotados.
