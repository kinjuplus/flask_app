import os

# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DATABASE_CONNECT_OPTIONS = {}

    # Turn off Flask-SQLAlchemy event system
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    JSON_AS_ASCII = False
    JSONIFY_MIMETYPE = 'application/json;charset=utf-8'
    # Application threads. A common general assumption is
    # using 2 per available processor cores - to handle
    # incoming requests using one and performing background
    # operations using the other.
    THREADS_PER_PAGE = 2

    # Enable protection agains *Cross-site Request Forgery (CSRF)*
    WTF_CSRF_ENABLED = True

    # Use a secure, unique and absolutely secret key for
    # signing the data.
    CSRF_SESSION_KEY = os.getenv('CSRF_SESSION_KEY')

    # Secret key for signing cookies
    if os.environ.get('SECRET_KEY'):
        SECRET_KEY = os.environ.get('SECRET_KEY')
    else:
        SECRET_KEY = 'SECRET'

    # for email with sendgrid
    SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
    SENDGRID_DEFAULT_FROM = 'admin@yourdomain.com'

    @staticmethod
    def init_app(app):
        pass
    


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')


class DevelopmentConfig(Config):
    """Statement for enabling the development environment"""
    # Define the database - we are working with
    oracle_connection_string = 'oracle+cx_oracle://{username}:{password}@{hostname}:{port}/{database}'
    ENV = 'development'
    DEBUG = True
    PSM_DB_USER_NAME = 'psm_ap'
    PSM_DB_USER_PWD = 'tpsmap'
    PSM_DB_HOST = 'tnvttncombdb.cminl.oa'
    PSM_DB_PORT = 1521
    PSM_DB_SID = 'ttncomb'

    PLMDE_DB_USER_NAME = 'pdm_int_admin'
    PLMDE_DB_USER_PWD = 'tpdmintadmin'
    PLMDE_DB_HOST = 'tnvtinnoplmdb.cminl.oa'
    PLMDE_DB_PORT = 1521
    PLMDE_DB_SID = 'tinnoplm'
    SQLALCHEMY_ECHO = True

    SQLALCHEMY_BINDS = {
        'psm': oracle_connection_string.format(
                username= PSM_DB_USER_NAME,
                password= PSM_DB_USER_PWD,
                hostname=PSM_DB_HOST,
                port='1521',
                database=PSM_DB_SID,
            ),
        'plmde': oracle_connection_string.format(
                username= PLMDE_DB_USER_NAME,
                password= PLMDE_DB_USER_PWD,
                hostname=PLMDE_DB_HOST,
                port='1521',
                database=PLMDE_DB_SID,
           )   
    }


class APIConfig(Config):
    """Statement for enabling the api environment"""
    # Define the database - we are working with
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'dev.db')
    WTF_CSRF_ENABLED = False


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'test.db')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'api': APIConfig,
}