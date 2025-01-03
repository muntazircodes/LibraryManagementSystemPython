from flask import Blueprint, request
from app.services.admin_service import AdminService
from app.utils.validators import Validators
from app.utils.responses import Responses

register_bp = Blueprint('register', __name__)

@register_bp.route('/library/register', methods=['POST'])
def register_library():
    try:
        data = request.get_json()

        required_fields = ["lib_name", "lib_address", "lib_admin", "lib_license", "lib_docs", "lib_email"]
        missing_fields = [field for field in required_fields if field not in data or not data[field]]
        if missing_fields:
            return Responses.missing_fields(missing_fields)

        validations = {
            "lib_name": Validators.validate_name,
            "lib_email": Validators.validate_email
        }

        for field, validator in validations.items():
            if not validator(data.get(field)):
                return Responses.validation_error({field: f"Invalid {field.replace('_', ' ')}"})

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

        validations = {
            "user_name": Validators.validate_name,
            "user_email": Validators.validate_email
        }

        for field, validator in validations.items():
            if not validator(data.get(field)):
                return Responses.validation_error({field: f"Invalid {field.replace('_', ' ')}"})

        result = AdminService.register_user(data)
        if "error" in result:
            return Responses.error(result["error"], status_code=400)

        return Responses.created("User", data=result)

    except Exception as e:
        return Responses.server_error()