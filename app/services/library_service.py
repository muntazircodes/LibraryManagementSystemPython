from app.utils.responses import Responses
from app.repositories.book_repository import BookRepository, CopiesRepository

class LibraryService:
    def __init__(self, book_repository: BookRepository, copy_repository: CopiesRepository):
        self.book_repository = book_repository
        self.copy_repository = copy_repository

    def get_all_books(self):
        books = self.book_repository.get_all()
        return Responses.success("Books", books)

    def get_book_by_id(self, book_id):
        book = self.book_repository.get_by_id(book_id)
        if not book:
            return Responses.not_found("Book")
        return Responses.success("Book", book)

    def get_all_copies(self):
        copies = self.copy_repository.get_all()
        return Responses.success("Copies", copies)

    def get_copy_by_id(self, copy_id):
        copy = self.copy_repository.get_by_id(copy_id)
        if not copy:
            return Responses.not_found("Copy")
        return Responses.success("Copy", copy)
