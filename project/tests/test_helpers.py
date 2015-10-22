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
        return self.client.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def remove_test_user(self, email):
        accounts = self.application.accounts.search({
            'email': email
        })
        href = ""
        for account in accounts:
            if account.email == email:
                href = account.href
                test_user = self.sp_client.accounts.get(href)
                test_user.delete()

    def remove_test_user_tenant_group(self, email):
        groups = self.application.groups.search({
            'description': email
        })
        href = ""
        for group in groups:
            if group.description == email:
                href = group.href
                test_user_group = self.sp_client.groups.get(href)
                test_user_group.delete()
