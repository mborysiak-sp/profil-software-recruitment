import json
import sqlite3
import re
import datetime

class JsonLoader:

    def __init__(self):
        self.data = {}


    def load_file(self):
        filename = "persons.json"

        with open(filename, "r+") as file:
            self.data = json.load(file)
    

    def modify_file(self):
        if self.data is not None:                
            for element in self.Data:
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
        current_date = datetime.date.today()
        dtb = self.days_difference(current_date, dob)
        return dtb


    def days_difference(self, d1, d2):
        date_format = "%Y-%m-%d"
        d1 = datetime.strptime(d1, date_format)
        d2 = datetime.strptime(d2, date_format)
        return abs(d1 - d2)
        