from datetime import datetime
from app.utils.responses import Responses
from app.utils.validators import Validators
from app.repositories.user_repository import UserRepository


class UserService:
    @staticmethod
    def handle_repository_action(action, *args, **kwargs):
        try:
            result = action(*args, **kwargs)
            if not result:
                return Responses.not_found(action.__name__.split('_')[1].capitalize())
            return Validators.serialize_model(result) if not isinstance(result, list) else [Validators.serialize_model(item) for item in result]
        except Exception:
            return Responses.server_error()

    @staticmethod
    def get_my_profile(user_id):
        return UserService.handle_repository_action(UserRepository.get_user_by_id, user_id)

    @staticmethod
    def update_my_profile(user_id, user_data):
        try:
            allowed_fields = [
                'user_name', 'user_email', 'user_password',
                'phone_number', 'profile_picture'
            ]
            update_data = {field: user_data.get(field) for field in allowed_fields}
            return UserService.handle_repository_action(UserRepository.update_user, user_id, **update_data)
        except Exception:
            return Responses.server_error()

    @staticmethod
    def check_my_borrowings(user_id):
        return UserService.handle_repository_action(UserRepository.get_user_borrowings, user_id)

    @staticmethod
    def check_my_reservations(user_id):
        return UserService.handle_repository_action(UserRepository.get_user_reservations, user_id)

    @staticmethod
    def change_my_password(user_id, old_password, new_password):
        try:
            user = UserRepository.get_user_by_id(user_id)
            if not user:
                return Responses.not_found("User")
            return UserService.handle_repository_action(UserRepository.update_password, user_id, new_password)
        except Exception:
            return Responses.server_error()

    @staticmethod
    def report_for_query(user_id, report_data):
        try:
            report_data['handled'] = report_data.get('handled', False)
            report_data['report_date'] = datetime.now()
            return UserService.handle_repository_action(UserRepository.add_report, user_id, **report_data)
        except Exception:
            return Responses.server_error()
