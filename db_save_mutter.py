import pandas as pd

from models.models import ProfilsCows

df = pd.read_csv("data/profils_mutter_split.csv", sep=';', encoding='cp1251')
df = df.drop_duplicates(subset=['number']).reset_index(drop=True)
for i in range(len(df)):
    query = ProfilsCows.select().where(ProfilsCows.number == df.loc[i, 'number'])
    if query.exists():
        pass
    else:
        try:
            bus = ProfilsCows(
                name=df.loc[i, "name"],
                number=float(df.loc[i, "number"]),
                farm=df.loc[i, "farm"],
                BM1818=df.loc[i, "BM1818"],
                BM1824=df.loc[i, "BM1824"],
                BM2113=df.loc[i, "BM2113"],
                CSRM60=df.loc[i, "CSRM60"],
                CSSM66=df.loc[i, "CSSM66"],
                CYP21=df.loc[i, "CYP21"],
                ETH10=df.loc[i, "ETH10"],
                ETH225=df.loc[i, "ETH225"],
                ETH3=df.loc[i, "ETH3"],
                ILSTS6=df.loc[i, "ILSTS6"],
                INRA023=df.loc[i, "INRA023"],
                RM067=df.loc[i, "RM067"],
                SPS115=df.loc[i, "SPS115"],
                TGLA122=df.loc[i, "TGLA122"],
                TGLA126=df.loc[i, "TGLA126"],
                TGLA227=df.loc[i, "TGLA227"],
                TGLA53=df.loc[i, "TGLA53"],
                MGTG4B=df.loc[i, "MGTG4B"],
                SPS113=df.loc[i, "SPS113"],
            )
            bus.save()
        except Exception as e:
            print(
                df.loc[i, "name"],
                df.loc[i, "number"]
            )
            print(e)
