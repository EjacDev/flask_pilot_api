import os
from sqlalchemy.engine import URL
basedir = os.path.abspath(os.path.dirname(__file__))


class Settings(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ['SECRET_KEY']

    url_object = URL.create(
        ""+os.environ['DATABASE_DRIVER']+"",
        username=os.environ['DATABASE_USER'],
        password=os.environ['DATABASE_PASS'],
        host=os.environ['DATABASE_URL'],
        database=os.environ['DATABASE_NAME'],
    )
    SQLALCHEMY_DATABASE_URI = url_object
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    #Zip code API
    ZIPCODE_API_URL = 'https://www.zipcodeapi.com/rest/'
    ZIPCODE_API_KEY = 'X84CyGx7w2EzHMACQ4WN2d6tpnm9sCIYVADVBIu1XjlqjJW4V7xWrtACBF0MtpZm'



class ProductionConfig(Settings):
    DEBUG = False


class StagingConfig(Settings):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Settings):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Settings):
    TESTING = True