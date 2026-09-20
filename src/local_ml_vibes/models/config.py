"""Configuration for an explicitly requested Hugging Face model load."""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ModelConfig:
    """Describe a model load without performing one."""

    repository_id: str
    revision: str | None = None
    cache_dir: Path | None = None
    local_files_only: bool = False
    device: str = "auto"
    torch_dtype: str | None = None
    trust_remote_code: bool = False

    def validate(self) -> None:
        """Reject ambiguous configuration before a runtime load is attempted."""

        if not self.repository_id.strip():
            raise ValueError("repository_id must not be empty")
        if self.local_files_only and self.cache_dir is None:
            raise ValueError(
                "cache_dir is required when local_files_only is enabled"
            )
