#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime as dt
import peewee as pw
from setting import DB as db


class Logs(pw.Model):
    name = pw.CharField(
        max_length=10,
        verbose_name='место вызова',
    )
    data_job = pw.DateTimeField(default=dt.datetime.now)

    class Meta:
        database = db


class BaseModelAnimal(pw.Model):
    id = pw.AutoField()
    name = pw.CharField(
        verbose_name='Кличка животного',
        max_length=20,
        null=True,
    )
    number = pw.IntegerField(
        null=False,
        verbose_name='Инвертарный номер животного',
    )
    farm = pw.CharField(
        verbose_name='Название хозяйства',
        max_length=100,
        null=True,
    )
    BM1818 = pw.CharField(
        default='-',
        max_length=10,
    )
    BM1824 = pw.CharField(
        default='-',
        max_length=10,
    )
    BM2113 = pw.CharField(
        default='-',
        max_length=10,
    )
    CSRM60 = pw.CharField(
        default='-',
        max_length=10,
    )
    CSSM66 = pw.CharField(
        default='-',
        max_length=10,
    )
    CYP21 = pw.CharField(
        default='-',
        max_length=10,
    )
    ETH10 = pw.CharField(
        default='-',
        max_length=10,
    )
    ETH225 = pw.CharField(
        default='-',
        max_length=10,
    )
    ETH3 = pw.CharField(
        default='-',
        max_length=10,
    )
    ILSTS6 = pw.CharField(
        default='-',
        max_length=10,
    )
    INRA023 = pw.CharField(
        default='-',
        max_length=10,
    )
    RM067 = pw.CharField(
        default='-',
        max_length=10,
    )
    SPS115 = pw.CharField(
        default='-',
        max_length=10,
    )
    TGLA122 = pw.CharField(
        default='-',
        max_length=10,
    )
    TGLA126 = pw.CharField(
        default='-',
        max_length=10,
    )
    TGLA227 = pw.CharField(
        default='-',
        max_length=10,
    )
    TGLA53 = pw.CharField(
        default='-',
        max_length=10,
    )
    MGTG4B = pw.CharField(
        default='-',
        max_length=10,
    )
    SPS113 = pw.CharField(
        default='-',
        max_length=10,
    )

    class Meta:
        database = db


class BullFather(BaseModelAnimal):
    """Хранение данных по отцам."""

    class Meta:
        verbose_name = 'Отцы животных'
        table_name = 'BullFather'


class DescendantCow(BaseModelAnimal):
    '''Хранение данных по потомкам.'''
    fater = pw.ForeignKeyField(BullFather, related_name='father')
    data_job = pw.DateTimeField(default=dt.datetime.now)

    class Meta:
        verbose_name = 'Животные потомки'
        table_name = 'DescendantCow'


class InvertoryCows(pw.Model):
    """"""
    id = pw.AutoField()
    number = pw.IntegerField(
        null=False,
        verbose_name='Инвертарный номер животного',
    )
    name = pw.CharField(
        verbose_name='Кличка животного',
        max_length=20,
        null=True,
    )
    code_sample = pw.IntegerField(
        verbose_name='Код пробы',
        null=True,
    )
    number_father = pw.IntegerField(
        verbose_name='Номер отца',
        null=True,
    )
    name_father = pw.CharField(
        verbose_name='Кличка отца',
        max_length=20,
        null=True,
    )
    number_muter = pw.IntegerField(
        verbose_name='Номер матери',
        null=True,
    )
    name_muter = pw.CharField(
        verbose_name='Кличка матери',
        max_length=20,
        null=True,
    )

    class Meta:
        database = db
        verbose_name = 'Опись коров'
        table_name = 'InvertoryCows'


class InvertoryCowsExample(InvertoryCows):
    """"""
    id = pw.AutoField()
    number = pw.IntegerField(
        null=False,
        verbose_name='Инвертарный номер животного',
    )
    BM1818_1 = pw.CharField(
        default='-',
        max_length=10,
    )
    BM1818_2 = pw.CharField(
        default='-',
        max_length=10,
    )
    BM1824_1 = pw.CharField(
        default='-',
        max_length=10,
    )
    BM1824_2 = pw.CharField(
        default='-',
        max_length=10,
    )
    BM2113_1 = pw.CharField(
        default='-',
        max_length=10,
    )
    BM2113_2 = pw.CharField(
        default='-',
        max_length=10,
    )
    CSRM60_1 = pw.CharField(
        default='-',
        max_length=10,
    )
    CSRM60_2 = pw.CharField(
        default='-',
        max_length=10,
    )
    CSSM66_1 = pw.CharField(
        default='-',
        max_length=10,
    )
    CSSM66_2 = pw.CharField(
        default='-',
        max_length=10,
    )
    CYP21_1 = pw.CharField(
        default='-',
        max_length=10,
    )
    CYP21_2 = pw.CharField(
        default='-',
        max_length=10,
    )
    ETH10_1 = pw.CharField(
        default='-',
        max_length=10,
    )
    ETH10_2 = pw.CharField(
        default='-',
        max_length=10,
    )
    ETH225_1 = pw.CharField(
        default='-',
        max_length=10,
    )
    ETH225_2 = pw.CharField(
        default='-',
        max_length=10,
    )
    ETH3_1 = pw.CharField(
        default='-',
        max_length=10,
    )
    ETH3_2 = pw.CharField(
        default='-',
        max_length=10,
    )
    ILSTS6_1 = pw.CharField(
        default='-',
        max_length=10,
    )
    ILSTS6_2 = pw.CharField(
        default='-',
        max_length=10,
    )
    INRA023_1 = pw.CharField(
        default='-',
        max_length=10,
    )
    INRA023_2 = pw.CharField(
        default='-',
        max_length=10,
    )
    RM067_1 = pw.CharField(
        default='-',
        max_length=10,
    )
    RM067_2 = pw.CharField(
        default='-',
        max_length=10,
    )
    SPS115_1 = pw.CharField(
        default='-',
        max_length=10,
    )
    SPS115_2 = pw.CharField(
        default='-',
        max_length=10,
    )
    TGLA122_1 = pw.CharField(
        default='-',
        max_length=10,
    )
    TGLA122_2 = pw.CharField(
        default='-',
        max_length=10,
    )
    TGLA126_1 = pw.CharField(
        default='-',
        max_length=10,
    )
    TGLA126_2 = pw.CharField(
        default='-',
        max_length=10,
    )
    TGLA227_1 = pw.CharField(
        default='-',
        max_length=10,
    )
    TGLA227_2 = pw.CharField(
        default='-',
        max_length=10,
    )
    TGLA53_1 = pw.CharField(
        default='-',
        max_length=10,
    )
    TGLA53_2 = pw.CharField(
        default='-',
        max_length=10,
    )
    MGTG4B_1 = pw.CharField(
        default='-',
        max_length=10,
    )
    MGTG4B_2 = pw.CharField(
        default='-',
        max_length=10,
    )
    SPS113_2 = pw.CharField(
        default='-',
        max_length=10,
    )
    SPS113_1 = pw.CharField(
        default='-',
        max_length=10,
    )

    class Meta:
        verbose_name = 'Опись коров (пример)'
        table_name = 'InvertoryCowsExample'


class ProfilsCows(BaseModelAnimal):
    """"""
    class Meta:
        database = db
        verbose_name = 'Результаты генотипирования коровы'
        table_name = 'ProfilsCows'


class ProfilsCowsForPassword(BaseModelAnimal):
    """"""
    class Meta:
        database = db
        verbose_name = 'Результаты генотипирования для подбора матерей'
        table_name = 'ProfilsCows'


class ProfilsCowsExample(BaseModelAnimal):
    """"""
    class Meta:
        database = db
        verbose_name = 'Результаты генотипирования коровы пример'
        table_name = 'ProfilsCows'


ProfilsCows.create_table()
ProfilsCowsExample.create_table()
InvertoryCowsExample.create_table()
InvertoryCows.create_table()
ProfilsCows.create_table()
ProfilsCowsForPassword.create_table()
Logs.create_table()
BullFather.create_table()
DescendantCow.create_table()
