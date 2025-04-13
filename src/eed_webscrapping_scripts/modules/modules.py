import copy
import os
from pathlib import Path

import dotenv
import duckdb
import git
from bs4 import BeautifulSoup

home_dir = os.path.expanduser("~")


def load_dotenv_(path_to_env: str = None, override=False) -> dict:
    if path_to_env is None:
        dotenv.load_dotenv()
        return None
    else:
        env_variables = dotenv.dotenv_values(path_to_env)
        for key, value in env_variables.items():
            if not override:
                if key in os.environ:
                    env_variables[key] = os.environ[key]
                else:
                    os.environ[key] = value
            else:
                os.environ[key] = value
        return env_variables


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
    if cfg["env"]["_ENVIRONMENT_"] == "PROD":  # TODO: ES-282 DWD anpasse
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


def save_webpage(page_source, path_to_file):
    soup = BeautifulSoup(page_source, "html.parser")
    prettyHTML = str(soup.prettify().encode("utf-8", "ignore"))
    with open(path_to_file, "w") as f:
        f.write(prettyHTML)
    return soup


def get_table_definition(
    table_name: str, cfg: dict, schema_name="datalake", database_name="pollenvorhersage"
) -> dict:
    """
    Retrieves the table definition from the configuration dictionary and constructs the full path for the table.

    Parameters:
    table_name (str): The name of the table to retrieve the definition for.
    cfg (dict): The configuration dictionary containing database, schema and table informations.
    schema_name (str, optional): The name of the schema. Default is "datalake".
    database_name (str, optional): The name of the database. Default is "pollenvorhersage".

    Returns:
    dict: The table definition dictionary with the full path included.
    """
    cfg_copy = copy.deepcopy(cfg)
    table_definition = cfg_copy[database_name]["db_infos"][schema_name]["tables"][table_name]
    schema_name_real = cfg_copy[database_name]["db_infos"][schema_name]["name"]
    table_definition["path"] = f"""{database_name}.{schema_name_real}.{table_definition["name"]}"""
    return table_definition
