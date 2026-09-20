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

## Discovering Hugging Face models, especially local LLMs

Hugging Face model discovery should begin with the task and hardware
constraints, not with a model name. For local large language models (LLMs),
use the Hub search filters and each model card to verify:

- **Task and architecture:** confirm whether the checkpoint is for
  text-generation, chat/instruction following, embeddings, classification, or
  another task supported by the intended runtime.
- **Model size and memory:** parameter count is only a rough guide. Account
  for weights, runtime overhead, context length, KV cache, and operating-system
  memory. Quantized variants can reduce memory requirements but may change
  quality and supported tooling.
- **Format and runtime compatibility:** check whether the model is provided
  for Transformers/PyTorch, GGUF/llama.cpp, GPTQ/AWQ, or another ecosystem.
  Choose a runtime that matches the artifact instead of assuming every Hub
  model works with the `transformers` pipeline.
- **License and usage restrictions:** read the license, acceptable-use terms,
  intended-use notes, and any restrictions on commercial or redistribution use.
- **Conversation template:** instruction-tuned models may require a chat
  template, special tokens, or a model-specific prompt format. Do not assume a
  base model behaves like a chat assistant.
- **Evidence and evaluation:** inspect benchmark definitions, limitations,
  known failure modes, context length, languages, and independent evaluations.
  Prefer task-specific tests in this repository over leaderboard ranking alone.
- **Revision and provenance:** record the model ID, revision or commit, source
  dataset information, quantization method, and date selected.

### A practical discovery workflow

1. Define the local task: generation, summarization, extraction, coding,
   embeddings, or classification.
2. Define the machine envelope: operating system, CPU/GPU, available RAM or
   VRAM, acceptable latency, context length, and whether network access is
   allowed.
3. Search the Hugging Face Hub for compatible task tags and inspect model-card
   metadata, files, license, and recent activity.
4. Shortlist a base or instruction-tuned model plus an appropriate quantized
   or runtime-specific variant.
5. Record a pinned revision and test prompts before using a model in an
   application.
6. Download to an explicit cache only when ready, then repeat tests with
   `local_files_only=True` to verify offline reproducibility.

For local LLMs, separate these decisions:

- **Model family:** the underlying pretrained or instruction-tuned checkpoint.
- **Variant:** parameter size, fine-tune, quantization, and context-window
  choice.
- **Runtime:** Transformers/PyTorch, llama.cpp, or another compatible engine.
- **Application adapter:** the narrow interface used by this repository.

Example discovery notes can be recorded before loading anything:

```text
Task: local text generation
Hardware: 16 GB system RAM, CPU-only
Runtime: Transformers/PyTorch
Candidate: <organization>/<model>
Revision: <commit or reviewed tag>
Format: safetensors or runtime-specific format
License: <reviewed license>
Offline cache: models/huggingface/
Evaluation prompts: tests/evals/<name>.json
```

Do not treat a model card as a guarantee of safety, factuality, or production
fitness. Validate outputs for the intended domain, protect prompts and
outputs that may contain sensitive data, and keep `trust_remote_code=False`
unless custom code has been reviewed. The repository's
[add-local-model skill](/Users/timothychin/PycharmProjects/local-ml-vibes/.claude/skills/add-local-model/SKILL.md)
contains the implementation checklist.

## Development

```bash
uv sync --dev
uv run pytest
```

The project follows a simple application boundary: production code belongs in
`src/`, tests mirror behavior in `tests/`, exploratory work belongs in
`examples/` or `scripts/`, and reusable workflows should be documented as
skills under `.claude/skills/`.
