from app.utils.responses import Responses
from app.utils.validators import Validators

from app.repositories.book_repository import BookRepository, BorrowRepository , ReserveRepository
from app.repositories.user_repository import UserRepository

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
    def check_avalible_copies(book_id):
        try:
            book = BookRepository.get_book_by_id(book_id)
            if not book:
                return Responses.not_found("Book")
            
            copies = BookRepository.get_copies_by_book_id(book_id)
            available_copies = [copy for copy in copies if copy.copy_available == "Yes"]
            return Responses.success("Available copies", available_copies)
        except Exception as e:
            return Responses.server_error()