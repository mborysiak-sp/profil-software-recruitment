from datetime import datetime


def string_to_date(string, date_format):
    return datetime.strptime(string, date_format).date()
