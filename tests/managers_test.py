import unittest, random, django, mox
from d51_django_db.managers import *

def connection_mocker(name):
    return "connection with %s" % name

class StubQuerySet(object):
    'Used for testing return of get_query_set()'
    def __init__(*args, **kwargs):
        pass

class StubQuery(object):
    'Used for testing return of get_query()'
    def __init__(*args, **kwargs):
        pass

class TestOfSpecificDatabaseManager(unittest.TestCase):
    def setUp(self):
        self.mox = mox.Mox()
        self.settings = self.mox.CreateMock(django.conf.LazySettings)
        self.settings.DATABASES = {}

    def tearDown(self):
        self.mox.UnsetStubs()

    def testRequiresDatabaseAsParameter(self):
        try:
            db = SpecificDatabaseManager()
            self.fail('should not have made it here')
        except TypeError, e:
            self.assertEqual(str(e), '__init__() takes at least 2 arguments (1 given)')

    def testDatabaseParamterIsSetOnManager(self):
        name = 'foobar %d' % random.randint(1, 100)
        db = SpecificDatabaseManager(name)
        self.assertEqual(db.database, name)

    def testDefaultsToTrueForUseForRelatedFields(self):
        self.assertTrue(SpecificDatabaseManager('foo').use_for_related_fields)

    def testGetConnectionRaisesErrorIfMissingConfig(self):
        db = SpecificDatabaseManager('foo')
        try:
            db.get_connection()
            self.fail('should not have made it here')
        except ImproperlyConfigured, e:
            self.assertEqual(str(e), 'Missing the DATABASES configuration value')

    def testCanTakeASettingsParameter(self):
        random_setting = random.randint(1, 100)
        db = SpecificDatabaseManager('foo', settings=random_setting);
        self.assertEqual(db.settings, random_setting)

    def testDefaultsToDjangoLazySettingsOtherwise(self):
        db = SpecificDatabaseManager('foo')
        self.assertEqual(db.settings.__class__, django.conf.LazySettings)

    def testGetConnectionReturnsConnectionWhenConfiguredProperly(self):
        db = SpecificDatabaseManager('foo', settings=self.settings, connection_factory=connection_mocker)
        self.assertEqual(db.get_connection(), "connection with foo")


    def testQuerySetAttributeEqualToKeywordValuePassedIn(self):
        query_set = 'random_query_set_%d' % random.randint(1, 100)
        db = SpecificDatabaseManager('foo', query_set=query_set)
        self.assertEqual(db.query_set, query_set)

    def testDefaultsToDjangoQuerySet(self):
        db = SpecificDatabaseManager('foo')
        self.assertEqual(db.query_set, django.db.models.query.QuerySet)

    def testReturnsQuerySet(self):
        db = SpecificDatabaseManager('foo',
            settings=self.settings,
            connection_factory=connection_mocker,
            query_set=StubQuerySet
        )
        self.assertEqual(db.get_query_set().__class__, StubQuerySet)

    def testQueryAttributeEqualToKeywordValuePassedIn(self):
        query = 'random_query_%d' % random.randint(1, 100)
        db = SpecificDatabaseManager('foo', query=query)
        self.assertEqual(db.query, query)

    def testQueryDefaultsToDjangoQuery(self):
        db = SpecificDatabaseManager('foo')
        self.assertEqual(db.query, django.db.models.sql.query.BaseQuery)

    def testGetQueryReturnsQueryObject(self):
        db = SpecificDatabaseManager(
            'foo',
            settings=self.settings,
            connection_factory=connection_mocker,
            query=StubQuery
        )
        self.assertEqual(db.get_query().__class__, StubQuery)

def get_suites():
    return unittest.TestSuite([
        unittest.defaultTestLoader.loadTestsFromTestCase(TestOfSpecificDatabaseManager),
    ])

if __name__ == '__main__':
    unittest.main()
