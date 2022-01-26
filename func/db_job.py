import pandas as pd

from models.models import BullFather
from setting import DB as db


def create_columns_name(row):
    name = row['name']
    number = row['number']
    return f"{name} {number}"


def upload_data_db_for_searh_father():
    list_col = [
        'name', 'number', 'farm', 'BM1818', 'BM1824',
        'BM2113', 'CSRM60', 'CSSM66', 'CYP21', 'ETH10',
        'ETH225', 'ETH3', 'ILSTS6', 'INRA023', 'RM067',
        'SPS115', 'TGLA122', 'TGLA126', 'TGLA227', 'TGLA53',
        'MGTG4B', 'SPS113'
    ]
    df = pd.DataFrame(columns=list_col)
    i = 0
    for bus in BullFather.select():
        df.loc[i, "name"] = bus.name
        df.loc[i, "number"] = bus.number
        df.loc[i, "farm"] = bus.farm
        df.loc[i, "BM1818"] = bus.BM1818
        df.loc[i, "BM1824"] = bus.BM1824
        df.loc[i, "BM2113"] = bus.BM2113
        df.loc[i, "CSRM60"] = bus.CSRM60
        df.loc[i, "CSSM66"] = bus.CSSM66
        df.loc[i, "CYP21"] = bus.CYP21
        df.loc[i, "ETH10"] = bus.ETH10
        df.loc[i, "ETH225"] = bus.ETH225
        df.loc[i, "ETH3"] = bus.ETH3
        df.loc[i, "ILSTS6"] = bus.ILSTS6
        df.loc[i, "INRA023"] = bus.INRA023
        df.loc[i, "RM067"] = bus.RM067
        df.loc[i, "SPS115"] = bus.SPS115
        df.loc[i, "TGLA122"] = bus.TGLA122
        df.loc[i, "TGLA126"] = bus.TGLA126
        df.loc[i, "TGLA227"] = bus.TGLA227
        df.loc[i, "TGLA53"] = bus.TGLA53
        df.loc[i, "MGTG4B"] = bus.MGTG4B
        df.loc[i, "SPS113"] = bus.SPS113
        i += 1
    return df


def upload_data_db_for_creat_pass():
    list_col = [
        'name', 'number', 'name_number', 'BM1818', 'BM1824',
        'BM2113', 'CSRM60', 'CSSM66', 'CYP21', 'ETH10',
        'ETH225', 'ETH3', 'ILSTS6', 'INRA023', 'RM067',
        'SPS115', 'TGLA122', 'TGLA126', 'TGLA227', 'TGLA53',
        'MGTG4B', 'SPS113'
    ]
    df = pd.DataFrame(columns=list_col)
    i = 0
    for bus in BullFather.select():
        df.loc[i, "name"] = bus.name
        df.loc[i, "number"] = bus.number
        df.loc[i, "BM1818"] = bus.BM1818
        df.loc[i, "BM1824"] = bus.BM1824
        df.loc[i, "BM2113"] = bus.BM2113
        df.loc[i, "CSRM60"] = bus.CSRM60
        df.loc[i, "CSSM66"] = bus.CSSM66
        df.loc[i, "CYP21"] = bus.CYP21
        df.loc[i, "ETH10"] = bus.ETH10
        df.loc[i, "ETH225"] = bus.ETH225
        df.loc[i, "ETH3"] = bus.ETH3
        df.loc[i, "ILSTS6"] = bus.ILSTS6
        df.loc[i, "INRA023"] = bus.INRA023
        df.loc[i, "RM067"] = bus.RM067
        df.loc[i, "SPS115"] = bus.SPS115
        df.loc[i, "TGLA122"] = bus.TGLA122
        df.loc[i, "TGLA126"] = bus.TGLA126
        df.loc[i, "TGLA227"] = bus.TGLA227
        df.loc[i, "TGLA53"] = bus.TGLA53
        df.loc[i, "MGTG4B"] = bus.MGTG4B
        df.loc[i, "SPS113"] = bus.SPS113
        i += 1
    df.name_number = df.apply(create_columns_name, axis=1)
    df.index = df.number
    df.number = df.number.astype('float')
    return df


if __name__ == '__main__':
    print((upload_data_db_for_creat_pass()).head())
