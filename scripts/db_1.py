import pandas as pd

from models.models import BullFather
from setting import DB as db

res = (BullFather
       .update(number=3144578369)
       .where(BullFather.id==197)
       .execute())
