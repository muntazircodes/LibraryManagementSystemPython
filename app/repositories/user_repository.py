from app.utils.db import db
from app.models import User, Report
from app.enums import UserRoleEnum, UserStatusEnum
from ..repositories import LibraryRepository


class UserRepository:   

    @staticmethod
    def addUser (
        user_name, user_email, user_password, lib_id, 
        phone_number, valid_docs
    ):
        if User.query.filter_by(user_email=user_email).first():
            raise ValueError("User with this email already exists")

        if not LibraryRepository.getLibraryById(lib_id):
            raise ValueError("Library with this ID does not exist")

        new_user = User(
            user_name=user_name,
            user_email=user_email,
            user_password=user_password, 
            lib_id=lib_id,
            phone_number=phone_number,
            valid_docs=valid_docs,
        )
        db.session.add(new_user)
        db.session.commit()
        return new_user
    

    @staticmethod
    def getAllUsers():
        return User.query.all()
    

    @staticmethod
    def getUserById(user_id):
        return User.query.get(user_id)

    @staticmethod
    def getUserByEmail(user_email): 
        return User.query.filter_by(user_email=user_email).first()

    @staticmethod
    def getUserByName(user_name):
        return User.query.filter(User.user_name.ilike(f"%{user_name}%")).all()

    @staticmethod
    def getVerifiedUsers():
        return User.query.filter_by(user_verified = UserStatusEnum.VERIFIED).all()

    @staticmethod
    def get_defaulter_user():
        return User.query.filter(User.user_fine > 0).all()

    @staticmethod
    def checkUserFine(user_id):
        user = User.query.get(user_id)
        return user.user_fine if user else None


    @staticmethod
    def userBorrowings(user_id):
        user = User.query.get(user_id)
        return user.alloted_books 

    @staticmethod
    def updateUser(user_id, **kwargs):
        user = User.query.get(user_id)
        if not user:
            raise ValueError("User not found")

        allowed_fields = [
            'user_name', 'user_email', 'user_password', 'user_type', 
            'user_verified', 'user_fine', 'phone_number', 
            'profile_picture', 'allowed_books', 'alloted_books'
        ]
        try:
            for key, value in kwargs.items():
                if key in allowed_fields and hasattr(user, key):
                    setattr(user, key, value)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        return user


    @staticmethod
    def updateUserFine(user_id, fine_amount):
        user = User.query.get(user_id)
        user.user_fine = fine_amount
        db.session.commit()


    @staticmethod
    def addUserAllowedBooks(user_id, allowed_books):
        user = User.query.get(user_id)
        user.allowed_books += allowed_books
        db.session.commit()


    @staticmethod
    def promoteAsAdmin(user_id):
        user = User.query.get(user_id)
        user.user_type = UserRoleEnum.ADMIN
        db.session.commit()


    @staticmethod     
    def getAdmin():
        return User.query.filter_by(user_type=UserRoleEnum.ADMIN).all()


    @staticmethod
    def verifyUser(user_id):
        user = User.query.get(user_id)
        user.user_verified =UserStatusEnum.VERIFIED
        db.session.commit()


    @staticmethod
    def deleteUser(user_id):
        user = User.query.get(user_id)
        db.session.delete(user)
        db.session.commit()


    @staticmethod
    def user_belong_this_lib(user_id, lib_id):
        user = User.query.get(user_id)
        return user.lib_id == lib_id if user else False
  
    
    @staticmethod
    def getVerifiedUsers():
        return User.query.filter_by(user_verified=True).all()
    
    
