import pandas as pd
import unittest
from code_app.managers import (
    ManagerDataISSR, ManagerUtilities, ConfigMeneger,
    ManagerDB, ManagerDataMS, ParserData, ManagerFile
)
from code_app.models import Bull, Cow, Logs, Farm, Deer, DeerIssr
from setting import DB_TEST, config_file_test
import os


DB_TEST.connect()


class Utility:
    @staticmethod
    def compare_str_data(left, right):
        if len(right) != len(left):
            print(f"Not equals len data: {left} - {right}")
            return
        print(f"{left} - {right}")
        for i in range(len(left)):
            if left[i] != right[i]:
                print(f"Not equals: {left[i]} - {right[i]} = {i}")

class Test(unittest.TestCase):
    databases: list = []

    @classmethod
    def setUpClass(cls) -> None:
        """
        Создает фикстуры для теста.
        Вызывается однажды перед запуском всех тестов класса.
        """
        cls.create_db()

    @classmethod
    def create_db(cls) -> None:
        for table in cls.databases:
            table.bind(DB_TEST)
        DB_TEST.create_tables(cls.databases)


# Complited
class TestManagerDB(Test):
    @classmethod
    def setUpClass(cls) -> None:
        """
        Создает фикстуры для теста.
        Вызывается однажды перед запуском всех тестов класса.
        """
        cls.databases = [Deer, Bull, Cow, Logs, Farm]
        super().setUpClass()
        cls.object_test: ManagerDB = ManagerDB()
        data_farm: tuple = (
            {"farm": "Farm_1", "species": "bos taurus"},
            {"farm": "Farm_2", "species": "bos taurus"},
            {"farm": "Farm_3", "species": "bos taurus"},
            {"farm": "Farm_4", "species": "deer"},
        )
        for data in data_farm:
            query = Farm.select().where(Farm.farm == data.get("farm"))
            if not query.exists():
                Farm.create(**data)
        farm_1 = Farm.get(Farm.farm == "Farm_1")
        farm_2 = Farm.get(Farm.farm == "Farm_2")
        farm_3 = Farm.get(Farm.farm == "Farm_3")
        farm_4 = Farm.get(Farm.farm == "Farm_4")
        test_data_father: tuple = (
            {
                "name": 'Test_1', "number": 1, "farm": farm_1,
                "BM1818": "100/100", "BM1824": "100/100", "BM2113": "100/100",
                "CSRM60": "100/100", "CSSM66": "100/100", "CYP21": "100/100",
                "ETH10": "100/100", "ETH225": "100/100", "ETH3": "100/100",
                "ILSTS6": "100/100", "INRA023": "100/100", "RM067": "100/100",
                "SPS115": "100/100", "TGLA122": "100/100",
                "TGLA126": "100/100", "TGLA227": "100/100",
                "TGLA53": "100/100", "MGTG4B": "100/100", "SPS113": "100/100",
            },
            {
                "name": 'Test_2', "number": 2, "farm": farm_1,
                "BM1818": "100/100", "BM1824": "100/100", "BM2113": "100/100",
                "CSRM60": "100/100", "CSSM66": "100/100", "CYP21": "100/100",
                "ETH10": "100/100", "ETH225": "100/100", "ETH3": "100/100",
                "ILSTS6": "100/100", "INRA023": "100/100", "RM067": "100/100",
                "SPS115": "100/100", "TGLA122": "100/100",
                "TGLA126": "100/100", "TGLA227": "100/100",
                "TGLA53": "100/100", "MGTG4B": "100/100", "SPS113": "100/100",
            },
            {
                "name": 'Test_3', "number": 3, "farm": farm_2,
                "BM1818": "100/100", "BM1824": "100/100", "BM2113": "100/100",
                "CSRM60": "100/100", "CSSM66": "100/100", "CYP21": "100/100",
                "ETH10": "100/100", "ETH225": "100/100", "ETH3": "100/100",
                "ILSTS6": "100/100", "INRA023": "100/100", "RM067": "100/100",
                "SPS115": "100/100", "TGLA122": "100/100",
                "TGLA126": "100/100", "TGLA227": "100/100",
                "TGLA53": "100/100", "MGTG4B": "100/100", "SPS113": "100/100",
            },
            {
                "name": 'Test_4', "number": 4, "farm": farm_2,
                "BM1818": "100/100", "BM1824": "100/100", "BM2113": "100/100",
                "CSRM60": "100/100", "CSSM66": "100/100", "CYP21": "100/100",
                "ETH10": "100/100", "ETH225": "100/100", "ETH3": "100/100",
                "ILSTS6": "100/100", "INRA023": "100/100", "RM067": "100/100",
                "SPS115": "100/100", "TGLA122": "100/100",
                "TGLA126": "100/100", "TGLA227": "100/100",
                "TGLA53": "100/100", "MGTG4B": "100/100", "SPS113": "100/100",
            },
            {
                "name": 'Test_5', "number": 5, "farm": farm_3,
                "BM1818": "100/100", "BM1824": "100/100", "BM2113": "100/100",
                "CSRM60": "100/100", "CSSM66": "100/100", "CYP21": "100/100",
                "ETH10": "100/100", "ETH225": "100/100", "ETH3": "100/100",
                "ILSTS6": "100/100", "INRA023": "100/100", "RM067": "100/100",
                "SPS115": "100/100", "TGLA122": "100/100",
                "TGLA126": "100/100", "TGLA227": "100/100",
                "TGLA53": "100/100", "MGTG4B": "100/100", "SPS113": "100/100",
            },
        )

        for data in test_data_father:
            Bull.create(**data)
        test_data_father: tuple = (
            {
                "name": 'Test_33', "number": 13, "farm": farm_4,
                "BMS1788": "100/100", "RT30": "100/100", "RT1": "100/100",
                "SRY": "100/100", "RT9": "100/100", "C143": "100/100",
                "RT7": "100/100", "OHEQ": "100/100", "FCB193": "100/100",
                "RT6": "100/100", "C217": "100/100", "RT24": "100/100",
                "C32": "100/100", "BMS745": "100/100",
                "NVHRT16": "100/100", "T40": "100/100",
                "C276": "100/100"
            },
            {
                "name": 'Test_34', "number": 23, "farm": farm_4,
                "BMS1788": "100/100", "RT30": "100/100", "RT1": "100/100",
                "SRY": "100/100", "RT9": "100/100", "C143": "100/100",
                "RT7": "100/100", "OHEQ": "100/100", "FCB193": "100/100",
                "RT6": "100/100", "C217": "100/100", "RT24": "100/100",
                "C32": "100/100", "BMS745": "100/100",
                "NVHRT16": "100/100", "T40": "100/100",
                "C276": "100/100"
            }
        )
        for data in test_data_father:
            Deer.create(**data)

    def test_get_farms(self) -> None:
        """Тестируется загрузка названий хозяйств."""
        farms: set = TestManagerDB.object_test.get_farms(
            Bull
        )
        test: list = ["Farm_1", "Farm_2", "Farm_3"]
        for farm in test:
            with self.subTest(title=f"Test {farm}"):
                self.assertTrue(farm in list(farms))
        farms: set = TestManagerDB.object_test.get_farms(
            Deer
        )
        test: list = ["Farm_4"]
        for farm in test:
            with self.subTest(title=f"Test {farm}"):
                self.assertTrue(farm in list(farms))

    def test_get_data_for_animals(self) -> None:
        test_deer = {
            "name": 'Test_33', "number": 13, "farm": "Farm_4",
            "BMS1788": "100/100", "RT30": "100/100", "RT1": "100/100",
            "SRY": "100/100", "RT9": "100/100", "C143": "100/100",
            "RT7": "100/100", "OHEQ": "100/100", "FCB193": "100/100",
            "RT6": "100/100", "C217": "100/100", "RT24": "100/100",
            "C32": "100/100", "BMS745": "100/100",
            "NVHRT16": "100/100", "T40": "100/100",
            "C276": "100/100"
        }
        test_cow: dict = {
            "name": 'Test_1', "number": 1, "farm": "Farm_1",
            "BM1818": "100/100", "BM1824": "100/100", "BM2113": "100/100",
            "CSRM60": "100/100", "CSSM66": "100/100", "CYP21": "100/100",
            "ETH10": "100/100", "ETH225": "100/100", "ETH3": "100/100",
            "ILSTS6": "100/100", "INRA023": "100/100", "RM067": "100/100",
            "SPS115": "100/100", "TGLA122": "100/100",
            "TGLA126": "100/100", "TGLA227": "100/100",
            "TGLA53": "100/100", "MGTG4B": "100/100", "SPS113": "100/100",
        }
        data: dict = (
            TestManagerDB.object_test.get_data_for_animals(
                Bull
            )
        )
        for key, label in test_cow.items():
            with self.subTest(title=f"Test {key} - {label}"):
                answer = data.get(0).get(key)
                self.assertEqual(answer, label)

        data_2: dict = (
            TestManagerDB.object_test.get_data_for_animals(
                Deer
            )
        )
        for key, label in test_deer.items():
            with self.subTest(title=f"Test {key}"):
                answer = data_2.get(0).get(key)
                self.assertEqual(answer, label)

    def test_get_data_for_animal(self) -> None:
        """Тестирование загрузки данных по животному."""
        test_data: dict = {
            "name": 'Test_1', "number": 1, "farm": "Farm_1",
            "BM1818": "100/100", "BM1824": "100/100", "BM2113": "100/100",
            "CSRM60": "100/100", "CSSM66": "100/100", "CYP21": "100/100",
            "ETH10": "100/100", "ETH225": "100/100", "ETH3": "100/100",
            "ILSTS6": "100/100", "INRA023": "100/100", "RM067": "100/100",
            "SPS115": "100/100", "TGLA122": "100/100",
            "TGLA126": "100/100", "TGLA227": "100/100",
            "TGLA53": "100/100", "MGTG4B": "100/100", "SPS113": "100/100",
        }
        data: dict = (
            TestManagerDB.object_test.get_data_for_animal(
                1,
                Bull
            )
        )
        for key, label in test_data.items():
            with self.subTest(title=f"Test {key} - {label}"):
                answer = data.get(key)
                self.assertEqual(answer, label)

        data_2: dict = (
            TestManagerDB.object_test.get_data_for_animal(
                132423,
                Bull
            )
        )
        for key in test_data.keys():
            with self.subTest(title=f"Test {key}"):
                answer = data_2.get(key)
                self.assertEqual(answer, "-")

    def test_save_data_animal_to_db(self) -> None:
        """Проверка сохранения данных в базу данных."""
        number: int = 7586
        farm_3 = Farm.get(Farm.farm == "Farm_3")
        farm_4 = Farm.get(Farm.farm == "Farm_4")
        data_test: dict = {
            Cow: {
                "number": number,
                "name": "Test",
                "farm": farm_3,
                "BM1818": "158/186",
                "BM1824": "158/186",
                "BM2113": "158/186",
                "CSRM60": "158/196",
                "CSSM66": "154/186",
                "CYP21": "158/186",
                "ETH10": "152/186",
                "ETH225": "-",
                "ETH3": "158/186",
                "ILSTS6": "154/186",
                "INRA023": "158/156",
                "RM067": "151/186",
                "SPS115": "158/186",
                "TGLA122": "158/136",
                "TGLA126": "153/186",
                "TGLA227": "158/186",
                "TGLA53": "158/181",
                "MGTG4B": "108/186",
                "SPS113": "-",
            },
            Deer: {
                "name": 'Test_33', "number": number, "farm": farm_4,
                "BMS1788": "100/100", "RT30": "100/100", "RT1": "100/100",
                "SRY": "100/100", "RT9": "100/100", "C143": "100/100",
                "RT7": "100/100", "OHEQ": "100/100", "FCB193": "100/100",
                "RT6": "100/100", "C217": "100/100", "RT24": "100/100",
                "C32": "100/100", "BMS745": "100/100",
                "NVHRT16": "100/100", "T40": "100/100",
                "C276": "100/100"
            }
        }
        data_test_answer: dict = {
            Cow: {
                "number": number,
                "name": "Test",
                "farm": "Farm_3",
                "BM1818": "158/186",
                "BM1824": "158/186",
                "BM2113": "158/186",
                "CSRM60": "158/196",
                "CSSM66": "154/186",
                "CYP21": "158/186",
                "ETH10": "152/186",
                "ETH225": "-",
                "ETH3": "158/186",
                "ILSTS6": "154/186",
                "INRA023": "158/156",
                "RM067": "151/186",
                "SPS115": "158/186",
                "TGLA122": "158/136",
                "TGLA126": "153/186",
                "TGLA227": "158/186",
                "TGLA53": "158/181",
                "MGTG4B": "108/186",
                "SPS113": "-",
            },
            Deer: {
                "name": 'Test_33', "number": number, "farm": "Farm_4",
                "BMS1788": "100/100", "RT30": "100/100", "RT1": "100/100",
                "SRY": "100/100", "RT9": "100/100", "C143": "100/100",
                "RT7": "100/100", "OHEQ": "100/100", "FCB193": "100/100",
                "RT6": "100/100", "C217": "100/100", "RT24": "100/100",
                "C32": "100/100", "BMS745": "100/100",
                "NVHRT16": "100/100", "T40": "100/100",
                "C276": "100/100"
            }
        }

        for model, data in data_test.items():
            TestManagerDB.object_test.save_data_animal_to_db(
                data,
                model
            )
            query = model.select().where(
                model.number == 1413
            )
            self.assertFalse(query.exists())

            query = model.select().where(
                model.number == number
            )
            self.assertTrue(query.exists())
            res = query.get().get_data()
            data = data_test_answer.get(model)

            for key, label in data.items():
                with self.subTest(title=f"Test {model} {key} - {label}"):
                    answer = res.get(key)
                    self.assertEqual(answer, label)

    def test_donwload_data_farmers(self) -> None:
        """Тестируется загрузка названий хозяйств из базы."""
        farms: set = TestManagerDB.object_test.get_farms(
            Bull
        )
        test: list = ["Farm_1", "Farm_2", "Farm_3"]
        for farm in test:
            with self.subTest(title=f"Test {farm}"):
                self.assertTrue(farm in list(farms))

    def test_donwload_data_for_animal(self) -> None:
        """Тестирование загрузки данных по животному из базы."""
        test_data: dict = {
            "name": 'Test_1', "number": 1, "farm": "Farm_1",
            "BM1818": "100/100", "BM1824": "100/100", "BM2113": "100/100",
            "CSRM60": "100/100", "CSSM66": "100/100", "CYP21": "100/100",
            "ETH10": "100/100", "ETH225": "100/100", "ETH3": "100/100",
            "ILSTS6": "100/100", "INRA023": "100/100", "RM067": "100/100",
            "SPS115": "100/100", "TGLA122": "100/100",
            "TGLA126": "100/100", "TGLA227": "100/100",
            "TGLA53": "100/100", "MGTG4B": "100/100", "SPS113": "100/100",
        }
        data: dict = (
            TestManagerDB.object_test.get_data_for_animal(
                1,
                Bull
            )
        )
        for key, label in test_data.items():
            with self.subTest(title=f"Test {key} - {label}"):
                answer = data.get(key)
                self.assertEqual(answer, label)

        data_2: dict = (
            TestManagerDB.object_test.get_data_for_animal(
                132423,
                Bull
            )
        )
        for key in test_data.keys():
            with self.subTest(title=f"Test {key}"):
                answer = data_2.get(key)
                self.assertEqual(answer, "-")

    def test_donwload_data_for_animals(self) -> None:
        test_cow: dict = {
            "name": 'Test_1', "number": 1, "farm": "Farm_1",
            "BM1818": "100/100", "BM1824": "100/100", "BM2113": "100/100",
            "CSRM60": "100/100", "CSSM66": "100/100", "CYP21": "100/100",
            "ETH10": "100/100", "ETH225": "100/100", "ETH3": "100/100",
            "ILSTS6": "100/100", "INRA023": "100/100", "RM067": "100/100",
            "SPS115": "100/100", "TGLA122": "100/100",
            "TGLA126": "100/100", "TGLA227": "100/100",
            "TGLA53": "100/100", "MGTG4B": "100/100", "SPS113": "100/100",
        }
        data: dict = (
            TestManagerDB.object_test.get_data_for_animals(
                Bull
            )
        )
        for key, label in test_cow.items():
            with self.subTest(title=f"Test {key} - {label}"):
                answer = data.get(0).get(key)
                self.assertEqual(answer, label)


# Complited
class TestConfigMeneger(Test):
    @classmethod
    def setUpClass(cls) -> None:
        """
        Создает фикстуры для теста.
        Вызывается однажды перед запуском всех тестов класса.
        """
        cls._object_test: ConfigMeneger = ConfigMeneger(config_file_test)
        super().setUpClass()

    def test_create_config(self):
        """Проверяет наличие файла конфига."""
        self._object_test.create_config()
        res: bool = os.path.isfile(config_file_test)
        with self.subTest(title=f"Test {res}"):
            self.assertTrue(res)

    def test_set_path(self):
        """Тестирует верное сохранение адреса."""
        self._object_test.set_path(
            "Desktop",
            "open"
        )
        list_data: list = []
        with open(config_file_test, "r") as f:
            list_data = f.readlines()
        answer = list_data[1].split(" = ")[-1]
        answer = (answer.strip().rstrip())

        with self.subTest(title=f"Test {answer}"):
            self.assertTrue(answer == "Desktop")

    def test_get_path(self):
        """Тестирует верное получение адреса."""
        self._object_test.set_path(
            "Tutututututut",
            "open"
        )
        answer = self._object_test.get_path("open")
        with self.subTest(title=f"Test Tutututututut"):
            self.assertTrue(answer == "Tutututututut")


# Complited
class TestManagerFile(Test):
    @classmethod
    def setUpClass(cls) -> None:
        """
        Создает фикстуры для теста.
        Вызывается однажды перед запуском всех тестов класса.
        """
        cls.object_test: ManagerFile = ManagerFile()
        super().setUpClass()

    def test_read_file(self) -> None:
        list_path = [
            r"tests\test_data\test_data_open.csv",
            r"tests\test_data\test_data_open.xlsx",
            r"tests\test_data\test_data_open.txt",
        ]
        for path in list_path:
            self.object_test.set_path_for_file_to_open(path)
            temp = self.object_test.read_file()
            col = temp.columns[0]
            with self.subTest(title=f"Test - {path}"):
                self.assertEqual(col, "animal")


# Complited
@unittest.skip("showing class skipping")
class TestParserData(Test):
    @classmethod
    def setUpClass(cls) -> None:
        """
        Создает фикстуры для теста.
        Вызывается однажды перед запуском всех тестов класса.
        """
        cls.object_test: ParserData = ParserData()
        cls.databases = [Bull, Farm]
        super().setUpClass()
        cls.answer = {
            3205251522: {
                'BM1818': '262/266', 'BM1824': '178/188',
                'BM2113': '125/127', 'CSRM60': 0.0, 'CSSM66': 0.0,
                'CYP21': '189/189', 'ETH10': '223/225', 'ETH225': '148/150',
                'ETH3': '117/129', 'ILSTS6': 0.0, 'INRA023': '202/202',
                'RM067': '92/102', 'SPS115': '248/248', 'TGLA122': '151/163',
                'TGLA126': '117/117', 'TGLA227': '89/99', 'TGLA53': '158/186',
                'MGTG4B': '135/135', 'SPS113': '141/151'
            },
            358633624: {
                'BM1818': '262/266', 'BM1824': '188/188',
                'BM2113': '125/139', 'CSRM60': 0.0, 'CSSM66': 0.0,
                'CYP21': 0.0, 'ETH10': '223/225', 'ETH225': '148/150',
                'ETH3': '127/129', 'ILSTS6': 0.0, 'INRA023': '214/214',
                'RM067': 0.0, 'SPS115': '248/248', 'TGLA122': '143/171',
                'TGLA126': '117/117', 'TGLA227': '89/97', 'TGLA53': '168/184',
                'MGTG4B': 0.0, 'SPS113': 0.0
            }
        }
        cls._manager_db: ManagerDB = ManagerDB()
        data_farm: tuple = (
            {"farm": "Farm_1", "species": "bos taurus"},
            {"farm": "Farm_2", "species": "bos taurus"},
            {"farm": "Farm_3", "species": "bos taurus"},
            {"farm": "Farm_4", "species": "deer"},
        )
        for data in data_farm:
            query = Farm.select().where(Farm.farm == data.get("farm"))
            if not query.exists():
                Farm.create(**data)

    def test_check_ms_in_cell(self):
        """Тестируется проверка на наличие данных по локусам."""
        rows: dict = {
            "BM1818 - 158/956, SPS113 - 259/9565": True,
            "ILSTS6 - 158/956": True,
            "POD - 158/956, HUY113 - 259/9565": False,
            "ILSTS6 - 158/956, ETH225 - 259/9565": True,
            "BM2113 - 158/956, CSSM66 - 259/9565": True,
            "CSSM66 - 158/956, ETH10 - 259/9565": True,
            "YIUGGIU - 158/956, fdsf - 259/9565": False,
        }
        for row, answer in rows.items():
            res: bool = self.object_test.check_ms_in_cell(row)
            with self.subTest(title=f"Test - {row}"):
                self.assertEqual(res, answer)

    def test_filter_id_bus(self):
        """Тестируется поиск нужной страницы."""
        number: int = 3205251522
        name: str = "ЛУНА"
        res = self.object_test.filter_id_bus(number, name)
        answer = 10402043
        with self.subTest(title=f"Test - {res}"):
            self.assertEqual(res[0], answer)

    def test_parser_ms(self):
        """Тестируется сбор данных по профилю."""
        number: int = 3205251522
        name: str = "ЛУНА"
        number_page, token = self.object_test.filter_id_bus(number, name)
        profils: dict = self.object_test.parser_ms(number_page, token)

        with self.subTest(title=f"Test - {self.answer.get(number)}"):
            self.assertEqual(self.answer.get(number), profils)

    def test_add_missing_father(self):
        farm_1 = Farm.get(Farm.farm == "Farm_1")
        print("FARM ", farm_1)
        self.object_test.add_missing_father(
            {358633624: "Сильвер", 3205251522: "ЛУНА"},
            Bull,
            farm_1
        )
        for key, val in self.answer.items():
            data = self._manager_db.get_data_for_animal(key, Bull)
            for key_in, val_in in val.items():
                with self.subTest(title="Test - {key_in}"):
                    self.assertEqual(str(val_in), data[key_in])

    def test_pipline_data_loading_for_bull(self):
        """Тестируем пайплайн загрузки данных по быкам."""
        number: int = 3205251522
        name: str = "ЛУНА"
        farm_1 = Farm.get(Farm.farm == "Farm_1")
        res: bool = self.object_test.pipline_data_loading_for_bull(
            number, name, farm_1
        )
        with self.subTest(title="Test - data"):
            self.assertEqual(res, 0)

        data = self._manager_db.get_data_for_animal(number, Bull)
        for key, val in self.answer.get(number).items():
            with self.subTest(title="Test - {key}"):
                self.assertEqual(str(val), data[key])


# Dev
class TestManagerMS(Test):
    @classmethod
    def setUpClass(cls) -> None:
        """
        Создает фикстуры для теста.
        Вызывается однажды перед запуском всех тестов класса.
        """
        cls.databases = [Deer, Bull, Cow, Logs, Farm]
        super().setUpClass()
        cls._manager_db: ManagerDB = ManagerDB()

        data_farm: tuple = (
            {"farm": "Farm_1", "species": "bos taurus"},
            {"farm": "Farm_2", "species": "bos taurus"},
            {"farm": "Farm_3", "species": "bos taurus"},
        )
        for data in data_farm:
            Farm.create(**data)
        farm_1 = Farm.get(Farm.farm == "Farm_1")
        farm_2 = Farm.get(Farm.farm == "Farm_2")
        farm_3 = Farm.get(Farm.farm == "Farm_3")
        cls._object_test: ManagerDataMS = ManagerDataMS(
            farm=farm_1, model=Bull
        )
        test_data_father: tuple = (
            {
                "name": 'Test_1', "number": 1, "farm": farm_1,
                "BM1818": "100/100", "BM1824": "100/100", "BM2113": "100/100",
                "CSRM60": "100/100", "CSSM66": "100/100", "CYP21": "100/100",
                "ETH10": "100/100", "ETH225": "100/100", "ETH3": "100/100",
                "ILSTS6": "100/100", "INRA023": "100/100", "RM067": "100/100",
                "SPS115": "100/100", "TGLA122": "100/100",
                "TGLA126": "100/100", "TGLA227": "100/100",
                "TGLA53": "100/100", "MGTG4B": "100/100", "SPS113": "100/100",
            },
            {
                "name": 'Test_2', "number": 2, "farm": farm_1,
                "BM1818": "100/100", "BM1824": "100/100", "BM2113": "100/100",
                "CSRM60": "100/100", "CSSM66": "100/100", "CYP21": "100/100",
                "ETH10": "100/100", "ETH225": "100/100", "ETH3": "100/100",
                "ILSTS6": "100/100", "INRA023": "100/100", "RM067": "100/100",
                "SPS115": "100/100", "TGLA122": "100/100",
                "TGLA126": "100/100", "TGLA227": "100/100",
                "TGLA53": "100/100", "MGTG4B": "100/100", "SPS113": "100/100",
            },
            {
                "name": 'Test_3', "number": 3, "farm": farm_2,
                "BM1818": "100/100", "BM1824": "100/100", "BM2113": "100/100",
                "CSRM60": "100/100", "CSSM66": "100/100", "CYP21": "100/100",
                "ETH10": "100/100", "ETH225": "100/100", "ETH3": "100/100",
                "ILSTS6": "100/100", "INRA023": "100/100", "RM067": "100/100",
                "SPS115": "100/100", "TGLA122": "100/100",
                "TGLA126": "100/100", "TGLA227": "100/100",
                "TGLA53": "100/100", "MGTG4B": "100/100", "SPS113": "100/100",
            },
            {
                "name": 'Test_4', "number": 4, "farm": farm_2,
                "BM1818": "100/100", "BM1824": "100/100", "BM2113": "100/100",
                "CSRM60": "100/100", "CSSM66": "100/100", "CYP21": "100/100",
                "ETH10": "100/100", "ETH225": "100/100", "ETH3": "100/100",
                "ILSTS6": "100/100", "INRA023": "100/100", "RM067": "100/100",
                "SPS115": "100/100", "TGLA122": "100/100",
                "TGLA126": "100/100", "TGLA227": "100/100",
                "TGLA53": "100/100", "MGTG4B": "100/100", "SPS113": "100/100",
            },
            {
                "name": 'Test_5', "number": 5, "farm": farm_3,
                "BM1818": "100/100", "BM1824": "100/100", "BM2113": "100/100",
                "CSRM60": "100/100", "CSSM66": "100/100", "CYP21": "100/100",
                "ETH10": "100/100", "ETH225": "100/100", "ETH3": "100/100",
                "ILSTS6": "100/100", "INRA023": "100/100", "RM067": "100/100",
                "SPS115": "100/100", "TGLA122": "100/100",
                "TGLA126": "100/100", "TGLA227": "100/100",
                "TGLA53": "100/100", "MGTG4B": "100/100", "SPS113": "100/100",
            },
        )
        for data in test_data_father:
            Bull.create(**data)

    def test_validate_invertory(self):
        list_path = [
            r"tests\test_data\inventory_example_bad_1.csv",
            r"tests\test_data\inventory_example_bad_2.csv"
        ]
        flag = False
        for path in list_path:
            try:
                self._object_test.loading_data_invertory(path)
            except ValueError:
                flag = True
            with self.subTest(title="Test - {path}"):
                self.assertTrue(flag)

    @unittest.skip("demonstrating skipping")
    def test_loading_data_invertory(self):
        path = r"tests\test_data\inventory_example.csv"
        self._object_test.loading_data_invertory(path)
        data = list(self._object_test.dataset_inverory.loc[0, :])
        answer = [60436, "nan", 1, 60407, "Ранетка", 72246370, "Мунрэйкер"]
        for i in range(len(data)):
            with self.subTest(title="Test - {data[i]}"):
                self.assertEqual(answer[i], data[i])

    @unittest.skip("demonstrating skipping")
    def test_loading_data_profils(self):
        path = r"tests\test_data\profils_example.csv"
        self._object_test.loading_data_profils(path)
        data = list(self._object_test.dataset_profils.loc[0, :])
        answer = [
            1, "129/129", "189/189", "206/206", "262/262", "294/296",
            "91/97", "115/117", "151/171", "248/248", "150/152", "176/186",
            "96/102", "127/137", "178/182", "209/217"
        ]
        for i in range(len(data)):
            with self.subTest(title=f"Test - {data[i]}"):
                self.assertEqual(answer[i], data[i])

    def test_filter_animals_by_farm(self):
        """Тестирует отбор хозяйств."""
        dict_farms = {
            "Farm_1": True,
            "Farm_2": True,
            "Farm_3": False,
        }
        data_father = self._object_test.filter_animals_by_farm(
            dict_farms, Bull
        )
        with self.subTest(title="Test - farm"):
            self.assertFalse("Farm_3" in data_father['farm'].unique())

    def test_search_father(self):
        path = r"tests\test_data\test_search_father.csv"
        data = self._object_test.search_father(
            path,
            {'Выбрать всех': True}
        )
        with self.subTest(title="Test - farm"):
            self.assertEqual(data.loc[0, "number"], 3205251522)

    def test_verification_ms(self):
        test_data = {
            1: ["159/265", "154/265", False],
            2: ["159/265", "154/259", True],
            3: ["115/265", "115/265", False],
            4: ["125/265", "125/3569", False],
            5: ["-", "154/265", False],
            6: ["nan", "154/265", False],
        }
        for key, val in test_data.items():
            res = self._object_test.verification_ms(
                val[0], val[1]
            )
            with self.subTest(title=f"Test - {key}"):
                self.assertEqual(res, val[2])

    def test_split__(self):
        data_test = {
            "sadsd_fdesaf": ["sadsd", "fdesaf"],
            "sadsdfdesaf": ["sadsdfdesaf"],
            "324 _fdesaf": ["324 ", "fdesaf"],
        }
        for key, val in data_test.items():
            res: list = self._object_test.split__(key)
            with self.subTest(title=f"Test - {key}"):
                self.assertTrue(res, val)

    def test_split_locus(self):
        data_test = {
            "sadsd_  - fdesaf": ["sadsd", "fdesaf"],
            "sadsdfdesaf": ["sadsdfdesaf"],
            "324  - _fdesaf": ["324 ", "fdesaf"],
        }
        for key, val in data_test.items():
            res: list = self._object_test.split__(key)
            with self.subTest(title=f"Test - {key}"):
                self.assertTrue(res, val)

    def test_ms_join(self):
        data = pd.Series(
            data=["100", "200"],
            index=["col_1", "col_2"]
        )
        answer = self._object_test.ms_join(data, "col_1", "col_2")
        with self.subTest(title="Test - join"):
            self.assertEqual("100/200", answer)

    def test_get_summary_data_error(self):
        self._object_test.dict_error = {
            "not_animal": [],
            "not_father": [],
        }
        res = self._object_test.get_summary_data_error()
        print(res)


# Complited
class TestManagerUtilities(Test):
    @classmethod
    def setUpClass(cls) -> None:
        """
        Создает фикстуры для теста.
        Вызывается однажды перед запуском всех тестов класса.
        """
        cls.object_test: ManagerUtilities = ManagerUtilities()
        cls.databases = [Deer, Bull, Cow, Logs, Farm]
        super().setUpClass()

    def test_is_float(self) -> None:
        """Проверяет тест на число с плавующей точкой"""
        data: dict = {
            1: True,
            "def": False,
            1.2324: True,
            "1.23": True,
            "1,23": False
        }

        for test, excepted in data.items():
            with self.subTest(title=test):
                answer = TestManagerUtilities.object_test.is_float(test)
                self.assertEqual(answer, excepted)

    def test_delit(self) -> None:
        """Проверяет правильность разделения данных"""
        data: dict = {
            "1": [
                pd.Series(
                    data=["32423/dsf.1"],
                    index=["Samples"]
                ),
                ".",
                "Samples"
            ],
            "2": [
                pd.Series(
                    data=["32423,2"],
                    index=["Samples"]
                ),
                ",",
                "Samples"
            ],
            "45": [
                pd.Series(
                    data=["32423.45"],
                    index=["Samples"]
                ),
                ".",
                "Samples"
            ],
            "456": [
                pd.Series(
                    data=["32423/dsf,456"],
                    index=["Samples"]
                ),
                ",",
                "Samples"
            ],
        }

        for excepted, test in data.items():
            with self.subTest(title=test):
                answer = TestManagerUtilities.object_test.delit(
                    test[0],
                    test[1],
                    test[2],
                )
                self.assertEqual(answer, excepted)


# Complited
class TestManagerISSR(Test):
    @classmethod
    def setUpClass(cls):
        """
        Создает фикстуры для теста.
        Вызывается однажды перед запуском всех тестов класса.
        """
        cls.databases = [DeerIssr]
        super().setUpClass()
        cls.calc: ManagerDataISSR = ManagerDataISSR()
        cls._manager_db: ManagerDB = ManagerDB()
        data_farm: tuple = (
            {"farm": "Farm_1", "species": "bos taurus"},
            {"farm": "Farm_2", "species": "bos taurus"},
            {"farm": "Farm_3", "species": "bos taurus"},
            {"farm": "Farm_4", "species": "deer"},
        )
        for data in data_farm:
            query = Farm.select().where(Farm.farm == data.get("farm"))
            if not query.exists():
                Farm.create(**data)

    def test_get_allel_label(self) -> None:
        """Проверяет точность оценки аллели."""
        allels_mode_g: dict = {
            165: "G38",
            3000: "-",
            50: "-",
            2350: "G1",
            2001: "G2",
            201: "G37",
        }
        allels_mode_a: dict = {
            165: "A38",
            3000: "-",
            50: "-",
            2350: "A1",
            2001: "A2",
            201: "A37",
        }
        for size, label in allels_mode_g.items():
            with self.subTest(title=f"Test GA - {size}"):
                answer = TestManagerISSR.calc.get_allel_label(size, "G")
                self.assertEqual(answer, label)

        for size, label in allels_mode_a.items():
            with self.subTest(title=f"Test AG - {size}"):
                answer = TestManagerISSR.calc.get_allel_label(size, "A")
                self.assertEqual(answer, label)

    def test_genotype_issr(self) -> None:
        """Проверяет работу с структурой данных."""
        row = pd.Series(
            data=[165, 2350],
            index=["AG", "GA"]
        )
        answer = TestManagerISSR.calc.genotype_issr(row, "A")
        self.assertEqual(answer, "A38")
        answer = TestManagerISSR.calc.genotype_issr(row, "G")
        self.assertEqual(answer, "G1")

    def test_data_transpose(self) -> None:
        """Проверяет транспонирование матриц таблиц."""

        data_test: pd.DataFrame = pd.DataFrame(
            data=[
                [1.0, "A1", "G34"],
                [1.099, "A2", None],
                [1.09999, "A26", None],
                [2.0, "A2", "G23"],
                [2.099, "A21", "G24"],
                [2.09999, "A36", "G37"],
            ],
            columns=['animal', 'AG_genotype', "GA_genotype"]
        )

        index_values: pd.DataFrame = pd.DataFrame(
            data_test['animal'].value_counts()
        )
        index_values = index_values.reset_index()
        index_values.columns = ['num', 'chast']
        index_values['num'] = index_values['num'].astype('float')
        index_values = index_values.sort_values(by=['num'], ascending=True)
        index_values = index_values.reset_index()

        data_answer: pd.DataFrame = pd.DataFrame(
            data=[
                ["animal", 1.0, 1.0, 1.0],
                ["AG_genotype", "A1", "A2", "A26"],
                ["GA_genotype", "G34", None, None],
                ["animal", 2.0, 2.0, 2.0],
                ["AG_genotype", "A2", "A21", "A36"],
                ["GA_genotype", "G23", "G24", "G37"],
            ],
            columns=['index', 0, 1, 2]
        )
        self.calc.merge_data = data_test
        self.calc.data_transpose(
            index_values
        )
        answer: pd.DataFrame = self.calc.result
        with self.subTest(erorr=answer.compare(data_answer)):
            self.assertTrue(data_answer.equals(answer))

    def test_create_indexes(self) -> None:
        """Проверяет присваивание индекса."""
        data_test: pd.DataFrame = pd.DataFrame(
            data=[
                [1, 2344],
                [None, 1234],
                [None, 232],
                [2, 2368],
                [None, 1254],
                [None, 956],
            ],
            columns=["animal", "AG"]
        ).fillna(0)
        data_answer: pd.DataFrame = pd.DataFrame(
            data=[
                [1.0, 2344],
                ["1.099", 1234],
                ["1.09999", 232],
                [2.0, 2368],
                ["2.099", 1254],
                ["2.09999", 956],
            ],
            columns=["animal", "AG"]
        )
        answer: pd.DataFrame = TestManagerISSR.calc.create_indexes(data_test)
        with self.subTest(error=data_answer.compare(answer)):
            self.assertTrue(data_answer.equals(answer))

    def test_pipline_issr_analis(self) -> None:
        """Проверяет результаты анализа данных."""
        data_answer: pd.DataFrame = pd.DataFrame(
            data=[
                ["animal", 1.0, 1.0, 1.0],
                ["AG_genotype", "A1", "-", "-"],
                ["GA_genotype", "G1", "G10", "G36"],
                ["animal", 2.0, 2.0, 2.0],
                ["AG_genotype", "A2", "A9", "A31"],
                ["GA_genotype", "G1", "G9", "G14"],
            ],
            columns=['index', 0, 1, 2]
        )
        farm_1 = Farm.get(Farm.farm == "Farm_1")
        answer: pd.DataFrame = TestManagerISSR.calc.pipline_issr_analis(
            r"tests\test_data\test_issr.csv",
            DeerIssr,
            farm_1
        )
        with self.subTest(erorr=answer.compare(data_answer)):
            self.assertTrue(data_answer.equals(answer))

    def test_binary_search(self) -> None:
        """Проверяет работу измененого бинарного поиска."""
        list_size: list = [
            2500, 2300, 2000, 1800, 1700, 1600, 1500, 1400, 1300,
            1240, 1180, 1120, 1060, 1000, 940, 880, 820, 760, 720,
            680, 640, 600, 560, 530, 500, 470, 440, 410, 380, 360,
            340, 320, 300, 280, 260, 240, 220, 200, 160,
        ]
        data: dict = {
            200: 200,
            198: 160,
            1800: 1800,
            1055: 1000,
            355: 340,
            2369: 2300
        }
        for test, expected in data.items():
            with self.subTest(title=f"Test size - {test}"):
                answer = TestManagerISSR.calc.binary_search(
                    list_size,
                    0,
                    len(list_size)-1,
                    test
                )
                self.assertEqual(list_size[answer], expected)

    def test_data_to_db(self) -> None:
        farm_1 = Farm.get(Farm.farm == "Farm_1")
        self.calc.merge_data = pd.DataFrame().from_dict(
            {
                'animal': {0: 1, 1: 1, 2: 1, 3: 2, 4: 2, 5: 2},
                'AG_genotype': {
                    0: 'A1', 1: '-', 2: '-',
                    3: 'A2', 4: 'A9', 5: 'A31'
                },
                'GA_genotype': {
                    0: 'G1', 1: 'G10', 2: 'G36',
                    3: 'G1', 4: 'G9', 5: 'G14'
                }
            }
        )
        """
           animal AG_genotype GA_genotype
        0       1          A1          G1
        1       1           -         G10
        2       1           -         G36
        3       2          A2          G1
        4       2          A9          G9
        5       2         A31         G14
        """
        dict_data = {}
        for i in range(2):
            number = i + 1
            query = self.calc.merge_data.query("animal == @number")
            dict_data[i] = list(pd.melt(
                query[["AG_genotype", "GA_genotype"]]
            )['value'])
        self.calc.data_to_db(DeerIssr, farm_1)

        genotype = {
            "A": "AG",
            "G": "GA",
            "-": "-"
        }

        data: dict = self._manager_db.get_data_for_animals(DeerIssr)
        for key, item in data.items():
            # Получаем данные по животным
            animal = dict_data.get(key)
            for val in animal:
                # Получаем ключ по данным
                key_in = genotype.get(val[0]) + val[1:]
                if key_in != '-':
                    # Получаем ответ
                    answer = item.get(key_in)
                    with self.subTest(
                        title=f"{key+1}: {key_in} - {answer}"
                    ):
                        self.assertTrue(answer)

    def test_data_from_db(self) -> None:

        farm_1 = Farm.get(Farm.farm == "Farm_1")
        self.calc.merge_data = pd.DataFrame().from_dict(
            {
                'animal': {0: 1, 1: 1, 2: 1, 3: 2, 4: 2, 5: 2},
                'AG_genotype': {
                    0: 'A1', 1: '-', 2: '-',
                    3: 'A2', 4: 'A9', 5: 'A31'
                },
                'GA_genotype': {
                    0: 'G1', 1: 'G10', 2: 'G36',
                    3: 'G1', 4: 'G9', 5: 'G14'
                }
            }
        )
        """
           animal AG_genotype GA_genotype
        0       1          A1          G1
        1       1           -         G10
        2       1           -         G36
        3       2          A2          G1
        4       2          A9          G9
        5       2         A31         G14
        """
        dict_data = {}
        for i in range(2):
            number = i + 1
            query = self.calc.merge_data.query("animal == @number")
            dict_data[i] = list(pd.melt(
                query[["AG_genotype", "GA_genotype"]]
            )['value'])
        self.calc.data_to_db(DeerIssr, farm_1)

        genotype = {
            "A": "AG",
            "G": "GA",
            "-": "-"
        }

        data = self.calc.data_from_db(DeerIssr)
        for key, item in data.items():
            # Получаем данные по животным
            animal = dict_data.get(key)
            for val in animal:
                # Получаем ключ по данным
                key_in = genotype.get(val[0]) + val[1:]
                if key_in != '-':
                    # Получаем ответ
                    answer = item.get(key_in)
                    with self.subTest(
                        title=f"{key+1}: {key_in} - {answer}"
                    ):
                        self.assertTrue(answer)


class Closer:
    '''Менеджер контекста для автоматического закрытия объекта вызовом метода close
    в with-выражении.'''

    def __init__(self, db_name, tables):
        self.db_name = db_name
        self.tables = tables

    def __enter__(self):
        self.db_name.connect()
        print("test")

        for table in self.tables:
            table.bind(self.db_name)
        self.db_name.create_tables(self.tables)
        return self.db_name

    def __exit__(self, exception_type, exception_val, trace):
        self.obj.drop_tables(self.tables)
        self.obj.close()
