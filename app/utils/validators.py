import re
from datetime import datetime
from typing import Any, Union

class Validators:

    @staticmethod
    def validate_email(email: Any) -> bool:
        if not isinstance(email, str):
            return False
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_password(password: Any) -> bool:
        if not isinstance(password, str):
            return False
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
    def validate_name(name: Any) -> bool:
        if not isinstance(name, str):
            return False
        return bool(re.match(r'^[A-Za-z\s-]{2,}$', name))
    
    @staticmethod
    def validate_phone(phone: Any) -> bool:
        if not isinstance(phone, str):
            return False
        return bool(re.match(r'^\+?[1-9]\d{9,14}$', phone))

    @staticmethod
    def validate_isbn(isbn: Any) -> bool:
        if not isinstance(isbn, str):
            return False
        isbn = isbn.replace('-', '').replace(' ', '')
        return bool(re.match(r'^(97(8|9))?\d{9}(\d|X)$', isbn))

    @staticmethod
    def validate_price(price: Any) -> bool:
        if isinstance(price, str):
            try:
                price = float(price)
            except ValueError:
                return False
        if not isinstance(price, (int, float)):
            return False
        try:
            return price > 0 and len(str(float(price)).split('.')[-1]) <= 2
        except (ValueError, TypeError):
            return False

    @staticmethod
    def validate_stock(stock: Any) -> bool:
        if isinstance(stock, str):
            try:
                stock = int(stock)
            except ValueError:
                return False
        return isinstance(stock, int) and stock >= 0

    @staticmethod
    def validate_date(date: Any) -> bool:
        if not isinstance(date, str):
            return False
        formats = ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d', '%d/%m/%Y']
        for fmt in formats:
            try:
                datetime.strptime(date, fmt)
                return True
            except ValueError:
                continue
        return False

    @staticmethod
    def validate_enum(value: Any, enum_values: list) -> bool:
        return value in enum_values

    @staticmethod
    def validate_boolean(value: Any) -> bool:
        if isinstance(value, str):
            return value.lower() in ('true', 'false', '1', '0')
        return isinstance(value, bool)
