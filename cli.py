import click
from database_handler import Person, DatabaseHandler
from query_handler import GenderHandler, DateHandler, PasswordHandler, PopularElementsHandler
from json_loader import JsonLoader


@click.group()
def cli():
    pass


@cli.command(help="Options: \"male\", \"female\", \"all\"")
@click.argument("gender", nargs=1)
def average_age(gender):
    temp_gender_handler = GenderHandler()
    click.echo(f"Average age for {gender}: {temp_gender_handler.get_average_gender_age(gender)}")


@cli.command(help="Prints -n most common cities")
@click.argument("n", nargs=1, type=int)
def most_common_cities(n):
    temp_cities_handler = PopularElementsHandler(Person.location, ("location", "city"))
    click.echo(f"Most common cities: {temp_cities_handler.get_n_popular_values(n)}")


@cli.command(help="Prints -n most common passwords")
@click.argument("n", nargs=1, type=int)
def most_common_passwords(n):
    temp_passwords_handler = PopularElementsHandler(Person.login, ("login", "password"))
    click.echo(f"Most common passwords: {temp_passwords_handler.get_n_popular_values(n)}")


@cli.command(help="Prints list of persons born between given dates")
@click.argument("dates", nargs=2)
def persons_between_dates(dates):
    temp_date_handler = DateHandler(dates[0], dates[1])
    click.echo(f"Persons between dates: {temp_date_handler.get_persons_between_dates()}")


@cli.command(help="Prints safest password from database with it's rating")
def safest_password():
    temp_password_handler = PasswordHandler()
    click.echo(f"Safest password from database: {temp_password_handler.get_best()}")


@cli.command(help="Loads given file to database")
@click.argument("file", nargs=1)
def load(file):
    temp_json_loader = JsonLoader()
    temp_json_loader.load_file(file)
    temp_json_loader.modify_file()
    temp_database_handler = DatabaseHandler()
    temp_database_handler.insert_data(temp_json_loader.data["results"])
    click.echo("File loaded")


if __name__ == '__main__':
    cli()
