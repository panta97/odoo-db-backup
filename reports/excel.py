import pandas as pd

# bundles = {df: df, sheet: sheet_name}
def dfs_excel(bundles, name):
    writer = pd.ExcelWriter("{}.xlsx".format(name), engine="xlsxwriter")
    for bundle in bundles:
        bundle["df"].to_excel(writer, sheet_name=bundle["sheet"], index=False)
    writer.save()


def df_excel(bundle, name):
    writer = pd.ExcelWriter("{}.xlsx".format(name), engine="xlsxwriter")
    bundle["df"].to_excel(writer, sheet_name=bundle["sheet"], index=False)
    writer.save()
