from app.utils.db import db
from app.models import Copies, Borrowing, Books, User
from app.enums import CopyAvaliabilityEnum


class BorrowRepository:

    @staticmethod
    def add_new_borrowing(user_id, copy_id, borrow_date):
        try:
            with db.session.begin():
                copy = Copies.query.get(copy_id)
                if not copy or copy.copy_available != CopyAvaliabilityEnum.YES:
                    raise ValueError("Copy not available for borrowing")

                new_borrowing = Borrowing(
                    user_id=user_id, 
                    copy_id=copy_id, 
                    borrow_date=borrow_date
                )
                db.session.add(new_borrowing)
                
                copy.copy_available = CopyAvaliabilityEnum.NO

                book = Books.query.get(copy.book_id)
                book.available_stock = max(0, book.available_stock - 1)
                
                db.session.commit()
                return new_borrowing
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
                copy.copy_available = CopyAvaliabilityEnum.YES
                
                book = Books.query.get(copy.book_id)
                book.available_stock += 1

                db.session.delete(borrowing)
                db.session.commit()

            return {"message": "Borrowing deleted"}
        except Exception as e:
            db.session.rollback()
            raise e