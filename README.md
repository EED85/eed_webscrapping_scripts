# eed_webscrapping_scripts

## run the script
recommended python version 3.11, it is developed with it.
just use `uv run --python 3.11 main.py`

## Developement
Please install the repo
```shell
gh repo clone EED85/eed_webscrapping_scripts
uv venv .venv
uv pip install e .
uvx pre-commit install
```
Please always create a pr before making changes


## Details
Stores data abot pollenflug into database ``dwd.duckdb`` on Motherduck.
