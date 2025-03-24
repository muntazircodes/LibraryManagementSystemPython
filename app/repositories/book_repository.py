from app.middleware.db import db
from app.models import Books, Copies


class BookRepository:

    @staticmethod
    def addNewBook(book_name, book_image, author, publisher, book_genre, edition, 
                     isbn, price, lib_id, book_stock, volume=None):
        try:
            with db.session.begin():
                if BookRepository.get_book_by_isbn(isbn):
                    raise ValueError("Books with this ISBN already exists")

                new_book = Books(
                    book_name=book_name,
                    book_image=book_image,
                    author=author,
                    publisher=publisher,
                    book_genre=book_genre,
                    edition=edition,
                    isbn=isbn,
                    price=price,
                    lib_id=lib_id,
                    book_stock=book_stock,
                    available_stock=book_stock,
                    volume=volume
                )
                db.session.add(new_book)
                db.session.flush()

                copies = [
                    Copies(book_id=new_book.book_id, rack_id=1) 
                    for _ in range(book_stock)
                ]
                db.session.add_all(copies)
                db.session.commit()
                return new_book
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod 
    def getAllBooks():
        return Books.query.all()

    @staticmethod
    def getBookById(book_id):
        return Books.query.get_or_404(book_id) 

    @staticmethod
    def getBookByFilter(**kwargs):
        allowed_fields = ['book_name', 'isbn', 'author', 'publisher', 'edition', 'book_genre']

        query = Books.query

        for field in allowed_fields:
            if field in kwargs:
                value = kwargs[field]
                if field in allowed_fields:
                    query = query.filter(getattr(Books, field).ilike(f"%{value}%"))
                else:  # For exact match
                    query = query.filter_by(**{field: value})

        return query.all() if kwargs else []
    


    @staticmethod
    def updateBook(book_id, **kwargs):
        try:
            with db.session.begin():
                book = Books.query.get_or_404(book_id)
                
                allowed_fields = [
                    'book_name', 'book_image', 'author', 'publisher', 
                    'book_genre', 'edition', 'isbn', 'price', 'lib_id', 
                    'book_stock', 'volume'
                ]
                
                if 'isbn' in kwargs:
                    existing_book = BookRepository.getBookByFilter(kwargs['isbn'])
                    if existing_book and existing_book.book_id != book_id:
                        raise ValueError("Books with this ISBN already exists")
                
                if 'book_stock' in kwargs:
                    new_stock = kwargs['book_stock']
                    stock_difference = new_stock - book.book_stock
                    book.available_stock = max(0, book.available_stock + stock_difference)
                
                for key, value in kwargs.items():
                    if key in allowed_fields and hasattr(book, key):
                        setattr(book, key, value)
                
                db.session.commit()
                return book
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def deleteBook(book_id):
        try:
            with db.session.begin():
                book = Books.query.get_or_404(book_id)
                Copies.query.filter_by(book_id=book_id).delete()
                db.session.delete(book)
                db.session.commit()
                return {"message": f"Books and all its copies deleted"}
        except Exception as e:
            db.session.rollback()
            raise e

