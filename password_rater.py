from string import printable


class Password:

    def __init__(self, password):
        self.password: str = password
        self.rating = 0

    def get_rating(self):
        return self.rating

    def get_password(self):
        return self.password

    def __str__(self):
        return "Password: "\
               + self.get_password()\
               + " Rating: " \
               + str(self.get_rating())


class PasswordRater(Password):

    def increase_rating_by(self, number):
        self.rating = self.rating + number

    def rate_password(self):
        self.check_for_small_letter()
        self.check_for_capital_letter()
        self.check_for_digit()
        self.check_for_special_char()
        self.check_for_8_chars()

    def check_for_small_letter(self):
        if any(char.islower() for char in self.password):
            self.increase_rating_by(1)

    def check_for_capital_letter(self):
        if any(char.isupper() for char in self.password):
            self.increase_rating_by(2)

    def check_for_digit(self):
        if any(char.isdigit() for char in  self.password):
            self.increase_rating_by(1)

    def check_for_special_char(self):
        if set(self.password).difference(printable):
            self.increase_rating_by(3)

    def check_for_8_chars(self):
        if len(self.password) >= 8:
            self.increase_rating_by(5)
