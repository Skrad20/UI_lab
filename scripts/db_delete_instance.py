from models.models import BullFather


res = (BullFather
       .get(BullFather.number == True)
       )

print(res)
res.delete_instance()
