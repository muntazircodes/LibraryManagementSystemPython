from app import db

# Library Model
class Libraries(db.Model):
    __tablename__ = 'libraries'

    lib_id = db.Column(db.Integer, primary_key=True)
    lib_name = db.Column(db.String(100), nullable=False)
    lib_location = db.Column(db.String(100), nullable=False)
    lib_admin = db.Column(db.String(100), nullable=False)
    lib_licence = db.Column(db.String(100), nullable=False)
    lib_docs = db.Column(db.String(100), nullable=False)
    lib_email = db.Column(db.String(100), nullable=False, unique=True)
    Library_verified = db.Column(db.Boolean, default=False, nullable=False)

    # Relationships
    books = db.relationship('Book', back_populates='library', cascade="all, delete-orphan")
    locations = db.relationship('Location', back_populates='library', cascade="all, delete-orphan")


class Location(db.Model):
    __tablename__ = 'location'

    loc_id = db.Column(db.Integer, primary_key=True)
    lib_id = db.Column(db.Integer, db.ForeignKey('libraries.lib_id'), nullable=False)
    block = db.Column(db.String(100), nullable=True)
    floor = db.Column(db.String(100), nullable=True)
    room = db.Column(db.String(100), nullable=True)
    locker = db.Column(db.String(100), nullable=True)
    rack = db.Column(db.String(100), nullable=True)

    # Relationships
    library = db.relationship('Libraries', back_populates='locations')
    copies = db.relationship('Copies', back_populates='location', cascade="all, delete-orphan")