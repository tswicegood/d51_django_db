d51_django_specificdb
=====================
Custom manager for Django that allows specific databases to be used.

This work stands firmly on the shoulders of giants:
    http://www.eflorenzano.com/blog/post/easy-multi-database-support-django/
    http://github.com/mmalone/django-multidb


Usage
-----
Import this code, then specify a custom manager for your model:

    objects = SpecificDatabaseManager('secondary')

In your settings.py file, you need to specify the database that you want to use
as part of the DATABASES variable:

    DATABASES = {
        'secondary': {
            'DATABASE_ENGINE': 'mysql',
            'DATABASE_NAME': 'secondary_db',
            'DATABASE_USER': 'some_user',
            'DATABASE_PASSWORD': 'shh',
            'DATABASE_OPTIONS': '',
            'DATABASE_HOST': '',
            'DATABASE_PORT': '',
        }
    }

The values work just like various DATABASE_* values in a normal settings.py file.

