from models.models import BullFather


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
    def get_bull_per_number(number):
        return BullFather.select().where(
            BullFather.number == number
        ).exists()

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


if __name__ == "__main__":
    instance = JobDataBaseBullFather()
    print(instance.get_bull_per_number(1073))
    print('Ok')
