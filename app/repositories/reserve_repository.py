from app.utils.db import db
from app.models import Books, Reserve


class ReserveRepository:

    @staticmethod
    def addReservation(user_id, book_id):
        try:
            with db.session.begin():
                # Check if book exists
                book = Books.query.get(book_id)
                if not book:
                    raise ValueError("Book not found")

                # Check if user has already reserved this book
                existing_reservation = Reserve.query.filter_by(
                    user_id=user_id, 
                    book_id=book_id,
                    is_expired=False
                ).first()
                
                if existing_reservation:
                    raise ValueError("User already has an active reservation for this book")

                new_reservation = Reserve(
                    user_id=user_id,
                    book_id=book_id,
                    is_expired=False
                )
                db.session.add(new_reservation)
                db.session.commit()
                return new_reservation
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def getAllReservations():
        return Reserve.query.all()

    @staticmethod
    def getReservationById(reserve_id):
        return Reserve.query.get_or_404(reserve_id)

    @staticmethod
    def getUserReservation(user_id):
        return Reserve.query.filter_by(user_id=user_id).all()

    @staticmethod
    def updateReservation(reserve_id, **kwargs):
        try:
            with db.session.begin():
                reservation = Reserve.query.get_or_404(reserve_id)
                
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
    def deleteReservation(reserve_id):
        try:
            with db.session.begin():
                reservation = Reserve.query.get_or_404(reserve_id)
                db.session.delete(reservation)
                db.session.commit()
            return {"message": "Reservation deleted"}
        except Exception as e:
            db.session.rollback()
            raise e
