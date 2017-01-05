import imp
from migrate.versioning import api
from app import db
from config import SQLALCHEMY_DATABASE_URI as DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO as MIGRATE_REPO

v = api.db_version(DATABASE_URI, MIGRATE_REPO)
migration = MIGRATE_REPO + ('/versions/%03d_migration.py' % (v + 1))
tmp_module = imp.new_module('old_model')
old_model = api.create_model(DATABASE_URI, MIGRATE_REPO)
exec(old_model, tmp_module.__dict__)
script = api.make_update_script_for_model(DATABASE_URI, MIGRATE_REPO, tmp_module.meta, db.metadata) # noqa
open(migration, "wt").write(script)
api.upgrade(DATABASE_URI, MIGRATE_REPO)
v = api.db_version(DATABASE_URI, MIGRATE_REPO)
print('New migrations saved as', migration)
print('Current database version', str(v))
