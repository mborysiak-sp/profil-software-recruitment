import json
import sqlite3
import re
from datetime import datetime
from datetime import date

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
                self.fix_numbers(element)
                self.add_days_to_birthday(element)


    def fix_numbers(self, element):
        if element["phone"] is not None:
           element["phone"] = self.remove_special_characters(element["phone"])
        if element["cell"] is not None:
           element["cell"] = self.remove_special_characters(element["cell"])


    def remove_special_characters(self, number):
        result = re.sub("[^0-9]+", "", number)
        return result


    def add_days_to_birthday(self, element):
        if element is not None:
            element["dtb"] = self.calculate_days_to_birthday(element["dob"])


    def calculate_days_to_birthday(self, dob):
        current_date = date.today()
        dtb = self.days_difference(current_date, dob["date"])
        dtb = str(dtb).split(',')
        print("days to birthday" + str(dtb))
        return dtb


    def days_difference(self, d1, d2):
        date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
        if type(d1) is str:
            d1 = datetime.strptime(d1, date_format).date()
        if type(d2) is str:
            d2 = datetime.strptime(d2, date_format).date()
            d2 = date(datetime.now().year, d2.month, d2.day)
        return d1 - d2
        