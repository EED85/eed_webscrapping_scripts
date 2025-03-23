import os
from collections.abc import Iterator
from pathlib import Path

import pytest
import yaml

from eed_webscrapping_scripts.modules import get_encryption_pasword


# Fixture to use the mock_load_config function
@pytest.fixture
def patch_get_config_dwd(monkeypatch):
    def get_config_dwd_mock():
        with open(Path("tests") / "dwd" / "config.yaml") as file:
            return yaml.safe_load(file)

    monkeypatch.setattr("eed_webscrapping_scripts.dwd.get_config", get_config_dwd_mock)


@pytest.fixture
def cfg_test() -> Iterator[dict]:
    home_dir = os.path.expanduser("~")
    password = get_encryption_pasword()
    cfg_test = {
        "home_dir": home_dir,
        "encrytpion": {"password": password},
    }
    yield cfg_test
