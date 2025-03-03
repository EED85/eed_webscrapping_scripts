from eed_webscrapping_scripts.dwd import get_config, prepare_db
from eed_webscrapping_scripts.modules import read_sql_file
from pathlib import Path


def create_views():
    cfg = get_config()
    information_layer = cfg["pollenflug_gefahrenindex"]["db_infos"]["information_layer"]
    con = prepare_db()

    # create views for information layer
    try:
        sql = read_sql_file(
            Path("dwd", "sqls", "information_layer_view_01_base.sql"), cfg["git_root"]
        )
        sql_view = f"CREATE OR REPLACE VIEW {information_layer}.Pollenflug_Gefahrenindex_01_base AS ({sql})"
        con.sql(sql_view)

        sql = read_sql_file(
            Path("dwd", "sqls", "information_layer_view_02.sql"), cfg["git_root"]
        )
        sql_view = f"CREATE OR REPLACE VIEW {information_layer}.Pollenflug_Gefahrenindex_02 AS ({sql})"
        con.sql(sql_view)

        sql = read_sql_file(
            Path("dwd", "sqls", "information_layer_view_03_unpivot.sql"),
            cfg["git_root"],
        )
        sql_view = f"CREATE OR REPLACE VIEW {information_layer}.Pollenflug_Gefahrenindex_03_unpivot AS ({sql})"
        con.sql(sql_view)

        sql = read_sql_file(
            Path("dwd", "sqls", "information_layer_view_04_features.sql"),
            cfg["git_root"],
        )
        sql_view = f"CREATE OR REPLACE VIEW {information_layer}.Pollenflug_Gefahrenindex_04_features AS ({sql})"
        con.sql(sql_view)
    except Exception as error:
        print(error)
        raise SyntaxError("some SQL syntax failed")
    finally:
        con.close()


if __name__ == "__main__":
    create_views()
