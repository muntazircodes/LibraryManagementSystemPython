from app.utils.responses import Responses
from app.utils.validators import Validators

from app.repositories.user_repository import UserRepository
from app.repositories.book_repository import BookRepository, CopiesRepository


class AdminService:
    def __init__(self, user_repository: UserRepository, book_repository: BookRepository, copy_repository: CopiesRepository):
        self.user_repository = user_repository
        self.book_repository = book_repository
        self.copy_repository = copy_repository



    def _validate_user_data(self, user_data):

        errors = {}
        if 'email' in user_data and not Validators.validate_email(user_data['email']):
            errors["email"] = "Invalid email format"
        if 'password' in user_data and not Validators.validate_password(user_data['password']):
            errors["password"] = "Password must be at least 8 characters"
        if 'name' in user_data and not Validators.validate_name(user_data['name']): 
            errors["name"] = "Name must be at least 3 characters"
        return errors

    def _validate_book_data(self, book_data):
        errors = {}
        if 'isbn' in book_data and not Validators.validate_isbn(book_data['isbn']):
            errors["isbn"] = "Invalid ISBN format"
        if 'title' in book_data and not Validators.validate_name(book_data['title']):
            errors["title"] = "Title must be at least 3 characters"
        if 'price' in book_data and not Validators.validate_price(book_data['price']):
            errors["price"] = "Price must be a positive number"
        return errors

    def _validate_copy_data(self, copy_data):
        errors = {}
        if 'stock' in copy_data and not Validators.validate_stock(copy_data['stock']):
            errors["stock"] = "Stock must be a positive number"
        return errors

    def create_user(self, user_data):
        errors = self._validate_user_data(user_data)
        if errors:
            return Responses.validation_error(errors)
        user_data['is_approved'] = False  # Default: not approved
        user = self.user_repository.add_user(**user_data)
        return Responses.created("User", user)

    def update_user(self, user_id, user_data):
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            return Responses.not_found("User")
        errors = self._validate_user_data(user_data)
        if errors:
            return Responses.validation_error(errors)
        updated_user = self.user_repository.update_user(user_id, **user_data)
        return Responses.updated("User", updated_user)

    def approve_user(self, user_id):
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            return Responses.not_found("User")
        updated_user = self.user_repository.update_user(user_id, is_approved=True)
        return Responses.updated("User", updated_user)

    def delete_user(self, user_id):
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            return Responses.not_found("User")
        self.user_repository.delete_user(user_id)
        return Responses.deleted("User")

    def get_all_users(self):
        users = self.user_repository.get_all()
        return Responses.success("Users", users)

    def get_user_by_id(self, user_id):
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            return Responses.not_found("User")
        return Responses.success("User", user)



    def create_book(self, book_data):
        errors = self._validate_book_data(book_data)
        if errors:
            return Responses.validation_error(errors)
        book = self.book_repository.create(book_data)
        return Responses.created("Book", book)

    def update_book(self, book_id, book_data):
        book = self.book_repository.get_by_id(book_id)
        if not book:
            return Responses.not_found("Book")
        errors = self._validate_book_data(book_data)
        if errors:
            return Responses.validation_error(errors)
        updated_book = self.book_repository.update(book_id, book_data)
        return Responses.updated("Book", updated_book)

    def delete_book(self, book_id):
        book = self.book_repository.get_by_id(book_id)
        if not book:
            return Responses.not_found("Book")
        self.book_repository.delete(book_id)
        return Responses.deleted("Book")

    def get_all_books(self):
        books = self.book_repository.get_all()
        return Responses.success("Books", books)

    def get_book_by_id(self, book_id):
        book = self.book_repository.get_by_id(book_id)
        if not book:
            return Responses.not_found("Book")
        return Responses.success("Book", book)

    def create_copy(self, copy_data):
        errors = self._validate_copy_data(copy_data)
        if errors:
            return Responses.validation_error(errors)
        copy = self.copy_repository.create(copy_data)
        return Responses.created("Copy", copy)

    def update_copy(self, copy_id, copy_data):
        copy = self.copy_repository.get_by_id(copy_id)
        if not copy:
            return Responses.not_found("Copy")
        errors = self._validate_copy_data(copy_data)
        if errors:
            return Responses.validation_error(errors)
        updated_copy = self.copy_repository.update(copy_id, copy_data)
        return Responses.updated("Copy", updated_copy)

    def delete_copy(self, copy_id):
        copy = self.copy_repository.get_by_id(copy_id)
        if not copy:
            return Responses.not_found("Copy")
        self.copy_repository.delete(copy_id)
        return Responses.deleted("Copy")

    def get_all_copies(self):
        copies = self.copy_repository.get_all()
        return Responses.success("Copies", copies)

    def get_copy_by_id(self, copy_id):
        copy = self.copy_repository.get_by_id(copy_id)
        if not copy:
            return Responses.not_found("Copy")
        return Responses.success("Copy", copy)


    def update_profile(self, admin_id, profile_data):
        """Update admin profile."""
        return self.update_user(admin_id, profile_data)
