import os
basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

##
# Database settings
##
DB_HOST = 'localhost'
DB_NAME = 'helptux'
DB_USER = 'helptux'
DB_PASS = 'pass'

##
# Flask-WTF
##
WTF_CSRF_ENABLED = True
SECRET_KEY = 'Zsfdcss7tSpmCTgnsoOmSEdQkfvk55ht6WB2zVDLcivKb4ekSbqYI4bsMmy1yGM'
WTF_CSRF_SECRET_KEY = SECRET_KEY

##
# Babel
##
BABEL_DEFAULT_LOCALE = 'en'
BABEL_DEFAULT_TIMEZONE = 'UTC'

##
# Debug settings
##
if DEBUG is True:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
else:
    SQLALCHEMY_DATABASE_URI = 'mysql://{user}:{passw}@{host}/{db}'.format(user=DB_USER, passw=DB_PASS, host=DB_HOST,
                                                                          db=DB_NAME)
