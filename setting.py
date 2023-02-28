#!/usr/bin/python
# -*- coding: utf-8 -*-
import peewee as pw

# База данных
DB = pw.SqliteDatabase('db.sqlite3')

# Включение странички для тестирования
IS_TEST = True

# Включение прозрачности окна
TRANSPARENCY = False

# Путь сохранения файла
path_save = r"C:\Users\Пользователь\Desktop"

# Путь для сохранения логов по МС
log_file = "./logs/log_preprocessor_ms_data.log"


# Путь для сохранения config
config_file = "./func/settings.ini"
