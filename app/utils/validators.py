import re
from datetime import datetime
from typing import Any
from werkzeug.security import generate_password_hash, check_password_hash


class Validators:
    
    @staticmethod
    def validate_boolean(value: Any) -> bool:
        if isinstance(value, str):
            return value.lower() in ('true', 'false', '1', '0')
        return isinstance(value, bool)

    @staticmethod
    def validate_book_condition(condition: Any) -> bool:
        valid_conditions = ['Excellent', 'Good', 'Damaged', 'Torn']
        return isinstance(condition, str) and condition.lower() in valid_conditions

    @staticmethod
    def validate_borrow_period(days: Any) -> bool:
        if isinstance(days, str):
            try:
                days = int(days)
            except ValueError:
                return False
        return isinstance(days, int) and 1 <= days <= 30

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
    def validate_email(email: Any) -> bool:
        if not isinstance(email, str):
            return False
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    @staticmethod
    def validate_enum(value: Any, enum_values: list) -> bool:
        return value in enum_values

    @staticmethod
    def validate_fine_amount(amount: Any) -> bool:
        if isinstance(amount, str):
            try:
                amount = float(amount)
            except ValueError:
                return False
        return isinstance(amount, (int, float)) and amount >= 0

    @staticmethod
    def validate_isbn(isbn: Any) -> bool:
        if not isinstance(isbn, str):
            return False
        isbn = isbn.replace('-', '').replace(' ', '')
        return bool(re.match(r'^(97(8|9))?\d{9}(\d|X)$', isbn))

    @staticmethod
    def validate_library_code(code: Any) -> bool:
        if not isinstance(code, str):
            return False
        return bool(re.match(r'^LIB-[A-Z0-9]{6}$', code))

    @staticmethod
    def validate_membership_id(member_id: Any) -> bool:
        if not isinstance(member_id, str):
            return False
        return bool(re.match(r'^MEM-\d{6}$', member_id))

    @staticmethod
    def validate_name(name: Any) -> bool:
        if not isinstance(name, str):
            return False
        return bool(re.match(r'^[A-Za-z\s-]{2,}$', name))
    
    @staticmethod
    def hash_password(password: str) -> str:
        return generate_password_hash(password)
    
    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        return check_password_hash(hashed_password, password)

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
    def validate_phone(phone: Any) -> bool:
        if not isinstance(phone, str):
            return False
        return bool(re.match(r'^\+?[1-9]\d{9,14}$', phone))

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
    def validate_image(image: Any) -> bool:
        if not isinstance(image, str):
            return False
        return bool(re.match(r'^data:image\/[a-z]+;base64,', image))
    
    @staticmethod
    def validate_image_extension(image: Any) -> bool:
        if not isinstance(image, str):
            return False
        return image.split('/')[-1] in ['jpg', 'jpeg', 'png']
    
    @staticmethod
    def validate_boolean(value: Any) -> bool:
        if isinstance(value, str):
            return value.lower() in ('true', 'false', '1', '0')
        return isinstance(value, bool)
