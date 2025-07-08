import pathlib
import tempfile

import pytest

from eed_webscrapping_scripts.eed_basic_utils import file_exists


@pytest.mark.parametrize(
    "file_path, expected",
    [
        ("existing_file.txt", True),
        ("non_existing_file.txt", False),
        (pathlib.Path("existing_file.txt"), True),
        (pathlib.Path("non_existing_file.txt"), False),
    ],
    ids=[
        "existing_file_str",
        "non_existing_file_str",
        "existing_file_pathlib",
        "non_existing_file_pathlib",
    ],
)
def test_file_exists_standard_cases(prepare_files, file_path, expected):
    tempdir = pathlib.Path(tempfile.gettempdir())
    full_file_path = tempdir / file_path
    if isinstance(file_path, str):
        full_file_path = str(full_file_path)
    file_does_exist = file_exists(full_file_path)
    assert file_does_exist == expected
