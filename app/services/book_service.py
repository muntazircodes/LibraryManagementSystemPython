from app.utils.responses import Responses
from app.utils.validators import Thevalidators

from app.repositories.book_repository import BookRepository, CopiesRepository, BorrowRepositoy , ReserveRepository
from app.repositories.user_repository import UserRepository


class BookService:

    def __init__(self, book_repository: BookRepository, copy_repository: CopiesRepository, borrow_repository: BorrowRepositoy, reserve_repository: ReserveRepository, user_repository: UserRepository):
        self.book_repository = book_repository
        self.copy_repository = copy_repository
        self.borrow_repository = borrow_repository
        self.reserve_repository = reserve_repository
        self.user_repository = user_repository

    def create_book(self, book_data):
        if not Thevalidators.validate_isbn(book_data.get('isbn')):
            return Responses.validation_error({"isbn": "Invalid ISBN format"})
        if not Thevalidators.validate_name(book_data.get('title')):
            return Responses.validation_error({"title": "Title must be at least 3 characters"})
        if not Thevalidators.validate_price(book_data.get('price')):
            return Responses.validation_error({"price": "Price must be a positive number"})
        
        book = self.book_repository.create(book_data)
        return Responses.created("Book", book)

    def create_copy(self, copy_data):
        if not Thevalidators.validate_stock(copy_data.get('stock')):
            return Responses.validation_error({"stock": "Stock must be a positive number"})
        
        copy = self.copy_repository.create(copy_data)
        return Responses.created("Copy", copy)

    def delete_book(self, book_id):
        book = self.book_repository.get_by_id(book_id)

        if not book:
            return Responses.not_found("Book")
        
        self.book_repository.delete(book_id)
        return Responses.deleted("Book")

    def borrow_book(self, borrow_data):
        user = self.user_repository.get_by_id(borrow_data.get('user_id'))
        if not user:
            return Responses.not_found("User")
        
        copy = self.copy_repository.get_by_id(borrow_data.get('copy_id'))
        if not copy:
            return Responses.not_found("Copy")
        
        if not self.copy_repository.is_available(copy.id):
            return Responses.unavailable("Copy")
        
        borrow = self.borrow_repository.create(borrow_data)
        return Responses.created("Borrow", borrow)

    def return_book(self, return_data):
        borrow = self.borrow_repository.get_by_id(return_data.get('borrow_id'))
        if not borrow:
            return Responses.not_found("Borrow")
        
        self.borrow_repository.return_book(return_data.get('borrow_id'))
        return Responses.success("Return", "Book returned successfully")

    def reserve_book(self, reserve_data):
        user = self.user_repository.get_by_id(reserve_data.get('user_id'))
        if not user:
            return Responses.not_found("User")
        
        book = self.book_repository.get_by_id(reserve_data.get('book_id'))
        if not book:
            return Responses.not_found("Book")
        
        reserve = self.reserve_repository.create(reserve_data)
        return Responses.created("Reserve", reserve)

