import peewee

from constants import DB_PATH

# Set Database
db = peewee.SqliteDatabase(DB_PATH)


class Account(peewee.Model):

	uuid = peewee.UUIDField(primary_key=True)
	full_name = peewee.CharField(max_length=50)
	balance = peewee.IntegerField()
	holds = peewee.IntegerField()
	is_opened = peewee.BooleanField(default=True)

	class Meta:
		database = db
		db_table = 'accounts'
