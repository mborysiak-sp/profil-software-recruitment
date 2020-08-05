from database_handler import DatabaseHandler, Person
from query_handler import PopularElementsHandler, PasswordHandler, DateHandler
from json_loader import JsonLoader


def get_modified_json():
    my_json_loader = JsonLoader()
    my_json_loader.load_file("persons.json")
    my_json_loader.modify_file()
    return my_json_loader.data


def __main__():
    data = get_modified_json()["results"]
    my_database_handler = DatabaseHandler()
    my_database_handler.insert_data(data)
    # print(database_handler.get_gender_percent("male"))
    # print(database_handler.get_gender_percent("female"))
    # print(database_handler.get_average_gender_age("male"))
    # print(database_handler.get_average_gender_age("female"))
    # print(database_handler.get_average_gender_age("all"))

    # my_cities_handler = PopularElementsHandler(Person.location, ("location", "city"))
    # my_passwords_handler = PopularElementsHandler(Person.login, ("login", "password"))
    # for element in my_cities_handler.get_n_popular_values(5):
    #     print(element)
    # for element in my_passwords_handler.get_n_popular_values(5):
    #     print(element)

    # my_date_handler = DateHandler("1948-10-10", "1970-10-10")
    # for person in my_date_handler.get_persons_between_dates():
    #     print(person["dob"]["date"])

    my_password_handler = PasswordHandler()
    print(my_password_handler.get_best())


if __name__ == "__main__":
    __main__()
