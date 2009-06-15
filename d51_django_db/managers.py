from django import conf
from django.core.exceptions import ImproperlyConfigured
from django.db import connection, models
from django.db.models import sql, query
from d51_django_db import create_custom_db_connection

class SpecificDatabaseManager(models.Manager):
    _connection = None

    def __init__(self,
                 database,
                 settings=conf.settings,
                 connection_factory=create_custom_db_connection,
                 query_set=query.QuerySet,
                 query=sql.Query,
                 *args, **kwargs):
        self.database = database
        self.use_for_related_fields = True
        self.settings = settings
        self.connection_factory = connection_factory
        self.query_set = query_set
        self.query = query
        super(SpecificDatabaseManager, self).__init__(*args, **kwargs)

    def get_query_set(self):
        return self.query_set(self.model, self.get_query())

    def get_query(self):
        return self.query(self.model, self.get_connection())

    def get_connection(self):
        if self._connection is None:
            if not hasattr(self.settings, 'DATABASES'):
                raise ImproperlyConfigured('Missing the DATABASES configuration value')

            self._connection = self.connection_factory(self.database)
        return self._connection


