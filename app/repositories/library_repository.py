from utils.db import db
from models.libraries_model import Libraries, Location


class LibraryRepository:

    @staticmethod
    def get_all_libraries():
        return Libraries.query.all()
    
    @staticmethod
    def get_library_by_id(lib_id):
        return Libraries.query.get(lib_id)
    
    @staticmethod
    def get_library_by_name(lib_name):
        return Libraries.query.filter_by(lib_name=lib_name).first()
    
    @staticmethod
    def get_library_by_email(lib_email):
        return Libraries.query.filter_by(lib_email=lib_email).first()
    
    @staticmethod
    def add_library(lib_name, lib_location, lib_admin, lib_licence, lib_docs, lib_email):
        new_library = Libraries(lib_name=lib_name, lib_location=lib_location, lib_admin=lib_admin, lib_licence=lib_licence, lib_docs=lib_docs, lib_email=lib_email)
        db.session.add(new_library)
        db.session.commit()

    @staticmethod
    def update_library(lib_id, lib_name, lib_location, lib_admin, lib_licence):
        library = Libraries.query.get(lib_id)
        library.lib_name = lib_name
        library.lib_location = lib_location
        library.lib_admin = lib_admin
        library.lib_licence = lib_licence
        db.session.commit()
    @staticmethod
    def delete_library(lib_id):
        library = Libraries.query.get(lib_id)
        db.session.delete(library)
        db.session.commit()

    @staticmethod
    def add_location(lib_id, block, floor, room, locker, rack):
        new_location = Location(lib_id=lib_id, block=block, floor=floor, room=room, locker=locker, rack=rack)
        db.session.add(new_location)
        db.session.commit()

    def delete_location(loc_id):
        location = Location.query.get(loc_id)
        db.session.delete(location)
        db.session.commit()