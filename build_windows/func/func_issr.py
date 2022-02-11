#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
from tqdm import tqdm
from .func_ms import read_file
tqdm.pandas()

def ga_issr(row) -> str:
    """Функция определения принадлежности данных к аллели"""
    genotype = 'G'
    size_ga = row['GA']
    if 2500 < size_ga:
        return '-'
    elif 2300 < size_ga < 2500:
        gt = [genotype, '1']
        return ''.join(gt)
    elif 2000 <= size_ga < 2300:
        gt1 = [genotype, '2']
        return ''.join(gt1)
    elif 1800 <= size_ga < 2000:
        gt2 = [genotype, '3']
        return ''.join(gt2)
    elif 1700 <= size_ga < 1800:
        gt3 = [genotype, '4']
        return ''.join(gt3)
    elif 1600 <= size_ga < 1700:
        gt4 = [genotype, '5']
        return ''.join(gt4)
    elif 1500 <= size_ga < 1600:
        gt5 = [genotype, '6']
        return ''.join(gt5)
    elif 1400 <= size_ga < 1500:
        gt6 = [genotype, '7']
        return ''.join(gt6)
    elif 1300 <= size_ga < 1400:
        gt7 = [genotype, '8']
        return ''.join(gt7)
    elif 1240 <= size_ga < 1300:
        gt8 = [genotype, '9']
        return ''.join(gt8)
    elif 1180 <= size_ga < 1240:
        gt9 = [genotype, '10']
        return ''.join(gt9)
    elif 1120 <= size_ga < 1180:
        gt10 = [genotype, '11']
        return ''.join(gt10)
    elif 1060 <= size_ga < 1120:
        gt11 = [genotype, '12']
        return ''.join(gt11)
    elif 1000 <= size_ga < 1060:
        gt12 = [genotype, '13']
        return ''.join(gt12)
    elif 940 <= size_ga < 1000:
        gt13 = [genotype, '14']
        return ''.join(gt13)
    elif 880 <= size_ga < 940:
        gt14 = [genotype, '15']
        return ''.join(gt14)
    elif 820 <= size_ga < 880:
        gt15 = [genotype, '16']
        return ''.join(gt15)
    elif 760 <= size_ga < 820:
        gt16 = [genotype, '17']
        return ''.join(gt16)
    elif 720 <= size_ga < 760:
        gt17 = [genotype, '18']
        return ''.join(gt17)
    elif 680 <= size_ga < 720:
        gt18 = [genotype, '19']
        return ''.join(gt18)
    elif 640 <= size_ga < 680:
        gt19 = [genotype, '20']
        return ''.join(gt19)
    elif 600 <= size_ga < 640:
        gt20 = [genotype, '21']
        return ''.join(gt20)
    elif 560 <= size_ga < 600:
        gt21 = [genotype, '22']
        return ''.join(gt21)
    elif 530 <= size_ga < 560:
        gt22 = [genotype, '23']
        return ''.join(gt22)
    elif 500 <= size_ga < 530:
        gt23 = [genotype, '24']
        return ''.join(gt23)
    elif 470 <= size_ga < 500:
        gt24 = [genotype, '25']
        return ''.join(gt24)
    elif 440 <= size_ga < 470:
        gt25 = [genotype, '26']
        return ''.join(gt25)
    elif 410 <= size_ga < 440:
        gt26 = [genotype, '27']
        return ''.join(gt26)
    elif 380 <= size_ga < 410:
        gt27 = [genotype, '28']
        return ''.join(gt27)
    elif 360 <= size_ga < 380:
        gt28 = [genotype, '29']
        return ''.join(gt28)
    elif 340 <= size_ga < 360:
        gt29 = [genotype, '30']
        return ''.join(gt29)
    elif 320 <= size_ga < 340:
        gt30 = [genotype, '31']
        return ''.join(gt30)
    elif 300 <= size_ga < 320:
        gt31 = [genotype, '32']
        return ''.join(gt31)
    elif 280 <= size_ga < 300:
        gt32 = [genotype, '33']
        return ''.join(gt32)
    elif 260 <= size_ga < 280:
        gt33 = [genotype, '34']
        return ''.join(gt33)
    elif 240 <= size_ga < 260:
        gt34 = [genotype, '35']
        return ''.join(gt34)
    elif 220 <= size_ga < 240:
        gt35 = [genotype, '36']
        return ''.join(gt35)
    elif 200 <= size_ga < 220:
        gt36 = [genotype, '37']
        return ''.join(gt36)
    elif 160 <= size_ga < 200:
        gt37 = [genotype, '38']
        return ''.join(gt37)
    elif size_ga < 160:
        return '-'

def ag_issr(row) -> str:
    """Функция определения принадлежности данных к аллели"""
    genotype = 'A'
    size_ga = row['AG']
    if 2500 < size_ga:
        return '-'
    elif 2300 < size_ga < 2500:
        gt = [genotype, '1']
        return ''.join(gt)
    elif 2000 <= size_ga < 2300:
        gt1 = [genotype, '2']
        return ''.join(gt1)
    elif 1800 <= size_ga < 2000:
        gt2 = [genotype, '3']
        return ''.join(gt2)
    elif 1700 <= size_ga < 1800:
        gt3 = [genotype,'4']
        return ''.join(gt3)
    elif 1600 <= size_ga < 1700:
        gt4 = [genotype, '5']
        return ''.join(gt4)
    elif 1500 <= size_ga < 1600:
        gt5 = [genotype, '6']
        return ''.join(gt5)
    elif 1400 <= size_ga < 1500:
        gt6 = [genotype, '7']
        return ''.join(gt6)
    elif 1300 <= size_ga < 1400:
        gt7 = [genotype, '8']
        return ''.join(gt7)
    elif 1240 <= size_ga < 1300:
        gt8 = [genotype, '9']
        return ''.join(gt8)
    elif 1180 <= size_ga < 1240:
        gt9 = [genotype, '10']
        return ''.join(gt9)
    elif 1120 <= size_ga < 1180:
        gt10 = [genotype, '11']
        return ''.join(gt10)
    elif 1060 <= size_ga < 1120:
        gt11 = [genotype, '12']
        return ''.join(gt11)
    elif 1000 <= size_ga < 1060:
        gt12 = [genotype, '13']
        return ''.join(gt12)
    elif 940 <= size_ga < 1000:
        gt13 = [genotype, '14']
        return ''.join(gt13)
    elif 880 <= size_ga < 940:
        gt14 = [genotype, '15']
        return ''.join(gt14)
    elif 820 <= size_ga < 880:
        gt15 = [genotype, '16']
        return ''.join(gt15)
    elif 760 <= size_ga < 820:
        gt16 = [genotype, '17']
        return ''.join(gt16)
    elif 720 <= size_ga < 760:
        gt17 = [genotype, '18']
        return ''.join(gt17)
    elif 680 <= size_ga < 720:
        gt18 = [genotype, '19']
        return ''.join(gt18)
    elif 640 <= size_ga < 680:
        gt19 = [genotype, '20']
        return ''.join(gt19)
    elif 600 <= size_ga < 640:
        gt20 = [genotype, '21']
        return ''.join(gt20)
    elif 560 <= size_ga < 600:
        gt21 = [genotype, '22']
        return ''.join(gt21)
    elif 530 <= size_ga < 560:
        gt22 = [genotype, '23']
        return ''.join(gt22)
    elif 500 <= size_ga < 530:
        gt23 = [genotype, '24']
        return ''.join(gt23)
    elif 470 <= size_ga < 500:
        gt24 = [genotype, '25']
        return ''.join(gt24)
    elif 440 <= size_ga < 470:
        gt25 = [genotype, '26']
        return ''.join(gt25)
    elif 410 <= size_ga < 440:
        gt26 = [genotype, '27']
        return ''.join(gt26)
    elif 380 <= size_ga < 410:
        gt27 = [genotype, '28']
        return ''.join(gt27)
    elif 360 <= size_ga < 380:
        gt28 = [genotype, '29']
        return ''.join(gt28)
    elif 340 <= size_ga < 360:
        gt29 = [genotype, '30']
        return ''.join(gt29)
    elif 320 <= size_ga < 340:
        gt30 = [genotype, '31']
        return ''.join(gt30)
    elif 300 <= size_ga < 320:
        gt31 = [genotype, '32']
        return ''.join(gt31)
    elif 280 <= size_ga < 300:
        gt32 = [genotype, '33']
        return ''.join(gt32)
    elif 260 <= size_ga < 280:
        gt33 = [genotype, '34']
        return ''.join(gt33)
    elif 240 <= size_ga < 260:
        gt34 = [genotype, '35']
        return ''.join(gt34)
    elif 220 <= size_ga < 240:
        gt35 = [genotype, '36']
        return ''.join(gt35)
    elif 200 <= size_ga < 220:
        gt36 = [genotype, '37']
        return ''.join(gt36)
    elif 160 <= size_ga < 200:
        gt37 = [genotype, '38']
        return ''.join(gt37)
    elif size_ga < 160:
        return '-'

def data_transpose(df: pd.DataFrame, index_zahl: pd.DataFrame) -> pd.DataFrame:
    """функция для транспонирования таблицы"""
    result_end_1 = pd.DataFrame()
    b = len(index_zahl)
    for i in range(b):
        a = index_zahl.loc[i, 'num']
        num_otbor = df.query('animal == @a')
        num_otbor = num_otbor.reset_index()
        num_otbor_n_i = pd.DataFrame()
        num_otbor_n_i['animal'] = num_otbor['animal']
        num_otbor_n_i['AG_genotype'] = num_otbor['AG_genotype']
        num_otbor_n_i['GA_genotype'] = num_otbor['GA_genotype']
        num_otbor_transp = num_otbor_n_i.transpose()
        num_otbor_transp = num_otbor_transp.reset_index()
        result_end_1 = result_end_1.append(num_otbor_transp)
    return result_end_1

def issr_analit_func(adres: str) -> pd.DataFrame:
    """Анлиза данных issr"""
    # загрузка входных данных с раделителем по ячейкам и долевым ","
    #func\data\issr\issr.txt
    df = read_file(adres)
    # Изменяем названия столбцов для удобства
    df.set_axis(['animal', 'GA', 'animal_1', 'AG'], axis='columns', inplace=True)
    # убираем пкстые ячейки
    df['animal'] = df['animal'].fillna(0)
    df['animal_1'] = df['animal_1'].fillna(0)
    # Изменяем тип данных на строковые
    df['GA'] = df['GA'].astype('str')
    df['AG'] = df['AG'].astype('str')
    # убираем неразрывный перенос
    df['GA'] = df['GA'].str.replace('\xa0', '')
    df['AG'] = df['AG'].str.replace('\xa0', '')
    # Заменяем запятые на точки для расчётов
    df['GA'] = df['GA'].str.replace(',', '.')
    df['AG'] = df['AG'].str.replace(',', '.')

    # Изменяем тип данных на плавающий
    df['GA'] = df['GA'].astype('float64')
    df['AG'] = df['AG'].astype('float64')

    # убираем пропуски 
    df['GA'] = df['GA'].fillna(0)
    df['AG'] = df['AG'].fillna(0)
    # создаем новые датафреймы с необходимыми столбцами
    ag = pd.DataFrame()
    ag['animal'] = df['animal_1']
    ag['genotype'] = df['AG']

    ga = pd.DataFrame()
    ga['animal'] = df['animal']
    ga['genotype'] = df['GA']

    # функция выравнивания даннх по номерам. Проходим по циклом по всему ДФ 
    # если строка равна нулю то она получает значение предыдущей с префиксом 
    # Если нет то остается имеющееся значение

    def ravn(data):
        for i in range(0, len(data)):
            j = i-1
            if data.loc[i, 'animal'] == 0.0:
                animall = str(data.loc[j, 'animal'])
                animn = [animall, '99']
                data.loc[i, 'animal'] = ''.join(animn)
            else:
                data.loc[i, 'animal'] = data.loc[i, 'animal']

    # Применение выравнивания с новым ДФ
    ravn(ga)
    ravn(ag)

    # Проверочная соединенная таблица
    tabl_ravn = ag.merge(ga, on='animal', how='outer')
    #(tabl_ravn.to_csv(r'C:\Users\Коптев\Desktop\pyton\ISSR\tabl.csv',
    #                sep=";",
    #                decimal=','))

    # вводим изменения для последующей работы в выравненкю и соединению таблицу

    tabl_ravn = tabl_ravn.reset_index()

    (tabl_ravn.set_axis(['index', 'animal', 'AG', 'GA'],
                        axis='columns',
                        inplace=True))
    tabl_ravn['animal'] = tabl_ravn['animal'].astype('float64')
    tabl_ravn['animal'] = round(tabl_ravn['animal'])
    tabl_ravn['animal'] = tabl_ravn['animal'].astype('int64')
    tabl_ravn['AG'] = tabl_ravn['AG'].fillna(0)
    tabl_ravn['GA'] = tabl_ravn['GA'].fillna(0)

    # применение функции к данным
    tabl_ravn['GA_genotype'] = tabl_ravn.progress_apply(ga_issr, axis=1)
    tabl_ravn['AG_genotype'] = tabl_ravn.progress_apply(ag_issr, axis=1)

    # сборка результирующей таблицы
    result = pd.DataFrame()
    result['animal'] = tabl_ravn['animal']
    result['AG_genotype'] = tabl_ravn['AG_genotype']
    result['GA_genotype'] = tabl_ravn['GA_genotype']

    # Возвращение первичных номеров животных
    index_zahl = pd.DataFrame(result['animal'].value_counts())
    index_zahl = index_zahl.reset_index()
    index_zahl.columns = ['num', 'chast']
    index_zahl = index_zahl.sort_values('num', ascending=True)
    index_zahl = index_zahl.reset_index()

    result_end = data_transpose(result, index_zahl)
    # Вывод результатов
    return result_end
    #save_file(result_end, 'Сохранить файл результатов анализа ISSR')
