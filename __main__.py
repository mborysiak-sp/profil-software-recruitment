from database_handler import DatabaseHandler
from json_loader import JsonLoader


def get_modified_json():
    json_loader = JsonLoader()
    json_loader.load_file("persons.json")
    json_loader.modify_file()
    return json_loader.data


def __main__():
    data = get_modified_json()["results"]
    database_handler = DatabaseHandler()
    database_handler.insert_json(data)
    # print(database_handler.get_gender_percent("male"))
    # print(database_handler.get_gender_percent("female"))
    # print(database_handler.get_average_gender_age("male"))
    # print(database_handler.get_average_gender_age("female"))
    # print(database_handler.get_average_gender_age("all"))
    database_handler.get_n_popular_cities(5)


if __name__ == "__main__":
    __main__()
