import pandas as pd
import requests
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import QMessageBox

from func.func_answer_error import answer_error
from code_app.models import BullFather

from .db_job import upload_data_db_for_creat_pass
import logging
from logging.handlers import RotatingFileHandler


logFile = "./logs/log_preprocessor_ms_data.log"
logging.basicConfig(
    filename=logFile,
    level=logging.DEBUG,
    filemode='w',
)
my_handler = RotatingFileHandler(
    logFile, mode='a', maxBytes=5*1024*1024,
    backupCount=2, encoding="cp1251", delay=0
)

logger = logging.getLogger(__name__)
logger.addHandler(my_handler)


def check_ms_in_cell(str_test):
    '''
    Возвращает булево значение содержит строка микросателлиты или нет.
    ----------------------
    Параметры:
        str_test (str): Тестовая строка данных с сайта
    ----------------------
    Возвращаемое значение:
        (bool): входит / не входит элемент в строку
    '''
    msatle = [
        'BM1818', 'BM1824',
        'BM2113', 'CSRM60', 'CSSM66',
        'CYP21', 'ETH10', 'ETH225',
        'ETH3', 'ILSTS6', 'INRA023',
        'RM067', 'SPS115', 'TGLA122',
        'TGLA126', 'TGLA227', 'TGLA53',
        'MGTG4B', 'SPS113'
    ]
    for col in msatle:
        if col in str_test:
            return True
    return False


def add_missing(df: pd.DataFrame, farm: str) -> pd.DataFrame:
    """
    Возращает датасет с быками.
    Проверяет наличие быков в базе. При необходимости добавляет.
    ----------------------
    Параметры:
        df (pd.DataFrame): датасет по описи нетелей.
        farm (str): название хозяйства.
    ----------------------
    Возвращаемое значение:
        df (pd.DataFrame): датасет по микросателлитам быков.
    """
    logger.debug("Start add_missing")
    logger.debug(df.head())
    df = df.dropna(subset=["number_father"])
    logger.debug("After dropna")
    logger.debug(df.head())
    try:
        df_dad = upload_data_db_for_creat_pass()
        list_father_db = df_dad.number
        list_father_invert = df["number_father"]
        for number in set(list_father_invert):
            if number in list_father_db:
                pass
            else:
                logger.debug(
                    f"Number father {number}"
                )
                name = (
                    df[df["number_father"] == number]["name_father"]
                    .reset_index(drop=True)[0]
                )
                if 1 == parser_ms_dad(number, name, farm):
                    print('Не добавлено')
                else:
                    print(f"Добавлен {number}")
        logger.debug("End add_missing")
        return upload_data_db_for_creat_pass()
    except Exception as e:
        logger.error(e)
        name = '\nparser_def.py.py\nadd_missing\n'
        QMessageBox.critical(
            None,
            'Ошибка ввода',
            (f'{answer_error()}{name}Подробности:\n {e}')
        )
        logger.debug("End add_missing")


def parser_ms_dad(number: int, name: str, farm: str) -> int:
    """
    Парсит и сохраняет данные в базу по быкам.
    ----------------------
    Параметры:
        number (int): инвентарный номер быка.
        name (str): кличка быка.
        farm (str): название предприятия.
    ----------------------
    Возвращаемое значение:
        res (bool): 0/1, 1 - ошибка.
    """
    try:
        print(number)
        query = BullFather.select().where(
            BullFather.number == number,
            BullFather.farm == farm
        )
        if query.exists():
            return 1
        number_page, token = filter_id_bus(str(number), name)
        df = parser_ms(number_page, token)
        i = 0
        df = df.reset_index(drop=True)

        if df.iloc[0, 0] != 1:
            bus = BullFather(
                name=name,
                number=number,
                farm=farm,
                BM1818=df.loc[i, "BM1818"],
                BM1824=df.loc[i, "BM1824"],
                BM2113=df.loc[i, "BM2113"],
                CSRM60=df.loc[i, "CSRM60"],
                CSSM66=df.loc[i, "CSSM66"],
                CYP21=df.loc[i, "CYP21"],
                ETH10=df.loc[i, "ETH10"],
                ETH225=df.loc[i, "ETH225"],
                ETH3=df.loc[i, "ETH3"],
                ILSTS6=df.loc[i, "ILSTS6"],
                INRA023=df.loc[i, "INRA023"],
                RM067=df.loc[i, "RM067"],
                SPS115=df.loc[i, "SPS115"],
                TGLA122=df.loc[i, "TGLA122"],
                TGLA126=df.loc[i, "TGLA126"],
                TGLA227=df.loc[i, "TGLA227"],
                TGLA53=df.loc[i, "TGLA53"],
                MGTG4B=df.loc[i, "MGTG4B"],
                SPS113=df.loc[i, "SPS113"],
            )
            bus.save()
            return 0
        else:
            return 1
    except Exception as e:
        name = '\nparser_def.py.py\nparser_ms_dad\n'
        QMessageBox.critical(
            None,
            'Ошибка ввода',
            f'{answer_error()}{name} Подробности:\n {e}'
        )


def parser_ms(number_page, token):
    """
    Собирает и парсит данные по МС быков.
    ----------------------
    Параметры:
        number_page (int): номер страницы с данными о быке.
        token (str): токен авторизации.
    ----------------------
    Возвращаемое значение:
        df_out (pd.DataFrame): датасет с данными
            по микросателлитым быков.
    """
    try:
        url_2 = f"https://xn--90aof1e.xn--p1ai/bulls/bull/{number_page}?token={token}"
        response_page = requests.put(url_2)
        soup = BeautifulSoup(response_page.text, 'lxml')

        res = soup.find_all('div', attrs={'class': 'fl_l'})

        out_res = '6666666666666666666'
        for row in res:
            if check_ms_in_cell(str(row)):
                out_res = str(row)
        if out_res[0] != '6':
            out_res = out_res.split('<div class="fl_l">')[1]
            out_res = out_res.split('</div>')[0]
            res_split = out_res.split(', ')
            dict_res = {}
            for i in range(len(res_split)):
                out_split = res_split[i].split('_')
                dict_res[out_split[0]] = out_split[1]

            columns = [
                'BM1818', 'BM1824', 'BM2113', 'CSRM60', 'CSSM66',
                'CYP21', 'ETH10',
                'ETH225', 'ETH3', 'ILSTS6', 'INRA023', 'RM067',
                'SPS115',
                'TGLA122', 'TGLA126', 'TGLA227', 'TGLA53', 'MGTG4B', 'SPS113'
            ]
            df = pd.DataFrame(columns=columns, index=[1]).fillna('-')
            for key, value in dict_res.items():
                df.loc[1, key] = value
            return df
        else:
            df_out = pd.DataFrame(index=[0], columns=[0])
            df_out.iloc[0, 0] = 1
            return df_out
    except Exception as e:
        name = '\nparser_def.py.py\nparser_ms\n'
        QMessageBox.critical(
            None,
            'Ошибка ввода',
            (f'{answer_error()}{name} Подробности:\n {e}')
        )


def filter_id_bus(number: str, name: str = '') -> list:
    """
    Отфильтровывает данные с сайта быки.рф.
    Возращает номер страницы и токен авторизации.
    ----------------------
    Параметры:
        number (str): инвентарный номер быка.
    ----------------------
    Возвращаемое значение:
        number_page (int): номер страницы с данными о быке
        token (str): токен авторизации
    """
    try:
        params = [
            {"value": 0, "im": "Общая база быков", "field": "", "method": "data_base", "group": "", "ready": True},
            {"method": "page", "value": 1, "ready": True}, {"value": "1", "field": "typeSearch", "method": "radio", "ready": True},
            {"value": True, "field": "bull", "method": "checkbox", "group": "prizn", "ready": True},
            {"value": True, "field": "sperm", "method": "checkbox", "group": "prizn", "ready": True},
            {"value": True, "field": "parent", "method": "checkbox", "group": "prizn", "ready": True},
            {"value": number, "field": "ninv", "type": "string", "param": {"like": True}, "method": "line", "ready": True},
            {"value": [["CVM", "CV", "TV"], ["BLAD", "BT", "TL"], ["Brachyspina", "BY", "TY"], ["DUMPS", "DP", "TD"], ["Mulefoot", "MF", "TM"], ["FXID", "FXIDC", "FXIDF"], ["Citrullinemia", "CNC", "CNF"], ["PT", "PTC", "PTF"], ["DF", "DFC", "DFF"], ["D2", "D2C", "D2F"], ["IS", "ISC", "ISF"], ["BD", "BDC", "BDF"], ["FH2", "FH2C", "FH2F"], ["Weaver", "WC", "WFF"], ["SMA", "SMAC", "SMAF"], ["SAA", "SAAC", "SAAF"], ["SDM", "SDMC", "SDMF"], ["DW", "DWC", "DWF"], ["OS", "OSC", "OSF"], ["AM", "AMC", "AMF"], ["DM", "DMC", "DMF"], ["NH", "NHC", "NHF"], ["aMAN", "aMANC", "aMANF"], ["bMAN", "bMANC", "bMANF"], ["CM1", "CM1C", "CM1F"], ["CM2", "CM2C", "CM2F"], ["CTS", "CTSC", "CTSF"], ["[HAM", "HAMC", "HAMF"], ["AP", "APC", "APF"], ["CA", "CAC", "CAF"], ["IE", "IEC", "IEF"], ["HDZ", "HDZC", "HDZF"], ["PK", "PKC", "PKF"], ["HHT", "HHTC", "HHTF"], ["HI", "HIC", "HIF"], ["DD", "DDC", "DDF"], ["CC", "CCC", "CCF"], ["HY", "HYC", "HYF"], ["TH", "THC", "THF"], ["CP", "CPC", "CPF"], ["PHA", "PHAC", "PHAF"], ["NS", "NSC", "NSF"], ["ICM", "ICMC", "ICMF"], ["OH", "OHC", "OHF"], ["OD", "ODC", "ODF"], ["GC", "GCC", "GCF"], ["MSUD", "MSUDC", "MSUDF"], ["HP", "HPC", "HPF"], ["NCL", "NCLC", "NCLF"], ["NPD", "NPDC", "NPDF"], ["TP", "TPC", "TPF"], ["A", "A", "A*"], ["BMS", "BMSC", "BMSF"], ["HG", "HGC", "HGF"], ["PP", "POC", "POF"], ["Pp", "POS", "POF"], ["Черн. окрас", "BC", "BF"], ["Красн. окрас", "RC", "RF"], ["POR", "POR"], ["RTF", "RTF"]], "method": "anomaly", "ready": True},
            {"method": "order", "data": {}},
            {"method": "token", "data": ""},
            {"method": "radio", "value": 1, "field": "typeSearch", "ready": True}
        ]

        url = 'https://xn--90aof1e.xn--p1ai/api/filter/1'

        response = requests.put(url, json=params)
        count = 0
        token = response.json().get('token')

        while len(response.json().get('idArray')) > count:
            number_page = response.json().get('idArray')[count]
            nickname = response.json().get('data')[count].get("klichka")
            print(nickname, name, nickname == name, nickname.lower() == name.lower())
            if nickname.lower().strip() == name.lower().strip():
                return number_page, token
            count += 1

        return -1, token
    except Exception as e:
        name = '\nparser_def.py.py\nfilter_id_bus\n '
        QMessageBox.critical(
            None,
            'Ошибка ввода',
            (f'{answer_error()}{name}Подробности:\n {e}')
        )


if __name__ == "__main__":
    text = "<div class=\"fl_l\">BM1824_180/182,</div>"
    print(check_ms_in_cell(text))
