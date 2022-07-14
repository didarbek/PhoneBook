import os

basedir = os.path.abspath(os.path.dirname(__file__))

# writing down all the configs
# defining "SQLALCHEMY_DATABASE_URI" to connect to Postgresql database
# otherwise we use default sqlite database
class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite://")
    SQLALCHEMY_TRACK_MODIFICATIONS = False