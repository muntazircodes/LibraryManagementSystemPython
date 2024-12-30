from app.utils.responses import Responses
from app.utils.validators import Validators
from app.utils.db import db

from app.repositories.user_repository import UserRepository, ReportRepository
from app.repositories.library_repository import LibraryRepository, LocationRepository
from app.repositories.book_repository import CopiesRepository, BorrowRepository

from datetime import datetime


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

            LibraryRepository.add_library(
                lib_name=lib_data.get('lib_name'),
                lib_location=lib_data.get('lib_location'),
                lib_admin=lib_data.get('lib_admin'),
                lib_licence=lib_data.get('lib_licence'),
                lib_docs=lib_data.get('lib_docs'),
                lib_email=lib_data.get('lib_email')
            )

            return Responses.created("Library")
        except Exception as e:
            return Responses.server_error()
        

    @staticmethod
    def get_all_libraries():
        try:
            libraries = LibraryRepository.get_all_libraries()
            return Responses.success("Libraries retrieved", libraries)
        except Exception as e:
            return Responses.server_error()
        
    @staticmethod
    def get_library(lib_id):
        try:
            library = LibraryRepository.get_library_by_id(lib_id)
            if not library:
                return Responses.not_found("Library")
            return Responses.success("Library retrieved", library)
        except Exception as e:
            return Responses.server_error()
        
    @staticmethod
    def get_all_admins():
        try:
            admins = UserRepository.get_library_admin()
            return Responses.success("Admins retrieved", admins)
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

            return Responses.success("Library verified successfully")
        except Exception as e:
            return Responses.server_error()

    @staticmethod
    def register_user(user_data):
        try:
            if not Validators.validate_email(user_data.get('user_email')):
                return Responses.validation_error({"email": "Invalid email format"})

            if not Validators.validate_name(user_data.get('user_name')):
                return Responses.validation_error({"name": "Invalid user name"})

            existing_user = UserRepository.get_user_by_email(user_data.get('user_email'))
            if existing_user:
                return Responses.conflict("User with this email already exists")

            UserRepository.add_user(
                user_name=user_data.get('user_name'),
                user_email=user_data.get('user_email'),
                user_password=user_data.get('user_password'),
                user_type=user_data.get('user_type'),
                lib_id=user_data.get('lib_id')
            )
            return Responses.created("User")
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
            return Responses.success("User verified successfully")
        except Exception as e:
            return Responses.server_error()
        
    @staticmethod
    def verify_all_users():
        try:
            UserRepository.verify_all_at_once()
            return Responses.success("All users verified successfully")
        except Exception as e:
            return Responses.server_error()

    @staticmethod
    def get_defaulter_users():
        try:
            defaulter_users = UserRepository.get_defaulter_user()
            return Responses.success("Defaulter users retrieved", defaulter_users)
        except Exception as e:
            return Responses.server_error()

    @staticmethod
    def track_user_fine(user_id):
        try:
            user = UserRepository.get_user_by_id(user_id)
            if not user:
                return Responses.not_found("User")
            return Responses.success("User fine retrieved", {"fine": user.user_fine})
        except Exception as e:
            return Responses.server_error()

    @staticmethod
    def check_user_borrowings(user_id):
        try:
            borrowings = BorrowRepository.get_borrowings_by_user_id(user_id)
            return Responses.success("Borrowings retrieved", borrowings)
        except Exception as e:
            return Responses.server_error()

    @staticmethod
    def check_copy_status(copy_id):
        try:
            copy = CopiesRepository.get_copies_by_book_id(copy_id)
            return Responses.success("Copy status retrieved", copy)
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
            return Responses.success("User fine calculated and updated", {"fine": fine})
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
            return Responses.success("Report updated successfully")
        except Exception as e:
            return Responses.server_error()
        

    def update_location(loc_id):
        try:
            location = LocationRepository.get_location_by_id(loc_id)
            if not location:
                return Responses.not_found("Location")

            LocationRepository.update_location(loc_id)
            return Responses.success("Location updated successfully")
        except Exception as e:
            return Responses.server_error()
        