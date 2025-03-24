from app.middleware.db import db
from app.models import Libraries, User
from app.enums import LibraryStatusEnum

class LibraryRepository:

    @staticmethod
    def addLibrary(lib_name, lib_address, lib_admin, lib_license, lib_docs, lib_email):
        try:
            new_library = Libraries(
                lib_name=lib_name,
                lib_address=lib_address,
                lib_admin=lib_admin,
                lib_license=lib_license,
                lib_docs=lib_docs,
                lib_email=lib_email,
                library_verified=LibraryStatusEnum.UNVERIFIED
            )
            db.session.add(new_library)
            db.session.commit()
            return new_library
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def getAllLibraries():
        return Libraries.query.all()
    
    @staticmethod
    def getLibraryById(lib_id):
        return Libraries.query.get(lib_id)

    @staticmethod
    def getLibraryByName(lib_name):
        return Libraries.query.filter(Libraries.lib_name.ilike(f"%{lib_name}%")).first()

    @staticmethod
    def getLibraryByEmail(lib_email):
        return Libraries.query.filter_by(lib_email=lib_email).first()


    @staticmethod
    def getVerifiedlibraries():
        return Libraries.query.filter_by(library_verified=LibraryStatusEnum.VERIFIED).all()
    
    @staticmethod
    def checkLibraryUsers(lib_id):
        library = LibraryRepository.getLibraryByid(lib_id) 
        if not library:
            return {"message":"Library not found"}
        users = User.query.filter_by(lib_id=lib_id).all()
        if not users:
            return{"message": "The library has no users"}
        else:
            return users

    @staticmethod
    def updateLibrary(lib_id, **kwargs):
        try:
            with db.session.begin():
                library = Libraries.query.get(lib_id)
                if library:
                
                    allowed_fields = [
                        'lib_name', 'lib_address', 'lib_admin', 'lib_license', 
                        'lib_docs', 'lib_email', 'library_verified'
                    ]
                    
                    for key, value in kwargs.items():
                        if key in allowed_fields and hasattr(library, key):
                            setattr(library, key, value)
                    
                    db.session.commit()
                    return library
                else:
                    return {"message": "Library not found"}
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def deleteLibrary(lib_id):
        try:
            library = Libraries.query.get(lib_id)
            if not library:
                return {"message": "Library not found"}
            else:
                db.session.delete(library)
                db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
