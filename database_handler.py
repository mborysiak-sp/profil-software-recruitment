from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase, JSONField

db = SqliteExtDatabase("persons.db", pragmas=(
    ("cache_size", -1024 * 64),
    ("journal_mode", "wal"),
    ("foreign_keys", 1)))


def insert_json(data):
    with db.atomic():
        for batch in chunked(data, 1):
            Person.insert_many(batch).execute()


class Person(Model):
    class Meta:
        database = db

    __tablename__ = "person"

    gender = TextField()
    name = JSONField()
    location = JSONField()
    email = TextField()
    login = JSONField()
    dob = JSONField()
    dtb = TextField()
    registered = JSONField()
    phone = TextField()
    cell = TextField()
    id = JSONField()
    nat = TextField()


Person.create_table()
