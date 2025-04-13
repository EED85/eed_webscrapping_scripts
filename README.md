# eed_webscrapping_scripts
Repository for ingesting public data into a database and performing basic data transformations.

## DWD

### Pollenflug Gefahrenindex
Data is collected daily via GitHub Actions and stored in a private database for non-commercial and personal use only.


#### running the script
To run the script, use:
`uv run rc/eed_webscrapping_scripts/main.py`
Please note, that the programm runs locally, the data is not stored in motherduck, only in a local in memory duckdb database.

## Pollenvorhersage
For personal use only.

### fetch and store html

fetches and stores html in Motherduck for various zip codes in Germany. Needs to executed manually.
Please note that all the url and the scrapped zip codes are encrypted. The programm can only be executed as Repository-Owner.

#### running the script

```python
from eed_webscrapping_scripts.pollenvorhersage.pollenvorhersage import PollenvorhersageHandler
pollenvorhersage_handler = PollenvorhersageHandler()
con = pollenvorhersage_handler.fetch_and_store_html()
```

## Developement
To install the repository, follow these steps:
```shell
gh repo clone EED85/eed_webscrapping_scripts
uv venv .venv
uv pip install e .
uvx pre-commit install
```

Please ensure to create a pull request before making any changes.

## Pipelines

### ruff
runs on every commit and fails, if code is not well formated

### pytests
runs on every commit and fails, if any pytest fails

### create views on release
When a tag is pushed to the main master, then all database views are beeing recreated.

### daily scrapping
runs daily main.py and scrappes data

#### Developement
add if: github.ref == 'refs/heads/master' # TODO for developement issues - remove before merge in master
before step Checkout latest release for developement puposese

