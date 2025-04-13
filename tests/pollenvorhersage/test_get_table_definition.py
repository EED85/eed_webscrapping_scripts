import pytest

from eed_webscrapping_scripts.modules import get_table_definition
from eed_webscrapping_scripts.pollenvorhersage import get_config


@pytest.mark.parametrize(
    "database_name,schema_name, table_name, path_expected",
    [
        ("pollenvorhersage", "datalake", "webpages", "pollenvorhersage.datalake.webpages"),
        (
            "pollenvorhersage",
            "information_layer",
            "pollenflug_vorhersage",
            "pollenvorhersage.information_layer.pollenflug_vorhersage",
        ),
    ],
    ids=["datalake.webpages", "information_layer.pollenflug_vorhersage"],
)
def test_get_table_definition(database_name, schema_name, table_name, path_expected):
    cfg = get_config()
    table_definition = get_table_definition(
        table_name, cfg, schema_name=schema_name, database_name=database_name
    )
    assert table_definition["path"] == path_expected
