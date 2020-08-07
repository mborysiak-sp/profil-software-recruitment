import json
import re
from datetime import datetime
from datetime import date
from utils import string_to_date
from api import Api


class JsonLoader:
    """Class that loads and modifies data stored in json format"""
    def __init__(self):
        self.data = {}

    def load_file(self, filename):
        """Load specified filename into the object data field"""
        with open(filename, 'r', encoding="utf-8") as file:
            self.data = json.load(file)

    def load_data_from_api(self, n):
        """
        Load specified amount of users from predefined api
        :param n: number of users to be loaded
        """
        self.data["results"] = []
        for i in range(0, int(n)):
            self.data["results"].append((Api.get("https://randomuser.me/api/")["results"][0]))

    def save_file(self, filename):
        """
        Saves data stored currently in data as json file.s
        :param filename: Name of file to be saved to
        """
        with open(filename, 'w') as file:
            json.dump(self.data, file)

    def modify_file(self):
        """
        Modifies data stored in object's data field by deleting every "picture" field, removing special characters
        from numbers and calculating days to person's birthday
        """
        if self.data is not None:
            for element in self.data["results"]:
                # This dictionary method removes 'picture' element and if it's not present, inserts 'None'
                element.pop("picture", None)
                self.fix_numbers(element)
                self.add_days_to_birthday(element)

    def remove_not_numbers(self, number):
        """
        Removes all characters save numbers from given number string
        :param number: string containing a number
        :return: Number with only numbers
        """
        result = re.sub("[^0-9]+", "", number)
        return result

    def fix_numbers(self, element):
        """
        If number related fields are not empty, it calls a method to remove special characters from them
        :param element: Single person from data dictionary
        """
        if element["phone"] is not None:
            element["phone"] = self.remove_not_numbers(element["phone"])
        if element["cell"] is not None:
            element["cell"] = self.remove_not_numbers(element["cell"])

    def days_difference(self, d1, d2):
        """
        Calculates difference between two given dates in days
        :param d1: First date
        :param d2: Second date
        :return: Calculated days between dates
        """
        result = (d1 - d2).days
        if result < 0:
            result = 365 - abs(result)
        return result

    def calculate_days_to_birthday(self, dob):
        """
        Converts "dob" parameter from string to date and changes it's year to the current one. Then
        :param dob: date of birth dictionary field from data which stores "date" key inside
        :return: Calculated days to
        """
        current_date = date.today()
        # Get's next birthday date as a current year to get not exact
        birthday_str = dob["date"]
        d = string_to_date(birthday_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        next_birthday_date = date(datetime.now().year, d.month, d.day)
        # If person had birthday in this year, we calculated days to the next year's one by incrementing current year
        if current_date < next_birthday_date:
            next_birthday_date.year = next_birthday_date.year + 1
        # Call method calculating days to birthday
        dtb = self.days_difference(current_date, next_birthday_date)
        # Cut string to get only needed days
        dtb = str(dtb).split(',')
        return dtb

    def add_days_to_birthday(self, element):
        """
        Inserts into given element parameter calculated days to birthday
        :param element: element which should receive a new key "dtb" with days to birthday as it's value
        """
        if element is not None:
            element["dtb"] = self.calculate_days_to_birthday(element["dob"])
