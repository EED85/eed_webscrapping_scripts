import os

from eed_webscrapping_scripts.modules import get_git_root, load_dotenv_


def test_load_dotenv_():
    git_root = get_git_root()
    path_to_env = git_root / "tests" / "modules" / ".env"
    load_dotenv_(path_to_env=path_to_env)
    TEST_VALUE = os.getenv("TEST_VALUE")
    assert TEST_VALUE == "TEST_VALUE"
