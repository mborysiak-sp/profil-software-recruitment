from utils import string_to_date
from password_rater import Password, PasswordRater
from database_handler import Person


class QueryHandler:

    def get_all_persons(self):
        return Person.select()


class PopularElementsHandler(QueryHandler):

    def __init__(self, searched_field, searched_keys):
        self.searched_field = searched_field
        self.searched_keys = searched_keys

    def sort_dictionary_decreasing(self, dictionary):
        return sorted(dictionary.items(), key=lambda x: x[1], reverse=True)

    def get_counts(self):
        # values_tuple[0] are just unique values, values_tuple[1] is list of all values
        values = {}
        values_tuple = self.get_all()
        for value in values_tuple[0]:
            values[value] = 0
        for value in values_tuple[1]:
            values[value] = values[value] + 1
        return values

    def get_all(self):
        elements = Person.select(self.searched_field).dicts()
        values = []
        for element in elements:
            values.append(element[self.searched_keys[0]][self.searched_keys[1]])
        return list(set(values)), values

    def get_n_popular_values(self, n):
        sorted_values = self.sort_dictionary_decreasing(self.get_counts())
        return sorted_values[0:n]


class PasswordHandler(QueryHandler):

    def __init__(self):
        self.best_password = Password("")

    def get_all_passwords(self):
        persons = self.get_all_persons().dicts()
        passwords = []
        for person in persons:
            passwords.append(person["login"]["password"])
        return passwords

    def rate_passwords(self):
        for password in self.get_all_passwords():
            temp_password_rater = PasswordRater(password)
            temp_password_rater.rate_password()
            self.check_rating(temp_password_rater)

    def get_best(self):
        self.rate_passwords()
        return self.best_password

    def change_best_password(self, password_with_rating):
        self.best_password = password_with_rating

    def check_rating(self, password_with_rating):
        if password_with_rating.get_rating() > self.best_password.get_rating():
            self.change_best_password(password_with_rating)


class DateHandler(QueryHandler):

    def __init__(self, first_date, second_date):
        self.first_date = string_to_date(first_date, "%Y-%m-%d")
        self.second_date = string_to_date(second_date, "%Y-%m-%d")

    def get_persons_between_dates(self):
        return filter(lambda person: self.first_date
                                     < string_to_date(person["dob"]["date"],
                                                      "%Y-%m-%dT%H:%M:%S.%fZ")
                                     < self.second_date, self.get_all_persons().dicts())


class GenderHandler(QueryHandler):

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
