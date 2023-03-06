#!/usr/bin/python
# -*- coding: utf-8 -*-
import peewee as pw
import os

# База данных
DB: pw.SqliteDatabase = pw.SqliteDatabase('db.sqlite3')
DB_TEST: pw.SqliteDatabase = pw.SqliteDatabase('db_test.sqlite3')

# Включение странички для тестирования
IS_TEST: bool = True

# Включение прозрачности окна
TRANSPARENCY: bool = False

# Путь сохранения файла
path_save: str = r"C:\Users\Пользователь\Desktop"

# Путь для сохранения логов по МС
log_file: str = "./logs/log_preprocessor_ms_data.log"

# Путь для сохранения config
config_file: str = "./func/settings.ini"

BASE_PATH = r"func/data"

# Пути для загрузки и сохранения атефактов
dict_paths: dict = {
    "temp_doc_file": os.path.join(
        BASE_PATH,
        r'\creat_pass_doc\gen_pass_2.docx'
    ),
    "not_father": os.path.join(
        BASE_PATH,
        r'\creat_pass_doc\not_father.csv'
    ),
    "error_ms_father": os.path.join(
        BASE_PATH,
        r'\creat_pass_doc\res_error_father.csv'
    ),
    "error_ms_mutter": os.path.join(
        BASE_PATH,
        r'\creat_pass_doc\res_error_mutter.csv'
    ),
}
