from eed_webscrapping_scripts.dwd import get_config, prepare_db
from eed_webscrapping_scripts.modules import read_sql_file


def create_views():
    cfg = get_config()
    datalake = cfg["pollenflug_gefahrenindex"]["db_infos"]["datalake"]
    sql = read_sql_file("dwd\sqls\list_available_tables.sql", cfg["git_root"])
    con = prepare_db()
    _tables = con.sql(sql).fetchall()
    tables = [item[0] for item in _tables]
    sql_union_view_base = " UNION BY NAME ".join(
        [f"SELECT *, '{table}' AS _table_ FROM {datalake}.{table}" for table in tables]
    )
    sql_union_view = f"CREATE OR REPLACE VIEW {datalake}.Pollenflug_Gefahrenindex AS ({sql_union_view_base})"
    con.sql(sql_union_view)


if __name__ == "__main__":
    create_views()
