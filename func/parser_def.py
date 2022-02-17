import pandas as pd
import requests
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import QMessageBox

from func.func_answer_error import answer_error
from models.models import BullFather
from setting import DB as db

from .db_job import upload_data_db_for_creat_pass


def add_missing(df: pd.DataFrame, farm: str) -> pd.DataFrame:
    """Добавляет данные по отцам"""
    try:
        df_dad = upload_data_db_for_creat_pass()
        list_father_db = df_dad.number
        list_father_invert = df[df.columns[5]]
        for number in list_father_invert:
            if number in list_father_db:
                pass
            else:
                name = (
                    df[df[df.columns[5]] == number][df.columns[6]]
                    .reset_index(drop=True)[0]
                )
                if 1 == parser_ms_dad(number, name, farm):
                    print('Не добавлено')
                else:
                    print(f"Добавлен {number}")
        return upload_data_db_for_creat_pass()
    except Exception as e:
        QMessageBox.critical(
            None,
            'Ошибка ввода',
            (f'{answer_error()}\nparser_def.py.py\nadd_missing\n Подробности:\n {e}')
        )


def parser_ms_dad(number: int, name: str, farm: str) -> int:
    """Парсит и сохраняет данные в базу по быкам"""
    try:
        print(number)
        number_page, token = filter_id_bus(str(number))
        df = parser_ms(number_page, token)
        i = 0
        df = df.reset_index(drop=True)
        query = BullFather.select().where(
            BullFather.number == number
        )

        if df.iloc[0, 0] != 1 and query.exists():
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
        QMessageBox.critical(
            None,
            'Ошибка ввода',
            (f'{answer_error()}\nparser_def.py.py\nparser_ms_dad\n Подробности:\n {e}')
        )


def parser_ms(number_page, token):
    """Собирает и парсит данные по МС быков"""
    try:
        url_2 = f"https://xn--90aof1e.xn--p1ai/bulls/bull/{number_page}?token={token}"
        response_page = requests.put(url_2)
        soup = BeautifulSoup(response_page.text, 'lxml')

        res = soup.find_all('div', attrs={'class': 'fl_l'})
        out_res = '6666666666666666666'
        for row in res:
            if (
                str(row)[18:24] == "BM1818" or
                str(row)[18:24] == "BM1824" or
                str(row)[18:24] == "BM2113" or
                str(row)[18:24] == "ETH225" or
                str(row)[18:24] == "SPS113" or
                str(row)[18:24] == "TGLA53"
            ):
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
                'BM1818', 'BM1824', 'BM2113', 'CSRM60', 'CSSM66', 'CYP21', 'ETH10',
                'ETH225', 'ETH3', 'ILSTS6', 'INRA023', 'RM067', 'SPS115', 
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
        QMessageBox.critical(
            None,
            'Ошибка ввода',
            (f'{answer_error()}\nparser_def.py.py\nparser_ms\n Подробности:\n {e}')
        )


def filter_id_bus(number: str) -> list:
    try:
        params = [
            {"value":0,"im":"Общая база быков","field":"","method":"data_base","group":"","ready":True},
            {"method":"page","value":1,"ready":True},{"value":"1","field":"typeSearch","method":"radio","ready":True},
            {"value":True,"field":"bull","method":"checkbox","group":"prizn","ready":True},
            {"value":True,"field":"sperm","method":"checkbox","group":"prizn","ready":True},
            {"value":True,"field":"parent","method":"checkbox","group":"prizn","ready":True},
            {"value":number,"field":"ninv","type":"string","param":{"like":False},"method":"line","ready":True},
            {"value":[["CVM","CV","TV"],["BLAD","BT","TL"],["Brachyspina","BY","TY"],["DUMPS","DP","TD"],["Mulefoot","MF","TM"],["FXID","FXIDC","FXIDF"],["Citrullinemia","CNC","CNF"],["PT","PTC","PTF"],["DF","DFC","DFF"],["D2","D2C","D2F"],["IS","ISC","ISF"],["BD","BDC","BDF"],["FH2","FH2C","FH2F"],["Weaver","WC","WFF"],["SMA","SMAC","SMAF"],["SAA","SAAC","SAAF"],["SDM","SDMC","SDMF"],["DW","DWC","DWF"],["OS","OSC","OSF"],["AM","AMC","AMF"],["DM","DMC","DMF"],["NH","NHC","NHF"],["aMAN","aMANC","aMANF"],["bMAN","bMANC","bMANF"],["CM1","CM1C","CM1F"],["CM2","CM2C","CM2F"],["CTS","CTSC","CTSF"],["[HAM","HAMC","HAMF"],["AP","APC","APF"],["CA","CAC","CAF"],["IE","IEC","IEF"],["HDZ","HDZC","HDZF"],["PK","PKC","PKF"],["HHT","HHTC","HHTF"],["HI","HIC","HIF"],["DD","DDC","DDF"],["CC","CCC","CCF"],["HY","HYC","HYF"],["TH","THC","THF"],["CP","CPC","CPF"],["PHA","PHAC","PHAF"],["NS","NSC","NSF"],["ICM","ICMC","ICMF"],["OH","OHC","OHF"],["OD","ODC","ODF"],["GC","GCC","GCF"],["MSUD","MSUDC","MSUDF"],["HP","HPC","HPF"],["NCL","NCLC","NCLF"],["NPD","NPDC","NPDF"],["TP","TPC","TPF"],["A","A","A*"],["BMS","BMSC","BMSF"],["HG","HGC","HGF"],["PP","POC","POF"],["Pp","POS","POF"],["Черн. окрас","BC","BF"],["Красн. окрас","RC","RF"],["POR","POR"],["RTF","RTF"]],"method":"anomaly","ready":True},
            {"method":"order","data":{}},
            {"method":"token","data":""},
            {"method":"radio","value":1,"field":"typeSearch","ready":True}
        ]

        url = 'https://xn--90aof1e.xn--p1ai/api/filter/1'

        response = requests.put(url, json=params)

        token = response.json().get('token')
        number_page = response.json().get('idArray')[0]
        return number_page, token
    except Exception as e:
        QMessageBox.critical(
            None,
            'Ошибка ввода',
            (f'{answer_error()}\nparser_def.py.py\nfilter_id_bus\n Подробности:\n {e}')
        )
