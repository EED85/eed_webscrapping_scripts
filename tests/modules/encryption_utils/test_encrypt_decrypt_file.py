import duckdb
import pytest

from eed_webscrapping_scripts.modules import decrypt_file, encrypt_file, get_git_root

path = get_git_root() / "tests" / "modules" / "encryption_utils"
file_path = path / "file_to_encrypt.txt"


@pytest.mark.parametrize(
    "file_path, file_path_out",
    [
        (file_path, None),
        (file_path, file_path),
        (str(file_path), str(file_path)),
    ],
    ids=[
        "overwrites file - file_path_out is None",
        "overwrites file - file_path_out is file_path",
        "overwrites file - file_path_out is file_path and both strings",
    ],
)
def test_encrypt_decrypt_file_pathlib(file_path, file_path_out):
    hash_01 = duckdb.sql(f"""SELECT HASH(content) FROM read_text('{file_path}')""").fetchall()[0][0]
    encrypt_file(file_path, file_path_out)
    decrypt_file(file_path, file_path_out)
    hash_02 = duckdb.sql(f"""SELECT HASH(content) FROM read_text('{file_path}')""").fetchall()[0][0]
    assert hash_01 == hash_02
