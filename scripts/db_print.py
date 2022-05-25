from models.models import ProfilsCows

res = (ProfilsCows
       .select()
       .where(ProfilsCows.number == 1442)
       .get()
       )
print(res.id)
