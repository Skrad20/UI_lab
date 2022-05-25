from models.models import BullFather

res = (BullFather
       .update(number=3144578369)
       .where(BullFather.number == 1795)
       .execute()
       )
print(res)
