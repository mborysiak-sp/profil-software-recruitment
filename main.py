from database_handler import init_database
from json_loader import JsonLoader


def modify_file():
    jsonloader = JsonLoader()
    jsonloader.load_file("persons.json")
    jsonloader.modify_file()
    jsonloader.save_file("edited.json")


def __main__():
    init_database()
    modify_file()
    

if __name__ == "__main__":
    __main__()