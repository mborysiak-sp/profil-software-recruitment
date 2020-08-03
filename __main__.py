from database_handler import DatabaseHandler
from query_handler import QueryHandler
from json_loader import JsonLoader


def get_modified_json():
    my_json_loader = JsonLoader()
    my_json_loader.load_file("persons.json")
    my_json_loader.modify_file()
    return my_json_loader.data


def __main__():
    data = get_modified_json()["results"]
    my_database_handler = DatabaseHandler()
    my_database_handler.insert_json(data)
    # print(database_handler.get_gender_percent("male"))
    # print(database_handler.get_gender_percent("female"))
    # print(database_handler.get_average_gender_age("male"))
    # print(database_handler.get_average_gender_age("female"))
    # print(database_handler.get_average_gender_age("all"))
    my_query_handler = QueryHandler()
    my_query_handler.get_n_popular_cities(5)


if __name__ == "__main__":
    __main__()
