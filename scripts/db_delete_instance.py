from code_app.models import BullFather


res = (BullFather
       .get(True)
       )

res.delete_instance()
