import pandas as pd
import unittest
from code.managers import ManagerDataISSR
from models.models import BaseModelAnimal
from setting import DB_TEST


class TestManagerISSR(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Создает фикстуры для теста.
        Вызывается однажды перед запуском всех тестов класса.
        """
        DB_TEST.create_tables([BaseModelAnimal])
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
        self.assertEqual(answer, "AG38")
        answer = TestManagerISSR.calc.genotype_issr(row, "G")
        self.assertEqual(answer, "GA1")

    def test_data_transpose(self) -> None:
        """Проверяет транспонирование матриц таблиц."""

        data_test: pd.DataFrame = pd.DataFrame(
            data=[
                [1.0, 2344, 2324],
                [1.099, 1234, None],
                [1.09999, 232, None],
                [2.0, 2368, 2158],
                [2.099, 1254, 1269],
                [2.09999, 956, 321],
            ],
            columns=['animal', 'AG', "GA"]
        )

        index_values = pd.DataFrame(data_test['animal'].value_counts())
        index_values = index_values.reset_index()
        index_values.columns = ['num', 'chast']
        index_values['num'] = index_values['num'].astype('float')
        index_values = index_values.sort_values(by=['num'], ascending=True)
        index_values = index_values.reset_index()
        
        data_answer: pd.DataFrame = pd.DataFrame(
            data=[
                [1.0, 2344, 1.0, 2324],
                ["1.099", 1234, None, None],
                ["1.09999", 232, None, None],
                [2.0, 2368, 2.0, 2158],
                ["2.099", 1254, 2.099, 1269],
                ["2.09999", 956, 2.09999, 321],
            ],
            columns=['animal', 'GA', 'animal_1', 'AG']
        )
        answer: pd.DataFrame = TestManagerISSR.calc.data_transpose(
            data_test,
            index_values
        )
        print(answer)
        with self.subTest(error=data_answer.compare(answer)):
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
        pass

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
    unittest.main()