from code_app.models import BullFather


def delete_rows(number: int):
    query = BullFather.delete().where(BullFather.number > number)
    query.execute()


if __name__ == "__main__":
    delete_rows(1)
