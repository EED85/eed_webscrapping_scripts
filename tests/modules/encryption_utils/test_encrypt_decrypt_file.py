import duckdb

from eed_webscrapping_scripts.modules import decrypt_file, encrypt_file, get_git_root

path = get_git_root() / "tests" / "modules" / "encryption_utils"
file = path / "file_to_encrypt.txt"


def test_encrypt_decrypt_file():
    hash_01 = duckdb.sql(f"""SELECT HASH(content) FROM read_text('{file}')""").fetchall()[0][0]
    encrypt_file(file)
    decrypt_file(file)
    hash_02 = duckdb.sql(f"""SELECT HASH(content) FROM read_text('{file}')""").fetchall()[0][0]
    assert hash_01 == hash_02
