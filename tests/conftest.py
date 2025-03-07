from pathlib import Path

import pytest
import yaml


# Fixture to use the mock_load_config function
@pytest.fixture
def patch_get_config_dwd(monkeypatch):
    def get_config_dwd_mock():
        with open(Path("tests") / "dwd" / "config.yaml") as file:
            return yaml.safe_load(file)

    monkeypatch.setattr("eed_webscrapping_scripts.dwd.get_config", get_config_dwd_mock)
