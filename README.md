# Local ML Vibes

A lightweight software-engineering workspace for running, evaluating, and
serving machine-learning models locally. The repository is intentionally
small: it provides clear seams for application code, model adapters, tests,
experiments, and operational configuration without prescribing a large
framework.

## Repository structure

```text
local-ml-vibes/
├── .claude/
│   └── skills/
│       ├── generate-swe-repo/
│       └── add-local-model/
├── src/
│   └── local_ml_vibes/
│       ├── models/
│       │   ├── config.py
│       │   └── loaders.py
│       └── settings.py
├── tests/
│   └── test_model_config.py
├── notebooks/
│   └── huggingface_local_model_loading.ipynb
├── examples/
├── scripts/
├── pyproject.toml
└── README.md
```

## Hugging Face model-loading scaffold

The [model configuration](/Users/timothychin/PycharmProjects/local-ml-vibes/src/local_ml_vibes/models/config.py)
and [loader interface](/Users/timothychin/PycharmProjects/local-ml-vibes/src/local_ml_vibes/models/loaders.py)
define the boundary for loading a model from a Hugging Face repository or a
local cache:

```python
from local_ml_vibes.models.config import ModelConfig
from local_ml_vibes.models.loaders import load_text_generator

config = ModelConfig(repository_id="your-org/your-model")
generator = load_text_generator(config)
```

This repository does **not** download or load a model during setup. Install the
optional `models` dependency group and call the loader explicitly when you are
ready:

```bash
uv sync --extra models
```

The loader supports explicit offline mode, local cache directories, device
selection, and dtype configuration. Keep credentials and private model
identifiers out of source control.

The [Hugging Face loading notebook](/Users/timothychin/PycharmProjects/local-ml-vibes/notebooks/huggingface_local_model_loading.ipynb)
walks through this configuration and includes a commented-out loading cell.
It is safe to open without downloading or initializing any model.

## Development

```bash
uv sync --dev
uv run pytest
```

The project follows a simple application boundary: production code belongs in
`src/`, tests mirror behavior in `tests/`, exploratory work belongs in
`examples/` or `scripts/`, and reusable workflows should be documented as
skills under `.claude/skills/`.
