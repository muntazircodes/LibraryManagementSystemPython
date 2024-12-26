from flask import Blueprint, request
from app.services.library_service import LibraryService
from app.utils.validators import Validators
from app.utils.responses import Responses

register_bp = Blueprint('register', __name__)

@register_bp.route('/library/register', methods=['POST'])
def register_library():
    try:
        data = request.get_json()

        required_fields = ["lib_name", "lib_admin", "lib_docs", "lib_licence", "lib_email"]
        missing_fields = [field for field in required_fields if field not in data or not data[field]]
        if missing_fields:
            return Responses.missing_fields(missing_fields)

        validation_errors = Validators.validate_library_data(data)
        if validation_errors:
            return Responses.validation_error(validation_errors)

        result = LibraryService.register_library(data)
        if "error" in result:
            return Responses.error(result["error"], status_code=400)

        return Responses.created("Library", data=result)

    except Exception as e:
        return Responses.server_error()

@register_bp.route('/user/register', methods=['POST'])
def register_user():
    try:
        data = request.get_json()

        required_fields = ["username", "email", "password", "lib_name"]
        missing_fields = [field for field in required_fields if field not in data or not data[field]]
        if missing_fields:
            return Responses.missing_fields(missing_fields)

        validation_errors = Validators.validate_user_data(data)
        if validation_errors:
            return Responses.validation_error(validation_errors)

        result = LibraryService.register_user(data)
        if "error" in result:
            return Responses.error(result["error"], status_code=400)

        return Responses.created("User", data=result)

    except Exception as e:
        return Responses.server_error()