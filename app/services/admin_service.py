from utils.responses import Responses
from utils.validators import Thevalidators

from repositories.user_repository import UserRepository
from repositories.book_repository import BookRepository, CopiesRepository


class AdminService:
    def __init__(self, user_repository: UserRepository, book_repository: BookRepository, copy_repository: CopiesRepository):
        self.user_repository = user_repository
        self.book_repository = book_repository
        self.copy_repository = copy_repository

    def approve_user(self, user_id):
        user = self.user_repository.get_by_id(user_id)
        if not user:
            return Responses.not_found("User")
        
        user_data = {'is_approved': True}
        updated_user = self.user_repository.update(user_id, user_data)
        return Responses.updated("User", updated_user)

    def create_book(self, book_data):
        if not Thevalidators.validate_isbn(book_data.get('isbn')):
            return Responses.validation_error({"isbn": "Invalid ISBN format"})
        if not Thevalidators.validate_name(book_data.get('title')):
            return Responses.validation_error({"title": "Title must be at least 3 characters"})
        if not Thevalidators.validate_price(book_data.get('price')):
            return Responses.validation_error({"price": "Price must be a positive number"})
        
        book = self.book_repository.create(book_data)
        return Responses.created("Book", book)

    def create_copy(self, copy_data):
        if not Thevalidators.validate_stock(copy_data.get('stock')):
            return Responses.validation_error({"stock": "Stock must be a positive number"})
        
        copy = self.copy_repository.create(copy_data)
        return Responses.created("Copy", copy)

    def create_user(self, user_data):
        if not Thevalidators.validate_email(user_data.get('email')):
            return Responses.validation_error({"email": "Invalid email format"})
        if not Thevalidators.validate_password(user_data.get('password')):
            return Responses.validation_error({"password": "Password must be at least 8 characters"})
        if not Thevalidators.validate_name(user_data.get('name')):
            return Responses.validation_error({"name": "Name must be at least 3 characters"})
        
        user_data['is_approved'] = False  # Set user as not approved initially
        user = self.user_repository.create(user_data)
        return Responses.created("User", user)

    def delete_book(self, book_id):
        book = self.book_repository.get_by_id(book_id)

        if not book:
            return Responses.not_found("Book")
        
        self.book_repository.delete(book_id)
        return Responses.deleted("Book")

    def delete_copy(self, copy_id):
        copy = self.copy_repository.get_by_id(copy_id)
        if not copy:
            return Responses.not_found("Copy")
        
        self.copy_repository.delete(copy_id)
        return Responses.deleted("Copy")

    def delete_user(self, user_id):
        user = self.user_repository.get_by_id(user_id)
        if not user:
            return Responses.not_found("User")
        
        self.user_repository.delete(user_id)
        return Responses.deleted("User")

    def update_book(self, book_id, book_data):
        book = self.book_repository.get_by_id(book_id)
        if not book:
            return Responses.not_found("Book")
        
        if 'isbn' in book_data and not Thevalidators.validate_isbn(book_data['isbn']):
            return Responses.validation_error({"isbn": "Invalid ISBN format"})
        if 'title' in book_data and not Thevalidators.validate_name(book_data['title']):
            return Responses.validation_error({"title": "Title must be at least 3 characters"})
        if 'price' in book_data and not Thevalidators.validate_price(book_data['price']):
            return Responses.validation_error({"price": "Price must be a positive number"})
        
        updated_book = self.book_repository.update(book_id, book_data)
        return Responses.updated("Book", updated_book)

    def update_copy(self, copy_id, copy_data):
        copy = self.copy_repository.get_by_id(copy_id)
        if not copy:
            return Responses.not_found("Copy")
        
        if 'stock' in copy_data and not Thevalidators.validate_stock(copy_data['stock']):
            return Responses.validation_error({"stock": "Stock must be a positive number"})
        
        updated_copy = self.copy_repository.update(copy_id, copy_data)
        return Responses.updated("Copy", updated_copy)

    def update_profile(self, admin_id, profile_data):
        admin = self.user_repository.get_by_id(admin_id)
        if not admin:
            return Responses.not_found("Admin")
        
        if 'email' in profile_data and not Thevalidators.validate_email(profile_data['email']):
            return Responses.validation_error({"email": "Invalid email format"})
        if 'password' in profile_data and not Thevalidators.validate_password(profile_data['password']):
            return Responses.validation_error({"password": "Password must be at least 8 characters"})
        if 'name' in profile_data and not Thevalidators.validate_name(profile_data['name']):
            return Responses.validation_error({"name": "Name must be at least 3 characters"})
        
        updated_admin = self.user_repository.update(admin_id, profile_data)
        return Responses.updated("Admin", updated_admin)

    def update_user(self, user_id, user_data):
        user = self.user_repository.get_by_id(user_id)
        if not user:
            return Responses.not_found("User")
        
        if 'email' in user_data and not Thevalidators.validate_email(user_data['email']):
            return Responses.validation_error({"email": "Invalid email format"})
        if 'password' in user_data and not Thevalidators.validate_password(user_data['password']):
            return Responses.validation_error({"password": "Password must be at least 8 characters"})
        if 'name' in user_data and not Thevalidators.validate_name(user_data['name']):
            return Responses.validation_error({"name": "Name must be at least 3 characters"})
        
        updated_user = self.user_repository.update(user_id, user_data)
        return Responses.updated("User", updated_user)