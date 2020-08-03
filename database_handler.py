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

    def get_all_persons(self):
        return Person.select()

    def get_persons_by_gender(self, gender):
        return Person.select().where(Person.gender == gender)

    def get_gender_percent(self, gender):
        count = self.get_persons_by_gender(gender).count()
        total_count = self.get_all_persons().count()
        return count / total_count * 100

    def calculate_average_age(self, persons, count):
        temp_sum = 0
        for person in persons:
            temp_sum = temp_sum + int(person["dob"]["age"])
        return temp_sum / count

    def get_average_gender_age(self, gender):
        if gender == "all":
            return self.calculate_average_age(self.get_all_persons().dicts(),
                                              self.get_all_persons().count())

        return self.calculate_average_age(self.get_persons_by_gender(gender).dicts(),
                                          self.get_persons_by_gender(gender).count())

    def get_city_population(self, city_name):
        population = 0
        cities_with_populations = {}


            # if person["location"]["city"] == city_name:

        # population = self.get_all_persons().where(Person.location == city_name).count()
        # for` location in Person.select(Person.location["location"]["city"]).dicts():
        #     print(location)

    def get_all_cities(self):
        locations = Person.select(Person.location).dicts()
        cities = []
        for location in locations:
            cities.append(location["location"]["city"])
        return list(set(cities))

    def get_n_popular_cities(self, n):
        cities = {}
        for city in self.get_all_cities():
            cities[city] = 0
        for person in self.get_all_persons().dicts():
            cities[person["location"]["city"]] = cities[person["location"]["city"]] + 1
        # print("finished")
        # sorted_cities = sorted(cities.items(), key=lambda x: x[1])
        # for i in sorted_cities:
        #    print(i[0], i[1])


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