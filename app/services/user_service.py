from datetime import datetime
from app.utils.responses import Responses
from app.utils.validators import Validators
from app.repositories.user_repository import UserRepository
from app.repositories.book_repository import BookRepository, CopiesRepository, BorrowRepository


class UserService:

    @staticmethod
    def register_user(user_data):
        try:
            if not Validators.validate_email(user_data.get('user_email')):
                return Responses.validation_error({"email": "Invalid email format"})
            
            if not Validators.validate_name(user_data.get('user_name')):
                return Responses.validation_error({"name": "Invalid user name"})
            
            existing_user = UserRepository.get_user_by_email(user_data.get('user_email'))
            if existing_user:
                return Responses.conflict("User with this email already exists")
            
            UserRepository.add_user(
                user_name=user_data.get('user_name'),
                user_email=user_data.get('user_email'),
                user_password=user_data.get('user_password')
            )
            return Responses.created("User")
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
    def get_my_profile(user_id):
        user = UserRepository.get_user_by_id(user_id)
        if not user:
            return Responses.not_found("User")
        return Responses.success("User details retrieved", user)
    

    @staticmethod
    def check_my_borrowings(user_id):
        borrowings = UserRepository.get_user_borrowings(user_id)
        return Responses.success("Borrowings retrieved", borrowings)
