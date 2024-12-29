from app.utils.responses import Responses
from app.utils.validators import Validators

from app.repositories.book_repository import BookRepository, BorrowRepository, ReserveRepository, CopiesRepository
from app.repositories.user_repository import UserRepository

from datetime import datetime


class BookService:

    @staticmethod
    def add_book(book_data):
        try:
            if not Validators.validate_name(book_data.get('book_title')):
                return Responses.validation_error({"title": "Invalid book title"})

            if not Validators.validate_name(book_data.get('book_author')):
                return Responses.validation_error({"author": "Invalid author name"})

            if not Validators.validate_name(book_data.get('book_publisher')):
                return Responses.validation_error({"publisher": "Invalid publisher name"})

            if not Validators.validate_number(book_data.get('book_stock')):
                return Responses.validation_error({"stock": "Invalid stock number"})

            if not Validators.validate_number(book_data.get('book_price')):
                return Responses.validation_error({"price": "Invalid price"})

            if not Validators.validate_number(book_data.get('book_category')):
                return Responses.validation_error({"category": "Invalid category"})

            BookRepository.add_book(
                book_title=book_data.get('book_title'),
                book_author=book_data.get('book_author'),
                book_publisher=book_data.get('book_publisher'),
                book_stock=book_data.get('book_stock'),
                book_price=book_data.get('book_price'),
                book_category=book_data.get('book_category')
            )
            return Responses.created("Book")
        except Exception as e:
            return Responses.server_error()

    @staticmethod
    def update_book(book_id, book_data):
        try:
            book = BookRepository.get_book_by_id(book_id)
            if not book:
                return Responses.not_found("Book")

            if not Validators.validate_name(book_data.get('book_title')):
                return Responses.validation_error({"title": "Invalid book title"})

            if not Validators.validate_name(book_data.get('book_author')):
                return Responses.validation_error({"author": "Invalid author name"})

            if not Validators.validate_name(book_data.get('book_publisher')):
                return Responses.validation_error({"publisher": "Invalid publisher name"})

            if not Validators.validate_number(book_data.get('book_stock')):
                return Responses.validation_error({"stock": "Invalid stock number"})

            if not Validators.validate_number(book_data.get('book_price')):
                return Responses.validation_error({"price": "Invalid price"})

            if not Validators.validate_number(book_data.get('book_category')):
                return Responses.validation_error({"category": "Invalid category"})

            BookRepository.update_book(
                book_id=book_id,
                book_title=book_data.get('book_title'),
                book_author=book_data.get('book_author'),
                book_publisher=book_data.get('book_publisher'),
                book_stock=book_data.get('book_stock'),
                book_price=book_data.get('book_price'),
                book_category=book_data.get('book_category')
            )
            return Responses.success("Book updated successfully")
        except Exception as e:
            return Responses.server_error()

    @staticmethod
    def delete_book(book_id):
        try:
            book = BookRepository.get_book_by_id(book_id)
            if not book:
                return Responses.not_found("Book")

            BookRepository.delete_book(book_id)
            return Responses.success("Book deleted successfully")
        except Exception as e:
            return Responses.server_error()

    @staticmethod
    def borrow_book(user_id, book_id):
        try:
            user = UserRepository.get_user_by_id(user_id)
            if not user:
                return Responses.not_found("User")

            book = BookRepository.get_book_by_id(book_id)
            if not book:
                return Responses.not_found("Book")

            if book.available_stock <= 0:
                return Responses.bad_request("No copies available for borrowing")

            existing_borrowings = BorrowRepository.get_borrowings_by_user_id(user_id)
            if len(existing_borrowings) >= 3:
                return Responses.bad_request("User has reached maximum book borrowing limit")

            copies = CopiesRepository.get_copies_by_book_id(book_id)
            available_copy = next((copy for copy in copies if copy.copy_available == "Yes"), None)
            if not available_copy:
                return Responses.bad_request("No available copies found")

            if any(b.copy_id == available_copy.copy_id for b in existing_borrowings):
                return Responses.conflict("User already has borrowed this book")

            BorrowRepository.add_new_borrowing(
                user_id=user_id,
                copy_id=available_copy.copy_id,
                borrow_date=datetime.now()
            )
            return Responses.success("Book borrowed successfully")
        except Exception as e:
            return Responses.server_error()

    @staticmethod
    def reserve_book(user_id, book_id):
        try:
            user = UserRepository.get_user_by_id(user_id)
            if not user:
                return Responses.not_found("User")

            book = BookRepository.get_book_by_id(book_id)
            if not book:
                return Responses.not_found("Book")

            if book.available_stock <= 0:
                return Responses.bad_request("No copies available for borrowing")

            existing_borrowings = BorrowRepository.get_borrowings_by_user_id(user_id)
            if any(b.book_id == book_id for b in existing_borrowings):
                return Responses.conflict("User already has borrowed this book")

            BorrowRepository.add_new_borrowing(
                user_id=user_id,
                book_id=book_id,
                borrow_date=datetime.now()
            )
            return Responses.success("Book reserved successfully")
        except Exception as e:
            return Responses.server_error()

    @staticmethod
    def search_for_books(book_title):
        try:
            books = BookRepository.get_books_by_title(book_title)
            if not books:
                return Responses.not_found("Books")
            return Responses.success("Books retrieved", books)
        except Exception as e:
            return Responses.server_error()

    @staticmethod
    def search_for_books_stock(book_title):
        try:
            books = BookRepository.get_books_by_title(book_title)
            if not books:
                return Responses.not_found("Books")
            return Responses.success("Books retrieved", books)
        except Exception as e:
            return Responses.server_error()

    @staticmethod
    def check_available_copies(book_id):
        try:
            book = BookRepository.get_book_by_id(book_id)
            if not book:
                return Responses.not_found("Book")

            copies = BookRepository.get_copies_by_book_id(book_id)
            available_copies = [copy for copy in copies if copy.copy_available == "Yes"]
            return Responses.success("Available copies", available_copies)
        except Exception as e:
            return Responses.server_error()
    @staticmethod
    def reserve_a_book(user_id, book_id):
        if not BookRepository.get_book_by_id(book_id):
            return Responses.not_found("Book")
        
        if not UserRepository.get_user_by_id(user_id):
            return Responses.not_found("User")
        
        if not BookRepository.get_copies_by_book_id(book_id):
            return Responses.bad_request("No copies available for borrowing")
        
        if BorrowRepository.get_borrowings_by_user_id(user_id):
            return Responses.bad_request("User has reached maximum book borrowing limit")
        
        if ReserveRepository.get_reservations_by_user_id(user_id):
            return Responses.bad_request("User has already reserved a book")
        
        ReserveRepository.add_new_reservation(user_id, book_id, datetime.now())
        return Responses.success("Book reserved successfully")