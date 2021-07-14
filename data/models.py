#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime as dt
from peewee import *
DATE_FORMAT = '%d.%m.%Y'


db = SqliteDatabase('db.sqlite3')

class BaseModel(Model):
    class Meta:
        database = db


class MSSearchFater(BaseModel):
    """"""
    number = CharField(max_length=200)
    BM1818 = CharField(max_length=200)



MSSearchFater.create_table()