from app.utils.responses import Responses
from app.utils.validators import Validators
from app.repositories.user_repository import UserRepository

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create_user(self, user_data):
        errors = self._validate_user_data(user_data)
        if errors:
            return Responses.validation_error(errors)
        user = self.user_repository.add_user(**user_data)
        return Responses.created("User", user)

    def update_user(self, user_id, user_data):
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            return Responses.not_found("User")
        errors = self._validate_user_data(user_data)
        if errors:
            return Responses.validation_error(errors)
        updated_user = self.user_repository.update_user(user_id, **user_data)
        return Responses.updated("User", updated_user)

    def delete_user(self, user_id):
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            return Responses.not_found("User")
        self.user_repository.delete_user(user_id)
        return Responses.deleted("User")

    def _validate_user_data(self, user_data):
        errors = {}
        if 'email' in user_data and not Validators.validate_email(user_data['email']):
            errors["email"] = "Invalid email format"
        if 'password' in user_data and not Validators.validate_password(user_data['password']):
            errors["password"] = "Password must be at least 8 characters"
        if 'name' in user_data and not Validators.validate_name(user_data['name']):
            errors["name"] = "Name must be at least 3 characters"
        return errors
