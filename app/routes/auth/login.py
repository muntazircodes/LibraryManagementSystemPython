from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from app.models.user_model import User
from app.utils.token import TokenManager

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'message': 'Missing email or password'}), 400

        user = User.query.filter_by(user_email=data['email']).first()

        if not user or not check_password_hash(user.user_password, data['password']):
            return jsonify({'message': 'Invalid email or password'}), 401

        if not user.user_verified:
            return jsonify({'message': 'User is not verified'}), 403

        access_token = TokenManager.generate_token(user.user_id, user.user_type) 

        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'user': {
                'id': user.user_id,
                'email': user.user_email,
                'name': user.user_name,
                'type': user.user_type
            }
        }), 200

    except Exception as e:
        return jsonify({'message': 'Login failed', 'error': str(e)}), 500
