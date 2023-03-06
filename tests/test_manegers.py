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


if __name__ == "__main__":
    unittest.main()
    