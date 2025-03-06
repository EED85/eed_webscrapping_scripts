import os

import duckdb

home_dir = os.path.expanduser("~")


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
