from app.utils.db import db
from app.models.libraries_model import Libraries, Racks


class LibraryRepository:

    @staticmethod
    def add_library(lib_name, lib_address, lib_admin, lib_license, lib_docs, lib_email):
        try:
            new_library = Libraries(
                lib_name=lib_name,
                lib_address=lib_address,
                lib_admin=lib_admin,
                lib_license=lib_license,
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
    def get_library_by_id(lib_id):
        return Libraries.query.get(lib_id)

    @staticmethod
    def get_library_by_name(lib_name):
        return Libraries.query.filter(Libraries.lib_name.ilike(f"%{lib_name}%")).first()

    @staticmethod
    def get_library_by_email(lib_email):
        return Libraries.query.filter_by(lib_email=lib_email).first()

    @staticmethod
    def get_all_libraries():
        return Libraries.query.all()

    @staticmethod
    def library_exists(lib_id):
        return Libraries.query.filter_by(lib_id=lib_id).first() is not None

    @staticmethod
    def update_library(lib_id, **kwargs):
        try:
            with db.session.begin():
                library = Libraries.query.get_or_404(lib_id)
                
                allowed_fields = [
                    'lib_name', 'lib_address', 'lib_admin', 'lib_license', 
                    'lib_docs', 'lib_email', 'library_verified'
                ]
                
                for key, value in kwargs.items():
                    if key in allowed_fields and hasattr(library, key):
                        setattr(library, key, value)
                
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


class RacksRepository:

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

    @staticmethod
    def update_rack(rack_id, **kwargs):
        try:
            with db.session.begin():
                rack = Racks.query.get_or_404(rack_id)
                
                allowed_fields = [
                    'block', 'floor', 'room', 'locker', 'rack_no'
                ]
                
                for key, value in kwargs.items():
                    if key in allowed_fields and hasattr(rack, key):
                        setattr(rack, key, value)
                
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
    def get_books_in_rack(rack_id):
        return Racks.query.get(rack_id).books