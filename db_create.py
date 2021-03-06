from migrate.versioning import api
from os.path import exists
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO
import helptux

##
# TODO: Update for MySQL
##

helptux.db.create_all()

if not exists(SQLALCHEMY_MIGRATE_REPO):
    api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
else:
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, api.version(SQLALCHEMY_MIGRATE_REPO))
