import os
from pathlib import Path

import dotenv
import duckdb
import git

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


def connect_to_db():
    """Connects to Motherduck database.
    Needs Github secret ``MD_TOKEN`` defined, if used in github Actions.
    Needs ``.motherduck_token`` file in your home directory.
    Returns:
        DuckDB / Motherduck connection:
    """
    try:
        with open(os.path.join(home_dir, ".motherduck_token")) as f:
            md_token = f.read()
    except Exception:
        md_token = os.getenv("MD_TOKEN")

    con = duckdb.connect(f"md:?motherduck_token={md_token.strip()}")
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
