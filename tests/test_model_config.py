from pathlib import Path

import pytest

from local_ml_vibes.models.config import ModelConfig


def test_model_config_does_not_load_a_model() -> None:
    config = ModelConfig(
        repository_id="example/model",
        cache_dir=Path("models"),
        local_files_only=True,
    )

    config.validate()


def test_local_only_configuration_requires_a_cache_directory() -> None:
    config = ModelConfig(
        repository_id="example/model",
        local_files_only=True,
    )

    with pytest.raises(ValueError, match="cache_dir"):
        config.validate()
