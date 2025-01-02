from app.utils.db import db
from app.models.libraries_model import Libraries, Racks


class LibraryRepository:

    @staticmethod
    def add_library(lib_name, lib_adress, lib_admin, lib_licence, lib_docs, lib_email):
        try:
            new_library = Libraries(
                lib_name=lib_name,
                lib_adress=lib_adress,
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
    def update_library(lib_id, lib_name, lib_adress, lib_admin):
        try:
            library = Libraries.query.get(lib_id)
            if not library:
                raise ValueError("Library not found")
            library.lib_name = lib_name
            library.lib_adress = lib_adress
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
    
    @staticmethod
    def library_exists(lib_id):
        return Libraries.query.filter_by(lib_id=lib_id).first() is not None


class RacksRepository:

    @staticmethod
    def get_rack_by_id(rack_id):
        return Racks.query.get(rack_id)
    
    @staticmethod
    def get_racks_by_library(lib_id):
        return Racks.query.filter_by(lib_id=lib_id).all()
    
    @staticmethod
    def add_rack(lib_id, block, floor, room, locker, rack_no):
        try:
            new_rack = Racks(
                lib_id=lib_id,
                block=block,
                floor=floor,
                room=room,
                locker=locker,
                rack_no=rack_no
            )
            db.session.add(new_rack)
            db.session.commit()
            return new_rack
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def update_rack(rack_id, block, floor, room, locker, rack_no):
        try:
            rack = Racks.query.get(rack_id)
            if not rack:
                raise ValueError("Racks not found")
            rack.block = block
            rack.floor = floor
            rack.room = room
            rack.locker = locker
            rack.rack_no = rack_no
            db.session.commit()
            return rack
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete_rack(rack_id):
        try:
            rack = Racks.query.get(rack_id)
            if not rack:
                raise ValueError("Racks not found")
            db.session.delete(rack)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_rack_by_id(rack_id):
        return Racks.query.get(rack_id)
    
    @staticmethod
    def get_racks_by_library(lib_id):
        return Racks.query.filter_by(lib_id=lib_id).all()
    
    @staticmethod
    def get_rack_by_block(lib_id, block):
        return Racks.query.filter_by(lib_id=lib_id, block=block).all()
    
    @staticmethod
    def get_rack_by_floor(lib_id, floor):
        return Racks.query.filter_by(lib_id=lib_id, floor=floor).all()
    
    @staticmethod
    def get_rack_by_room(lib_id, room):
        return Racks.query.filter_by(lib_id=lib_id, room=room).all()
    
    @staticmethod
    def get_rack_by_locker(lib_id, locker):
        return Racks.query.filter_by(lib_id=lib_id, locker=locker).all()
    
    @staticmethod
    def get_rack_by_rack_no(lib_id, rack_no):
        return Racks.query.filter_by(lib_id=lib_id, rack_no=rack_no).all()
    
    def get_books_in_rack(rack_id):
        return Racks.query.get(rack_id).books