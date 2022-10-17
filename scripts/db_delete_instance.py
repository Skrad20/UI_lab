from models.models import BullFather


res = (BullFather
       .get(BullFather.number == 4240000000)
       )

print(res)
res.delete_instance()
