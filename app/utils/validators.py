import re
from datetime import datetime

class Validators:
    @staticmethod
    def validate_email(email):
        # More comprehensive email validation pattern
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_password(password):
        # Check for minimum length, uppercase, lowercase, number and special character
        if len(password) < 8:
            return False
        if not re.search(r'[A-Z]', password):
            return False
        if not re.search(r'[a-z]', password):
            return False
        if not re.search(r'[0-9]', password):
            return False
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False
        return True
    
    @staticmethod
    def validate_name(name):
        # Allow only letters, spaces and hyphens, minimum 2 characters
        return bool(re.match(r'^[A-Za-z\s-]{2,}$', name))
    
    @staticmethod
    def validate_phone(phone):
        # International phone number format (simplified)
        return bool(re.match(r'^\+?[1-9]\d{9,14}$', phone))

    @staticmethod
    def validate_isbn(isbn):
        # ISBN-10 or ISBN-13 validation
        isbn = isbn.replace('-', '').replace(' ', '')
        return bool(re.match(r'^(97(8|9))?\d{9}(\d|X)$', isbn))

    @staticmethod
    def validate_price(price):
        # Price should be positive and have max 2 decimal places
        try:
            return price > 0 and len(str(float(price)).split('.')[-1]) <= 2
        except (ValueError, TypeError):
            return False

    @staticmethod
    def validate_stock(stock):
        # Stock should be a non-negative integer
        try:
            return isinstance(stock, int) and stock >= 0
        except ValueError:
            return False

    @staticmethod
    def validate_date(date):
        # Support multiple date formats
        formats = ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d', '%d/%m/%Y']
        for fmt in formats:
            try:
                datetime.strptime(date, fmt)
                return True
            except ValueError:
                continue
        return False

    @staticmethod
    def validate_enum(value, enum_values):
        return value in enum_values

    @staticmethod
    def validate_boolean(value):
        return isinstance(value, bool)
