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

        required_fields = [
            'lib_name', 
            'lib_email', 
            'lib_address',
            'lib_admin', 
            'lib_license', 
            'lib_docs'
        ]

        # Check for missing fields
        missing_fields = [
            field for field in required_fields 
            if field not in data or not data[field]
        ]
        if missing_fields:
            return Responses.missing_fields(missing_fields)
        
        # Define validators
        validators = {
            'lib_name': Validators.validate_name,
            'lib_email': Validators.validate_email,
            'lib_admin': Validators.validate_name,
        }

        validation_error = AdminService.validate_and_serialize(data, validators)
        if validation_error:
            return Responses.validation_error(validation_error)

        existing_library = LibraryRepository.get_library_by_email(data.get('lib_email'))
        if existing_library:
            return Responses.conflict("Library with this email already exists")
        
        existing_library_name = LibraryRepository.get_library_by_name(data.get('lib_name'))
        if existing_library_name:
            return Responses.conflict("Library with this name already exists")

        result = AdminService.register_library(data)
        if not result:
            return Responses.error("Failed to create library")
        
        created_library = LibraryRepository.get_library_by_id(result.get('lib_id'))
        if not created_library:
            return Responses.error("Library creation failed - database verification failed")

        return Responses.created("Library", data=created_library)

    except Exception as e:
        return Responses.server_error()
    

@register_bp.route('/user/register', methods=['POST'])
def register_user():
    try:
        data = request.get_json()

        # Define required fields
        required_fields = [
            'user_name',
            'user_email',
            'user_password',
            'phone_number',
            'valid_docs',
            'lib_id'
        ]

        missing_fields = [
            field for field in required_fields 
            if field not in data or not data[field]
        ]
        if missing_fields:
            return Responses.missing_fields(missing_fields)

        library = LibraryRepository.get_library_by_id(data.get('lib_id'))
        if not library:
            return Responses.not_found("Library with provided ID does not exist")

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

        data['user_password'] = Validators.hash_password(data.get('user_password'))

        new_user_data = {field: data.get(field) for field in required_fields}
        result = AdminService.handle_repository_action(
            UserRepository.add_user, 
            **new_user_data
        )

        if not result:
            return Responses.error("Failed to create user")

        created_user = UserRepository.get_user_by_email(data.get('user_email'))
        if not created_user:
            return Responses.error("User creation failed - database verification failed")

        if isinstance(created_user, dict) and 'user_password' in created_user:
            del created_user['user_password']

        return Responses.created("User", data=created_user)

    except Exception as e:
        return Responses.server_error()
