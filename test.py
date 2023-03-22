from code_app import models

print(*models.Sheep.get_filds(), sep="\n")
print(*models.Deer.get_filds(), sep="\n")
