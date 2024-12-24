from app.models.book_model import Book, Copies, Borrowing, Reserve
from app.models.user_model import User
from app.utils.db import db


class BookRepository:

    @staticmethod
    def get_all_books():
        return Book.query.all()

    @staticmethod
    def get_book_by_id(book_id):
        return Book.query.get(book_id)

    @staticmethod
    def get_book_by_name(book_name):
        return Book.query.filter(Book.book_name.ilike(f"%{book_name}%")).all()

    @staticmethod
    def get_book_by_isbn(isbn):
        return Book.query.filter_by(isbn=isbn).first()

    @staticmethod
    def get_book_by_author(author):
        return Book.query.filter_by(Book.author.ilike(f"%{author}%")).all()
                                    

    @staticmethod
    def get_book_by_publisher(publisher):
        return Book.query.filter_by(Book.publisher.ilike(f"%{publisher}%")).all()

    @staticmethod
    def get_book_by_edition(edition):
        return Book.query.filter_by(edition=edition).all()

    @staticmethod
    def get_book_by_genre(genre):
        return Book.query.filter_by(Book.book_genre.ilike(f"%{genre}%")).all()
    
    @staticmethod
    def add_new_book(book_name, book_image, author, publisher, book_genre, edition, isbn, price, lib_id, book_stock):
        new_book = Book(book_name=book_name, book_image=book_image, author=author, publisher=publisher, 
                        book_genre=book_genre, edition=edition, isbn=isbn, price=price, lib_id=lib_id, 
                        book_stock=book_stock, available_stock=book_stock)
        db.session.add(new_book)
        db.session.flush()

        copies = [Copies(book_id=new_book.book_id) for _ in range(book_stock)]
        db.session.add_all(copies)
        
        db.session.commit()
        return new_book
    
    
    @staticmethod
    def delete_book(book_id):
        try:
            with db.session.begin():
                book = Book.query.get(book_id)
                if not book:
                    raise ValueError("Book not found")

                # Delete all copies of the book
                Copies.query.filter_by(book_id=book_id).delete()

                db.session.delete(book)
                db.session.commit()

            return {"message": f"Book and all its copies deleted"}

        except Exception as e:
            db.session.rollback()
            raise e


class CopiesRepository:

    @staticmethod
    def get_all_copies():
        return Copies.query.all()

    @staticmethod
    def get_copies_by_book_id(book_id):
        return Copies.query.filter_by(book_id=book_id).all()


    @staticmethod
    def add_copies(book_id, quantity):
        try:
            with db.session.begin():
                book = Book.query.get(book_id)
                if not book:
                    raise ValueError("Book not found")
                
                copies = [Copies(book_id=book.book_id) for _ in range(quantity)]
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
        
class BorrowRepositoy:

    @staticmethod
    def get_all_borrowings():
        return Borrowing.query.all()
    
    def get_borrowings_by_user_name(user_name):
        return Borrowing.query.join(User, Borrowing.user_id == User.user_id).filter(User.user_name == user_name).all()

    @staticmethod
    def get_borrowing_by_id(borrow_id):
        return Borrowing.query.get(borrow_id)

    @staticmethod
    def get_borrowings_by_user_id(user_id):
        return Borrowing.query.filter_by(user_id=user_id).all()

    @staticmethod
    def get_borrowings_by_copy_id(copy_id):
        return Borrowing.query.filter_by(copy_id=copy_id).all()
    
    @staticmethod
    def get_borrowings_by_return_date(borrow_date):
        return Borrowing.query.filter_by(borrow_date=borrow_date).all()

    @staticmethod
    def add_new_borrowing(user_id, copy_id, borrow_date):
        new_borrowing = Borrowing(user_id=user_id, copy_id=copy_id, borrow_date=borrow_date)
        db.session.add(new_borrowing)
        db.session.commit()
        return new_borrowing

    @staticmethod
    def delete_borrowing(borrow_id, user_id):
        try:
            with db.session.begin():
                borrowing = Borrowing.query.get(borrow_id)
                if not borrowing:
                    raise ValueError("Borrowing not found")
                
                if borrowing.user_id != user_id:
                    raise ValueError("User did not borrow this book")

                db.session.delete(borrowing)
                db.session.commit()

            return {"message": f"Borrowing deleted"}

        except Exception as e:
            db.session.rollback()
            raise e
        
class ReserveRepository:
    
    @staticmethod
    def get_all_reservations():
        return Reserve.query.all()

    @staticmethod
    def get_reservation_by_id(reserve_id):
        return Reserve.query.get(reserve_id)

    @staticmethod
    def get_reservations_by_user_id(user_id):
        return Reserve.query.filter_by(user_id=user_id).all()

    @staticmethod
    def get_reservations_by_copy_id(copy_id):
        return Reserve.query.filter_by(copy_id=copy_id).all()

    @staticmethod
    def add_new_reservation(user_id, copy_id):
        new_reservation = Reserve(user_id=user_id, copy_id=copy_id)
        db.session.add(new_reservation)
        db.session.commit()
        return new_reservation

    @staticmethod
    def delete_reservation(reserve_id):
        try:
            with db.session.begin():
                reservation = Reserve.query.get(reserve_id)
                if not reservation:
                    raise ValueError("Reservation not found")

                db.session.delete(reservation)
                db.session.commit()

            return {"message": f"Reservation deleted"}

        except Exception as e:
            db.session.rollback()
            raise e