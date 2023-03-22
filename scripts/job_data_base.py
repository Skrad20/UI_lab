from code_app.models import BullFather


class JobDataBaseBullFather:
    """Функции для работы с базами данных Peewee"""
    def __init__(self):
        self.name = None

    @staticmethod
    def update_number_bull(number, new_val):
        (
            BullFather
            .update(number=new_val)
            .where(BullFather.number == number)
            .execute()
        )

    @staticmethod
    def delete_bull(number):
        res = (
            BullFather
            .get(BullFather.number == number)
        )
        res.delete_instance()

    @staticmethod
    def update_name_farm(old_val, new_val):
        (
            BullFather
            .update(farm=new_val)
            .where(BullFather.farm == old_val)
            .execute()
        )

    @staticmethod
    def delete_data_in_table(value):
        BullFather.delete().where(BullFather.number == value)


if __name__ == "__main__":
    instance = JobDataBaseBullFather()
    for number in [691, 1056, 397, 998, 704, 816]:
        instance.delete_bull(number)
    print('Ok')
