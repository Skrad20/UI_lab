import pandas as pd
import requests
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import QMessageBox


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


def parser_ms(number_page, token):
    """Собирает и парсит данные по МС быков"""
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
            (f'{name} Подробности:\n {e}')
        )


def filter_id_bus(number: str) -> list:
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
        print(response.json())
        token = response.json().get('token')
        if len(response.json().get('idArray')) > 0:
            number_page = response.json().get('idArray')[0]
            return number_page, token
        else:
            return -1, token
    except Exception as e:
        name = '\nparser_def.py.py\nfilter_id_bus\n '
        QMessageBox.critical(
            None,
            'Ошибка ввода',
            (f'{name}Подробности:\n {e}')
        )


if __name__ == "__main__":
    number_page, token = filter_id_bus(294)
    print(number_page, token)
    df = parser_ms(number_page, token)
    print(df)
