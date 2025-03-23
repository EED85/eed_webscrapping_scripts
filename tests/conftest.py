import os
from pathlib import Path

import pytest
import yaml

from eed_webscrapping_scripts.modules import generate_key, get_encryption_pasword


# Fixture to use the mock_load_config function
@pytest.fixture
def patch_get_config_dwd(monkeypatch):
    def get_config_dwd_mock():
        with open(Path("tests") / "dwd" / "config.yaml") as file:
            return yaml.safe_load(file)

    monkeypatch.setattr("eed_webscrapping_scripts.dwd.get_config", get_config_dwd_mock)


def get_encryption_result(home_dir) -> bytes:
    """Reads password either from disk or from a github secret.

    Args:

    Returns:
        str: password -> use it in functions encrypt and decrypt
    """
    try:
        with open(os.path.join(home_dir, ".encryption_result")) as f:
            encryption_result = f.read()
    except Exception:
        encryption_result = os.getenv("ENCRYPTION_RESULT")  # TODO
    return encryption_result.encode()


@pytest.fixture
def cfg_test():
    home_dir = os.path.expanduser("~")
    password = get_encryption_pasword()
    key = generate_key(password)
    encryption_result = get_encryption_result(home_dir)
    cfg_test = {
        "home_dir": home_dir,
        "encrytpion": {"password": password, "key": key, "result": encryption_result},
    }
    yield cfg_test
