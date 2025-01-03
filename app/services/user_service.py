from datetime import datetime
from app.utils.responses import Responses
from app.utils.validators import Validators
from app.repositories.user_repository import UserRepository


class UserService:

    @staticmethod
    def validate_and_serialize(data, validators):
        for field, validator in validators.items():
            if not validator(data.get(field)):
                return Responses.validation_error({field: f"Invalid {field.replace('user_', '').replace('_', ' ')} format"})
        return None

    @staticmethod
    def handle_repository_action(action, *args, **kwargs):
        try:
            result = action(*args, **kwargs)
            if not result:
                return Responses.not_found(action.__name__.split('_')[1].capitalize())
            return Validators.serialize_model(result) if not isinstance(result, list) else [Validators.serialize_model(item) for item in result]
        except Exception as e:
            return Responses.server_error()

    @staticmethod
    def get_my_profile(user_id):
        return UserService.handle_repository_action(UserRepository.get_user_by_id, user_id)

    @staticmethod
    def update_my_profile(user_id, user_data):
        validators = {
            'user_name': Validators.validate_name,
            'user_email': Validators.validate_email,
            'user_password': Validators.validate_password,
            'phone_number': Validators.validate_phone,
            'profile_picture': Validators.validate_image
        }

        validation_error = UserService.validate_and_serialize(user_data, validators)
        if validation_error:
            return validation_error

        return UserService.handle_repository_action(UserRepository.update_user, user_id, **user_data)

    @staticmethod
    def check_my_borrowings(user_id):
        return UserService.handle_repository_action(UserRepository.get_user_borrowings, user_id)

    @staticmethod
    def check_my_reservations(user_id):
        return UserService.handle_repository_action(UserRepository.get_user_reservations, user_id)

    @staticmethod
    def change_my_password(user_id, old_password, new_password):
        user = UserRepository.get_user_by_id(user_id)
        if not user:
            return Responses.not_found("User")

        if not Validators.verify_password(old_password, user.get('user_password')):
            return Responses.validation_error({"password": "Invalid password"})

        if not Validators.validate_password(new_password):
            return Responses.validation_error({"password": "Invalid password"})

        new_password = Validators.hash_password(new_password)
        return UserService.handle_repository_action(UserRepository.update_password, user_id, new_password)

    @staticmethod
    def report_for_query(user_id, report_data):
        validators = {
            'subject': Validators.validate_name,
            'message': Validators.validate_text,
            'handled_by': Validators.validate_name
        }

        validation_error = UserService.validate_and_serialize(report_data, validators)
        if validation_error:
            return validation_error

        report_data['handled'] = report_data.get('handled', False)
        report_data['report_date'] = datetime.now()
        return UserService.handle_repository_action(UserRepository.add_report, user_id, **report_data)
