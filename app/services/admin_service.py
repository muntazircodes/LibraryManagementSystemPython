from app.utils.responses import Responses
from app.utils.validators import Validators
from app.utils.db import db


from app.repositories.library_repository import LibraryRepository, LocationRepository

class AdminService:
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
    def create_library(lib_data):
        try:
            if not Validators.validate_email(lib_data.get('lib_email')):
                return Responses.validation_error({"email": "Invalid email format"})
            
            if not Validators.validate_name(lib_data.get('lib_name')):
                return Responses.validation_error({"name": "Invalid library name"})
            
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
    def get_library_locations(lib_id):
        try:
            library = LibraryRepository.get_library_by_id(lib_id)
            if not library:
                return Responses.not_found("Library")
            
            locations = LocationRepository.get_locations_by_library(lib_id)
            return Responses.success("Locations retrieved successfully", locations)
        except Exception as e:
            return Responses.server_error()