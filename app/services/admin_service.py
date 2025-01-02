from app.utils.responses import Responses
from app.utils.validators import Validators
from app.utils.db import db

from app.repositories.user_repository import UserRepository, ReportRepository
from app.repositories.library_repository import LibraryRepository, RacksRepository
from app.repositories.book_repository import CopiesRepository, BorrowRepository


class AdminService:

    @staticmethod
    def register_library(lib_data):
        try:
            if not Validators.validate_name(lib_data.get('lib_name')):
                return Responses.validation_error({"name": "Invalid library name"})

            if not Validators.validate_email(lib_data.get('lib_email')):
                return Responses.validation_error({"email": "Invalid email format"})

            existing_library = LibraryRepository.get_library_by_email(lib_data.get('lib_email'))

            if existing_library:
                return Responses.conflict("Library with this email already exists")

            new_library = LibraryRepository.add_library(
                lib_name=lib_data.get('lib_name'),
                lib_adress=lib_data.get('lib_adress'),
                lib_admin=lib_data.get('lib_admin'),
                lib_licence=lib_data.get('lib_licence'),
                lib_docs=lib_data.get('lib_docs'),
                lib_email=lib_data.get('lib_email')
            )
            return Validators.serialize_model(new_library)
        except Exception as e:
            return Responses.server_error()

    @staticmethod
    def get_all_libraries():
        try:
            libraries = LibraryRepository.get_all_libraries()
            if not libraries:
                return Responses.not_found("Libraries")
            serialized_libraries = [Validators.serialize_model(lib) for lib in libraries]
            return f"{serialized_libraries}\n {Responses.success("Libraries retrieved")}"
        except Exception as e:
            return Responses.server_error()

    @staticmethod
    def get_library(lib_id):
        try:
            library = LibraryRepository.get_library_by_id(lib_id)
            if not library:
                return Responses.not_found("Library")
            return Validators.serialize_model(library)
        except Exception as e:
            return Responses.server_error()

    @staticmethod
    def verify_library(lib_id):
        try:
            library = LibraryRepository.get_library_by_id(lib_id)
            if not library:
                return Responses.not_found("Library")

            library.library_verified = True
            db.session.commit()
            return Validators.serialize_model(library)
        except Exception as e:
            return Responses.server_error()


    @staticmethod
    def register_user(user_data):
        try:
            if not Validators.validate_email(user_data.get('user_email')):
                return Responses.validation_error({"email": "Invalid email format"})

            if not Validators.validate_name(user_data.get('user_name')):
                return Responses.validation_error({"name": "Invalid user name"})

            if not Validators.validate_password(user_data.get('user_password')):
                return Responses.validation_error({"password": "Invalid password format"})

            existing_user = UserRepository.get_user_by_email(user_data.get('user_email'))
            if existing_user:
                return Responses.conflict("User with this email already exists")

            hashed_password = Validators.hash_password(user_data.get('user_password'))

            new_user = UserRepository.add_user(
                user_name=user_data.get('user_name'),
                user_email=user_data.get('user_email'),
                user_password=hashed_password,
                user_type=user_data.get('user_type'),
                lib_id=user_data.get('lib_id')
            )

            return Validators.serialize_model(new_user)

        except Exception as e:
            return Responses.server_error()


    @staticmethod
    def verify_user(user_id):
        try:
            user = UserRepository.get_user_by_id(user_id)
            if not user:
                return Responses.not_found("User")

            user.user_verified = True
            db.session.commit()
            return Validators.serialize_model(user)
        except Exception as e:
            return Responses.server_error()

    @staticmethod
    def promote_user(user_id):
        try:
            user = UserRepository.get_user_by_id(user_id)
            if not user:
                return Responses.not_found("User")

            UserRepository.promote_user(user_id)
            return Validators.serialize_model(user)
        except Exception as e:
            return Responses.server_error()

    @staticmethod
    def get_all_admins():
        try:
            admins = UserRepository.get_library_admin()
            if not admins:
                return Responses.not_found("Admins")
            serialized_admins = [Validators.serialize_model(admin) for admin in admins]
            return f"{Responses.success("Admins retrieved")}\n {serialized_admins}"
        except Exception as e:
            return Responses.server_error()

    @staticmethod
    def get_defaulter_users():
        try:
            defaulter_users = UserRepository.get_defaulter_user()
            serialized_defaulters = [Validators.serialize_model(user) for user in defaulter_users]
            return f"{Responses.success("Defaulter users retrieved")}\n{serialized_defaulters})"
        except Exception as e:
            return Responses.server_error()

    @staticmethod
    def track_user_fine(user_id):
        try:
            user = UserRepository.get_user_by_id(user_id)
            if not user:
                return Responses.not_found("User")
            user_fine = Validators.serialize_model(user)
            return f"{Responses.success('User fine retrieved')}\n{user_fine}"
        except Exception as e:
            return Responses.server_error()

    @staticmethod
    def check_user_borrowings(user_id):
        try:
            borrowings = BorrowRepository.get_borrowings_by_user_id(user_id)
            serialized_borrowings = [Validators.serialize_model(borrowing) for borrowing in borrowings]
            return f"{Responses.success('User borrowings retrieved')}\n{serialized_borrowings}"
        except Exception as e:
            return Responses.server_error()

    @staticmethod
    def check_copy_status(copy_id):
        try:
            copy = CopiesRepository.get_copies_by_book_id(copy_id)
            serialized_copy = Validators.serialize_model(copy)
            return f"{Responses.success('Copy status retrieved')}\n{serialized_copy}"
        except Exception as e:
            return Responses.server_error()

    @staticmethod
    def calculate_and_manage_user_fine(user_id):
        try:
            user = UserRepository.get_user_by_id(user_id)
            if not user:
                return Responses.not_found("User")

            fine = UserRepository.calculate_fine(user_id)
            user.user_fine = fine
            db.session.commit()
            serialized_user = Validators.serialize_model(user)
            return f"{Responses.success('User fine calculated')}\n{ {"fine": fine, "user": serialized_user}}"
        except Exception as e:
            return Responses.server_error()

    @staticmethod
    def discard_user(user_id):
        try:
            user = UserRepository.get_user_by_id(user_id)
            if not user:
                return Responses.not_found("User")

            UserRepository.delete_user(user_id)
            return Responses.success("User discarded successfully")
        except Exception as e:
            return Responses.server_error()

    @staticmethod
    def check_and_update_reports(report_id, report_data):
        try:
            report = ReportRepository.get_report_by_id(report_id)
            if not report:
                return Responses.not_found("Report")

            ReportRepository.mark_report_handled(report_id, report_data.get('handled_by'))
            db.session.commit()
            serialized_report = Validators.serialize_model(report)
            return f"{Responses.success('Report updated successfully')}\n{serialized_report}"
        except Exception as e:
            return Responses.server_error()

    @staticmethod
    def update_racks(rack_id):
        try:
            rack = RacksRepository.get_rack_by_id(rack_id)
            if not rack:
                return Responses.not_found("Rack")

            RacksRepository.update_rack(rack_id)
            serialized_rack = Validators.serialize_model(rack)
            return f"{Responses.success('Rack updated successfully')}\n{serialized_rack}"
        except Exception as e:
            return Responses.server_error()
