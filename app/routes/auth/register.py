from flask import Blueprint, request, jsonify
from app.services.library_service import LibraryService
from app.utils.validators import Validators
from app.utils.responses import Responses

register_bp = Blueprint('register', __name__)

@register_bp.route('/library/register', methods=['POST'])
def register_library():
    try:
        data = request.get_json()
        
        if validation_error := Validators.validate_library_data(data):
            return jsonify({
                'success': False,
                'message': 'Validation error',
                'errors': validation_error
            }), 400

        result = LibraryService.register_library(data)
        if "error" in result:
            return jsonify({
                'success': False,
                'message': result["error"]
            }), 400

        return jsonify({
            'success': True,
            'message': 'Library registered successfully',
            'data': result
        }), 201

    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Internal server error',
            'error': str(e)
        }), 500
