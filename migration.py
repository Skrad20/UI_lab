from playhouse.migrate import SqliteDatabase, SqliteMigrator, migrate
import peewee as pw

my_db = SqliteDatabase('db.sqlite3')
migrator = SqliteMigrator(my_db)
number_column = pw.IntegerField(
    null=False,
    verbose_name='Инвертарный номер животного',
    default=0
)

migrate(
    migrator.add_column(
        "BullFather", "number", number_column
    )
)
