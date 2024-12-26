from app.utils.db import db
from app.models.libraries_model import Libraries, Location


class LibraryRepository:

    @staticmethod
    def add_library(lib_name, lib_location, lib_admin, lib_licence, lib_docs, lib_email):
        try:
            new_library = Libraries(
                lib_name=lib_name,
                lib_location=lib_location,
                lib_admin=lib_admin,
                lib_licence=lib_licence,
                lib_docs=lib_docs,
                lib_email=lib_email,
                library_verified=False
            )
            db.session.add(new_library)
            db.session.commit()
            return new_library
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def update_library(lib_id, lib_name, lib_location, lib_admin):
        try:
            library = Libraries.query.get(lib_id)
            if not library:
                raise ValueError("Library not found")
            library.lib_name = lib_name
            library.lib_location = lib_location
            library.lib_admin = lib_admin
            db.session.commit()
            return library
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete_library(lib_id):
        try:
            library = Libraries.query.get(lib_id)
            if not library:
                raise ValueError("Library not found")
            db.session.delete(library)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_all_libraries():
        return Libraries.query.all()
    
    @staticmethod
    def get_library_by_id(lib_id):
        return Libraries.query.get(lib_id)
    
    @staticmethod
    def get_library_by_name(lib_name):
        return Libraries.query.filter(Libraries.lib_name.ilike(f"%{lib_name}%")).first()
    
    @staticmethod
    def get_library_by_email(lib_email):
        return Libraries.query.filter_by(lib_email=lib_email).first()


class LocationRepository:
    @staticmethod
    def get_location_by_id(loc_id):
        return Location.query.get(loc_id)
    
    @staticmethod
    def get_locations_by_library(lib_id):
        return Location.query.filter_by(lib_id=lib_id).all()
    
    @staticmethod
    def add_location(lib_id, block, floor, room, locker, rack):
        try:
            new_location = Location(
                lib_id=lib_id,
                block=block,
                floor=floor,
                room=room,
                locker=locker,
                rack=rack
            )
            db.session.add(new_location)
            db.session.commit()
            return new_location
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def update_location(loc_id, block, floor, room, locker, rack):
        try:
            location = Location.query.get(loc_id)
            if not location:
                raise ValueError("Location not found")
            location.block = block
            location.floor = floor
            location.room = room
            location.locker = locker
            location.rack = rack
            db.session.commit()
            return location
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete_location(loc_id):
        try:
            location = Location.query.get(loc_id)
            if not location:
                raise ValueError("Location not found")
            db.session.delete(location)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

class LocationRepository:
    @staticmethod
    def get_location_by_id(loc_id):
        return Location.query.get(loc_id)
    
    @staticmethod
    def get_locations_by_library(lib_id):
        return Location.query.filter_by(lib_id=lib_id).all()
    
    @staticmethod
    def add_location(lib_id, block, floor, room, locker, rack):
        try:
            new_location = Location(
                lib_id=lib_id,
                block=block,
                floor=floor,
                room=room,
                locker=locker,
                rack=rack
            )
            db.session.add(new_location)
            db.session.commit()
            return new_location
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def update_location(loc_id, block, floor, room, locker, rack):
        try:
            location = Location.query.get(loc_id)
            if not location:
                raise ValueError("Location not found")
            location.block = block
            location.floor = floor
            location.room = room
            location.locker = locker
            location.rack = rack
            db.session.commit()
            return location
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete_location(loc_id):
        try:
            location = Location.query.get(loc_id)
            if not location:
                raise ValueError("Location not found")
            db.session.delete(location)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e