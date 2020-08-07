import json
from peewee import Model, TextField, chunked
from playhouse.sqlite_ext import SqliteExtDatabase


class DatabaseHandler:
    """Class for managing database connection and loading given data into database"""
    # static field for storing database connection by peewee
    db = SqliteExtDatabase("database.db", pragmas=(
        ("cache_size", -1024 * 64),
        ("journal_mode", "wal"),
        ("foreign_keys", 1)))

    def __init__(self):
        """Calls method create_table for Person class"""
        self.create_table(Person)

    def create_table(self, table_class):
        """Create table from Person class in database"""
        table_class.create_table()

    def insert_data_into_person(self, data):
        """Call insert_data method with Person as parameter"""
        self.insert_data(data, Person)

    def insert_data(self, data, table_class):
        """
        Insert data into database in chunks using peewee functions
        :param table_class: Class which should store the given date in database
        :param data: List of persons to be stored in database
        """
        with self.db.atomic():
            for batch in chunked(data, 5):
                table_class.insert_many(batch).execute()


class Person(Model):
    """Class serving as a model for person table in database"""
    class MyJSONField(TextField):
        """Class for translating strings with json format into strings and vice-versa"""
        def db_value(self, value):
            return json.dumps(value)

        def python_value(self, value):
            if value is not None:
                return json.loads(value)
            return None

    class Meta:
        """Meta class for database connection"""
        database = DatabaseHandler.db

    def __str__(self):
        """
        __str__ overload for Person class
        :return: Name and date of birth of a person
        """
        return f"Name: {self.name}, Date of birth: {self.dob}"

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