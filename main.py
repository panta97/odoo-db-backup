import settings
from reports.connection import get_df
from reports.excel import dfs_excel, df_excel
from reports.clients.main import (
    cliente_puntos,
    cliente_compras,
    cliente_compras_all,
    cliente_descuentos,
    cliente_descuentos_all,
)
from reports.metas.main import metas as metas_query


def clientes():
    ab = "B001,B003,B004,B005,B006,BA01"
    sm = "B002,BA02"
    all = "B001,B002,B003,B004,B005,B006"

    series = ["B001", "B002", "B003", "B004", "B005", "B006"]
    series_grouped = [ab, sm, all]
    limit = 100
    bundle_cp = {"df": get_df(cliente_puntos(limit)), "sheet": "Hoja 1"}
    bundles_cd = []
    bundles_cc = []

    for serie in series:
        # format sql filter
        serie_formatted = "'{}'".format(serie)
        bundles_cd.append(
            {
                "df": get_df(cliente_descuentos(serie_formatted, limit)),
                "sheet": serie,
            }
        )
        bundles_cc.append(
            {
                "df": get_df(cliente_compras(serie_formatted, limit)),
                "sheet": serie,
            }
        )

    for serie in series_grouped:
        # format sql filter
        serie_formatted = serie.split(",")
        serie_formatted = list(map(lambda e: "'{}'".format(e), serie_formatted))
        serie_formatted = ",".join(serie_formatted)
        # format sheet name
        sheetname = serie
        if serie == ab:
            sheetname = "abtao"
        elif serie == sm:
            sheetname = "san martin"
        elif serie == all:
            sheetname = "todo"
        bundles_cd.append(
            {
                "df": get_df(cliente_descuentos_all(serie_formatted, limit)),
                "sheet": sheetname,
            }
        )
        bundles_cc.append(
            {
                "df": get_df(cliente_compras_all(serie_formatted, limit)),
                "sheet": sheetname,
            }
        )

    df_excel(bundle_cp, "PUNTOS POR CLIENTE")
    dfs_excel(bundles_cd, "DESCUENTOS POR CLIENTE")
    dfs_excel(bundles_cc, "COMPRAS POR CLIENTE")


def metas():
    poscats = ["CABALLERO", "DAMA", "NINO y HOME", "DEPORTIVO"]
    bundle = []
    for poscat in poscats:
        bundle.append({"df": get_df(metas_query(poscat, "AB")), "sheet": poscat})
    dfs_excel(bundle, "METAS")


if __name__ == "__main__":
    metas()
