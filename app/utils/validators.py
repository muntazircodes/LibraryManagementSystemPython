import re

class Thevalidators:
    @staticmethod
    def validate_email(email):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return False
        return True
    
    @staticmethod
    def validate_password(password):
        if len(password) < 8:
            return False
        return True
    
    @staticmethod
    def validate_name(name):
        if len(name) < 3:
            return False
        return True
    
    @staticmethod
    def validate_phone(phone):
        if len(phone) < 10 or not re.match(r"^[0-9]+$", phone):
            return False
        return True

    @staticmethod
    def validate_isbn(isbn):
        if not re.match(r"^(97(8|9))?\d{9}(\d|X)$", isbn):
            return False
        return True

    @staticmethod
    def validate_price(price):
        if price < 0:
            return False
        return True

    @staticmethod
    def validate_stock(stock):
        if stock < 0:
            return False
        return True

    @staticmethod
    def validate_date(date):
        try:
            from datetime import datetime
            datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
            return True
        except ValueError:
            return False

    @staticmethod
    def validate_enum(value, enum_values):
        if value not in enum_values:
            return False
        return True

    @staticmethod
    def validate_boolean(value):
        if not isinstance(value, bool):
            return False
        return True
