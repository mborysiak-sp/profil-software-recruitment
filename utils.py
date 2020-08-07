from datetime import datetime


def string_to_date(string, date_format):
    """
    Function converting given string to date
    :param string: string containing date
    :param date_format: format in which date is saved in string
    :return: date object
    """
    return datetime.strptime(string, date_format).date()
