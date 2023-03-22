import requests
import os
from urllib.parse import urlencode
import pandas as pd
from code_app.models import BullFather


def donwload_data() -> str:
     base_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?'
     public_key = 'https://disk.yandex.ru/i/jogEfkP7VAV1ow'
     final_url = base_url + urlencode(dict(public_key=public_key))
     response = requests.get(final_url)
     download_url = response.json()['href']

     rq = requests.get(download_url)
     file_name = "update_database.xlsx"
     basname = os.path.join(os.getcwd(), "data")
     path = os.path.join(basname, file_name)

     with open(path, 'wb+') as file:
          file.write(rq.content)

     return path

def update_db(path: str) -> None:
     df = pd.read_excel(path)
     df = df.reset_index(drop=True)
     for i in range(len(df)):
          query = BullFather.select().where(
               BullFather.number == df.loc[i, 'number'],
               BullFather.farm == df.loc[i, 'farms'],
          )
          if query.exists():
               pass
          else:
               try:
                    print(df.loc[i, "name"])
                    bus = BullFather(
                         name=df.loc[i, "name"],
                         number=float(df.loc[i, "number"]),
                         farm=df.loc[i, "farms"],
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


if __name__ == "__main__":
     update_db(donwload_data())
