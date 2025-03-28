from app.middleware import db, Responses, Validators
from app.enums import UserStatusEnum, LibraryStatusEnum
from app.repositories import (
    UserRepository,
    LibraryRepository,
    RacksRepository,
    BorrowRepository,
)


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
                "lib_name",
                "lib_email",
                "lib_address",
                "lib_admin",
                "lib_license",
                "lib_docs",
            ]

            existing_library = LibraryRepository.getLibraryByEmail(
                lib_data.get("lib_email")
            )
            if existing_library:
                return Responses.conflict("Library with this email already exists")

            new_library_data = {
                field: lib_data.get(field) for field in allowed_fields
            }
            return Validators.handle_repository_action(
                LibraryRepository.addLibrary, **new_library_data
            )
        except Exception:
            return Responses.server_error()

    @staticmethod
    def register_user(user_data):
        try:
            allowed_fields = [
                "user_name",
                "user_email",
                "user_password",
                "lib_id",
                "phone_number",
                "valid_docs",
            ]

            existing_user = UserRepository.getUserByEmail(user_data.get("user_email"))
            if existing_user:
                return Responses.conflict("User with this email already exists")

            if not LibraryRepository.getLibraryById(user_data.get("lib_id")):
                return Responses.not_found("Library")

            new_user_data = {field: user_data.get(field) for field in allowed_fields}
            return Validators.handle_repository_action(
                UserRepository.addUser, **new_user_data
            )
        except Exception:
            return Responses.server_error()

    @staticmethod
    def get_all_libraries():
        return Validators.handle_repository_action(LibraryRepository.getAllLibraries)

    @staticmethod
    def get_library(lib_id):
        return Validators.handle_repository_action(
            LibraryRepository.getLibraryById, lib_id
        )

    @staticmethod
    def get_verified_users():
        return Validators.handle_repository_action(UserRepository.getVerifiedUsers)

    @staticmethod
    def delete_library(lib_id):
        return Validators.handle_repository_action(
            LibraryRepository.deleteLibrary, lib_id
        )

    @staticmethod
    def get_user(user_id):
        return Validators.handle_repository_action(
            UserRepository.getUserById, user_id
        )

    @staticmethod
    def verify_library(lib_id):
        try:
            library = LibraryRepository.getVerifiedlibraries(lib_id)
            if not library:
                return Responses.not_found("Library")

            library.library_verified = LibraryStatusEnum.VERIFIED
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

            user.user_verified = UserStatusEnum.VERIFIED
            db.session.commit()
            return Validators.serialize_model(user)
        except Exception:
            return Responses.server_error()

    @staticmethod
    def promote_user(user_id):
        return Validators.handle_repository_action(
            UserRepository.promoteAsAdmin, user_id
        )

    @staticmethod
    def get_all_admins():
        return Validators.handle_repository_action(UserRepository.getAdmin)

    @staticmethod
    def get_defaulter_users():
        return Validators.handle_repository_action(UserRepository.get_defaulter_user)

    @staticmethod
    def track_user_fine(user_id):
        return Validators.handle_repository_action(
            UserRepository.checkUserFine, user_id
        )

    @staticmethod
    def check_user_borrowings(user_id):
        return Validators.handle_repository_action(
            BorrowRepository.getBorrowingById, user_id
        )

    @staticmethod
    def discard_user(user_id):
        return Validators.handle_repository_action(
            UserRepository.deleteUser, user_id
        )

    @staticmethod
    def update_racks(rack_id):
        return Validators.handle_repository_action(
            RacksRepository.updateRack, rack_id
        )
