from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import connection

def create_custom_db_connection(name = None):
    if name is None:
        return connection
    if not settings.DATABASES.has_key(name):
        raise ImproperlyConfigured('Unable to locate configuration for %s' % name)

    database_conf = settings.DATABASES[name]
    to_import = 'django.db.backends.' + database_conf['DATABASE_ENGINE'] + '.base'
    backend = __import__(to_import, {}, {}, ['base'])
    return backend.DatabaseWrapper(database_conf)


