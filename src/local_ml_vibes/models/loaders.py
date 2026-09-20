"""Optional Hugging Face loading boundary.

Importing this module does not import Transformers, download files, or load a
model. The optional dependency is imported only when a caller explicitly
invokes a loader.
"""

from collections.abc import Callable
from typing import Any

from .config import ModelConfig


def load_text_generator(config: ModelConfig) -> Callable[[str], str]:
    """Load a text-generation pipeline only when explicitly requested.

    This function is scaffolding for local use: it performs no work until
    called. The caller must install the optional ``models`` dependency group.
    """

    config.validate()

    try:
        from transformers import pipeline
    except ImportError as error:
        raise RuntimeError(
            "Install optional model dependencies with `uv sync --extra models`."
        ) from error

    pipeline_kwargs: dict[str, Any] = {
        "model": config.repository_id,
        "revision": config.revision,
        "cache_dir": str(config.cache_dir) if config.cache_dir else None,
        "local_files_only": config.local_files_only,
        "trust_remote_code": config.trust_remote_code,
    }
    if config.device != "auto":
        pipeline_kwargs["device"] = config.device
    if config.torch_dtype is not None:
        pipeline_kwargs["torch_dtype"] = config.torch_dtype

    generator = pipeline("text-generation", **pipeline_kwargs)

    def generate(prompt: str) -> str:
        """Generate one text continuation from a prompt."""

        outputs = generator(prompt, max_new_tokens=128)
        return str(outputs[0]["generated_text"])

    return generate
