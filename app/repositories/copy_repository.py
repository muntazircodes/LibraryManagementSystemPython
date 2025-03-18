from app.utils.db import db
from app.enums import CopyAvaliabilityEnum, CopyConditionEnum
from app.models import Books, Copies

class CopiesRepository:

    @staticmethod
    def addCopies(book_id, quantity, rack_id, copy_condition=CopyConditionEnum.EXCELENT, copy_available=CopyAvaliabilityEnum.AVALIABLE):
        try:
            with db.session.begin():
                book = Books.query.get(book_id)
                if not book:
                    return {"message": "Book not found"}
                        
                copies = [
                    Copies(
                        book_id=book.book_id,
                        rack_id=rack_id,
                        copy_condition=copy_condition,
                        copy_available=copy_available
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
    def getAllCopies():
        return Copies.query.all()

    @staticmethod
    def getCopiesByBook(book_id):
        return Copies.query.filter_by(book_id=book_id).all()

    @staticmethod
    def updateCopy(copy_id, **kwargs):
        try:
            with db.session.begin():
                copy = Copies.query.get_or_404(copy_id)
                allowed_fields = ['rack_id', 'copy_condition', 'copy_status', 'copy_available']
                        
                for key, value in kwargs.items():
                    if key in allowed_fields:
                        setattr(copy, key, value)
                        
                db.session.commit()
                return copy
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def updateAllCopies(book_id, **kwargs):
        try:
             with db.session.begin():
                copies = Copies.query.filter_by(book_id=book_id).all()
                allowed_fields = ['rack_id', 'copy_condition', 'copy_status', 'copy_available']
                        
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
    def deleteCopy(copy_id):
        try:
            with db.session.begin():
                copy = Copies.query.get(copy_id)
                if not copy:
                    raise ValueError("Copy not found")

                book = Books.query.get(copy.book_id)
                db.session.delete(copy)
                        
                book.available_stock = max(0, book.available_stock - 1)
                        
                db.session.commit()
                return {"message": f"Copy deleted, updated quantity for {book.book_name}: {book.book_stock}"}
        except Exception as e:
            db.session.rollback()
            raise e