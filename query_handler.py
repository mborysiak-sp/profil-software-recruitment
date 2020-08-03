from database_handler import Person


class QueryHandler:

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

    def sort_dictionary_decreasing(self, cities):
        return sorted(cities.items(), key=lambda x: x[1], reverse=True)

    def get_city_populations(self):
        cities = {}
        cities_tuple = self.get_all_cities()
        for city in cities_tuple[0]:
            cities[city] = 0
        for city in cities_tuple[1]:
            cities[city] = cities[city] + 1
        return cities

    def get_all_cities(self):
        locations = Person.select(Person.location).dicts()
        cities = []
        for location in locations:
            cities.append(location["location"]["city"])
        return list(set(cities)), cities

    def get_n_popular_cities(self, n):
        sorted_cities = self.sort_dictionary_decreasing(self.get_city_populations())
        return sorted_cities[0:n]

    def get_all_passwords(self):
        logins = Person.select(Person.login).dicts()
        passwords = []
        for login in logins:
            passwords.append(login["login"]["password"])
        return list(set(passwords)), passwords

    def get_n_popular_passwords(self, n):
        pass