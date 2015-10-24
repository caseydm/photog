"""
Test helpers.
These utilities are meant to simplify our tests, and abstract away common test
operations.
"""

from os import environ
from unittest import TestCase
from views import app
from stormpath.client import Client
from itsdangerous import URLSafeTimedSerializer


class PhotogTestCase(TestCase):

    def setUp(self):
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['TESTING'] = True
        app.config['STORMPATH_APPLICATION'] = 'photog_test'
        self.app = app
        self.client = app.test_client()

        # stormpath client
        self.sp_client = Client(
            id=environ.get('STORMPATH_API_KEY_ID'),
            secret=environ.get('STORMPATH_API_KEY_SECRET'),
        )

        # retrieve photog_test application instance
        href = 'https://api.stormpath.com/v1/applications/Nq2qQQegOh9a9qJRekxeA'
        self.application = self.sp_client.applications.get(href)

        self.test_email = 'test_user@photog.com'

        self.user = self.create_default_user()

    def tearDown(self):
        self.user.delete()
        group = self.get_test_user_group('test_user2@example.com')
        group.delete()

    def login(self, email, password):
        return self.client.post('/login', data=dict(
            login=email,
            password=password
        ), follow_redirects=True)

    def get_test_user(self, email):
        accounts = self.application.accounts.search({
            'email': email
        })
        for account in accounts:
            if account.email == email:
                return account

    def get_test_user_group(self, email):
        groups = self.application.groups.search({
            'description': email
        })
        for group in groups:
            if group.description == email:
                return group

    def create_token(self, email, tenant_id):
        ts = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        token = ts.dumps([email, tenant_id])
        return token

    def create_default_user(self):
        #user = self.application.accounts.create({
        user = self.application.accounts.create({
            'given_name': 'anonymous',
            'surname': 'anonymous',
            'email': 'test_user2@example.com',
            'password': '4P@$$w0rd!',
            "custom_data": {
                "tenant_id": "cf336120-25ef-4b01-8bb1-ba2b69213b71",
                "site_admin": True,
            }
        })

        directory = self.application.default_account_store_mapping.account_store
        
        tenant_group = directory.groups.create({
            'name': 'cf336120-25ef-4b01-8bb1-ba2b69213b71',
            'description': 'test_user2@example.com',
        })

        # assign new user to the newly created group
        user.add_group(tenant_group)
        user.add_group('site_admin')

        return user
