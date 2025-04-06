import os

import pytest

from eed_webscrapping_scripts.modules import get_git_root, load_dotenv_

git_root = get_git_root()


@pytest.mark.parametrize(
    "path_to_env, override, additional_env_var, env_variables_expected",
    [
        (git_root / "tests" / "modules" / ".env", False, None, {"TEST_VALUE": "TEST_VALUE"}),
        (
            git_root / "tests" / "modules" / ".env",
            False,
            {"TEST_VALUE": "123"},
            {"TEST_VALUE": "123"},
        ),
        (
            git_root / "tests" / "modules" / ".env",
            True,
            {"TEST_VALUE": "123"},
            {"TEST_VALUE": "TEST_VALUE"},
        ),
    ],
    ids=[
        "test if env gets set",
        "test if override=False is respected",
        "test if override=True is respected",
    ],
)
def test_load_dotenv_(
    path_to_env, override: bool, additional_env_var: dict, env_variables_expected: dict
):
    if additional_env_var is not None:
        for key, value in additional_env_var.items():
            os.environ[key] = value
    env_variables = load_dotenv_(path_to_env=path_to_env, override=override)
    TEST_VALUE = os.getenv("TEST_VALUE")
    TEST_VALUE_EXPECTED = env_variables_expected["TEST_VALUE"]
    assert TEST_VALUE == TEST_VALUE_EXPECTED and env_variables_expected == env_variables
