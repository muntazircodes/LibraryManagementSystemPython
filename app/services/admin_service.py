from app.utils.responses import Responses
from app.utils.validators import Validators
from app.utils.db import db
from app.repositories.user_repository import UserRepository, ReportRepository
from app.repositories.library_repository import LibraryRepository, RacksRepository
from app.repositories.book_repository import CopiesRepository, BorrowRepository


class AdminService:

    @staticmethod
    def validate_and_serialize(data, validators):
        for field, validator in validators.items():
            if not validator(data.get(field)):
                return field
        return None


    @staticmethod
    def register_library(lib_data):
        try:
            allowed_fields = [
                'lib_name', 'lib_email', 'lib_address',
                'lib_admin', 'lib_license', 'lib_docs'
            ]
            existing_library = LibraryRepository.get_library_by_email(lib_data.get('lib_email'))
            if existing_library:
                return Responses.conflict("Library with this email already exists")

            new_library_data = {field: lib_data.get(field) for field in allowed_fields}
            return Validators.handle_repository_action(LibraryRepository.add_library, **new_library_data)
        except Exception:
            return Responses.server_error()


    @staticmethod
    def register_user(user_data):
        try:
            allowed_fields = [
                'user_name', 'user_email', 'user_password',
                'lib_id', 'phone_number', 'valid_docs'
            ]
            existing_user = UserRepository.get_user_by_email(user_data.get('user_email'))
            if existing_user:
                return Responses.conflict("User with this email already exists")

            if not LibraryRepository.library_exists(user_data.get('lib_id')):
                return Responses.not_found("Library")

            new_user_data = {field: user_data.get(field) for field in allowed_fields}
            return Validators.handle_repository_action(UserRepository.add_user, **new_user_data)
        except Exception:
            return Responses.server_error()
        

    @staticmethod
    def get_all_libraries():
        return Validators.handle_repository_action(LibraryRepository.get_all_libraries)


    @staticmethod
    def get_library(lib_id):
        return Validators.handle_repository_action(LibraryRepository.get_library_by_id, lib_id)
    

    @staticmethod
    def get_unverified_libraries():
        return Validators.handle_repository_action(LibraryRepository.get_unverified_libraries)
    
    @staticmethod
    def get_unverified_users():
        return Validators.handle_repository_action(UserRepository.get_unverified_users)

    @staticmethod
    def delete_library(lib_id):
        return Validators.handle_repository_action(LibraryRepository.delete_library, lib_id)

    @staticmethod
    def get_user(user_id):
        return Validators.handle_repository_action(UserRepository.get_user_by_id, user_id)
    @staticmethod
    def verify_library(lib_id):
        try:
            library = LibraryRepository.get_library_by_id(lib_id)
            if not library:
                return Responses.not_found("Library")
            library.library_verified = True
            db.session.commit()
            return Validators.serialize_model(library)
        except Exception:
            return Responses.server_error()
        
    
    @staticmethod
    def verify_user(user_id):
        try:
            user = UserRepository.get_user_by_id(user_id)
            if not user:
                return Responses.not_found("The user not found")
            user.user_verified = True
            db.session.commit()
            return Validators.serialize_model(user)
        except Exception:
            return Responses.server_error()


    @staticmethod
    def promote_user(user_id):
        return Validators.handle_repository_action(UserRepository.promote_as_admin, user_id)


    @staticmethod
    def get_all_admins():
        return Validators.handle_repository_action(UserRepository.get_admin)


    @staticmethod
    def get_defaulter_users():
        return Validators.handle_repository_action(UserRepository.get_defaulter_user)


    @staticmethod
    def track_user_fine(user_id):
        return Validators.handle_repository_action(UserRepository.check_user_fine, user_id)


    @staticmethod
    def check_user_borrowings(user_id):
        return Validators.handle_repository_action(BorrowRepository.get_borrowings_by_user_id, user_id)


    @staticmethod
    def check_copy_status(copy_id):
        return Validators.handle_repository_action(CopiesRepository.get_copies_by_book_id, copy_id)


    @staticmethod
    def calculate_and_manage_user_fine(user_id):
        try:
            user = UserRepository.get_user_by_id(user_id)
            if not user:
                return Responses.not_found("User")
            fine = UserRepository.calculate_fine(user_id)
            user.user_fine = fine
            db.session.commit()
            response_data = Validators.serialize_model(user)
            response_data['fine'] = fine
            return Responses.success(response_data) if fine else Responses.success("No fine for this user")
        except Exception:
            return Responses.server_error()


    @staticmethod
    def discard_user(user_id):
        return Validators.handle_repository_action(UserRepository.delete_user, user_id)


    @staticmethod
    def check_and_update_reports(report_id, report_data):
        try:
            report = ReportRepository.get_report_by_id(report_id)
            if not report:
                return Responses.not_found("Report")
            ReportRepository.mark_report_handled(report_id, report_data.get('handled_by'))
            db.session.commit()
            return Validators.serialize_model(report)
        except Exception:
            return Responses.server_error()


    @staticmethod
    def update_racks(rack_id):
        return Validators.handle_repository_action(RacksRepository.update_rack, rack_id)

