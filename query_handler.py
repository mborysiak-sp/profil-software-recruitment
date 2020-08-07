from utils import string_to_date
from password_rater import Password, PasswordRater
from database_handler import Person


class QueryHandler:
    """
    Class storing methods for basic database queries
    """
    def get_all_persons(self):
        """Select all persons from database query. Used as a base of other methods"""
        return Person.select()

    def get_all(self, searched_key, searched_value):
        """
        Gets a list of requested values ecause of how json is formatted we have to call for a [key][value] to get
        the exact value.
        :param searched_key: Searched key of dictionary
        :param searched_value: Searched value of that key
        :return: list of values
        """
        persons = self.get_all_persons().dicts()
        values = []
        for person in persons:
            values.append(person[searched_key][searched_value])
        return values


class CommonElementsHandler(QueryHandler):
    """Class inheriting from QueryHandler and adding methods for getting common elements from data"""
    def __init__(self, searched_key, searched_value):
        """
        :param searched_key: Searched key string
        :param searched_value: Searched value storing another key string
        """
        self.searched_value = searched_value
        self.searched_key = searched_key

    def sort_dictionary_decreasing(self, dictionary):
        """
        Sorts dictionary in decreasing order to get the highest values first
        :param dictionary: Dictionary value storing the data
        :return: Sorted dictionary by key assigned values
        """
        return sorted(dictionary.items(), key=lambda x: x[1], reverse=True)

    def get_counts(self):
        """
        Assigns values to keys by incrementing them
        :return: Dictionary of keys with their counts as values
        """
        dictionary = {}
        for value in self.get_all(self.searched_key, self.searched_value):
            dictionary[value] = dictionary.setdefault(value, 0) + 1
        return dictionary

    def get_n_common_values(self, n):
        """
        Calls sort_dictionary_decreasing
        :param n: number of most common values
        :return: list of n most common values
        """
        sorted_values = self.sort_dictionary_decreasing(self.get_counts())
        return sorted_values[0:n]


class CommonPasswordsHandler(CommonElementsHandler):
    """Class inheriting from CommonElementsHandler to get only most popular passwords"""
    def __init__(self):
        super().__init__("login", "password")

    def get_n_common_passwords(self, n):
        """
        Method getting n most common passwords.
        :param n: number of requested passwords
        :return: sorted list of most common passwords
        """
        return self.get_n_common_values(n)


class CommonCitiesHandler(CommonElementsHandler):
    """Class inheriting from CommonElementsHandler to get only most popular cities"""
    def __init__(self):
        super().__init__("location", "city")

    def get_n_common_cities(self, n):
        """
        Method getting n most common cities.
        :param n: number of requested cities
        :return: sorted list of most common cities
        """
        return self.get_n_common_values(n)


class PasswordHandler(QueryHandler):
    """Class for rating given passwords"""
    def __init__(self):
        self.best_password = Password("")

    def get_all_passwords(self):
        """
        Gets all passwords from database
        :return: list of all passwords
        """
        return self.get_all("login", "password")

    def rate_passwords(self):
        """
        Rates all passwords got by get_all_passwords() method and assigns rating to them. If current rating is better
        than stored one in class object then it is replaced by check_rating() method
        """
        for password in self.get_all_passwords():
            temp_password_rater = PasswordRater(password)
            temp_password_rater.rate_password()
            self.check_rating(temp_password_rater)

    def get_best_password(self):
        """
        Calls rate_passwords() method to get the best one and then returns it
        :return: best password object
        """
        self.rate_passwords()
        return self.best_password

    def check_rating(self, password_with_rating):
        """
        Checks if given password is better than the stored one and if true, replaces it
        :param password_with_rating: password with calculated rating
        """
        if password_with_rating.get_rating() > self.best_password.get_rating():
            self.best_password = password_with_rating


class DateHandler(QueryHandler):
    """Class for managing date related queries"""
    def __init__(self, first_date, second_date):
        """
        :param first_date: first date string to be compared
        :param second_date: second date string to be compared
        """
        self.first_date = string_to_date(first_date, "%Y-%m-%d")
        self.second_date = string_to_date(second_date, "%Y-%m-%d")

    def get_persons_between_dates(self):
        """
        Returns filtered list of all persons born between dates
        :return: list of person dictionaries
        """
        return list(filter(lambda person: self.first_date
                                     < string_to_date(person["dob"]["date"],
                                                      "%Y-%m-%dT%H:%M:%S.%fZ")
                                     < self.second_date, self.get_all_persons().dicts()))


class GenderHandler(QueryHandler):
    """Class for managing all gender related queries"""
    def get_persons_by_gender(self, gender):
        """
        :param gender: string with gender name
        :return: list of persons with given gender
        """
        return Person.select().where(Person.gender == gender)

    def get_gender_percent(self, gender):
        """
        Calculates what percent of total population given gender makes
        :param gender: string with gender name
        :return: int with percentage
        """
        count = self.get_persons_by_gender(gender).count()
        total_count = self.get_all_persons().count()
        return count / total_count * 100

    def calculate_average_age(self, persons, count):
        """
        Calculates average age of persons in list
        :param persons: list of persons
        :param count: count of persons
        :return: int with average age of persons
        """
        temp_sum = 0
        for person in persons:
            temp_sum = temp_sum + int(person["dob"]["age"])
        return temp_sum / count

    def get_average_gender_age(self, gender):
        """
        Gets average age for given gender
        :param gender: string with gender name
        :return: average age of persons with gender parameter matching
        """
        if gender == "all":
            return self.calculate_average_age(self.get_all_persons().dicts(),
                                              self.get_all_persons().count())

        return self.calculate_average_age(self.get_persons_by_gender(gender).dicts(),
                                          self.get_persons_by_gender(gender).count())
