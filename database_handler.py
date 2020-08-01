import os
import json
from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase, JSONField

db = SqliteExtDatabase("persons.db", pragmas=(
    ("cache_size", -1024 * 64),
    ("journal_mode", "wal"),
    ("foreign_keys", 1)))


class BaseModel(Model):
    class Meta:
        database = db


class Person(BaseModel):
    __tablename__ = "person"
    json_data = JSONField(json_dumps=json.dumps)


Person.create_table()
