from app.utils.responses import Responses
from app.utils.validators import Validators
from app.repositories.user_repository import UserRepository

class UserService:

    @staticmethod 
    def get_my_profile(user_id):
        user = UserRepository.get_user_by_id(user_id)
        if not user:
            return Responses.not_found("User")
        return Responses.success("User details retrieved", user)
    
    @staticmethod
    def check_email_exists(email):
        user = UserRepository.get_user_by_email(email)
        if user:
            return Responses.success("Email exists")
        return Responses.error("Email does not exist")
    
    @staticmethod
    def check_my_borrowings(user_id):
        borrowings = UserRepository.get_user_borrowings(user_id)
        return Responses.success("Borrowings retrieved", borrowings)
    