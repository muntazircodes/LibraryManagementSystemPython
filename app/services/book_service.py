from app.utils.responses import Responses
from app.utils.validators import Validators

from app.repositories.book_repository import BookRepository, BorrowRepository, ReserveRepository, CopiesRepository
from app.repositories.user_repository import UserRepository

from datetime import datetime, timedelta


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

            new_book = BookRepository.add_book(
                book_title=book_data.get('book_title'),
                book_author=book_data.get('book_author'),
                book_publisher=book_data.get('book_publisher'),
                book_stock=book_data.get('book_stock'),
                book_price=book_data.get('book_price'),
                book_category=book_data.get('book_category')
            )
            serialized_book = Validators.serialize_model(new_book)
            return Responses.created("Book", serialized_book)
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

            updated_book = BookRepository.update_book(
                book_id=book_id,
                book_title=book_data.get('book_title'),
                book_author=book_data.get('book_author'),
                book_publisher=book_data.get('book_publisher'),
                book_stock=book_data.get('book_stock'),
                book_price=book_data.get('book_price'),
                book_category=book_data.get('book_category')
            )
            serialized_book = Validators.serialize_model(updated_book)
            return Responses.success("Book updated successfully", serialized_book)
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
    def search_for_books(book_title):
        try:
            books = BookRepository.get_books_by_title(book_title)
            if not books:
                return Responses.not_found("Books")
            serialized_books = [Validators.serialize_model(book) for book in books]
            return Responses.success("Books retrieved", serialized_books)
        except Exception as e:
            return Responses.server_error()

    @staticmethod
    def search_for_books_stock(book_title):
        try:
            books = BookRepository.get_books_by_title(book_title)
            if not books:
                return Responses.not_found("Books")
            serialized_books = [Validators.serialize_model(book) for book in books]
            return Responses.success("Books retrieved", serialized_books)
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
            serialized_copies = [Validators.serialize_model(copy) for copy in available_copies]
            return Responses.success("Available copies", serialized_copies)
        except Exception as e:
            return Responses.server_error()

    @staticmethod
    def add_copies(book_id, copies_data):
        try:
            book = BookRepository.get_book_by_id(book_id)
            if not book:
                return Responses.not_found("Book")

            if not Validators.validate_number(copies_data.get('copies')):
                return Responses.validation_error({"copies": "Invalid copies number"})

            new_copies = CopiesRepository.add_copies(
                book_id=book_id,
                copies=copies_data.get('copies')
            )
            serialized_copies = Validators.serialize_model(new_copies)
            return Responses.success("Copies added successfully", serialized_copies)
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
            if len(existing_borrowings) >= user.allowed_books:
                return Responses.bad_request("User has reached maximum book borrowing limit")

            copies = CopiesRepository.get_copies_by_book_id(book_id)
            available_copy = next((copy for copy in copies if copy.copy_available == "Yes"), None)
            if not available_copy:
                return Responses.bad_request("No available copies found")

            new_borrowing = BorrowRepository.add_new_borrowing(
                user_id=user_id,
                copy_id=available_copy.copy_id,
                borrow_date=datetime.now()
            )
            serialized_borrowing = Validators.serialize_model(new_borrowing)
            return Responses.success("Book borrowed successfully", serialized_borrowing)
        except Exception as e:
            return Responses.server_error()

    @staticmethod
    def return_book(user_id, book_id):
        try:
            user = UserRepository.get_user_by_id(user_id)
            if not user:
                return Responses.not_found("User")

            book = BookRepository.get_book_by_id(book_id)
            if not book:
                return Responses.not_found("Book")

            borrowings = BorrowRepository.get_borrowings_by_user_id(user_id)
            borrowing = next((borrowing for borrowing in borrowings if borrowing.copy.book_id == book_id), None)
            if not borrowing:
                return Responses.not_found("Borrowing")

            BorrowRepository.delete_borrowing(borrowing.borrow_id)
            return Responses.success("Book returned successfully")
        except Exception as e:
            return Responses.server_error()

    @staticmethod
    def reserve_a_book(user_id, book_id):
        try:
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

            user_fines = UserRepository.get_user_fines(user_id)
            if user_fines and user_fines > 0:
                return Responses.bad_request("User has outstanding fines")

            reservation_expiry = datetime.now() + timedelta(hours=3)
            new_reservation = ReserveRepository.add_new_reservation(user_id, book_id, datetime.now(), reservation_expiry)
            serialized_reservation = Validators.serialize_model(new_reservation)
            return Responses.success("Book reserved successfully", serialized_reservation)
        except Exception as e:
            return Responses.server_error()
