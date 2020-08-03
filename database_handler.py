import json
from peewee import Model, TextField, chunked
from playhouse.sqlite_ext import SqliteExtDatabase


class DatabaseHandler:

    db = SqliteExtDatabase("persons.db", pragmas=(
        ("cache_size", -1024 * 64),
        ("journal_mode", "wal"),
        ("foreign_keys", 1)))

    def __init__(self):
        self.create_person_table()

    def create_person_table(self):
        Person.create_table()

    def insert_json(self, data):
        with self.db.atomic():
            for batch in chunked(data, 5):
                Person.insert_many(batch).execute()


class Person(Model):
    class MyJSONField(TextField):
        def db_value(self, value):
            return json.dumps(value)

        def python_value(self, value):
            if value is not None:
                return json.loads(value)
            return None

    class Meta:
        database = DatabaseHandler.db

    __tablename__ = "person"
    gender = TextField()
    name = MyJSONField()
    location = MyJSONField()
    email = TextField()
    login = MyJSONField()
    dob = MyJSONField()
    dtb = TextField()
    registered = MyJSONField()
    phone = TextField()
    cell = TextField()
    id = MyJSONField()
    nat = TextField()