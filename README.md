# eed_webscrapping_scripts
Repository for ingesting public data into a database and performing basic data transformations.

## DWD

### Pollenflug Gefahrenindex
Data is collected daily via GitHub Actions and stored in a private database for non-commercial and personal use only.


## running the script
To run the script, use:
`uv run rc/eed_webscrapping_scripts/main.py`

## Developement
To install the repository, follow these steps:
```shell
gh repo clone EED85/eed_webscrapping_scripts
uv venv .venv
uv pip install e .
uvx pre-commit install
```
Please ensure to create a pull request before making any changes
