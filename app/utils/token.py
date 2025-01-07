from flask_jwt_extended import create_access_token, decode_token, jwt_required, get_jwt_identity
from flask_jwt_extended import JWTManager
from datetime import timedelta

jwt = JWTManager()

class TokenManager:
    @staticmethod
    def generate_token(user_id, user_type, expires_in=1):
        expires = timedelta(hours=expires_in)
        return create_access_token(identity={'id': user_id, 'type': user_type}, expires_delta=expires)

    @staticmethod
    def decode_token(token):
        try:
            decoded_token = decode_token(token)
            return decoded_token
        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def user_type_required(required_type):
        def decorator(fn):
            @jwt_required()
            def wrapper(*args, **kwargs):
                current_user = get_jwt_identity()
                if current_user['type'] != required_type:
                    return {'message': 'Access forbidden: insufficient permissions'}, 403
                return fn(*args, **kwargs)
            return wrapper
        return decorator