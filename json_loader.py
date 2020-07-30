import json
import sqlite3

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
