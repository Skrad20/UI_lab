#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd 
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

  
def enter_adres() -> str:
    """Возращает адрес файла."""
    adres =  QFileDialog.getOpenFileName(None, 
                        'Open File', 
                        './', 
                        'CSV (*.csv);; Text Files (*.txt)')[0]
    return adres

def ResOut(df_res) -> QTableWidget:
    """Выводит результаты в таблицу."""
    table = QTableWidget()
    table.setColumnCount(len(df_res.columns))
    table.setRowCount(len(df_res))
    for column in range(len(df_res.columns)):
        for row in range(len(df_res)):
            item = QTableWidgetItem(str(df_res.iloc[row, column]))
            table.setItem(row, column, item)

    return table

def search_father(adres: str) -> pd.DataFrame:
    """Поиск возможных отцов."""
    df = pd.read_csv(r'func\data\search_fatherh\Bulls.txt', sep='\t', decimal=',')
    df_search = pd.read_csv(adres, sep=';', decimal=',')
    df_search = df_search.T
    df = df.fillna('-')
    df = df.replace('  ','')
    df_search = df_search.fillna('-')
    df_search = df_search.reset_index()
    df_search.iloc[1,0] = df_search.iloc[0,1]
    df_search = df_search.drop(0, axis=1)
    df_search.columns = df_search.loc[0,:]
    df_search= df_search.drop(0)
    if len(df_search.columns) == len(df.columns):
        return 'Ошибка в данных.'
    df_res = df.copy()
    for i in range(1, len(df_search.columns)):
        for j in range(len(df_res)): 
            if df_search.iloc[0,i] != '-':
                locus = df_search.iloc[0,i].split('/')
                if df_res.iloc[j,i] != '-' :
                    locus_base = df_res.iloc[j,i].split('/')
                    if locus[0] != locus_base[0] and locus[1] != locus_base[0] and locus[0] != locus_base[1] and locus[1] != locus_base[1]:
                        df_res.iloc[j,i] = np.nan
    df_res = df_res.dropna()
    df_res.to_csv(r'func\data\search_fatherh\bus_search.csv', sep=';', decimal=',', encoding='cp1251')

    return df_res

def ms_out_word(adres) -> pd.DataFrame:
    '''Переводит данные из word в csv.'''
    doc = (pd.read_csv(adres,
                    sep='\t',
                    error_bad_lines=False))
    doc.columns = ['ms', 'ms_size', 'vater', 'mom']
    msatle = ['name', 'numer', 'vater', 'number_vater',
            'BM1818', 'BM1824',
            'BM2113', 'CSRM60', 'CSSM66',
            'CYP21', 'ETH10', 'ETH225',
            'ETH3', 'ILSTS6', 'INRA023',
            'RM067', 'SPS115', 'TGLA122',
            'TGLA126', 'TGLA227', 'TGLA53',
            'MGTG4B', 'SPS113']
    result = pd.DataFrame(columns=msatle)

    def ms_select(data_in: pd.DataFrame, data_out: pd.DataFrame, ms: str, no: int) -> None:
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
        count= 0
        for i in range(len(data_in)):
            if data_in.loc[i,'ms'] == 'Локус':
                count += 1
                a = i + 1
                res_name = data_in.loc[a,'ms_size'].split(' ')
                res_vater = data_in.loc[a,'vater'].split(' ')
                nom_date_out = count - 1
                try:
                    data_out.loc[nom_date_out, 'numer'] = res_name[1]
                    data_out.loc[nom_date_out, 'name'] = res_name[0]                
                except:
                    data_out.loc[nom_date_out, 'numer'] = res_name[0]
                try:
                    data_out.loc[nom_date_out, 'vater'] = res_vater[0]
                    data_out.loc[nom_date_out, 'number_vater'] = res_vater[1]
                except:
                    data_out.loc[nom_date_out, 'number_vater'] = res_vater[0]

    name_select(doc, result)    

    result = result.transpose()
    (result.to_csv(r'func\data\ms_word\result_ms_word.csv',
                sep=";",
                decimal=',',
                encoding = "cp1251"))
    
    return result
