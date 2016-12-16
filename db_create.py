from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI as DB_URI
from config import SQLALCHEMY_MIGRATE_REPO as MIGRATE_REPO
from app import db
import os.path

db.create_all()
if not os.path.exists(MIGRATE_REPO):
    api.create(MIGRATE_REPO, 'database repository')
    api.version_control(DB_URI, MIGRATE_REPO)
else:
    api.version_control(DB_URI, MIGRATE_REPO, api.version(MIGRATE_REPO))
