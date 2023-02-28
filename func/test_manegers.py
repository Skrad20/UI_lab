import pandas as pd




def genotype_issr(row: pd.Series, genotype: str = "G") -> str:
        """Функция определения принадлежности данных к аллели"""
        """
        Описание

        Параметры:
        ----------
            genotype: str = "G" - вариант генотипа
        Возвращает:
        ----------
            str - название аллели
        """
        dict_genotype = {
            "G": "GA",
            "A": "AG"
        }
        list_size = [
            2500, 2300, 2000, 1800, 1700, 1600, 1500, 1400, 1300,
            1240, 1180, 1120, 1060, 1000, 940, 880, 820, 760, 720,
            680, 640, 600, 560, 530, 500, 470, 440, 410, 380, 360,
            340, 320, 300, 280, 260, 240, 220, 200, 160,
        ]

        size = row[dict_genotype.get(genotype)]
        temp_i = 0
        genotype_result = "-"
        if size > 2500 or size < 160:
            genotype_result = "-"
        else:
            temp_i = bunary_search(list_size, 0, len(list_size)-1, size)
            genotype_result = genotype + str(temp_i)

        return genotype_result


if "__main__" == __name__:
    test_data = [2600, 2400, 2150, 1750, 800, 178, 158]
    for elem in test_data:
        series = pd.Series(index=["GA"], data=[elem])
        print(elem, genotype_issr(series, genotype="G"))
    print("#########################################")
    test_data = [1, 3, 5, 7, 9, 10, 14]
    for i in [2,4,6,8,12,16]:
        print(bunary_search(test_data, 0, len(test_data)-1, i))
