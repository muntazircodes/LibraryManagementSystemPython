from app.utils.responses import Responses
from app.utils.validators import Validators

from app.repositories.book_repository import BorrowRepository , ReserveRepository
from app.repositories.user_repository import UserRepository

class BookService:
    
    @staticmethod
    def borrow_book(user_id, copy_id, borrow_date):
        try:
            user = UserRepository.get_user_by_id(user_id)
            if not user:
                return Responses.not_found("User")
            
            if not user.user_verified:
                return Responses.forbidden()
            
            if user.user_fine > 0:
                return Responses.error("Cannot borrow book. Please clear pending fines.")
            
            if user.alloted_books >= user.allowed_books:
                return Responses.error("Maximum book limit reached")

            if not Validators.validate_date(borrow_date):
                return Responses.validation_error({"borrow_date": "Invalid date format"})

            borrowing = BorrowRepository.add_new_borrowing(user_id, copy_id, borrow_date)
            
            UserRepository.update_user(
                user_id=user_id,
                user_name=user.user_name,
                user_email=user.user_email,
                user_password=user.user_password,
                user_type=user.user_type,
                user_fine=user.user_fine,
                alloted_books=user.alloted_books + 1
            )

            return Responses.success("Book borrowed successfully", borrowing)
        
        except ValueError as e:
            return Responses.error(str(e))
        except Exception as e:
            return Responses.server_error()

    @staticmethod
    def return_book(borrow_id, user_id):
        try:
            borrowing = BorrowRepository.get_borrowing_by_id(borrow_id)
            if not borrowing:
                return Responses.not_found("Borrowing record")

            BorrowRepository.delete_borrowing(borrow_id, user_id)
            
            user = UserRepository.get_user_by_id(user_id)
            UserRepository.update_user(
                user_id=user_id,
                user_name=user.user_name,
                user_email=user.user_email,
                user_password=user.user_password,
                user_type=user.user_type,
                user_fine=user.user_fine,
                alloted_books=max(0, user.alloted_books - 1)
            )

            return Responses.success("Book returned successfully")

        except ValueError as e:
            return Responses.error(str(e))
        except Exception as e:
            return Responses.server_error()

    @staticmethod
    def reserve_book(user_id, copy_id):
        try:
            user = UserRepository.get_user_by_id(user_id)
            if not user:
                return Responses.not_found("User")

            if not user.user_verified:
                return Responses.forbidden()

            if user.user_fine > 0:
                return Responses.error("Cannot reserve book. Please clear pending fines.")

            reservation = ReserveRepository.add_new_reservation(user_id, copy_id)
            return Responses.success("Book reserved successfully", reservation)

        except ValueError as e:
            return Responses.error(str(e))
        except Exception as e:
            return Responses.server_error()

    @staticmethod
    def cancel_reservation(reserve_id):
        try:
            ReserveRepository.delete_reservation(reserve_id)
            return Responses.success("Reservation cancelled successfully")
        except Exception as e:
            return Responses.server_error()

    @staticmethod
    def update_fine(user_id, days_overdue, fine_per_day=1.0):
        try:
            user = UserRepository.get_user_by_id(user_id)
            if not user:
                return Responses.not_found("User")

            new_fine = days_overdue * fine_per_day
            UserRepository.update_user_fine(user_id, new_fine)
            return Responses.success("Fine updated successfully")

        except Exception as e:
            return Responses.server_error()