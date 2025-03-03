import os
import duckdb

home_dir = os.path.expanduser("~")


def read_sql_file(path_to_file, git_root=None):
    git_root = git_root or ""
    path_to_file = os.path.join(git_root, path_to_file)
    with open(path_to_file, "r") as file:
        sql = file.read()
    return sql


def connect_to_db():
    try:
        with open(os.path.join(home_dir, ".motherduck_token")) as f:
            md_token = f.read()
    except Exception:
        md_token = os.getenv("MD_TOKEN")

    con = duckdb.connect(f"md:?motherduck_token={md_token.strip()}")
    return con
