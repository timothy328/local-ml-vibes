# Add a Local Hugging Face Model Adapter

Add scaffolding for an explicitly requested Hugging Face model without
downloading weights or loading a model during generation.

## Required approach

1. Put model identifiers, revisions, cache paths, offline behavior, device,
   dtype, and remote-code policy in a typed configuration object.
2. Validate configuration before importing runtime libraries.
3. Keep `transformers` and `torch` optional unless the repository already
   requires them.
4. Import optional runtime dependencies inside the explicit loader function.
5. Expose a narrow application-facing interface instead of leaking pipeline
   details throughout the codebase.
6. Keep model artifacts and credentials out of Git.

## Safety and reproducibility

- Default to `trust_remote_code=False`.
- Support pinned revisions and `local_files_only=True`.
- Make cache directories explicit.
- Surface missing dependencies and invalid configuration as actionable errors.
- Do not hide downloads, network access, or model initialization in imports,
  constructors, tests, or package setup.

## Validation

Test configuration and validation paths only. A successful scaffold check must
not call a Hugging Face endpoint, download weights, initialize a tokenizer, or
load a model.
