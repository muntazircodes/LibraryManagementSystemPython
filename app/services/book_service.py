from app.utils.responses import Responses
from app.utils.validators import Validators
from app.repositories.book_repository import BookRepository, BorrowRepository, ReserveRepository, CopiesRepository
from app.repositories.user_repository import UserRepository
from datetime import datetime, timedelta


class BookService:

    def handle_repository_action(action, *args, **kwargs):         
        try:             
            result = action(*args, **kwargs)             
            if not result:                 
                return None
                
            return (                 
                Validators.serialize_model(result)                 
                if not isinstance(result, list)                 
                else [Validators.serialize_model(item) for item in result]             
            )
            
        except Exception as e:             
            return Responses.server_error()


    @staticmethod
    def add_book(book_data):
        try:
            allowed_fields = [
                'book_title', 'book_author', 'book_publisher',
                'book_stock', 'book_price', 'book_category'
            ]
            new_book_data = {field: book_data.get(field) for field in allowed_fields}
            return BookService.handle_repository_action(BookRepository.add_new_book, **new_book_data)
        except Exception:
            return Responses.server_error()


    @staticmethod
    def update_book(book_id, book_data):
        try:
            allowed_fields = [
                'book_title', 'book_author', 'book_publisher',
                'book_stock', 'book_price', 'book_category'
            ]
            book = BookRepository.get_book_by_id(book_id)
            if not book:
                return Responses.not_found("Book")

            update_data = {field: book_data.get(field) for field in allowed_fields}
            return BookService.handle_repository_action(BookRepository.update_book, book_id, **update_data)
        except Exception:
            return Responses.server_error()


    @staticmethod
    def delete_book(book_id):
        return BookService.handle_repository_action(BookRepository.delete_book, book_id)


    @staticmethod
    def search_for_books(book_title):
        return BookService.handle_repository_action(BookRepository.get_book_by_name, book_title)


    @staticmethod
    def search_for_books_stock(book_title):
        return BookService.handle_repository_action(BookRepository.get_book_by_name, book_title)


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
        except Exception:
            return Responses.server_error()


    @staticmethod
    def add_copies(book_id, copies_data):
        try:
            book = BookRepository.get_book_by_id(book_id)
            if not book:
                return Responses.not_found("Book")
            return BookService.handle_repository_action(CopiesRepository.add_copies, book_id, copies_data.get('copies'))
        except Exception:
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

            return BookService.handle_repository_action(BorrowRepository.add_new_borrowing, user_id, available_copy.copy_id, datetime.now())
        except Exception:
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

            return BookService.handle_repository_action(BorrowRepository.delete_borrowing, borrowing.borrow_id)
        except Exception:
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
            return BookService.handle_repository_action(
                ReserveRepository.add_new_reservation,
                user_id,
                book_id,
                datetime.now(),
                reservation_expiry
            )
        except Exception:
            return Responses.server_error()
