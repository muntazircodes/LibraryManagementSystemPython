from app.models.book_model import Book, Copies, Borrowing, Reserve
from app.models.user_model import User
from app.utils.db import db


class BookRepository:

    @staticmethod
    def add_new_book(book_name, book_image, author, publisher, book_genre, edition, 
                     isbn, price, lib_id, book_stock, volume=None):
        try:
            with db.session.begin():
                if BookRepository.get_book_by_isbn(isbn):
                    raise ValueError("Book with this ISBN already exists")

                new_book = Book(
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
                    Copies(book_id=new_book.book_id, loc_id=1) 
                    for _ in range(book_stock)
                ]
                db.session.add_all(copies)
                db.session.commit()
                return new_book
        except Exception as e:
            db.session.rollback()
            raise e


    @staticmethod
    def update_book(book_id, **kwargs):
        try:
            with db.session.begin():
                book = Book.query.get_or_404(book_id)
                
                allowed_fields = [
                    'book_name', 'book_image', 'author', 'publisher', 
                    'book_genre', 'edition', 'isbn', 'price', 'lib_id', 
                    'book_stock', 'volume'
                ]
                
                if 'isbn' in kwargs:
                    existing_book = BookRepository.get_book_by_isbn(kwargs['isbn'])
                    if existing_book and existing_book.book_id != book_id:
                        raise ValueError("Book with this ISBN already exists")
                
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
    def delete_book(book_id):
        try:
            with db.session.begin():
                book = Book.query.get_or_404(book_id)
                Copies.query.filter_by(book_id=book_id).delete()
                db.session.delete(book)
                db.session.commit()
                return {"message": f"Book and all its copies deleted"}
        except Exception as e:
            db.session.rollback()
            raise e


    @staticmethod 
    def get_all_books():
        return Book.query.all()


    @staticmethod
    def get_book_by_id(book_id):
        return Book.query.get_or_404(book_id) 


    @staticmethod
    def get_book_by_name(book_name):
        return Book.query.filter(Book.book_name.ilike(f"%{book_name}%")).all()


    @staticmethod 
    def get_book_by_isbn(isbn):
        return Book.query.filter_by(isbn=isbn).first()


    @staticmethod
    def get_book_by_author(author):
        return Book.query.filter(Book.author.ilike(f"%{author}%")).all()


    @staticmethod
    def get_book_by_publisher(publisher):
        return Book.query.filter(Book.publisher.ilike(f"%{publisher}%")).all()


    @staticmethod
    def get_book_by_edition(edition):
        return Book.query.filter_by(edition=edition).all()


    @staticmethod
    def get_book_by_genre(genre):
        return Book.query.filter(Book.book_genre.ilike(f"%{genre}%")).all()


class CopiesRepository:

    @staticmethod
    def add_copies(book_id, quantity, loc_id=1, condition="Excellent", status="Available"):
        try:
            with db.session.begin():
                book = Book.query.get(book_id)
                if not book:
                    raise ValueError("Book not found")
                        
                copies = [
                    Copies(
                        book_id=book.book_id,
                        loc_id=loc_id,
                        copy_condition=condition,
                        copy_status=status,
                        copy_available="Yes"
                    ) for _ in range(quantity)
                ]
                        
                db.session.add_all(copies)
                book.book_stock += quantity
                book.available_stock += quantity
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
                        
                book.available_stock = max(0, book.available_stock - 1)
                        
                db.session.commit()
                return {"message": f"Copy deleted, updated quantity for {book.book_name}: {book.book_stock}"}
        except Exception as e:
            db.session.rollback()
            raise e


    @staticmethod
    def update_copy(copy_id, **kwargs):
        try:
            with db.session.begin():
                copy = Copies.query.get_or_404(copy_id)
                allowed_fields = ['loc_id', 'copy_condition', 'copy_status', 'copy_available']
                        
                for key, value in kwargs.items():
                    if key in allowed_fields:
                        setattr(copy, key, value)
                        
                db.session.commit()
                return copy
        except Exception as e:
            db.session.rollback()
            raise e


    @staticmethod
    def update_all_copies(book_id, **kwargs):
        try:
             with db.session.begin():
                copies = Copies.query.filter_by(book_id=book_id).all()
                allowed_fields = ['loc_id', 'copy_condition', 'copy_status', 'copy_available']
                        
                for copy in copies:
                    for key, value in kwargs.items():
                        if key in allowed_fields:
                            setattr(copy, key, value)
                        
                db.session.commit()
                return copies
        except Exception as e:
            db.session.rollback()
            raise e


    @staticmethod
    def get_all_copies():
        return Copies.query.all()


    @staticmethod
    def get_copies_by_book_id(book_id):
        return Copies.query.filter_by(book_id=book_id).all()


    @staticmethod
    def get_copies_by_book_name(book_name):
        return Copies.query.join(Book, Copies.book_id == Book.book_id)\
            .filter(Book.book_name.ilike(f"%{book_name}%")).all()


class BorrowRepository:

    @staticmethod
    def add_new_borrowing(user_id, copy_id, borrow_date):
        try:
            with db.session.begin():
                copy = Copies.query.get(copy_id)
                if not copy or copy.copy_available != "Yes":
                    raise ValueError("Copy not available for borrowing")

                new_borrowing = Borrowing(
                    user_id=user_id, 
                    copy_id=copy_id, 
                    borrow_date=borrow_date
                )
                db.session.add(new_borrowing)
                
                copy.copy_available = "No"
                copy.copy_status = "Borrowed"

                book = Book.query.get(copy.book_id)
                book.available_stock = max(0, book.available_stock - 1)
                
                db.session.commit()
                return new_borrowing
        except Exception as e:
            db.session.rollback()
            raise e


    @staticmethod
    def delete_borrowing(borrow_id, user_id):
        try:
            with db.session.begin():
                borrowing = Borrowing.query.get(borrow_id)
                if not borrowing:
                    raise ValueError("Borrowing not found")

                if borrowing.user_id != user_id:
                    raise ValueError("User did not borrow this book")

                copy = Copies.query.get(borrowing.copy_id)
                copy.copy_available = "Yes"
                copy.copy_status = "Available"
                
                book = Book.query.get(copy.book_id)
                book.available_stock += 1

                db.session.delete(borrowing)
                db.session.commit()

            return {"message": "Borrowing deleted"}
        except Exception as e:
            db.session.rollback()
            raise e


    @staticmethod
    def get_all_borrowings():
        return Borrowing.query.all()


    @staticmethod
    def get_borrowing_by_id(borrow_id):
        return Borrowing.query.get_or_404(borrow_id)


    @staticmethod
    def get_borrowings_by_user_id(user_id):
        return Borrowing.query.filter_by(user_id=user_id).all()


    @staticmethod
    def get_borrowings_by_copy_id(copy_id):
        return Borrowing.query.filter_by(copy_id=copy_id).all()


    @staticmethod
    def get_borrowings_by_return_date(return_date):
        return Borrowing.query.filter_by(return_date=return_date).all()


    @staticmethod
    def get_borrowings_by_user_name(user_name):
        return Borrowing.query.join(User, Borrowing.user_id == User.user_id)\
            .filter(User.user_name == user_name).all()


class ReserveRepository:

    @staticmethod
    def add_new_reservation(user_id, copy_id):
        try:
            with db.session.begin():
                # Check if copy exists
                copy = Copies.query.get(copy_id)
                if not copy:
                    raise ValueError("Copy not found")

                # Check if user has already reserved this copy
                existing_reservation = Reserve.query.filter_by(
                    user_id=user_id, 
                    copy_id=copy_id,
                    is_expired=False
                ).first()
                
                if existing_reservation:
                    raise ValueError("User already has an active reservation for this copy")

                new_reservation = Reserve(
                    user_id=user_id,
                    copy_id=copy_id,
                    is_expired=False
                )
                db.session.add(new_reservation)
                db.session.commit()
                return new_reservation
        except Exception as e:
            db.session.rollback()
            raise e


    @staticmethod
    def update_reservation(reserve_id, **kwargs):
        try:
            with db.session.begin():
                reservation = Reserve.query.get_or_404(reserve_id)
                
                # Only update allowed fields
                allowed_fields = ['receiving_time', 'is_expired']
                for field, value in kwargs.items():
                    if field in allowed_fields:
                        setattr(reservation, field, value)

                db.session.commit()
                return reservation
        except Exception as e:
            db.session.rollback()
            raise e


    @staticmethod
    def delete_reservation(reserve_id):
        try:
            with db.session.begin():
                reservation = Reserve.query.get_or_404(reserve_id)
                db.session.delete(reservation)
                db.session.commit()
            return {"message": "Reservation deleted"}
        except Exception as e:
            db.session.rollback()
            raise e


    @staticmethod
    def get_all_reservations():
        return Reserve.query.all()


    @staticmethod
    def get_reservation_by_id(reserve_id):
        return Reserve.query.get_or_404(reserve_id)


    @staticmethod
    def get_reservations_by_user_id(user_id):
        return Reserve.query.filter_by(user_id=user_id).all()


    @staticmethod
    def get_reservations_by_copy_id(copy_id):
        return Reserve.query.filter_by(copy_id=copy_id).all()
