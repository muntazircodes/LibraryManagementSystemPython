from app.utils.db import db
from app.models import Racks

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
    def get_racks_by_filters(lib_id, **kwargs):
        filters = {'lib_id': lib_id}
        allowed_filters = ['block', 'floor', 'room', 'locker', 'rack_no']
        
        for key, value in kwargs.items():
            if key in allowed_filters:
                filters[key] = value
                
        return Racks.query.filter_by(**filters).all()

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