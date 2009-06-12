from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import connection, models
from django.db.models import sql, query

class SpecificDatabaseManager(models.Manager):
    _connection = None

    def __init__(self, database, *args, **kwargs):
        self.database = database
        super(SpecificDatabaseManager, self).__init__(*args, **kwargs)

    def get_query_set(self):
        return query.QuerySet(self.model, self.create_query())

    def create_query(self):
        return sql.Query(self.model, self.get_connection())

    def get_connection(self):
        if self._connection is None:
            if not hasattr(settings, 'DATABASES'):
                raise ImproperlyConfigured('Missing the DATABASES configuration value')

            self._connection = self.create_custom_db()
        return self._connection

    def create_custom_db(self):
        if not settings.DATABASES.has_key(self.database):
            raise ImproperlyConfigured('Unable to locate configuration for %s' % self.database)

        database_conf = settings.DATABASES[self.database]
        to_import = 'django.db.backends.' + database_conf['DATABASE_ENGINE'] + '.base'
        backend = __import__(to_import, {}, {}, ['base'])
        return backend.DatabaseWrapper(database_conf)


