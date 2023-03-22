#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
from logging.handlers import RotatingFileHandler
import os
import configparser
import pandas as pd
import numpy as np
import requests
import datetime
from docx import Document as Document_compose
from docxcompose.composer import Composer
from docxtpl import DocxTemplate, RichText
from PyQt5.QtWidgets import (QAbstractItemView, QAbstractScrollArea,
                             QFileDialog, QMessageBox, QTableWidget,
                             QTableWidgetItem)

from code_app import models
from setting import log_file, config_file, dict_paths
from bs4 import BeautifulSoup
from func.func_answer_error import answer_error

logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG,
    filemode='w',
)
my_handler = RotatingFileHandler(
    log_file,
    mode='a',
    maxBytes=5*1024*1024,
    backupCount=2,
    encoding="cp1251",
    delay=0
)

logger = logging.getLogger(__name__)
logger.addHandler(my_handler)


class Manager:
    def __init__(self) -> None:
        pass


class DataFixManager(Manager):
    def __init__(self) -> None:
        super().__init__()
        self.create_fix_data()

    def create_fix_data(self):
        self.list_name_row_add_father = [
            'Имя',
            'Инвертарный номер',
            'Хозяйство',
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

        self.list_name_row_search_father = [
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


class ManagerUtilities(Manager):
    def __init__(self) -> None:
        pass

    @staticmethod
    def is_float(s: str) -> bool:
        """
        Возвращает ответ является ли строка числом с плавующей точкой.

        Параметры:
        ----------
            s: str - Строка для проверки.
        Возвращает:
        -------
            bool - Число/Не число.
        """
        try:
            float(s)
            return True
        except ValueError:
            return False

    @staticmethod
    def result_to_table(df_res: pd.DataFrame) -> QTableWidget:
        """
        Возвращает таблицу виджета.

        Параметры:
        ----------
            df_res: pd.DataFrame - Выводимый датасет.
        Возвращает:
        -----------
            table: QTableWidget - Таблица виджета.
        """
        table = QTableWidget()
        table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.setColumnCount(len(df_res.columns))
        table.setRowCount(len(df_res))
        try:
            columns = df_res.columns
            table.setHorizontalHeaderLabels(columns)
        except Exception as e:
            logger.error(e)

        for column in range(len(df_res.columns)):
            for row in range(len(df_res)):
                item = QTableWidgetItem(str(df_res.iloc[row, column]))
                table.setItem(row, column, item)
        return table

    @staticmethod
    def delit(row: pd.Series, delitel: str, col: str) -> str:
        '''
        Возвращает выдленнное значение из нужного столбца строки по делителю.
        Заточена под apply.
        Параметры:
        ----------
            row: pd.Series - Набор данных.
            delitel: str - Разделитель.
            col: str - Название столбца для отбора.

        Возвращает:
        -----------
            num: str - Выделенный номер.
        '''
        try:
            num = row[col].split(delitel)[-1]
            return num
        except Exception as e:
            logger.error(e)
            logger.error(col)
            logger.error(str(row[col]))


class ManagerDataMS(Manager):
    def __init__(self, farm: str, model: models.BaseModelAnimal) -> None:
        self._farm = farm
        self._model = model
        self._locus_list = model.get_filds()[4:]
        self.__manager_db = ManagerDB()
        self.__manager_utilites = ManagerUtilities()
        self.__manager_files = ManagerFile()
        self.__manager_parser = ParserData()
        self._list_names_columns_dataset = [
                'number_animal',
                'name_animal',
                'number_sample',
                'number_mutter',
                'name_mutter',
                'number_father',
                'name_father',
            ]

        self._list_numeric_columns = [
            'number_animal',
            'number_sample',
            'number_mutter',
            'number_father',
        ]
        self.__maneger_utilites = ManagerUtilities()
        self.__maneger_files = ManagerFile()
        self.__parser_data = ParserData()

    def loading_data_invertory(self, address: str) -> None:
        self.dataset_inverory: pd.DataFrame = (
            self.__manager_files.read_file(address)
        )
        self.preprocessing_invertory()

    def preprocessing_invertory(self):
        # Выделение нужных столбцов
        self.dataset_inverory = self.dataset_inverory.iloc[:, :8]
        df_data_bull: pd.DataFrame = self.dataset_inverory.iloc[:, 5:8]
        if len(df_data_bull) == 3:
            self.transform_data_for_database(df_data_bull, self._farm)

        self.dataset_inverory = self.dataset_inverory.iloc[:, :7]
        self.dataset_inverory.columns = self._list_names_columns_dataset
        if (self._model == models.Bull):
            self.__manager_parser.add_missing_father(
                self.dataset_inverory,
                self._farm
            )

        # Приведение типов
        self.dataset_inverory = self.dataset_inverory.astype('str')
        for col in self._list_numeric_columns:
            self.dataset_inverory[col] = pd.to_numeric(
                self.dataset_inverory[col],
                downcast='integer'
            )

    def loading_data_profils(self, address: str) -> None:
        self.dataset_profils: pd.DataFrame = (
            self.__manager_files.read_file(address)
        )
        self.preprocessing_profils()

    def preprocessing_profils(self) -> None:
        # Выделение номеров проб
        self.dataset_profils['num'] = self.dataset_profils.apply(
            self.__manager_utilites.delit,
            delitel='-',
            col='Sample Name',
            axis=1
        )
        # Приведение типов
        self.dataset_profils.drop(['Sample Name'], axis=1, inplace=True)
        self.dataset_profils = self.dataset_profils.fillna(0).astype('int')

        # Предобработка данных по микросателлитам
        list_col: list = []
        for i in range(1, len(self.dataset_profils.columns), 2):
            j = i + 1
            col1 = self.dataset_profils.columns[i]
            col2 = self.dataset_profils.columns[j]
            col_split = col1.upper().split()[0]
            self.dataset_profils[col_split] = self.dataset_profils.apply(
                self.ms_join,
                col1=col1,
                col2=col2,
                axis=1
            )
            list_col.append(col_split)

        self.dataset_profils = self.dataset_profils[["num"] + list_col]

    def filter_father(
            self,
            farms: dict,
            model_father: models.BaseModelAnimal = models.Bull
            ) -> pd.DataFrame:
        """
        Возвращает отфильтрованный датасет по хозяйствам.

        Параметры:
        ----------
            farms: dict - набор хозяйств, котроые должны остаться.
            model_father = models.Bull - Модель для подбора отцов
        Возвращает:
        -----------
            df_res: pd.DataFrame - Отфильтрованный датасет.
        """
        logger.debug("Start filter_father")
        df_fathers = self.__manager_db.get_data_for_animals(model=model_father)
        if farms.get('Выбрать всех', False):
            return df_fathers

        list_farms = []
        for key, item in farms.items():
            if item:
                if key != 'Выбрать всех':
                    list_farms.append(key)

        list_fathers = []
        for i in range(len(df_fathers)):
            if df_fathers.loc[i, "farm"] in list_farms:
                list_fathers.append(df_fathers.iloc[i, :])

        df_res = pd.DataFrame(data=list_fathers).reset_index(drop=True)
        logger.debug("End filter_father")
        return df_res

    def search_father(self, adres: str, filter_farms: dict) -> pd.DataFrame:
        """Поиск возможных отцов.
        Возвращает датасет с отцами подходящими по ген по паспорту.

        Параметры:
        ----------
            adres: str - Файл с генотипом для побора отцов.
            filter_farms: dict - Набор хозяйств для фильтрации.
        Возвращает:
        -----------
            df_res: pd.DataFrame - Датасет с отобранными отцами.
        """
        try:
            logger.debug("Start add_search_father")
            logger.debug("Load data father")
            df = self.filter_father(filter_farms)

            logger.debug("Data transform")
            df_search = self.__manager_files.read_file(adres)
            df_search = df_search.T
            df = df.fillna('-').replace('  ', '')
            df_search = df_search.fillna('-').reset_index()
            df_search.columns = df_search.loc[0, :]
            df_search = df_search.drop(0).reset_index(drop=True)
            df.reset_index(drop=True, inplace=True)

            logger.debug("Cycle search")
            for col in df_search.columns[1:]:
                for j in range(0, len(df)):
                    logger.debug(
                        f"Cycle search: col - {col}, j - {j}," +
                        f" len df_s_col - {len(df_search.columns)}," +
                        f"  len df_r - {len(df)}"
                    )

                    if df_search.loc[0, col] != '-':
                        logger.debug("Comparison, level 1")
                        locus = df_search.loc[0, col].strip().split('/')
                        if (
                            df.loc[j, col] != '-' and
                            str(df.loc[j, col]) != 'nan'
                        ):
                            locus_base = df.loc[j, col].strip().split('/')
                            logger.debug("Comparison search_father")
                            logger.debug("locus" + str(locus))
                            logger.debug("locus_base" + str(locus_base))
                            if (
                                locus[0] != locus_base[0] and
                                locus[1] != locus_base[0] and
                                locus[0] != locus_base[1] and
                                locus[1] != locus_base[1]
                            ):
                                logger.debug("Inner comparison")
                                df.loc[j, col] = np.nan

                df = df.dropna().reset_index(drop=True)
            logger.debug("Cycle end")
            df.to_csv(
                r'func\data\search_fatherh\father_searched.csv',
                sep=';',
                decimal=',',
                encoding='cp1251'
            )
            logger.debug("End search_father")
            return df

        except Exception as e:
            logger.error("Error search_father")
            logger.error(e)
            QMessageBox.critical(
                None,
                'Ошибка',
                f'{answer_error()}\nПодробности:\n {e}'
            )

    def ms_from_word(self, adres: str) -> pd.DataFrame:
        """
        Возвращает распарсинные данные по генетическим паспортам
        из документов Word.

        Параметры:
        ----------
            adres: str - Адрес для прочтения файла.
        Возвращает:
        ----------
            result: pd.DataFrame - Результат парсинга.
        """
        doc: pd.DataFrame = self.__manager_files.read_file(adres)
        doc.columns = ['ms', 'ms_size', 'vater', 'mom']
        msatle: list = (
            [
                'name_animal',
                'numer_animal',
                'name_father',
                'number_vater'
            ] + self.__list_locus
        )
        result = pd.DataFrame(columns=msatle)
        for j in range(4, len(msatle)):
            ms_r = msatle[j]
            self.ms_select(doc, result, ms_r, j)
        result = result.reset_index()
        self.name_select(doc, result)
        result = result.transpose()
        result.to_csv(
            r'func\data\ms_word\data_ms_from_word.csv',
            sep=";",
            decimal=',',
            encoding="cp1251"
        )
        return result

    def ms_select(
        self,
        data_in: pd.DataFrame,
        data_out: pd.DataFrame,
        ms: str,
        no: int
    ) -> None:
        """
        Собирает данные по МС.

        Параметры:
        ----------
            data_in: pd.DataFrame - Входной датасет.
            data_out: pd.DataFrame - Выходной датасет.
            ms: str - Название МС.
            no: int - Номер МС в списке.

        Возвращает:
        -----------
            None
        """
        for i in range(len(data_in)):
            if data_in.loc[i, 'ms'] == ms:
                res = data_in.loc[i, 'ms_size']
                nom_date_out = i - no + 4
                data_out.loc[nom_date_out, ms] = res

    def name_select(
        self,
        data_in: pd.DataFrame,
        data_out: pd.DataFrame
        ) -> None:
        """
        Отбор кличек и номеров.

        Параметры:
        ----------
            data_in: pd.DataFrame - Входной датасет.
            data_out: pd.DataFrame - Выходной датасет.
        Возвращает:
        -----------
            None
        """
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
                    logger.error(e)
                    data_out.loc[nom_date_out, 'numer'] = res_name[0]
                try:
                    data_out.loc[nom_date_out, 'vater'] = res_vater[0]
                    data_out.loc[nom_date_out, 'number_vater'] = res_vater[1]
                except Exception as e:
                    logger.error(e)
                    data_out.loc[nom_date_out, 'number_vater'] = res_vater[0]

    def verification_ms(self, one_ms: str, second_ms: str) -> bool:
        """Возращает True, если данные МС неподходят

        Параметры:
        ----------
            one_ms: str - Первый набор МС.
            second_ms: str - Второй набор МС.
        Возвращает:
        ----------
            res: bool - Неподходит/подходит.
        """
        logger.debug("start verification_ms")
        logger.debug(f"Input data: {one_ms}, {second_ms}")
        one_ms = one_ms.replace(" ", '')
        second_ms = second_ms.replace(" ", '')
        res = False
        one_split = one_ms.split('/')
        second_split = second_ms.split('/')
        if (
            int(one_split[0]) != int(second_split[0]) and
            int(one_split[0]) != int(second_split[1]) and
            int(one_split[1]) != int(second_split[0]) and
            int(one_split[1]) != int(second_split[1])
        ):
            res = True
        logger.debug(f"result {res}")
        logger.debug("end verification_ms")
        return res

    def data_verification(self, context: dict) -> dict:
        """
        Возвращает имзенный контекст с пометками ошибок.

        Параметры:
        ----------
            context: dict - Входящий словарь данных.
        Возвращает:
        -----------
            context: dict - Изменный словарь данных.
        """
        logger.debug("start data_verification")
        flag_mutter, flag_father, flag_null_mutter, flag_null_father = (
            False, False, False, False
        )
        number_null_mutter, number_null_father = 0, 0
        for key in self._locus_list:
            child = context.get(key, context.get(key.replace("0", "")))
            father = context.get(key+'_father')
            mutter = context.get(key+'_mutter')
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
                if self.verification_ms(child, father):
                    flag_father = True
                    context[key] = RichText(
                        context.get(key, context.get(key.replace("0", ""))),
                        color='#ff0000',
                        bold=True
                    )
                    context[key.replace("0", "")] = RichText(
                        context.get(key, context.get(key.replace("0", ""))),
                        color='#ff0000',
                        bold=True
                    )
                    context[key+'_father'] = RichText(
                        context.get(key+'_father'),
                        color='#ff0000',
                        bold=True
                    )
            else:
                number_null_father += 1
                if number_null_father > 10:
                    flag_null_father = True
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
                if self.verification_ms(child, mutter):
                    flag_mutter = True
                    context[key] = RichText(
                        context.get(key),
                        color='#ff0000',
                        bold=True
                    )
                    context[key.replace("0", "")] = RichText(
                        context.get(key, context.get(key.replace("0", ""))),
                        color='#ff0000',
                        bold=True
                    )
                    context[key+'_mutter'] = RichText(
                        context.get(key+'_mutter'),
                        color='#ff0000',
                        bold=True
                    )
            else:
                number_null_mutter += 1
                if number_null_mutter > 10:
                    flag_null_mutter = True

        logger.debug("end data_verification")
        if flag_father and flag_mutter:
            conclusion = 'Родители не соответствуют'
        elif flag_father:
            conclusion = 'Отец не соответствует'
        elif flag_mutter or flag_null_mutter:
            conclusion = 'Отец соответствует'
        elif not flag_null_mutter and not flag_null_father:
            conclusion = 'Родители соответствуют'
        else:
            conclusion = ''
        context['conclusion'] = conclusion
        return context

    def split__(self, str_input: str) -> list:
        return str_input.split("_")

    def split_locus(self, row: str) -> pd.Series:
        list_in_locus = row.split("  - ")
        return pd.Series(dict(map(self.split__, list_in_locus)))

    def transform_data_for_database(
            self,
            data: pd.DataFrame,
            farm: str
            ) -> None:
        """
        Трансформирует данные по отцам и передает в базу данных.
        Параметры:
        ----------
            data: pd.DataFrame - Датасет с профилем отца
            farm: str - Название хозяйства.
        Возвращает:
        ----------
            None
        """
        df: pd.DataFrame = data.iloc[:, [0, 1, 2]]
        df.columns = ["number", "name", "prof"]

        df = df.dropna().drop_duplicates(
            subset=['number']
        ).reset_index(drop=True)

        df[self.__list_locus] = "-"
        res: pd.Series = df['prof'].apply(self.split_locus)

        for col in self.__list_locus:
            if col in res.columns:
                df[col] = res[col]

        df.fillna('-', inplace=True)
        df['prof'] = farm
        df.rename(
            columns={
                "prof": "farm",
                "number": "number_animal",
                "name": "name_animal",
                },
            inplace=True
        )
        for i in range(len(df)):
            temp = (df.iloc[i, :]).reset_index(drop=True)
            self.__manager_db.save_data_bus_to_db(temp.to_dict(), BullFather)

    def save_text_to_file(
            self,
            data: dict,
            adress: str = r'data\log\log_error_profils.txt'
            ) -> None:
        """
        Сохраняет данные в файл.
        Параметры:
        ----------
            data: dict - данные об ошибках.
                not_father: list - Номера отцов.
                not_animal: list - Номера проб.
                father: list - Номера животных с ошибками по отцу.
                mutter: list - Номера животных с ошибками по матери.
        Возвращает:
        -----------
            None.
        """
        logger.debug("start save_text_to_file")
        with open(adress, "w+") as f:
            logger.debug("write data to file")
            for key, val in data.items():
                str_res: str = f"{key}: {val}\n"
                f.write(str_res)
        logger.debug("end save_text_to_file")

    def get_summary_data_error(self, errors: dict) -> dict:
        """
        Анализирует и возвращает данные об ошибках.
        Параметры:
        ----------
            df_error: dict - данные об ошибках.
            Ожидамые ключи:
                not_father: list - Номера отцов
                not_animal: list - Номера проб
                father: pd.DataFrame - columns: number	locus	parent	animal	male
                mutter: pd.DataFrame - columns: number	locus	parent	animal	male

        Возвращает:
        -----------
            result: dict - Сводные данные по ошибкам.
        """
        logger.debug("start analys_error")
        result: dict = {
            "not_animal": list(set(errors.get("not_animal"))),
            "not_father": list(set(errors.get("not_father"))),
        }
        logger.debug("cycle transport data to dict")
        for key in ["father", "mutter"]:
            temp: pd.DataFrame = errors.get(key)
            temp.drop_duplicates(subset="animal", inplace=True)
            result[key] = list(set(temp["animal"]))

        logger.debug("end analys_error")
        return result

    def ms_join(
            self,
            row: pd.Series,
            col1: str,
            col2: str,
            sep: str = "/") -> str:
        '''
        Возвращает объединенное значение выделенных строк через знак.
        Заточена под apply.
        Параметры:
        ----------
            row: pd.Series - Набор данных.
            col1: str - Первый столбец.
            col2: str - Второй столбец.
            sep: str - Разделитель
        Возвращает:
        -----------
            ms0: str - Объединенные значения
        '''
        ms1 = row[col1]
        ms2 = row[col2]
        join_ms = [str(ms1), str(ms2)]
        ms0 = sep.join(join_ms)
        return ms0

    def combine_all_docx(
        self,
        filename_master: str,
        files_list: list,
        adres: str,
        ) -> None:
        '''
        Сбор документа для Word.
        Параметры:
        ----------
            filename_master: str - Название выходного файла.
            files_list: list - Лист названий промежуточных файлов.
            adres: str - Адрес места сохранения файла.
        Возвращает:
        -----------
            None
        '''
        number_sections = len(files_list)
        doc_m = Document_compose(filename_master)
        composer = Composer(doc_m)
        for i in range(0, number_sections):
            doc_temp = Document_compose(files_list[i])
            composer.append(doc_temp)
        composer.save(adres)

    def creat_doc_pas_gen(
        self,
        adress_invertory: str,
        adress_genotyping: str,
        adres: str,
        model_fater: models.BaseModelAnimal = models.Bull,
        model_mutter: models.BaseModelAnimal = models.Cow,
        model_descendant: models.BaseModelAnimal = models.Cow,
        flag_mutter: bool = False
    ) -> pd.DataFrame:
        """
        Создает паспорта генетические. Созраняет по адресу.
        Возвращает данные по ошибкам.

        Параметры:
        ----------
            adres_invertory: str - Адрес описи.
            adres_genotyping: str - Адрес результатов.
            adres: str - Адрес сохранения паспортов.
            farm: str = 'Хозяйство' - Название хозяйства.
            model_fater: models.BaseModelAnimal = models.Bull -
                модель для отца,
            model_mutter: models.BaseModelAnimal = models.Cow -
                модель для матери,
            model_descendant: models.BaseModelAnimal = models.Cow -
                модель для потомка,
            flag_mutter: bool = False - Нужна ли проверка матерей.
        Возвращает:
        -----------
            res_err: pd.DataFrame - Данные по ошибкам.
        """
        logger.debug("start creat_doc_pas_gen")

        species = model_descendant.get_title()
        now = datetime.datetime.now()
        date = now.strftime("%d-%m-%Y")
        self.loading_data_invertory(adress_invertory)
        self.loading_data_profils(adress_genotyping)
        dataset_faters: pd.DataFrame = (
            self.__manager_db.get_data_for_animals(model_fater)
        )
        list_number_faters = list(dataset_faters.loc[:, 'number'])
        numbers_sample_from_profil = list(self.dataset_profils['num'])
        numbers_sample_from_invertory = list(
            self.dataset_inverory['number_sample']
        )

        dict_error: dict = {}
        dict_error['not_father'] = []
        dict_error['not_animal'] = []

        logger.debug("start cycle create pass")
        files_list = []
        for i in range(len(numbers_sample_from_invertory)):
            doc = DocxTemplate(
                dict_paths.get("templates_pass").get(species)
            )
            context = {}
            if numbers_sample_from_invertory[i] in numbers_sample_from_profil:
                num_sample = numbers_sample_from_invertory[i]
                info = self.dataset_inverory.query(
                    'number_proba == @num_sample'
                ).reset_index()
                profil = self.dataset_profils.query(
                    'num == @num_sample'
                ).reset_index()

                number_animal: int = info.loc[0, 'number_animal']
                name_animal: int = info.loc[0, 'name_animal']
                number_father: int = info.loc[0, 'number_father']
                name_father: str = info.loc[0, 'name_father']
                number_mutter: int = int(info.loc[0, 'number_mutter'])
                name_mutter: str = info.loc[0, 'name_mutter']
                animal_join: str = [name_animal, str(number_animal)]
                fater_join: str = [name_father, str(number_father)]
                mutter_join: str = [name_mutter, str(number_mutter)]

                context['number_animal'] = number_animal
                context['name_animal'] = name_animal
                context['farm'] = self._farm
                context['number_father'] = number_father
                context['name_father'] = name_father
                context['animal'] = ' '.join(animal_join)
                context['father'] = ' '.join(fater_join)
                context['mutter'] = ' '.join(mutter_join)
                context['date'] = date

                dict_profil = profil.loc[0, :].to_dict()
                context = {**context, **dict_profil}
                self.__manager_db.save_data_animal_to_db(
                    context,
                    model_descendant
                )

                if number_father in list_number_faters:
                    father = (dataset_faters.query(
                        'number == @number_father'
                    ).reset_index(drop=True))
                    father = father.loc[0, :].to_dict()
                    dict_fater = {}
                    for key, val in father.items():
                        dict_fater[key+"_father"] = val
                    context = {**context, **dict_fater}
                else:
                    dict_error['not_father'].append(number_father)
            else:
                dict_error['not_animal'].append(num_sample)

            if flag_mutter:
                mutter = (
                    self.__manager_db.get_data_for_animal(
                        number_mutter,
                        model_mutter
                    )
                )
                dict_mutter = {}
                for key, val in mutter.items():
                    dict_mutter[key+"_mutter"] = val

                context = {**context, **dict_mutter}
            context = self.data_verification(context)
            doc.render(context)
            doc.save(str(i) + ' generated_doc.docx')
            title = str(i) + ' generated_doc.docx'
            files_list.append(title)

        logger.debug("start cycle create word doc")
        filename_master = files_list.pop(0)
        self.combine_all_docx(filename_master, files_list, adres, date)
        files_list.append(filename_master)
        for i in range(len(files_list)):
            if os.path.isfile(files_list[i]):
                os.remove(files_list[i])
            else:
                print("File doesn't exists!")
        logger.debug("end cycle create word doc. Return")

        # Сохраняем данные об ошибках в файл в логе.
        self.save_text_to_file(self.get_summary_data_error(dict_error))


class ManagerDataISSR(Manager):
    def __init__(self) -> None:
        self.__manager_file: ManagerFile = ManagerFile()
        self.__list_size: list = [
            2500, 2300, 2000, 1800, 1700, 1600, 1500, 1400, 1300,
            1240, 1180, 1120, 1060, 1000, 940, 880, 820, 760, 720,
            680, 640, 600, 560, 530, 500, 470, 440, 410, 380, 360,
            340, 320, 300, 280, 260, 240, 220, 200, 160,
        ]

    def get_allel_label(self, size: int, genotype: str = "G") -> str:
        """Функция определения принадлежности данных к аллели.
        Описание

        Параметры:
        ----------
            size: int - размер фрагмента
            genotype: str = "G" - вариант генотипа
        Возвращает:
        ----------
            str - название аллели
        """
        temp_i = None
        genotype_result = "-"
        if size > 2500 or size < 160:
            genotype_result = "-"
        else:
            temp_i = self.binary_search(
                self.__list_size,
                0,
                len(self.__list_size)-1,
                size
            )
            genotype_result = genotype + str(temp_i)
        return genotype_result

    def genotype_issr(self, row: pd.Series, allel: str = "G") -> str:
        """Функция определения принадлежности данных к аллели.
        Адаптер под apply.
        Описание

        Параметры:
        ----------
            row: pd.Series, axis=1 - строка датасета
            genotype: str = "G" - вариант генотипа
        Возвращает:
        ----------
            str - название аллели
        """
        dict_genotype = {
            "G": "GA",
            "A": "AG"
        }
        size = row[dict_genotype.get(allel)]
        return self.get_allel_label(size, allel)

    def binary_search(self, data: list, low, hight, n) -> int:
        if hight == low:
            return low
        mid = (hight + low) // 2
        if data[mid] == n:
            return mid

        if data[mid] < n:
            return self.binary_search(data, low, mid, n)
        else:
            return self.binary_search(data, mid + 1, hight, n)

    def data_transpose(
            self,
            df: pd.DataFrame,
            index_values: pd.DataFrame
            ) -> pd.DataFrame:
        """
        Возвращает транспонированную таблицу для вывода данных.

        Параметры:
        ----------
            df: pd.DataFrame - Данные фрагментов.
            index_values: pd.DataFrame - Датасет индексов.
        Возвращает:
        -----------
            result: pd.DataFrame
        """
        result = pd.DataFrame()
        list_index = index_values['num'].round(0)
        df["animal"] = df["animal"].round(0)
        for index in set(list_index):
            number_select_samples = df.query(
                'animal == @index'
            ).reset_index(drop=True)
            result = result.append(
                number_select_samples.T
            )
        return result.reset_index()

    def create_indexes(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Функция выравнивания данных по номерам. Проходим по циклом
        по всему датасету.
        Если строка равна нулю, то она получает значение
        предыдущей строки с префиксом.
        Если нет, то остается имеющееся значение
        """
        for i in range(0, len(data)):
            j = i-1
            if data.loc[i, 'animal'] == 0.0 or data.loc[i, 'animal'] is None:
                animall = str(data.loc[j, 'animal'])
                animn = [animall, '99']
                data.loc[i, 'animal'] = ''.join(animn)
            else:
                data.loc[i, 'animal'] = data.loc[i, 'animal']
        return data

    def issr_analis(self, adress: str) -> pd.DataFrame:
        """
        Возвращает результаты анлиза данных по issr.
        Параметры:
        ----------
            adress: str - Адрес загрузки данных.
        Возвращает:
        -----------
            result: pd.DataFrame - Датасет с результами анализа.
        """
        self.__manager_file.set_path_for_file_to_open(adress)
        df = self.__manager_file.read_file()
        df.set_axis(
            ['animal', 'GA', 'animal_1', 'AG'],
            axis='columns',
            inplace=True
        )
        df[['animal', 'animal_1']] = df[['animal', 'animal_1']].fillna(0)

        # Предобработка
        dict_dataset: dict = {}
        for genotype in ["GA", "AG"]:
            df[genotype] = df[genotype].astype('str')
            df[genotype] = df[genotype].str.replace('\xa0', '')
            df[genotype] = df[genotype].str.replace(',', '.')
            df[genotype] = df[genotype].astype('float64')
            df[genotype] = df[genotype].fillna(0)
            temp = pd.DataFrame()
            temp['animal'] = df['animal']
            temp['genotype'] = df[genotype]
            dict_dataset[genotype] = self.create_indexes(temp)

        # Выравнивание с помощью соединения
        merge_data = dict_dataset.get("AG").merge(
             dict_dataset.get("GA"), on='animal', how='outer'
        ).reset_index()
        merge_data.set_axis(
            ['index', 'animal', 'AG', 'GA'],
            axis='columns',
            inplace=True
        )
        # Преобразование типов
        merge_data['animal'] = merge_data['animal'].astype('float64')
        merge_data['animal'] = round(merge_data['animal'])
        merge_data['animal'] = merge_data['animal'].astype('int64')
        merge_data[['AG', "GA"]] = merge_data[['AG', "GA"]].fillna(0)

        # Собственно анализ
        for genotype, allel in zip(["GA", "AG"], ["G", "A"]):
            merge_data[genotype + '_genotype'] = merge_data.apply(
                self.genotype_issr,
                allel=allel,
                axis=1
            )

        merge_data = merge_data[['animal', 'AG_genotype', 'GA_genotype']]

        # Возвращение первичных номеров животных
        index_values = pd.DataFrame(merge_data['animal'].value_counts())
        index_values = index_values.reset_index()
        index_values.columns = ['num', 'chast']
        index_values = index_values.sort_values('num', ascending=True)
        index_values = index_values.reset_index()
        # Фомирование выходных данных
        result_end = self.data_transpose(merge_data, index_values)
        return result_end


class ParserData:
    def __init__(self) -> None:
        self.__manager_db: ManagerDB = ManagerDB()

    def check_ms_in_cell(self, str_test: str) -> bool:
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

    def add_missing_father(
            self,
            df: pd.DataFrame,
            farm: str) -> None:
        """
        Возращает датасет с быками.
        Проверяет наличие быков в базе. При необходимости добавляет.
        ----------------------
        Параметры:
            df (pd.DataFrame): датасет по описи нетелей.
            ключи
                number: int
                name: str
                sample: int
                number_mother: int
                name_mother: str
                number_father: int
                name_father: str
            farm (str): название хозяйства.
        ----------------------
        Возвращаемое значение:
            None.
        """
        logger.debug("Start add_missing")
        logger.debug(df.head())

        df = df.dropna(subset=["number_father"])
        try:
            data_father: dict = (
                self.__manager_db.get_data_for_animals(model)
            )
            list_father_numbers: list = pd.DataFrame.from_dict(
                data_father
            ).number
            list_father_invertory: list = df["number_father"]

            for number_father in set(list_father_invertory):
                if number_father in list_father_numbers:
                    pass
                else:
                    logger.debug(
                        f"Number father {number_father}"
                    )
                    name_father = (
                        df[df["number_father"] == number_father]["name_father"]
                        .reset_index(drop=True)[0]
                    )
                    if 1 == self.parser_ms_father(
                        number_father,
                        name_father,
                        farm
                    ):
                        print('Не добавлено')
                    else:
                        print(f"Добавлен {number_father}")
            logger.debug("End add_missing")

        except Exception as e:
            logger.error(e)
            QMessageBox.critical(
                None,
                'Ошибка ввода',
                (f'{answer_error()} Подробности:\n {e}')
            )
            logger.debug("End add_missing")

    def parser_ms_father(self, number: int, name: str, farm: str) -> int:
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
            number_page, token = self.filter_id_bus(str(number), name)
            df = self.parser_ms(number_page, token)
            df = df.reset_index(drop=True)
            i = 0
            if df.iloc[0, 0] != 1:
                bus = {
                    "name": name,
                    "number": number,
                    "farm": farm,
                    "BM1818": df.loc[i, "BM1818"],
                    "BM1824": df.loc[i, "BM1824"],
                    "BM2113": df.loc[i, "BM2113"],
                    "CSRM60": df.loc[i, "CSRM60"],
                    "CSSM66": df.loc[i, "CSSM66"],
                    "CYP21": df.loc[i, "CYP21"],
                    "ETH10": df.loc[i, "ETH10"],
                    "ETH225": df.loc[i, "ETH225"],
                    "ETH3": df.loc[i, "ETH3"],
                    "ILSTS6": df.loc[i, "ILSTS6"],
                    "INRA023": df.loc[i, "INRA023"],
                    "RM067": df.loc[i, "RM067"],
                    "SPS115": df.loc[i, "SPS115"],
                    "TGLA122": df.loc[i, "TGLA122"],
                    "TGLA126": df.loc[i, "TGLA126"],
                    "TGLA227": df.loc[i, "TGLA227"],
                    "TGLA53": df.loc[i, "TGLA53"],
                    "MGTG4B": df.loc[i, "MGTG4B"],
                    "SPS113": df.loc[i, "SPS113"],
                }
                self.manager_db.save_data_bus_to_db(bus, BullFather)
                return 0
            else:
                return 1
        except Exception as e:
            QMessageBox.critical(
                None,
                'Ошибка ввода',
                f'{answer_error()}Подробности:\n {e}'
            )

    def parser_ms(self, number_page: int, token: str) -> dict:
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
                if self.check_ms_in_cell(str(row)):
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
                    'BM1818', 'BM1824', 'BM2113',
                    'CSRM60', 'CSSM66', 'CYP21',
                    'ETH10', 'ETH225', 'ETH3',
                    'ILSTS6', 'INRA023', 'RM067',
                    'SPS115', 'TGLA122', 'TGLA126',
                    'TGLA227', 'TGLA53', 'MGTG4B',
                    'SPS113'
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

    def filter_id_bus(self, number: str, name: str = '') -> list:
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
                print(
                    nickname,
                    name,
                    nickname == name,
                    nickname.lower() == name.lower()
                )
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


class ManagerFile(Manager):

    def save_path_file_for_pass(self, name_str: str = 'Save File') -> None:
        """Сохраняет в конфиг адрес сохранения паспортов"""
        path = ConfigMeneger.get_path("save")
        adres = QFileDialog.getSaveFileName(
            None,
            name_str,
            path,
            'Word (*.docx);; CSV (*.csv);; Text Files (*.txt)'
        )[0]
        after_path = '/'.join(adres.split('/')[:-1])
        ConfigMeneger.set_path(after_path, "save")

    def set_path_for_file_to_open(self, path: str) -> None:
        """Устанавливает пут для открытия файлов"""
        ConfigMeneger.set_path(path, "open")

    def save_path_for_file_to_open(self, name_str: str = 'Open File') -> None:
        """
        Сохраняет в конфиг адрес файла из диалогового окна открытия.
        Параметры:
        ----------
            name_str: str - Заголовок диалогового окна.
        Возвращает:
        -----------
            adres: str - Адрес файла.
        """
        path = ConfigMeneger.get_path("open")
        adres = QFileDialog.getOpenFileName(
            None,
            name_str,
            path,
            ' Excel (*.xlsx) ;; CSV (*.csv);; Text Files (*.txt)'
        )[0]
        after_path = '/'.join(adres.split('/')[:-1])
        ConfigMeneger.set_path(after_path, "open")

    def get_path_save_dataset_to_file(
            self,
            df_res: pd.DataFrame,
            name_str: str = 'Save File'
            ) -> None:
        """
        Сохраняет датасет по адресу сохранения из конфига.
        Параметры:
        ----------
            df_res: pd.DataFrame - Сохраняемый датасет.
            name_str: str - Заголовок диалогового окна.
        Возвращает:
        -----------
            adres: str - Адрес файла.
        """
        path = ConfigMeneger.get_path("save")
        adres = QFileDialog.getSaveFileName(
            None,
            name_str,
            path,
            'CSV (*.csv);; Text Files (*.txt)'
        )[0]
        after_path = '/'.join(adres.split('/')[:-1])
        ConfigMeneger.set_path(after_path, "save")
        df_res.to_csv(adres, sep=";", decimal=',')

    def read_file(self) -> pd.DataFrame:
        '''
        Возращает датасет, прочитанный из файла по полученному адресу.
        Параметры:
        ----------
            adres: str - Адрес расположения датасета.
        Возвращает:
        -----------
            df_doc: pd.DataFrame - Прочитанный датасет.
        '''
        adres = ConfigMeneger.get_path("open")
        adres_split = adres.split('.')
        df_doc: pd.DataFrame = pd.DataFrame()
        if adres_split[-1] == 'csv':
            df_doc = pd.read_csv(
                adres,
                sep=';',
                decimal=',',
                encoding='cp1251'
            )
        elif adres_split[-1] == 'txt':
            df_doc = pd.read_csv(
                adres,
                sep='\t',
                decimal=',',
                encoding='utf-8'
            )
        elif adres_split[-1] == 'xlsx':
            df_doc = pd.read_excel(adres)

        return df_doc


class ConfigMeneger(Manager):
    @staticmethod
    def createConfig():
        """
        Create a config file
        """
        path = config_file
        config = configparser.ConfigParser()
        config.add_section("AdressOpen")
        config.set(
            "AdressOpen",
            "adress_open",
            r"C:\Users\Пользователь\Desktop"
        )
        config.add_section("AdressSave")
        config.set(
            "AdressSave",
            "adress_save",
            r"C:\Users\Пользователь\Desktop"
        )
        with open(path, "w") as config_file_temp:
            config.write(config_file_temp)

    @staticmethod
    def get_path(mode: str) -> str:
        """
        Read config
        """
        path = config_file
        if not os.path.exists(path):
            ConfigMeneger.createConfig()

        config = configparser.ConfigParser()
        config.read(path)

        dict_mode = {
            "open": ["AdressOpen", "adress_open"],
            "save": ["AdressSave", "adress_save"],
        }
        adress_open = config.get(*dict_mode.get(mode))
        return adress_open

    @staticmethod
    def set_path(new_path_adress: str, mode: str) -> None:
        """
        Update config
        """
        path = config_file
        if not os.path.exists(path):
            ConfigMeneger.createConfig()

        config = configparser.ConfigParser()
        config.read(path)
        dict_mode = {
            "open": ["AdressOpen", "adress_open"],
            "save": ["AdressSave", "adress_save"],
        }
        config.set(*dict_mode.get(mode), new_path_adress)
        with open(path, "w") as config_file_temp:
            config.write(config_file_temp)


class ManagerDB(Manager):
    def __init__(self) -> None:
        self.__farms_set: set = None
        self.__dict_data_animal: dict = None
        self.__dict_data_animals: dict = None

    def get_farms(
            self,
            model: models.BaseModelAnimal = models.Cow
            ) -> set:
        """Возвращает инвентарные номера отцов."""
        if self.__farms_set is None:
            self.donwload_data_farmers(model)
        return self.__farms_set

    def get_data_for_animals(
            self,
            model: models.BaseModelAnimal = models.Cow
            ) -> dict:
        """Возвращает данные по животным из базы."""
        name_model_data: str = str(model)
        if self.__dict_data_animals.get(name_model_data, None) is None:
            self.donwload_data_for_animals(model)
        return self.__dict_data_animals.get(name_model_data)

    def get_data_for_animal(
            self,
            number: int,
            model: models.BaseModelAnimal = models.Cow
            ) -> dict:
        """Возвращает данные по животному из базы."""
        self.donwload_data_for_animal(number, model)
        return self.__dict_data_animal

    def save_data_animal_to_db(
            self,
            data: dict,
            model: models.BaseModelAnimal = models.Cow
            ) -> None:
        """
        Сохраняет данные по коровам в базу.
        ----------------------
        Параметры:
            data: dict - данные для сохранения в базу.
            Ключи: str
                number_animal
                farm
                name_animal
                MS....
            model: BaseModelAnimal - Модель хранения данных
        ----------------------
        Возвращаемое значение:
            None.
        """
        logger.debug("Start save_data_bus_to_db")
        query = model.select().where(
            model.number == data.get("number"),
            model.farm == data.get("farm"),
        )
        try:
            if query.exists():
                print(data.get("number"), 'существует.')
            else:
                model_data = model(
                    name=data.get("name", '-'),
                    number=data.get("number", '-'),
                    farm=data.get("farm", '-'),
                    BM1818=data.get("BM1818", '-'),
                    BM1824=data.get("BM1824", '-'),
                    BM2113=data.get("BM2113", '-'),
                    CSRM60=data.get("CSRM60", '-'),
                    CSSM66=data.get("CSSM66", '-'),
                    CYP21=data.get("CYP21", '-'),
                    ETH10=data.get("ETH10", '-'),
                    ETH225=data.get("ETH225", '-'),
                    ETH3=data.get("ETH3", '-'),
                    ILSTS6=data.get("ILSTS6", '-'),
                    INRA023=data.get("INRA023", '-'),
                    RM067=data.get("RM067", '-'),
                    SPS115=data.get("SPS115", '-'),
                    TGLA122=data.get("TGLA122", '-'),
                    TGLA126=data.get("TGLA126", '-'),
                    TGLA227=data.get("TGLA227", '-'),
                    TGLA53=data.get("TGLA53", '-'),
                    MGTG4B=data.get("MGTG4B", '-'),
                    SPS113=data.get("SPS113", '-'),
                )
                model_data.save()
                logger.debug("End save_data_bus_to_db")
        except Exception as e:
            logger.error(e)
            QMessageBox.critical(
                None,
                'Ошибка входящих данных',
                f'{answer_error()} Подробности:\n {e}'
            )
        logger.debug("End save_data_bus_to_db")

    def donwload_data_farmers(
            self,
            model: models.BaseModelAnimal = models.Bull
            ) -> None:
        """
        Загружает список хозяйств из базы данных.
        ----------------------
        Параметры:
            model: BaseModelAnimal = ProfilsCows -
                Модель по которой собираем данные.
        ----------------------
        Возвращаемое значение:
            res_set (set): список номеров отцов.
        """
        logger.debug("Start upload_data_farmers")

        self.__farms_set: list = []
        buses = model.select()
        for bus in buses:
            if bus.farm in self.__farms_set:
                pass
            else:
                self.__farms_set.append(bus.farm)
        self.__farms_set = set(self.__farms_set)
        logger.debug("End upload_data_farmers")

    def donwload_data_for_animal(
            self,
            number: int,
            model: models.BaseModelAnimal = models.Cow
            ) -> None:
        """
        Загружает данные по животному из базы.
        ----------------------
        Параметры:
            number (int): инвентарный номер животному.
        ----------------------
        Возвращаемое значение:
            res (dict): словарь с данными по животному.
        """
        logger.debug("Start donwload_data_for_animal")
        query = model.select().where(
            model.number == number
        )
        if query.exists():
            self.__dict_data_animal = model.select().where(
                model.number == number
            ).dicts().get()
            logger.debug("End donwload_data_for_animal")
        else:
            self.__dict_data_animal = {
                "name": "-",
                "number": "-",
                "farm": "-",
                "BM1818": '-',
                "BM1824": '-',
                "BM2113": '-',
                "CSRM60": '-',
                "CSSM66": '-',
                "CYP21": '-',
                "ETH10": '-',
                "ETH225": '-',
                "ETH3": '-',
                "ILSTS6": '-',
                "INRA023": '-',
                "RM067": '-',
                "SPS115": '-',
                "TGLA122": '-',
                "TGLA126": '-',
                "TGLA227": '-',
                "TGLA53": '-',
                "MGTG4B": '-',
                "SPS113": '-',
            }
            logger.debug("End donwload_data_for_animal")

    def donwload_data_for_animals(
            self,
            model: models.BaseModelAnimal = models.Cow
            ) -> None:
        """
        Загружает данные по животным из базы для поиска.
        ----------------------
        Параметры:
        ----------------------
        Возвращаемое значение:
            res (pd.DataFrame): датасет с данными по животным.
        """
        logger.debug("Start upload_data_for_animals")
        list_col = [
            'name', 'number', 'farm', 'BM1818', 'BM1824',
            'BM2113', 'CSRM60', 'CSSM66', 'CYP21', 'ETH10',
            'ETH225', 'ETH3', 'ILSTS6', 'INRA023', 'RM067',
            'SPS115', 'TGLA122', 'TGLA126', 'TGLA227', 'TGLA53',
            'MGTG4B', 'SPS113'
        ]
        df = pd.DataFrame(columns=list_col)
        i = 0
        for bus in model.select():
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
        self.__dict_data_animals[str(model)] = df.to_dict()
        logger.debug("End upload_data_for_animals")
