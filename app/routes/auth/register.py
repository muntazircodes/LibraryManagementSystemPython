from flask import Blueprint, request
from app.services.admin_service import AdminService
from app.repositories.user_repository import UserRepository
from app.repositories.library_repository import LibraryRepository
from app.utils.validators import Validators
from app.utils.responses import Responses

register_bp = Blueprint('register', __name__)

@register_bp.route('/library/register', methods=['POST'])
def register_library():
    try:
        data = request.get_json()

        required_fields = ['lib_name', 'lib_address', 'lib_admin', 'lib_license', 'lib_docs', 'lib_email']
        missing_fields = [field for field in required_fields if field not in data or not data[field]]
        if missing_fields:
            return Responses.missing_fields(missing_fields)

        validators = {
            'lib_name': Validators.validate_name,
            'lib_email': Validators.validate_email
        }

        validation_error = AdminService.validate_and_serialize(data, validators)
        if validation_error:
            return Responses.validation_error(validation_error)

        existing_library = LibraryRepository.get_library_by_email(data.get('lib_email'))
        if existing_library:
            return Responses.conflict("Library with this email already exists")

        new_library_data = {field: data.get(field) for field in required_fields}
        result = AdminService.handle_repository_action(LibraryRepository.add_library, **new_library_data)

        if not result or 'error' in result:
            return Responses.error(result.get('error', "Failed to create library"))

        return Responses.created("Library", data=result)

    except Exception as e:
        return Responses.server_error()


@register_bp.route('/user/register', methods=['POST'])

def register_user():
    try:
        data = request.get_json()

        required_fields = ['user_name', 'user_email', 'user_password', 'phone_number', 'valid_docs', 'lib_id']
        missing_fields = [field for field in required_fields if field not in data or not data[field]]
        if missing_fields:
            return Responses.missing_fields(missing_fields)

        validators = {
            'user_name': Validators.validate_name,
            'user_email': Validators.validate_email,
            'user_password': Validators.validate_password,
            'phone_number': Validators.validate_phone
        }

        validation_error = AdminService.validate_and_serialize(data, validators)
        if validation_error:
            return Responses.validation_error(validation_error)

        existing_user = UserRepository.get_user_by_email(data.get('user_email'))
        if existing_user:
            return Responses.conflict("User with this email already exists")

        hashed_password = Validators.hash_password(data.get('user_password'))
        data['user_password'] = hashed_password

        new_user_data = {field: data.get(field) for field in required_fields}
        result = AdminService.handle_repository_action(UserRepository.add_user, **new_user_data)

        if not result or 'error' in result:
            return Responses.error(result.get('error', "Failed to create user"))

        return Responses.created("User", data=result)

    except Exception as e:
        return Responses.server_error()
