from utils.db import db
from models.user_model import User
class UserRepository:
    @staticmethod
    def get_all_users():
        return User.query.all()
    
    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(user_id)
    
    @staticmethod
    def get_user_by_email(user_email):
        return User.query.filter_by(user_email=user_email).first()
    
    @staticmethod
    def get_user_by_name(user_name):
        return User.query.filter_by(user_name=user_name).first()
    
    @staticmethod
    def get_defaulter_user():
        return User.query.filter(User.user_fine > 0).all()

                
    
