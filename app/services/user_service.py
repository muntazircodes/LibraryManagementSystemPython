from datetime import datetime
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
    def update_my_profile(user_id, user_data):
        user = UserRepository.get_user_by_id(user_id)
        if not user:
            return Responses.not_found("User")
        
        if not Validators.validate_name(user_data.get('user_name')):
            return Responses.validation_error({"name": "Invalid name"})
        
        if not Validators.validate_email(user_data.get('user_email')):
            return Responses.validation_error({"email": "Invalid email"})
        
        if not Validators.validate_password(user_data.get('user_password')):
            return Responses.validation_error({"password": "Invalid password"})
        
        if not Validators.validate_phone(user_data.get('phone_number')):
            return Responses.validation_error({"phone": "Invalid phone number"})
        
        if not Validators.validate_image(user_data.get('profile_picture')):
            return Responses.validation_error({"picture": "Invalid picture"})
        
        UserRepository.update_user(
            user_id=user_id,
            user_name=user_data.get('user_name'),
            user_email=user_data.get('user_email'),
            user_password=user_data.get('user_password'),
            phone_number=user_data.get('phone_number'),
            profile_picture=user_data.get('profile_picture')
        )
        return Responses.success("User details updated")
    
    @staticmethod
    def check_my_borrowings(user_id):
        borrowings = UserRepository.get_user_borrowings(user_id)
        return Responses.success("Borrowings retrieved", borrowings)
    
    @staticmethod
    def check_my_reservations(user_id):
        reservations = UserRepository.get_user_reservations(user_id)
        return Responses.success("Reservations retrieved", reservations)
    
    @staticmethod
    def change_my_pssword(user_id, old_password, new_password):
        user = UserRepository.get_user_by_id(user_id)
        if not user:
            return Responses.not_found("User")
        
        if not Validators.verify_password(old_password, user.get('user_password')):
            return Responses.validation_error({"password": "Invalid password"})
        
        if not Validators.validate_password(new_password):
            return Responses.validation_error({"password": "Invalid password"})
        
        new_password = Validators.hash_password(new_password)
        UserRepository.update_password(user_id, new_password)
        return Responses.success("Password updated")
    
    @staticmethod
    def report_for_query(user_id, report_data):
        if not Validators.validate_name(report_data.get('subject')):
            return Responses.validation_error({"subject": "Invalid subject"})
        
        if not Validators.validate_text(report_data.get('message')):
            return Responses.validation_error({"message": "Invalid message"})
        
        if not Validators.validate_name(report_data.get('handled_by')):
            return Responses.validation_error({"handled_by": "Invalid handler name"})
        
        UserRepository.add_report(
            user_id=user_id,
            subject=report_data.get('subject'),
            message=report_data.get('message'),
            handled_by=report_data.get('handled_by', 'None'),
            handled=report_data.get('handled', False),
            report_date=datetime.now()
        )
        return Responses.created("Report")