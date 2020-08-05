import json
import re
from datetime import datetime
from datetime import date
from utils import string_to_date
from api import Api


class JsonLoader:

    def __init__(self):
        self.data = {}

    def load_file(self, filename):
        with open(filename, 'r', encoding="utf-8") as file:
            self.data = json.load(file)

    def load_data_from_api(self, n):
        self.data["results"] = []
        for i in range(0, int(n)):
            self.data["results"].append((Api.get("https://randomuser.me/api/")["results"][0]))

    def save_file(self, filename):
        with open(filename, 'w') as file:
            json.dump(self.data, file)

    def modify_file(self):
        if self.data is not None:
            for element in self.data["results"]:
                element.pop("picture", None)
                self.fix_numbers(element)
                self.add_days_to_birthday(element)

    def remove_special_characters(self, number):
        result = re.sub("[^0-9]+", "", number)
        return result

    def fix_numbers(self, element):
        if element["phone"] is not None:
            element["phone"] = self.remove_special_characters(element["phone"])
        if element["cell"] is not None:
            element["cell"] = self.remove_special_characters(element["cell"])

    def days_difference(self, d1, d2):
        if type(d1) is str:
            d1 = string_to_date(d1, "%Y-%m-%dT%H:%M:%S.%fZ")
        if type(d2) is str:
            d2 = string_to_date(d2, "%Y-%m-%dT%H:%M:%S.%fZ")
            d2 = date(datetime.now().year, d2.month, d2.day)
        result = (d1 - d2).days
        if result < 0:
            result = 365 - abs(result)
        return result

    def calculate_days_to_birthday(self, dob):
        current_date = date.today()
        dtb = self.days_difference(current_date, dob["date"])
        dtb = str(dtb).split(',')
        return dtb

    def add_days_to_birthday(self, element):
        if element is not None:
            element["dtb"] = self.calculate_days_to_birthday(element["dob"])
