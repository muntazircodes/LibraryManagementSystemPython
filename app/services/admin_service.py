from app.utils.responses import Responses
from app.utils.validators import Validators
from app.utils.db import db
from app.repositories.user_repository import UserRepository
from app.repositories.book_repository import BookRepository, CopiesRepository, BorrowRepository


from app.repositories.library_repository import LibraryRepository, LocationRepository
from datetime import datetime

class AdminService:
    @staticmethod
    def verify_library(lib_id):
        try:
            library = LibraryRepository.get_library_by_id(lib_id)
            if not library:
                return Responses.not_found("Library")
            
            library.library_verified = True
            db.session.commit()
            return Responses.success("Library verified successfully")
        except Exception as e:
            return Responses.server_error()

    @staticmethod
    def create_library(lib_data):
        try:
            if not Validators.validate_email(lib_data.get('lib_email')):
                return Responses.validation_error({"email": "Invalid email format"})
            
            if not Validators.validate_name(lib_data.get('lib_name')):
                return Responses.validation_error({"name": "Invalid library name"})
            
            existing_library = LibraryRepository.get_library_by_email(lib_data.get('lib_email'))
            if existing_library:
                return Responses.conflict("Library with this email already exists")
            
            LibraryRepository.add_library(
                lib_name=lib_data.get('lib_name'),
                lib_location=lib_data.get('lib_location'),
                lib_admin=lib_data.get('lib_admin'),
                lib_licence=lib_data.get('lib_licence'),
                lib_docs=lib_data.get('lib_docs'),
                lib_email=lib_data.get('lib_email')
            )
            return Responses.created("Library")
        except Exception as e:
            return Responses.server_error()

    @staticmethod
    def get_library_locations(lib_id):
        try:
            library = LibraryRepository.get_library_by_id(lib_id)
            if not library:
                return Responses.not_found("Library")
            
            locations = LocationRepository.get_locations_by_library(lib_id)
            return Responses.success("Locations retrieved successfully", locations)
        except Exception as e:
            return Responses.server_error()
        
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
                
                # Check if user has reached borrowing limit
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