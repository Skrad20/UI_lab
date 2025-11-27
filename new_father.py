import pandas as pd

from models.models import BullFather

df = pd.read_excel('data/update_database_father.xlsx')
df = df.drop_duplicates(subset=['number']).reset_index(drop=True)
for i in range(len(df)):
    query = BullFather.select().where(BullFather.number == df.loc[i, 'number'])
    if query.exists():
        pass
    else:
        print(df.loc[i, 'number'])
