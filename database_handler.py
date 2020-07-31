import sqlite3


def init_database():
    connection = sqlite3.connect("persons.db")

    cursor = connection.cursor()

    sql_create_command = """CREATE TABLE IF NOT EXISTS
        person(id INTEGER PRIMARY KEY, data json)"""

    cursor.execute(sql_create_command)