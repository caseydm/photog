"""
Test helpers.
These utilities are meant to simplify our tests, and abstract away common test
operations.
"""

from os import environ
from unittest import TestCase
from views import app
from stormpath.client import Client


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

    def tearDown(self):
        pass

    def login(self, username, password):
        return self.sp_client.post('/login', data=dict(
            username=username,
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

    def remove_test_user(self, email):
        test_user = self.get_test_user(email)
        test_user.delete()

    def remove_test_user_tenant_group(self, email):
        test_user_group = self.get_test_user_group(email)
        test_user_group.delete()
