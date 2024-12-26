from app.utils.responses import Responses
from app.utils.validators import Validators


from app.repositories.user_repository import UserRepository
from app.repositories.library_repository import LibraryRepository


class LibraryService:

    # Library Management Methods
    @staticmethod
    def get_library_details(lib_id):
        library = LibraryRepository.get_library_by_id(lib_id)
        if not library:
            return Responses.error_response("Library not found", 404)
        return Responses.success_response("Library details retrieved", {"library": library})

    @staticmethod
    def add_new_library(data):
        if not Validators.validate_email(data.get('lib_email')):
            return Responses.error_response("Invalid email format", 400)
            
        existing_library = LibraryRepository.get_library_by_email(data.get('lib_email'))
        if existing_library:
            return Responses.error_response("Library with this email already exists", 400)

        try:
            LibraryRepository.add_library(
                data.get('lib_name'),
                data.get('lib_location'),
                data.get('lib_admin'),
                data.get('lib_licence'),
                data.get('lib_docs'),
                data.get('lib_email')
            )
            return Responses.success_response("Library added successfully", None)
        except Exception as e:
            return Responses.error_response(str(e), 500)

    @staticmethod
    def update_library_details(lib_id, data):
        library = LibraryRepository.get_library_by_id(lib_id)
        if not library:
            return Responses.error_response("Library not found", 404)

        try:
            LibraryRepository.update_library(
                lib_id,
                data.get('lib_name'),
                data.get('lib_location'),
                data.get('lib_admin')
            )
            return Responses.success_response("Library updated successfully", None)
        except Exception as e:
            return Responses.error_response(str(e), 500)

    # User Management Methods
    @staticmethod
    def verify_user(user_id):
        user = UserRepository.get_user_by_id(user_id)
        if not user:
            return Responses.error_response("User not found", 404)
        try:
            UserRepository.verify_user(user_id, 'verified')
            return Responses.success_response("User verified successfully", None)
        except Exception as e:
            return Responses.error_response(str(e), 500)

    @staticmethod
    def delete_user(user_id):
        user = UserRepository.get_user_by_id(user_id)
        if not user:
            return Responses.error_response("User not found", 404)
        try:
            UserRepository.delete_user(user_id)
            return Responses.success_response("User deleted successfully", None)
        except Exception as e:
            return Responses.error_response(str(e), 500)

    # Library Settings Methods
    @staticmethod
    def update_book_limit(lib_id, new_limit):
        library = LibraryRepository.get_library_by_id(lib_id)
        if not library:
            return Responses.error_response("Library not found", 404)
        try:
            LibraryRepository.update_book_limit(lib_id, new_limit)
            return Responses.success_response("Book limit updated successfully", None)
        except Exception as e:
            return Responses.error_response(str(e), 500)

    @staticmethod
    def update_fine_rate(lib_id, daily_rate):
        library = LibraryRepository.get_library_by_id(lib_id)
        if not library:
            return Responses.error_response("Library not found", 404)
        if daily_rate < 0:
            return Responses.error_response("Fine rate cannot be negative", 400)
        try:
            LibraryRepository.update_fine_rate(lib_id, daily_rate)
            return Responses.success_response("Fine rate updated successfully", None)
        except Exception as e:
            return Responses.error_response(str(e), 500)
