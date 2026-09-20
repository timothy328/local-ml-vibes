# Generate a Lightweight SWE Repository

Create or extend a small software-engineering repository for local machine
learning without adding unnecessary framework complexity.

## Required structure

- Use `src/<package_name>/` for importable application code.
- Use `tests/` for focused automated tests.
- Use `examples/` or `scripts/` for exploratory or operational entry points.
- Add `README.md`, `.gitignore`, `.gitattributes`, `.python-version`, and
  `pyproject.toml` when starting a Python repository.
- Keep dependencies minimal and put optional heavyweight runtimes in an
  optional dependency group.

## Content requirements

- Document the repository purpose, structure, development commands, and
  boundaries between application code and experiments.
- Prefer small typed modules with explicit interfaces.
- Add tests for configuration and pure behavior without requiring model
  downloads, credentials, GPUs, or network access.
- Never commit model weights, secrets, generated data, or environment-specific
  artifacts.

## Validation

Run `git diff --check` and the repository's existing focused tests. Do not
download or load a model merely to validate the scaffold.
