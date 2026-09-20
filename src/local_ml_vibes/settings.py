"""Small application settings boundary.

Keep environment-specific configuration outside model-loading code so model
adapters remain easy to test and reuse.
"""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    """Runtime paths and defaults for local development."""

    cache_dir: Path | None = None
    offline: bool = False
