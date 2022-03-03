#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
from logging.handlers import RotatingFileHandler
import datetime
import os

import numpy as np
import pandas as pd
from docx import Document as Document_compose
from docxcompose.composer import Composer
from docxtpl import DocxTemplate, RichText
from PyQt5.QtWidgets import (QAbstractItemView, QAbstractScrollArea,
                             QFileDialog, QMessageBox, QTableWidget,
                             QTableWidgetItem)

from func.db_job import (save_bus_data, upload_bus_data,
                         upload_data_db_for_searh_father, upload_fater_data)
from func.func_answer_error import answer_error

from .parser_def import add_missing
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


def read_file(adres: str) -> pd.DataFrame:
    '''Чтение файла по полученному адресу'''
    adres_split = adres.split('.')
    if adres_split[-1] == 'csv':
        df_doc = (pd.read_csv(adres, sep=';', decimal=',', encoding='cp1251'))
    elif adres_split[-1] == 'txt':
        df_doc = (pd.read_csv(adres, sep='\t', decimal=',', encoding='utf-8'))
    elif adres_split[-1] == 'xlsx':
        df_doc = (pd.read_excel(adres))
    else:
        QMessageBox.critical(
            None,
            'Ошибка ввода', 'Вы выбрали файл неверного формата'
        )
    return df_doc


def combine_all_docx(filename_master, files_list: list, adres, date) -> None:
    '''Сбор документа для Word.'''
    number_sections = len(files_list)
    doc_m = Document_compose(filename_master)
    composer = Composer(doc_m)
    for i in range(0, number_sections):
        doc_temp = Document_compose(files_list[i])
        composer.append(doc_temp)
    composer.save(adres)


def delit(row: dict, delitel: str, col: str) -> str:
    '''Разделение строки по делителю.'''
    num = row[col]
    print(num)
    num = num.split(delitel)
    return num[-1]


def ms_clutch(row: dict, col1: str, col2: str) -> str:
    '''Объединение строки через знак.'''
    ms1 = row[col1]
    ms2 = row[col2]
    join_ms = [str(ms1), str(ms2)]
    ms0 = '/'.join(join_ms)
    return ms0


def enter_adres(name_str: str = 'Open File') -> str:
    """Возращает адрес файла."""
    adres = QFileDialog.getOpenFileName(
        None,
        name_str,
        './',
        'CSV (*.csv);; Text Files (*.txt);; Excel (*.xlsx)'
    )[0]
    return adres


def save_file(df_res: pd.DataFrame, name_str: str = 'Save File') -> None:
    """Возращает адрес файла."""
    adres = QFileDialog.getSaveFileName(
        None,
        name_str,
        './',
        'CSV (*.csv);; Text Files (*.txt)'
    )[0]
    df_res.to_csv(adres, sep=";", decimal=',')
    return adres


def save_file_for_word(name_str: str = 'Save File') -> None:
    """Возращает адрес файла."""
    adres = QFileDialog.getSaveFileName(
        None,
        name_str,
        './',
        'CSV (*.csv);; Word (*.docx);; Text Files (*.txt)'
    )[0]
    return adres


def ResOut(df_res: pd.DataFrame) -> QTableWidget:
    """Выводит результаты в таблицу."""
    table = QTableWidget()
    table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
    table.setEditTriggers(QAbstractItemView.NoEditTriggers)
    table.setColumnCount(len(df_res.columns))
    table.setRowCount(len(df_res))
    try:
        columns = df_res.columns
        table.setHorizontalHeaderLabels(columns)
    except Exception as e:
        print(e)
    for column in range(len(df_res.columns)):
        for row in range(len(df_res)):
            item = QTableWidgetItem(str(df_res.iloc[row, column]))
            table.setItem(row, column, item)
    return table


def split_hosbut_father(row):
    if type(row['farm']) == str:
        row['farm'] = row['farm'].split(', ')


def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def filer_father(hosbut: dict) -> pd.DataFrame:
    df = upload_data_db_for_searh_father()
    if hosbut['Выбрать всех']:
        return df.drop('farm', axis=1)
    df.apply(split_hosbut_father, axis=1)
    list_hosbut = []
    for key, item in hosbut.items():
        if item:
            if key != 'Выбрать всех':
                list_hosbut.append(key)
    list_res = []
    for i in range(len(df)):
        if not is_float(df.iloc[i, 1]):
            len_ = len(df.iloc[i, 2])
            for j in range(len_):
                print(df.iloc[i, 2][j], df.iloc[i, 1], list_hosbut)
                print(df.iloc[i, 2][j] in list_hosbut)
                if df.iloc[i, 2][j] in list_hosbut:
                    list_res.append(df.iloc[i, :])
        else:
            if df.iloc[i, 2] in list_hosbut:
                list_res.append(df.iloc[i, :])
    df_res = pd.DataFrame(data=list_res)
    df = df_res.reset_index(drop=True)
    df['farm'] = df.pop('farm')
    return df


def search_father(adres: str, filter: dict) -> pd.DataFrame:
    """Поиск возможных отцов."""
    df = filer_father(filter)
    df_search = read_file(adres)
    df_search = df_search.T
    df = df.fillna('-')
    df = df.replace('  ', '')
    df_search = df_search.fillna('-')
    df_search = df_search.reset_index()
    df_search.columns = df_search.loc[0, :]
    df_search = df_search.drop(0)
    df_res = df.copy()
    for i in range(2, len(df_search.columns)):
        for j in range(len(df_res)):
            if df_search.iloc[0, i-1] != '-':
                locus = df_search.iloc[0, i-1].split('/')
                if (
                    df_res.iloc[j, i] != '-' and
                    str(df_res.iloc[j, i]) != 'nan'
                ):
                    locus_base = df_res.iloc[j, i].split('/')
                    if (
                        locus[0] != locus_base[0] and
                        locus[1] != locus_base[0] and
                        locus[0] != locus_base[1] and
                        locus[1] != locus_base[1]
                    ):
                        df_res.iloc[j, i] = np.nan
    df_res = df_res.dropna()
    df_res.to_csv(
        r'func\data\search_fatherh\bus_search.csv',
        sep=';',
        decimal=',',
        encoding='cp1251'
    )
    return df_res


def ms_out_word(adres: str) -> pd.DataFrame:
    '''Переводит данные из word в csv.'''
    doc = read_file(adres)
    doc.columns = ['ms', 'ms_size', 'vater', 'mom']
    msatle = [
        'name', 'numer', 'vater', 'number_vater',
        'BM1818', 'BM1824',
        'BM2113', 'CSRM60', 'CSSM66',
        'CYP21', 'ETH10', 'ETH225',
        'ETH3', 'ILSTS6', 'INRA023',
        'RM067', 'SPS115', 'TGLA122',
        'TGLA126', 'TGLA227', 'TGLA53',
        'MGTG4B', 'SPS113'
    ]
    result = pd.DataFrame(columns=msatle)

    def ms_select(
        data_in: pd.DataFrame,
        data_out: pd.DataFrame,
        ms: str,
        no: int
    ) -> None:
        for i in range(len(data_in)):
            if data_in.loc[i, 'ms'] == ms:
                res = data_in.loc[i, 'ms_size']
                nom_date_out = i - no + 4
                data_out.loc[nom_date_out, ms] = res

    for j in range(4, len(msatle)):
        ms_r = msatle[j]
        ms_select(doc, result, ms_r, j)

    result = result.reset_index()

    def name_select(data_in: pd.DataFrame, data_out: pd.DataFrame) -> None:
        count = 0
        for i in range(len(data_in)):
            if data_in.loc[i, 'ms'] == 'Локус':
                count += 1
                a = i + 1
                res_name = data_in.loc[a, 'ms_size'].split(' ')
                res_vater = data_in.loc[a, 'vater'].split(' ')
                nom_date_out = count - 1
                try:
                    data_out.loc[nom_date_out, 'numer'] = res_name[1]
                    data_out.loc[nom_date_out, 'name'] = res_name[0]
                except Exception as e:
                    print(e)
                    data_out.loc[nom_date_out, 'numer'] = res_name[0]
                try:
                    data_out.loc[nom_date_out, 'vater'] = res_vater[0]
                    data_out.loc[nom_date_out, 'number_vater'] = res_vater[1]
                except Exception as e:
                    print(e)
                    data_out.loc[nom_date_out, 'number_vater'] = res_vater[0]

    name_select(doc, result)

    result = result.transpose()
    result.to_csv(
        r'func\data\ms_word\result_ms_word.csv',
        sep=";",
        decimal=',',
        encoding="cp1251"
    )
    return result


def check_error_ms(
    df: pd.DataFrame,
    df_profil: pd.DataFrame
) -> dict:
    logger.debug("Страт check_error_ms")
    df = df.dropna(subset=[df.columns[5]])
    try:
        list_number_father = []
        list_locus_er_father = []
        list_father_er = []
        list_animal_father = []
        list_number_mutter = []
        list_locus_er_mutter = []
        list_mutter_er = []
        list_animal_mutter = []
        for i in range(len(df)):
            number = int(df.loc[i, 'number_proba'])
            number_animal = int(df.loc[i, 'number_animal'])
            number_mutter = int(df.loc[i, 'number_mutter'])
            number_fater = int(df.loc[i, 'number_father'])
            dict_mutter = upload_bus_data(number_mutter)
            dict_father = upload_fater_data(number_fater)
            df_profil['num'] = df_profil['num'].astype('int')
            print(number, list(df_profil['num']))
            if number in list(df_profil['num']):
                pass
            else:
                QMessageBox.information(
                    None,
                    'Инфорамция',
                    f'Животного {number_animal} нет в данных. Проба {number}'
                )
                continue
            print("Анализ ошибок" + str(number))
            df_animal_prof = df_profil.query(
                'num == @number'
            ).loc[:, 'ETH3': 'ETH10'].reset_index(drop=True).T.to_dict().get(0)

            logger.debug(
                "MS father"
            )
            for locus, val in dict_father.items():
                logger.debug(f"Values dict: {locus}, {val}")
                value_fater_ms = val
                if value_fater_ms != '-' and (value_fater_ms is not None):
                    logger.debug(
                        f"Values MS father: {value_fater_ms}, locus {locus}"
                        )
                    locus_a = locus.split('_father')[0]
                    value_animal_ms = df_animal_prof.get(locus_a, 1)
                    logger.debug(
                        "Выделение локуса животного: " +
                        f"{value_animal_ms}, locus {locus_a}"
                        )
                    if value_animal_ms != 1:
                        if verification_ms(
                            value_fater_ms,
                            value_animal_ms
                        ):
                            list_number_father.append(number)
                            list_locus_er_father.append(locus)
                            list_father_er.append(number_fater)
                            list_animal_father.append(number_animal)
            logger.debug(
                "MS Mutter"
            )
            for locus, val in dict_mutter.items():
                value_mutter_ms = val
                if value_mutter_ms != '-':
                    logger.debug(
                        f"Values MS mutter: {value_mutter_ms}, locus {locus}"
                        )
                    locus_a = locus.split('_mutter')[0]
                    value_animal_ms = df_animal_prof.get(locus_a, 1)
                    if value_animal_ms != 1:
                        if verification_ms(
                            value_mutter_ms,
                            value_animal_ms
                        ):
                            list_number_mutter.append(i)
                            list_locus_er_mutter.append(locus)
                            list_mutter_er.append(number_mutter)
                            list_animal_mutter.append(number_animal)

        res_error_father = pd.DataFrame({
            'number': list_number_father,
            'locus': list_locus_er_father,
            'father': list_father_er,
            'animal': list_animal_father,
        })
        res_error_mutter = pd.DataFrame({
            'number': list_number_mutter,
            'locus': list_locus_er_mutter,
            'mutter': list_mutter_er,
            'animal': list_animal_mutter,
        })
        logger.debug("Конец check_error_ms")
        return {"father": res_error_father, "mutter": res_error_mutter}
    except Exception as e:
        logger.error(e)
        name = "\nfunc_ms.py | check_error_ms\n"
        QMessageBox.critical(
            None,
            'Ошибка ввода',
            f'{answer_error()} {name}Подробности:\n {e}'
        )
        logger.debug("Конец check_error_ms")


def verification_ms(one_ms: str, second_ms: str) -> bool:
    """Возращает True, если данные МС неподходят"""
    try:
        logger.debug("Стартует verification_ms")
        logger.debug(f"Приходящие значения: {one_ms}, {second_ms}")
        res = False
        one_split = one_ms.split('/')
        second_split = second_ms.split('/')
        if (
            one_split[0] != second_split[0] and
            one_split[0] != second_split[1] and
            one_split[1] != second_split[0] and
            one_split[1] != second_split[1]
        ):
            res = True
        logger.debug("Конец verification_ms")
        return res
    except Exception as e:
        logger.error(
            f"data error {one_split}, {second_split}"
        )
        name = '\nfunc_ms.py\verification_ms\n '
        QMessageBox.critical(
            None,
            'Ошибка ввода',
            (f'{answer_error()}{name}Подробности:\n {e}')
        )
        logger.debug("end verification_ms")


def data_verification(context: dict) -> dict:
    """Проверка сответствия Данных матери, отца и потомка"""
    logger.debug("Начало data_verification")
    list_keys = [
        'BM1818',
        'BM1824',
        'BM2113',
        'CSRM60',
        'CSSM66',
        'CYP21',
        'ETH10',
        'ETH225',
        'ETH3',
        'ILSTS6',
        'INRA023',
        'RM067',
        'SPS115',
        'TGLA122',
        'TGLA126',
        'TGLA227',
        'TGLA53',
        'MGTG4B',
        'SPS113',
    ]
    try:
        for key in list_keys:
            child = context.get(key)
            father = context.get(key+'_father')
            mutter = context.get(key+'_mutter')
            logger.debug(
                f"Значения ключа {key}. Потомок: {child}," +
                f" отец: {father}, мать: {mutter}"
            )
            if (
                father != '-' and
                father != '0/0' and
                father != '' and
                father is not None and
                child != '-' and
                child != '0/0' and
                child != '' and
                child is not None
            ):
                if verification_ms(child, father):
                    context[key] = RichText(
                        context.get(key),
                        color='#ff0000',
                        bold=True
                    )
                    context[key+'_father'] = RichText(
                        context.get(key+'_father'),
                        color='#ff0000',
                        bold=True
                    )
            if (
                mutter != '-' and
                mutter != '0/0' and
                mutter != '' and
                mutter is not None and
                child != '-' and
                child != '0/0' and
                child != '' and
                child is not None
            ):
                if verification_ms(child, mutter):
                    context[key] = RichText(
                        context.get(key),
                        color='#ff0000',
                        bold=True
                    )
                    context[key+'_mutter'] = RichText(
                        context.get(key+'_mutter'),
                        color='#ff0000',
                        bold=True
                    )
        logger.debug("конец data_verification")
        return context
    except Exception as e:
        name = '\nfunc_ms.py\\data_verification\n'
        logger.error(
            f"Значение ключа {key}. Потомок: {child}," +
            f" отец: {father}, мать: {mutter}"
        )
        QMessageBox.critical(
            None,
            'Ошибка ввода',
            (f'{answer_error()}{name}Подробности:\n {e}')
        )
        logger.debug("Конец data_verification")


def check_conclusion(context: dict) -> str:
    logger.debug("Запуск check_conclusion")
    res = ''
    list_keys = [
        'BM1818',
        'BM1824',
        'BM2113',
        'CSRM60',
        'CSSM66',
        'CYP21',
        'ETH10',
        'ETH225',
        'ETH3',
        'ILSTS6',
        'INRA023',
        'RM067',
        'SPS115',
        'TGLA122',
        'TGLA126',
        'TGLA227',
        'TGLA53',
        'MGTG4B',
        'SPS113',
    ]
    mutter = context.get('BM1818_mutter')
    father = context.get('BM1818_father')
    flag = False
    for key in list_keys:
        child = context.get(key)
        father = context.get(key+'_father')
        mutter = context.get(key+'_mutter')
        logger.debug(
            f"Значения ключа {key}. Потомок: {child}," +
            f" отец: {father}, мать: {mutter}"
        )
        if (
            father != '-' and
            father != '0/0' and
            father != '' and
            father is not None and
            child != '-' and
            child != '0/0' and
            child != '' and
            child is not None
        ):
            if verification_ms(child, father):
                flag = True
                break
        if (
            mutter != '-' and
            mutter != '0/0' and
            mutter != '' and
            mutter is not None and
            child != '-' and
            child != '0/0' and
            child != '' and
            child is not None
        ):
            if verification_ms(child, mutter):
                flag = True
                break

    if flag:
        if (
            mutter != '' and
            mutter != '-' and
            mutter != '0/0' and
            mutter is not None and
            father != '' and
            father != '-' and
            father != '0/0' and
            father is not None
        ):
            res = 'Родители не соответствуют'
        elif (
            mutter == '' or
            mutter == '-' or
            mutter == '0/0' or
            mutter is None
        ):
            res = 'Отец не соответствует'
        else:
            res = ''
    else:
        if (
            mutter != '' and
            mutter != '-' and
            mutter != '0/0' and
            mutter is not None and
            father != '' and
            father != '-' and
            father != '0/0' and
            father is not None
        ):
            res = 'Родители соответствуют'
        elif (
            mutter == '' or
            mutter == '-' or
            mutter == '0/0' or
            mutter is None
        ):
            res = 'Отец соответствует'
        else:
            res = ''
    logger.debug("Конец check_conclusion")
    return res


def creat_doc_pas_gen(
    adres_invertory: str,
    adres_genotyping: str,
    adres: str,
    hosut: str = 'Хозяйство'
) -> pd.DataFrame:
    try:
        now = datetime.datetime.now()
        list_father_non = []
        date = now.strftime("%d-%m-%Y")
        df = read_file(adres_invertory)
        df.columns = [
            'number_animal',
            'name_animal',
            'number_proba',
            'number_mutter',
            'name_mutter',
            'number_father',
            'name_father',
        ]
        df_faters = add_missing(df, hosut)
        df_profil = read_file(adres_genotyping)
        try:
            df_profil['num'] = df_profil.apply(
                delit,
                delitel='-',
                col='Sample Name',
                axis=1
            )
        except Exception as e:
            name = "\nfunc_ms.py|delit in creat_doc_pas_gen\n"
            QMessageBox.critical(
                None,
                'Ошибка ввода',
                f'{answer_error()} {name}Подробности:\n {e}'
            )
        df_profil['num'] = df_profil['num'].astype('int')
        df = df.fillna(0)
        series_num = list(df_profil['num'])
        series_proba = list(df['number_proba'].astype('int'))
        df_profil['Sample Name'] = df_profil.pop('num')
        df_profil = df_profil.rename(columns={'Sample Name': 'num'})
        df_profil = df_profil.fillna(0)
        df_profil = df_profil.astype('int')
        for i in range(1, len(df_profil.columns), 2):
            j = i + 1
            col1 = df_profil.columns[i]
            col_split = col1.split()[0]
            col_split = col_split.upper()
            col2 = df_profil.columns[j]
            df_profil[col_split] = df_profil.apply(
                ms_clutch,
                col1=col1,
                col2=col2,
                axis=1
            )
        df_profil_end = df_profil.iloc[:, -15:]
        df_profil_end['num'] = df_profil['num']
        df = df.astype('str')
        df['number_father'] = df['number_father'].astype('float')
        list_number_faters = list(df_faters.loc[:, 'number'].astype('float'))

        df['number_animal'] = pd.to_numeric(
            df['number_animal'],
            downcast='integer'
        )
        df['number_proba'] = pd.to_numeric(
            df['number_proba'],
            downcast='integer'
        )
        df['number_father'] = pd.to_numeric(
            df['number_father'],
            downcast='integer'
        )
        df['number_mutter'] = pd.to_numeric(
            df['number_mutter'],
            downcast='integer'
        )
        dict_error = check_error_ms(df, df_profil)
        dict_error.get("mutter").to_csv(
            r'func\data\creat_pass_doc\res_error_mutter.csv',
            sep=";",
            decimal=',',
            encoding="cp1251")
        dict_error.get("father").to_csv(
            r'func\data\creat_pass_doc\res_error.csv',
            sep=";",
            decimal=',',
            encoding="cp1251")

        files_list = []
        try:
            for i in range(len(series_num)):
                doc = DocxTemplate(r'func\data\creat_pass_doc\gen_pass_2.docx')
                if series_num[i] in series_proba:
                    num_anim = series_num[i]
                    df_info = df.query(
                        'number_proba == @num_anim'
                    ).reset_index()
                    df_profil_only = df_profil_end.query(
                        'num == @num_anim'
                    ).reset_index()

                    number_animal = df_info.loc[0, 'number_animal']
                    name_animal = df_info.loc[0, 'name_animal']
                    number_proba = df_info.loc[0, 'number_proba']
                    number_father = df_info.loc[0, 'number_father']
                    name_father = df_info.loc[0, 'name_father']
                    number_mutter = int(df_info.loc[0, 'number_mutter'])
                    name_mutter = df_info.loc[0, 'name_mutter']
                    animal_join = [name_animal, str(number_animal)]
                    fater_join = [name_father, str(number_father)]
                    mutter_join = [name_mutter, str(number_mutter)]
                    animal = ' '.join(animal_join)
                    fater = ' '.join(fater_join)
                    mutter = ' '.join(mutter_join)

                    dict_profil_only = df_profil_only.loc[0, :].to_dict()

                    if number_father in list_number_faters:
                        df_faters_only = (df_faters.query(
                            'number == @number_father'
                        ).reset_index(drop=True))
                        dict_faters_only = df_faters_only.loc[0, :].to_dict()
                        dict_faters_new = {}
                        for key, val in dict_faters_only.items():
                            dict_faters_new[key+"_father"] = val
                        context = {
                            'number_animal': number_animal,
                            'name_animal': name_animal,
                            'hosbut': hosut,
                            'number_proba': number_proba,
                            'number_father': number_father,
                            'name_father': name_father,
                            'animal': animal,
                            'father': fater,
                            'mutter': mutter,
                            'date': date
                        }
                        context = {**context, **dict_faters_new}
                        context = {**context, **dict_profil_only}
                        save_bus_data(context)
                        dict_mutter = upload_bus_data(number_mutter)
                        context = {**context, **dict_mutter}
                        context['conclusion'] = check_conclusion(context)
                        context = data_verification(context)
                        doc.render(context)
                        doc.save(str(i) + ' generated_doc.docx')
                        title = str(i) + ' generated_doc.docx'
                        files_list.append(title)

                    else:
                        context = {
                            'number_animal': number_animal,
                            'name_animal': name_animal,
                            'hosbut': hosut,
                            'number_proba': number_proba,
                            'number_father': number_father,
                            'name_father': name_father,
                            'animal': animal,
                            'father': fater,
                            'mutter': mutter,
                            'date': date
                        }
                        context = {**context, **dict_profil_only}
                        save_bus_data(context)
                        dict_mutter = upload_bus_data(number_mutter)
                        context = {**context, **dict_mutter}
                        context['conclusion'] = check_conclusion(context)
                        context = data_verification(context)
                        doc.render(context)
                        doc.save(str(i) + ' generated_doc.docx')
                        title = str(i) + ' generated_doc.docx'
                        files_list.append(title)
                        list_father_non.append(str(number_father))
                        print(f'Нет быка: {number_father}, страница: {i+1}')
                else:
                    print(
                        f'Нет животного: проба {int(series_num[i])},' +
                        f' номер {num_anim}, страница: {i+1}'
                    )
        except Exception as e:
            name = '\nfunc_ms.py\ncreat_doc_pas_gen\ngenerate password\n'
            QMessageBox.critical(
                None,
                'Ошибка ввода',
                f'{answer_error()}{name}Подробности:\n {e}'
            )
        non_father = pd.DataFrame({'Отцы': list(set(list_father_non))})
        non_father.to_csv(
            r'func\data\creat_pass_doc\non_father.csv',
            sep=";",
            decimal=',',
            encoding="cp1251")
        filename_master = files_list.pop(0)

        combine_all_docx(filename_master, files_list, adres, date)
        files_list.append(filename_master)
        for i in range(len(files_list)):
            if os.path.isfile(files_list[i]):
                os.remove(files_list[i])
            else:
                print("File doesn't exists!")
        return dict_error.get("father")
    except Exception as e:
        name = '\nfunc_ms.py\ncreat_doc_pas_gen\n '
        QMessageBox.critical(
            None,
            'Ошибка ввода',
            (f'{answer_error()}{name}Подробности:\n {e}')
        )
