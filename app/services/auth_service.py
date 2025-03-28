from app.middleware import TokenManager
from app.models import User
from werkzeug.security import check_password_hash, generate_password_hash
from flask import jsonify, request


class AuthService:

    @staticmethod
    def register(data):
        try:
            email = data.get('email')
            password = data.get('password')

            if not email or not password:
                return {'message': 'Missing email or password'}, 400

            if User.query.filter_by(user_email=email).first():
                return {'message': 'Email already exists'}, 409

            new_user = User(
                user_email=email,
                user_password=generate_password_hash(password),
            )
            new_user.save()

            return {'message': 'User registered successfully'}, 201

        except Exception as e:
            return {'message': 'Registration failed', 'error': str(e)}, 500

    @staticmethod
    def login(data):
        try:
            email, password = data.get('email'), data.get('password')
            if not email or not password:
                return {'message': 'Missing email or password'}, 400

            user = User.query.filter_by(user_email=email).first()
            if not user or not check_password_hash(user.user_password, password):
                return {'message': 'Invalid email or password'}, 401

            if not user.user_verified:
                return {'message': 'User is not verified'}, 403

            return {
                'message': 'Login successful',
                'access_token': TokenManager.generate_token(user.user_id, user.user_type)
            }, 200

        except Exception as e:
            return {'message': 'Login failed', 'error': str(e)}, 500
