from flask_jwt_extended import create_access_token, decode_token
from flask_jwt_extended import JWTManager
from datetime import timedelta

jwt = JWTManager()

class TokenManager:
    @staticmethod
    def generate_token(user_id, expires_in=1):
        expires = timedelta(hours=expires_in)
        return create_access_token(identity=user_id, expires_delta=expires)

    @staticmethod
    def decode_token(token):
        try:
            decoded_token = decode_token(token)
            return decoded_token
        except Exception as e:
            return {'error': str(e)}
