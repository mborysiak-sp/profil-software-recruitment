import json
import re
from datetime import datetime
from datetime import date


def remove_special_characters(number):
    result = re.sub("[^0-9]+", "", number)
    return result


def fix_numbers(element):
    if element["phone"] is not None:
        element["phone"] = remove_special_characters(element["phone"])
    if element["cell"] is not None:
        element["cell"] = remove_special_characters(element["cell"])


def days_difference(d1, d2):
    date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
    if type(d1) is str:
        d1 = datetime.strptime(d1, date_format).date()
    if type(d2) is str:
        d2 = datetime.strptime(d2, date_format).date()
        d2 = date(datetime.now().year, d2.month, d2.day)
    result = (d1 - d2).days
    if result < 0:
        result = 365 - abs(result)
    return result


def calculate_days_to_birthday(dob):
    current_date = date.today()
    dtb = days_difference(current_date, dob["date"])
    dtb = str(dtb).split(',')
    print("days to birthday" + str(dtb))
    return dtb


def add_days_to_birthday(element):
    if element is not None:
        element["dtb"] = calculate_days_to_birthday(element["dob"])


class JsonLoader:
    def __init__(self):
        self.data = {}

    def load_file(self, filename):
        print("attempting to load file")
        with open(filename, 'r', encoding="utf-8") as file:
            self.data = json.load(file)

    def save_file(self, filename):
        print("attempting to save file")
        with open(filename, 'w') as file:
            json.dump(self.data, file)

    def modify_file(self):
        print("attempting to modify file")
        if self.data is not None:
            for element in self.data["results"]:
                element.pop("picture", None)
                fix_numbers(element)
                add_days_to_birthday(element)
