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


class Farm(pw.Model):
    id = pw.AutoField()
    farm = pw.CharField(
        verbose_name='Название хозяйства',
        max_length=100,
        null=False
    )
    species = pw.CharField(
        verbose_name='Вид',
        max_length=100,
        null=False,
        default="Cow"
    )

    def __str__(self) -> str:
        return f"{self.farm}"

    def __repr__(self) -> str:
        return f"{self.farm}"

    class Meta:
        database = db
        verbose_name = 'Хозяйства'
        table_name = 'Farms'


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
    farm = pw.ForeignKeyField(Farm, backref='Animals')

    @classmethod
    def get_filds(cls) -> list:
        return list(cls._meta.fields.keys())

    @classmethod
    def get_title(cls) -> str:
        return cls._meta.species

    def get_data(self) -> dict:
        return self.complement_data()

    def complement_data(self) -> dict:
        contex = self.__data__
        id_farm = contex.get("farm")
        query: pw.Model = Farm.select().where(Farm.id == id_farm)
        if query.exists():
            name_farm = Farm.select().where(Farm.id == id_farm).get()
            name_farm = name_farm.farm
            contex["farm"] = name_farm
        else:
            pass
            # print("Not data farm", contex)
        return contex

    class Meta:
        database = db
        species = "animal"
        verbose_name = 'Животные'


class ISSR(pw.Model):
    AG1 = pw.BooleanField(
        default=False,
    )
    AG2 = pw.BooleanField(
        default=False,
    )
    AG3 = pw.BooleanField(
        default=False,
    )
    AG4 = pw.BooleanField(
        default=False,
    )
    AG5 = pw.BooleanField(
        default=False,
    )
    AG6 = pw.BooleanField(
        default=False,
    )
    AG7 = pw.BooleanField(
        default=False,
    )
    AG8 = pw.BooleanField(
        default=False,
    )
    AG9 = pw.BooleanField(
        default=False,
    )
    AG10 = pw.BooleanField(
        default=False,
    )
    AG11 = pw.BooleanField(
        default=False,
    )
    AG12 = pw.BooleanField(
        default=False,
    )
    AG13 = pw.BooleanField(
        default=False,
    )
    AG14 = pw.BooleanField(
        default=False,
    )
    AG15 = pw.BooleanField(
        default=False,
    )
    AG16 = pw.BooleanField(
        default=False,
    )
    AG17 = pw.BooleanField(
        default=False,
    )
    AG18 = pw.BooleanField(
        default=False,
    )
    AG19 = pw.BooleanField(
        default=False,
    )
    AG20 = pw.BooleanField(
        default=False,
    )
    AG21 = pw.BooleanField(
        default=False,
    )
    AG22 = pw.BooleanField(
        default=False,
    )
    AG23 = pw.BooleanField(
        default=False,
    )
    AG24 = pw.BooleanField(
        default=False,
    )
    AG25 = pw.BooleanField(
        default=False,
    )
    AG26 = pw.BooleanField(
        default=False,
    )
    AG27 = pw.BooleanField(
        default=False,
    )
    AG28 = pw.BooleanField(
        default=False,
    )
    AG29 = pw.BooleanField(
        default=False,
    )
    AG30 = pw.BooleanField(
        default=False,
    )
    AG31 = pw.BooleanField(
        default=False,
    )
    AG32 = pw.BooleanField(
        default=False,
    )
    AG33 = pw.BooleanField(
        default=False,
    )
    AG34 = pw.BooleanField(
        default=False,
    )
    AG35 = pw.BooleanField(
        default=False,
    )
    AG36 = pw.BooleanField(
        default=False,
    )
    AG37 = pw.BooleanField(
        default=False,
    )
    AG38 = pw.BooleanField(
        default=False,
    )
    GA1 = pw.BooleanField(
        default=False,
    )
    GA2 = pw.BooleanField(
        default=False,
    )
    GA3 = pw.BooleanField(
        default=False,
    )
    GA4 = pw.BooleanField(
        default=False,
    )
    GA5 = pw.BooleanField(
        default=False,
    )
    GA6 = pw.BooleanField(
        default=False,
    )
    GA7 = pw.BooleanField(
        default=False,
    )
    GA8 = pw.BooleanField(
        default=False,
    )
    GA9 = pw.BooleanField(
        default=False,
    )
    GA10 = pw.BooleanField(
        default=False,
    )
    GA11 = pw.BooleanField(
        default=False,
    )
    GA12 = pw.BooleanField(
        default=False,
    )
    GA13 = pw.BooleanField(
        default=False,
    )
    GA14 = pw.BooleanField(
        default=False,
    )
    GA15 = pw.BooleanField(
        default=False,
    )
    GA16 = pw.BooleanField(
        default=False,
    )
    GA17 = pw.BooleanField(
        default=False,
    )
    GA18 = pw.BooleanField(
        default=False,
    )
    GA19 = pw.BooleanField(
        default=False,
    )
    GA20 = pw.BooleanField(
        default=False,
    )
    GA21 = pw.BooleanField(
        default=False,
    )
    GA22 = pw.BooleanField(
        default=False,
    )
    GA23 = pw.BooleanField(
        default=False,
    )
    GA24 = pw.BooleanField(
        default=False,
    )
    GA25 = pw.BooleanField(
        default=False,
    )
    GA26 = pw.BooleanField(
        default=False,
    )
    GA27 = pw.BooleanField(
        default=False,
    )
    GA28 = pw.BooleanField(
        default=False,
    )
    GA29 = pw.BooleanField(
        default=False,
    )
    GA30 = pw.BooleanField(
        default=False,
    )
    GA31 = pw.BooleanField(
        default=False,
    )
    GA32 = pw.BooleanField(
        default=False,
    )
    GA33 = pw.BooleanField(
        default=False,
    )
    GA34 = pw.BooleanField(
        default=False,
    )
    GA35 = pw.BooleanField(
        default=False,
    )
    GA36 = pw.BooleanField(
        default=False,
    )
    GA37 = pw.BooleanField(
        default=False,
    )
    GA38 = pw.BooleanField(
        default=False,
    )


class CowMS(pw.Model):
    """Микросателлиты коров."""
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
        species = "bos taurus"


class DeerMS(pw.Model):
    """Микросателлиты оленей."""
    BMS1788 = pw.CharField(
        default='-',
        max_length=10,
    )
    RT30 = pw.CharField(
        default='-',
        max_length=10,
    )
    RT1 = pw.CharField(
        default='-',
        max_length=10,
    )
    SRY = pw.CharField(
        default='-',
        max_length=10,
    )
    RT9 = pw.CharField(
        default='-',
        max_length=10,
    )
    C143 = pw.CharField(
        default='-',
        max_length=10,
    )
    RT7 = pw.CharField(
        default='-',
        max_length=10,
    )
    OHEQ = pw.CharField(
        default='-',
        max_length=10,
    )
    FCB193 = pw.CharField(
        default='-',
        max_length=10,
    )
    RT6 = pw.CharField(
        default='-',
        max_length=10,
    )
    C217 = pw.CharField(
        default='-',
        max_length=10,
    )
    RT24 = pw.CharField(
        default='-',
        max_length=10,
    )
    C32 = pw.CharField(
        default='-',
        max_length=10,
    )
    BMS745 = pw.CharField(
        default='-',
        max_length=10,
    )
    NVHRT16 = pw.CharField(
        default='-',
        max_length=10,
    )
    T40 = pw.CharField(
        default='-',
        max_length=10,
    )
    C276 = pw.CharField(
        default='-',
        max_length=10,
    )

    class Meta:
        species = "deer"


class SheepMS(pw.Model):
    """Микросателлиты овец."""
    MCM042 = pw.CharField(
        default='-',
        max_length=10,
    )
    INRA006 = pw.CharField(
        default='-',
        max_length=10,
    )
    MCM527 = pw.CharField(
        default='-',
        max_length=10,
    )
    ETH152 = pw.CharField(
        default='-',
        max_length=10,
    )
    CSRD247 = pw.CharField(
        default='-',
        max_length=10,
    )
    OARFCB20 = pw.CharField(
        default='-',
        max_length=10,
    )
    INRA172 = pw.CharField(
        default='-',
        max_length=10,
    )
    INRA063 = pw.CharField(
        default='-',
        max_length=10,
    )
    AMEL = pw.CharField(
        default='-',
        max_length=10,
    )
    MAF065 = pw.CharField(
        default='-',
        max_length=10,
    )
    MAF214 = pw.CharField(
        default='-',
        max_length=10,
    )
    INRA005 = pw.CharField(
        default='-',
        max_length=10,
    )
    INRA023 = pw.CharField(
        default='-',
        max_length=10,
    )

    class Meta:
        species = "sheep"


class Cow(BaseModelAnimal, CowMS):
    """Хранение данных по коровам."""

    class Meta:
        verbose_name = 'Коровы'
        table_name = 'Cows'
        species = "bos taurus"


class Bull(BaseModelAnimal, CowMS):
    """Хранение данных по отцам коров."""

    class Meta:
        verbose_name = 'Быки'
        table_name = 'Bull'
        species = "bos taurus"


class Deer(BaseModelAnimal, DeerMS):
    """Хранение данных по оленям."""

    class Meta:
        database = db
        verbose_name = 'Олени'
        table_name = 'Deer'
        species = "deer"


class DeerFemale(BaseModelAnimal, DeerMS):
    """Хранение данных по важенкам."""
    class Meta:
        database = db
        verbose_name = 'Важенки'
        table_name = 'DeerFemale'
        species = "deer"


class Sheep(BaseModelAnimal, SheepMS):
    """Хранение данных по овцам."""

    class Meta:
        database = db
        verbose_name = 'Овцы'
        table_name = 'Sheep'
        species = "sheep"


class Ram(BaseModelAnimal, SheepMS):
    """Хранение данных по баранам."""
    class Meta:
        database = db
        verbose_name = 'Бараны'
        table_name = 'Ram'
        species = "sheep"


class SheepIssr(BaseModelAnimal, ISSR):
    """Хранение данных ISSR по овцам."""
    class Meta:
        database = db
        verbose_name = 'Овцы ISSR'
        table_name = 'SheepISSR'
        species = "sheep"


class RamIssr(BaseModelAnimal, ISSR):
    """Хранение данных ISSR по баранам."""
    class Meta:
        database = db
        verbose_name = 'Бараны ISSR'
        table_name = 'Ram ISSR'
        species = "sheep"


class CowIssr(BaseModelAnimal, ISSR):
    """Хранение данных ISSR по коровам."""
    class Meta:
        database = db
        verbose_name = 'Коровы ISSR'
        table_name = 'CowISSR'
        species = "cow"


class BullIssr(CowIssr, ISSR):
    """Хранение данных ISSR по быкам."""
    class Meta:
        database = db
        verbose_name = 'Быки ISSR'
        table_name = 'BullISSR'
        species = "bos taurus"


class DeerIssr(BaseModelAnimal, ISSR):
    """Хранение данных ISSR по оленям."""
    class Meta:
        database = db
        verbose_name = 'Олени ISSR'
        table_name = 'DeerISSR'
        species = "deer"


class DeerFemaleIssr(DeerIssr, ISSR):
    """Хранение данных ISSR по важенкам."""
    class Meta:
        database = db
        verbose_name = 'Важенкам ISSR'
        table_name = 'DeerFemaleISSR'
        species = "deer"


DICT_MODEL_FATHER_BY_SPECIES = {
    "deer": Deer,
    "bos taurus": Bull,
    "sheep": Ram,
}


Logs.create_table()
Bull.create_table()
Cow.create_table()
Deer.create_table()
DeerFemale.create_table()
Sheep.create_table()
Ram.create_table()
CowIssr.create_table()
BullIssr.create_table()
DeerIssr.create_table()
DeerFemaleIssr.create_table()
SheepIssr.create_table()
RamIssr.create_table()
Farm.create_table()
