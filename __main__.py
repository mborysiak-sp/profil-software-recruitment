import database_handler
from json_loader import JsonLoader


def get_modified_json():
    json_loader = JsonLoader()
    json_loader.load_file("persons.json")
    json_loader.modify_file()
    return json_loader.data


def __main__():
    data = get_modified_json()["results"]
    database_handler.insert_json(data)


if __name__ == "__main__":
    __main__()
