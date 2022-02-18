from models.models import BullFather

res = (BullFather
       .update(number=3144578369)
       .where(BullFather.id == 197)
       .execute()
       )
