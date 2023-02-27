from models.models import BullFather


res = (BullFather
       .get(True)
       )

res.delete_instance()
