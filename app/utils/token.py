from flask_jwt_extended import create_access_token, decode_token
from datetime import timedelta

class TokenManager:
    @staticmethod
    def generate_token(user_id, expires_in=1):

        expires = timedelta(hours=expires_in)
        return create_access_token(identity=user_id, expires_delta=expires)

    @staticmethod
    def decode_token(token):

        return decode_token(token)
