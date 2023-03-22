import pandas as pd
import unittest
from code_app.managers import (
    ManagerDataISSR, ManagerUtilities, ConfigMeneger,
    ManagerDB, ManagerDataMS, ParserData, ManagerFile
)
from code_app.models import BullFather, ProfilsCows, Logs
from setting import DB_TEST


class TestManagerDB(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        """
        Создает фикстуры для теста.
        Вызывается однажды перед запуском всех тестов класса.
        """
        cls.object_test: ManagerDB = ManagerDB()
        test_data_father: tuple = (
            {
                "name": 'Test_1', "number": 1, "farm": "Farm_1",
                "BM1818": "100/100", "BM1824": "100/100", "BM2113": "100/100",
                "CSRM60": "100/100", "CSSM66": "100/100", "CYP21": "100/100",
                "ETH10": "100/100", "ETH225": "100/100", "ETH3": "100/100",
                "ILSTS6": "100/100", "INRA023": "100/100", "RM067": "100/100",
                "SPS115": "100/100", "TGLA122": "100/100",
                "TGLA126": "100/100", "TGLA227": "100/100",
                "TGLA53": "100/100", "MGTG4B": "100/100", "SPS113": "100/100",
            },
            {
                "name": 'Test_2', "number": 2, "farm": "Farm_1",
                "BM1818": "100/100", "BM1824": "100/100", "BM2113": "100/100",
                "CSRM60": "100/100", "CSSM66": "100/100", "CYP21": "100/100",
                "ETH10": "100/100", "ETH225": "100/100", "ETH3": "100/100",
                "ILSTS6": "100/100", "INRA023": "100/100", "RM067": "100/100",
                "SPS115": "100/100", "TGLA122": "100/100",
                "TGLA126": "100/100", "TGLA227": "100/100",
                "TGLA53": "100/100", "MGTG4B": "100/100", "SPS113": "100/100",
            },
            {
                "name": 'Test_3', "number": 3, "farm": "Farm_2",
                "BM1818": "100/100", "BM1824": "100/100", "BM2113": "100/100",
                "CSRM60": "100/100", "CSSM66": "100/100", "CYP21": "100/100",
                "ETH10": "100/100", "ETH225": "100/100", "ETH3": "100/100",
                "ILSTS6": "100/100", "INRA023": "100/100", "RM067": "100/100",
                "SPS115": "100/100", "TGLA122": "100/100",
                "TGLA126": "100/100", "TGLA227": "100/100",
                "TGLA53": "100/100", "MGTG4B": "100/100", "SPS113": "100/100",
            },
            {
                "name": 'Test_4', "number": 4, "farm": "Farm_2",
                "BM1818": "100/100", "BM1824": "100/100", "BM2113": "100/100",
                "CSRM60": "100/100", "CSSM66": "100/100", "CYP21": "100/100",
                "ETH10": "100/100", "ETH225": "100/100", "ETH3": "100/100",
                "ILSTS6": "100/100", "INRA023": "100/100", "RM067": "100/100",
                "SPS115": "100/100", "TGLA122": "100/100",
                "TGLA126": "100/100", "TGLA227": "100/100",
                "TGLA53": "100/100", "MGTG4B": "100/100", "SPS113": "100/100",
            },
            {
                "name": 'Test_5', "number": 5, "farm": "Farm_3",
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
            BullFather.create(**data)

    def test_get_farms(self) -> None:
        """Тестируется загрузка названий хозяйств."""
        farms: set = TestManagerDB.object_test.get_farms(
            BullFather
        )
        test: list = ["Farm_1", "Farm_2", "Farm_3"]
        for farm in test:
            with self.subTest(title=f"Test {farm}"):
                self.assertTrue(farm in list(farms))

    def test_get_data_for_animals(self) -> None:
        pass

    def test_get_data_for_animal(self) -> None:
        """Тестирование загрузки данных по животному"""
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
                BullFather
            )
        )
        for key, label in test_data.items():
            with self.subTest(title=f"Test {key} - {label}"):
                answer = data.get(key)
                self.assertEqual(answer, label)

        data_2: dict = (
            TestManagerDB.object_test.get_data_for_animal(
                132423,
                BullFather
            )
        )
        for key in test_data.keys():
            with self.subTest(title=f"Test {key}"):
                answer = data_2.get(key)
                self.assertEqual(answer, "-")

    def test_save_data_bus_to_db(self) -> None:
        """Проверка сохранения данных в базу данных."""
        number: int = 7586
        data: dict = {
            "number": number,
            "name": "Test",
            "farm": "Test_farm",
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
        }

        TestManagerDB.object_test.save_data_bus_to_db(
            data,
            ProfilsCows
        )
        query = ProfilsCows.select().where(
            ProfilsCows.number == 1413
        )
        self.assertFalse(query.exists())
        query = ProfilsCows.select().where(
            ProfilsCows.number == number
        )
        self.assertTrue(query.exists())
        for key, label in data.items():
            with self.subTest(title=f"Test {key} - {label}"):
                answer = query.dicts().get().get(key)
                self.assertEqual(answer, label)

    def test_donwload_data_farmers(self) -> None:
        pass

    def test_donwload_data_for_animal(self) -> None:
        pass

    def test_donwload_data_for_animals(self) -> None:
        pass


class TestConfigMeneger(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        """
        Создает фикстуры для теста.
        Вызывается однажды перед запуском всех тестов класса.
        """
        cls.object_test: ConfigMeneger = ConfigMeneger()


class TestManagerFile(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        """
        Создает фикстуры для теста.
        Вызывается однажды перед запуском всех тестов класса.
        """
        cls.object_test: ManagerFile = ManagerFile()


class TestParserData(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        """
        Создает фикстуры для теста.
        Вызывается однажды перед запуском всех тестов класса.
        """
        cls.object_test: ParserData = ParserData()


class TestManagerMS(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        """
        Создает фикстуры для теста.
        Вызывается однажды перед запуском всех тестов класса.
        """
        cls.object_test: ManagerDataMS = ManagerDataMS()

    def test_filter_father(self) -> None:
        pass

    def test_search_father(self) -> None:
        pass

    def test_ms_from_word(self) -> None:
        pass

    def test_ms_select(self) -> None:
        pass

    def test_name_select(self) -> None:
        pass

    def test_check_error_ms(self) -> None:
        pass

    def test_verification_ms(self) -> None:
        pass

    def test_data_verification(self) -> None:
        pass

    def test_check_conclusion(self) -> None:
        pass

    def test_split__(self) -> None:
        pass

    def test_split_locus(self) -> None:
        pass

    def test_transform_data_for_database(self) -> None:
        pass

    def test_save_text_to_file(self) -> None:
        pass

    def test_get_summary_data_error(self) -> None:
        pass

    def test_ms_join(self) -> None:
        pass

    def test_split_data_from_row(self) -> None:
        pass

    def test_combine_all_docx(self) -> None:
        pass

    def test_creat_doc_pas_gen(self) -> None:
        pass


class TestManagerUtilities(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        """
        Создает фикстуры для теста.
        Вызывается однажды перед запуском всех тестов класса.
        """
        cls.object_test: ManagerUtilities = ManagerUtilities()

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


class TestManagerISSR(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Создает фикстуры для теста.
        Вызывается однажды перед запуском всех тестов класса.
        """
        cls.calc: ManagerDataISSR = ManagerDataISSR()

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
        answer: pd.DataFrame = TestManagerISSR.calc.data_transpose(
            data_test,
            index_values
        )
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

    def test_issr_analis(self) -> None:
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

        answer: pd.DataFrame = TestManagerISSR.calc.issr_analis(
            r"tests\test_data\test_issr.csv",
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


if __name__ == "__main__":
    DB_TEST.connect()
    ProfilsCows.bind(DB_TEST)
    BullFather.bind(DB_TEST)
    Logs.bind(DB_TEST)
    databases = [BullFather, ProfilsCows, Logs]
    DB_TEST.create_tables(databases)

    unittest.main()

    #DB_TEST.drop_tables(databases)
