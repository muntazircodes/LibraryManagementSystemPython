from datetime import timedelta
import dotenv
from os import environ

env = dotenv.load_dotenv()

DB_HOST = environ.get('DB_HOST')
DB_USER = environ.get('DB_USER')
DB_PASSWORD = environ.get('DB_PASSWORD')
DB_NAME = environ.get('DB_NAME')
PORT = int(environ.get('PORT'))
HOST = environ.get('HOST')

class Config:
    SECRET_KEY = environ.get('SECRET_KEY')
    JWT_SECRET_KEY = environ.get('JWT_SECRECT_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)



    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False