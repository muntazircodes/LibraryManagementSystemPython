from flask import Blueprint, request
from app.services.admin_service import AdminService
from app.utils.validators import Validators
from app.utils.responses import Responses

register_bp = Blueprint('register', __name__)

@register_bp.route('/library/register', methods=['POST'])
def register_library():
    try:
        data = request.get_json()

        required_fields = ["lib_name", "lib_location", "lib_admin", "lib_licence", "lib_docs", "lib_email"]
        missing_fields = [field for field in required_fields if field not in data or not data[field]]
        if missing_fields:
            return Responses.missing_fields(missing_fields)

        if not Validators.validate_name(data.get('lib_name')):
            return Responses.validation_error({"name": "Invalid library name"})

        if not Validators.validate_email(data.get('lib_email')):
            return Responses.validation_error({"email": "Invalid email format"})

        result = AdminService.register_library(data)
        if "error" in result:
            return Responses.error(result["error"], status_code=400)

        return Responses.created("Library", data=result)

    except Exception as e:
        return Responses.server_error()

@register_bp.route('/user/register', methods=['POST'])
def register_user():
    try:
        data = request.get_json()

        required_fields = ["user_name", "user_email", "user_password", "user_type", "lib_id"]
        missing_fields = [field for field in required_fields if field not in data or not data[field]]
        if missing_fields:
            return Responses.missing_fields(missing_fields)

        if not Validators.validate_name(data.get('user_name')):
            return Responses.validation_error({"name": "Invalid user name"})

        if not Validators.validate_email(data.get('user_email')):
            return Responses.validation_error({"email": "Invalid email format"})

        result = AdminService.register_user(data)
        if "error" in result:
            return Responses.error(result["error"], status_code=400)

        return Responses.created("User", data=result)

    except Exception as e:
        return Responses.server_error()