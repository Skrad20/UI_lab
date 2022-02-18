import pandas as pd
from PyQt5.QtWidgets import QMessageBox

from func.func_answer_error import answer_error
from models.models import BullFather, ProfilsCows


def upload_data_farmers_father() -> set:
    res = []
    buses = BullFather.select()
    for bus in buses:
        if bus.farm in res:
            pass
        else:
            res.append(bus.farm)
    res_set = set(res)
    return res_set


def save_bus_data(dt_in: dict) -> None:
    """Сохраняет данные по коровам в базу"""
    query = ProfilsCows.select().where(
        ProfilsCows.number == dt_in.get("number_animal")
    )
    try:
        if query.exists():
            print(dt_in.get("number_animal"), 'существует.')
        else:
            pc = ProfilsCows(
                name=dt_in.get("name_animal", '-'),
                number=dt_in.get("number_animal", '-'),
                farm=dt_in.get("hosbut", '-'),
                BM1818=dt_in.get("BM1818", '-'),
                BM1824=dt_in.get("BM1824", '-'),
                BM2113=dt_in.get("BM2113", '-'),
                CSRM60=dt_in.get("CSRM60", '-'),
                CSSM66=dt_in.get("CSSM66", '-'),
                CYP21=dt_in.get("CYP21", '-'),
                ETH10=dt_in.get("ETH10", '-'),
                ETH225=dt_in.get("ETH225", '-'),
                ETH3=dt_in.get("ETH3", '-'),
                ILSTS6=dt_in.get("ILSTS6", '-'),
                INRA023=dt_in.get("INRA023", '-'),
                RM067=dt_in.get("RM067", '-'),
                SPS115=dt_in.get("SPS115", '-'),
                TGLA122=dt_in.get("TGLA122", '-'),
                TGLA126=dt_in.get("TGLA126", '-'),
                TGLA227=dt_in.get("TGLA227", '-'),
                TGLA53=dt_in.get("TGLA53", '-'),
                MGTG4B=dt_in.get("MGTG4B", '-'),
                SPS113=dt_in.get("SPS113", '-'),
            )
            pc.save()
    except Exception as e:
        name = '\ndb_job.py\nsave_bus_data\n'
        QMessageBox.critical(
            None,
            'Ошибка ввода',
            f'{answer_error()} {name} Подробности:\n {e}'
        )


def save_bus_data_fater(data_job: pd.DataFrame) -> None:
    """Сохраняет данные по быкам в базу"""
    try:
        pc = BullFather(
            name=data_job.loc[0, "Имя"],
            number=data_job.loc[0, "Инвертарный номер"],
            farm=data_job.loc[0, "Хозяйство"],
            BM1818=data_job.loc[0, "BM1818"],
            BM1824=data_job.loc[0, "BM1824"],
            BM2113=data_job.loc[0, "BM2113"],
            CSRM60=data_job.loc[0, "CSRM60"],
            CSSM66=data_job.loc[0, "CSSM66"],
            CYP21=data_job.loc[0, "CYP21"],
            ETH10=data_job.loc[0, "ETH10"],
            ETH225=data_job.loc[0, "ETH225"],
            ETH3=data_job.loc[0, "ETH3"],
            ILSTS6=data_job.loc[0, "ILSTS6"],
            INRA023=data_job.loc[0, "INRA023"],
            RM067=data_job.loc[0, "RM067"],
            SPS115=data_job.loc[0, "SPS115"],
            TGLA122=data_job.loc[0, "TGLA122"],
            TGLA126=data_job.loc[0, "TGLA126"],
            TGLA227=data_job.loc[0, "TGLA227"],
            TGLA53=data_job.loc[0, "TGLA53"],
            MGTG4B=data_job.loc[0, "MGTG4B"],
            SPS113=data_job.loc[0, "SPS113"],
        )
        pc.save()
    except Exception as e:
        name = '\ndb_job.py\nsave_bus_data_fater\n '
        QMessageBox.critical(
            None,
            'Ошибка ввода',
            (f'{answer_error()} {name}Подробности:\n {e}')
            )


def upload_fater_data(number: int) -> dict:
    """Загружает данные по отцу из базы"""
    try:
        query = BullFather.select().where(
            BullFather.number == number
        )
        if query.exists():
            bus = BullFather.select().where(
                BullFather.number == number
            ).get()
            res = {
                "BM1818_father": bus.BM1818,
                "BM1824_father": bus.BM1824,
                "BM2113_father": bus.BM2113,
                "CSRM60_father": bus.CSRM60,
                "CSSM66_father": bus.CSSM66,
                "CYP21_father": bus.CYP21,
                "ETH10_father": bus.ETH10,
                "ETH225_father": bus.ETH225,
                "ETH3_father": bus.ETH3,
                "ILSTS6_father": bus.ILSTS6,
                "INRA023_father": bus.INRA023,
                "RM067_father": bus.RM067,
                "SPS115_father": bus.SPS115,
                "TGLA122_father": bus.TGLA122,
                "TGLA126_father": bus.TGLA126,
                "TGLA227_father": bus.TGLA227,
                "TGLA53_father": bus.TGLA53,
                "MGTG4B_father": bus.MGTG4B,
                "SPS113_father": bus.SPS113,
            }
            return res
        else:
            res = {
                "BM1818_father": '-',
                "BM1824_father": '-',
                "BM2113_father": '-',
                "CSRM60_father": '-',
                "CSSM66_father": '-',
                "CYP21_father": '-',
                "ETH10_father": '-',
                "ETH225_father": '-',
                "ETH3_father": '-',
                "ILSTS6_father": '-',
                "INRA023_father": '-',
                "RM067_father": '-',
                "SPS115_father": '-',
                "TGLA122_father": '-',
                "TGLA126_father": '-',
                "TGLA227_father": '-',
                "TGLA53_father": '-',
                "MGTG4B_father": '-',
                "SPS113_father": '-',
            }
            return res
    except Exception as e:
        name = '\njob_db.py\nupload_bus_data\n'
        QMessageBox.critical(
            None,
            'Ошибка ввода',
            f'{answer_error()}{name}Подробности:\n {e}'
        )


def upload_bus_data(number: int) -> dict:
    """Загружает данные по матерям из базы"""
    try:
        query = ProfilsCows.select().where(
            ProfilsCows.number == number
        )
        if query.exists():
            bus = ProfilsCows.select().where(
                ProfilsCows.number == number
            ).get()
            res = {
                "BM1818_mutter": bus.BM1818,
                "BM1824_mutter": bus.BM1824,
                "BM2113_mutter": bus.BM2113,
                "CSRM60_mutter": bus.CSRM60,
                "CSSM66_mutter": bus.CSSM66,
                "CYP21_mutter": bus.CYP21,
                "ETH10_mutter": bus.ETH10,
                "ETH225_mutter": bus.ETH225,
                "ETH3_mutter": bus.ETH3,
                "ILSTS6_mutter": bus.ILSTS6,
                "INRA023_mutter": bus.INRA023,
                "RM067_mutter": bus.RM067,
                "SPS115_mutter": bus.SPS115,
                "TGLA122_mutter": bus.TGLA122,
                "TGLA126_mutter": bus.TGLA126,
                "TGLA227_mutter": bus.TGLA227,
                "TGLA53_mutter": bus.TGLA53,
                "MGTG4B_mutter": bus.MGTG4B,
                "SPS113_mutter": bus.SPS113,
            }
            return res
        else:
            res = {
                "BM1818_mutter": '-',
                "BM1824_mutter": '-',
                "BM2113_mutter": '-',
                "CSRM60_mutter": '-',
                "CSSM66_mutter": '-',
                "CYP21_mutter": '-',
                "ETH10_mutter": '-',
                "ETH225_mutter": '-',
                "ETH3_mutter": '-',
                "ILSTS6_mutter": '-',
                "INRA023_mutter": '-',
                "RM067_mutter": '-',
                "SPS115_mutter": '-',
                "TGLA122_mutter": '-',
                "TGLA126_mutter": '-',
                "TGLA227_mutter": '-',
                "TGLA53_mutter": '-',
                "MGTG4B_mutter": '-',
                "SPS113_mutter": '-',
            }
            return res
    except Exception as e:
        name = '\njob_db.py\nupload_bus_data\n'
        QMessageBox.critical(
            None,
            'Ошибка ввода',
            f'{answer_error()}{name}Подробности:\n {e}'
        )


def create_columns_name(row):
    name = row['name']
    number = row['number']
    return f"{name} {number}"


def upload_data_db_for_searh_father():
    """Загружает данные по отцам из базы для поиска."""
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
    """Загружает данные по отцам из базы для паспартов."""
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
