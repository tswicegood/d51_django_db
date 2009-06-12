from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import connection, models
from django.db.models import sql, query
from d51_django_db import create_custom_db_connection

class SpecificDatabaseManager(models.Manager):
    _connection = None

    def __init__(self, database, *args, **kwargs):
        self.database = database
        self.use_for_related_fields = True
        super(SpecificDatabaseManager, self).__init__(*args, **kwargs)

    def get_query_set(self):
        return query.QuerySet(self.model, self.create_query())

    def create_query(self):
        return sql.Query(self.model, self.get_connection())

    def get_connection(self):
        if self._connection is None:
            if not hasattr(settings, 'DATABASES'):
                raise ImproperlyConfigured('Missing the DATABASES configuration value')

            self._connection = create_custom_db_connection(self.database)
        return self._connection


