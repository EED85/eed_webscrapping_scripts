import base64
import os
from pathlib import Path

import dotenv
import duckdb
import git
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# loading variables from .env file


home_dir = os.path.expanduser("~")


def load_dotenv_():
    dotenv.load_dotenv()


def read_sql_file(path_to_file: str, git_root: str = None) -> str:
    """_summary_

    Args:
        path_to_file (str): path to sql file, that shall be imported.
        git_root (str, optional): Will be joined with ``path_to_file``. Defaults to None.

    Returns:
        str: content of ``path_to_file``.
    """
    git_root = git_root or ""
    path_to_file = os.path.join(git_root, path_to_file)
    with open(path_to_file) as file:
        sql = file.read()
    return sql


def connect_to_db(cfg=None):
    """Connects to Motherduck database.
    Needs Github secret ``MD_TOKEN`` defined, if used in github Actions.
    Needs ``.motherduck_token`` file in your home directory.
    Returns:
        DuckDB / Motherduck connection:
    """
    if cfg["env"]["_ENVIRONMENT_"] == "GITHUB":
        try:
            with open(os.path.join(home_dir, ".motherduck_token")) as f:
                md_token = f.read()
        except Exception:
            md_token = os.getenv("MD_TOKEN")

        con = duckdb.connect(f"md:?motherduck_token={md_token.strip()}")
        print("Connected to Motherduck")
    else:
        con = duckdb.connect()
        con.sql("ATTACH ':memory:' AS dwd;")
        con.sql("USE dwd")
        print("Connected to in memory duckdb database")
    return con


def get_git_root(path=None):
    """_summary_

    Args:
        path (str / Path, optional): _description_. Defaults to cwd.
    Returns:
        Path: finds top level git repository path of input ``path``.
    """
    path = path or Path.cwd()
    git_repo = git.Repo(path, search_parent_directories=True)
    git_root = Path(git_repo.git.rev_parse("--show-toplevel"))
    return git_root


def get_encryption_pasword() -> str:
    """Reads password either from disk or from a github secret.

    Args:

    Returns:
        str: password -> use it in functions encrypt and decrypt
    """
    try:
        with open(os.path.join(home_dir, ".encryption_key")) as f:
            encryption_pasword = f.read()
    except Exception:
        encryption_pasword = os.getenv("ENCRYPTION_PASWORD")  # TODO
    return encryption_pasword


def get_encryption_salt() -> bytes:
    """Reads password either from disk or from a github secret.

    Args:

    Returns:
        str: password -> use it in functions encrypt and decrypt
    """
    try:
        with open(os.path.join(home_dir, ".encryption_salt")) as f:
            encryption_salt = f.read()
    except Exception:
        encryption_salt = os.getenv("ENCRYPTION_SALT")
    return bytes(encryption_salt, encoding="utf-8")


def generate_key(password: str) -> bytes:
    salt = get_encryption_salt()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=1_200_000,
    )
    password_kdf = kdf.derive(password.encode("utf-8"))
    key = base64.urlsafe_b64encode(password_kdf)

    return key


def encrypt(phrase: str, key) -> str:
    fernet = Fernet(key)
    enc_phrase = fernet.encrypt(phrase.encode())
    return enc_phrase


def decrypt(enc_phrase: str, key, encoding: str = "utf-8") -> str:
    fernet = Fernet(key)
    phrase = fernet.decrypt(enc_phrase)
    return phrase.decode(encoding)


if __name__ == "__main__":
    encryptd_phrase = encrypt("123", generate_key(get_encryption_pasword()))
    pass
