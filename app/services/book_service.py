from utils.responses import Responses
from utils.validators import Thevalidators

from repositories.book_repository import BookRepository, CopiesRepository, BorrowRepositoy , ReserveRepository
from repositories.user_repository import UserRepository


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

