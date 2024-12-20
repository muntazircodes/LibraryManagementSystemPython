from models.book_model import Book, Copies, Borrowing, Reserve
from utils.db import db


class BookRepository:
    @staticmethod
    def get_all_books():
        return Book.query.all()

    @staticmethod
    def get_book_by_id(book_id):
        return Book.query.get(book_id)

    @staticmethod
    def get_book_by_name(book_name):
        return Book.query.filter_by(book_name=book_name).all()

    @staticmethod
    def get_book_by_isbn(isbn):
        return Book.query.filter_by(isbn=isbn).first()

    @staticmethod
    def get_book_by_author(author):
        return Book.query.filter_by(author=author).all()

    @staticmethod
    def get_book_by_publisher(publisher):
        return Book.query.filter_by(publisher=publisher).all()

    @staticmethod
    def get_book_by_edition(edition):
        return Book.query.filter_by(edition=edition).all()

    @staticmethod
    def get_book_by_genre(genre):
        return Book.query.filter_by(book_genre=genre).all()
    @staticmethod
    def add_new_book(book_name, book_image, author, publisher, book_genre, edition, isbn, price,lib_id, book_stock):
        new_book = Book(book_name=book_name, book_image=book_image, author=author, publisher=publisher, 
        book_genre=book_genre, edition=edition, isbn=isbn, price=price,lib_id=lib_id, book_stock=book_stock, available_stock=book_stock)
        for _ in range(book_stock):
            pass
        db.session.add(new_book)
        db.session.commit()
        return new_book


class CopiesRepository:
    @staticmethod
    def get_all_copies():
        return Copies.query.all()

    @staticmethod
    def get_copies_by_book_id(book_id):
        return Copies.query.filter_by(book_id=book_id).all()


    @staticmethod
    def add_copies(book_name, quantity):
        try:

            with db.session.begin():

                book = Book.query.get(book_name)
                if not book:
                    raise ValueError("Book not found")
                
                copies = [Copies(book_name=book.book_name) for _ in range(quantity)]
                db.session.add_all(copies)
                
        
                book.book_stock += quantity 
                db.session.commit() 

            return {"message": f"{quantity} copies added to {book.book_name}"}

        except Exception as e:
            db.session.rollback() 
            raise e  
        
    @staticmethod
    def delete_copy(copy_id):
        try:
            with db.session.begin():
                copy = Copies.query.get(copy_id)
                if not copy:
                    raise ValueError("Copy not found")

                book = Book.query.get(copy.book_id)

                db.session.delete(copy)

            
                book.book_stock -= 1
                if book.book_stock < 0:
                    book.book_stock = 0

                db.session.commit() 

            return {"message": f"Copy deleted, updated quantity for {book.book_name}: {book.book_stock}"}

        except Exception as e:
            db.session.rollback()
            raise e