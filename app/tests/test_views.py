"""Run tests against our custom views."""

import mock
from test_helpers import PhotogTestCase


class TestRegister(PhotogTestCase):
    """Test our registration view."""

    def test_register_page_loads(self):
        # Page loads with correct text
        resp = self.client.get('/register')
        assert 'Register for an Account' in resp.data

    def test_register_bad_input(self):
        # Ensure that no password results in error
        resp = self.client.post('/register', data={
            'email': 'testuser@photog.com',
            'password': '',
            'password_again': '',
            })
        assert 'Register for an Account' in resp.data

        # Ensure that no email address results in error
        resp = self.client.post('/register', data={
            'email': '',
            'password': 'TempPass123',
            'password_again': 'TempPass123',
            })
        assert 'Register for an Account' in resp.data

    def test_register_valid_input(self):
        # Valid data results in success
        resp = self.client.post('/register', data={
            'email': self.test_email,
            'password': 'TempPass123',
            'password_again': 'TempPass123',
            }, follow_redirects=True)
        assert 'Dashboard' in resp.data

        # ensure user is member of UUID-generated group, and tenant_id matches
        test_user = self.get_test_user(self.test_email)
        test_user_group = self.get_test_user_group(self.test_email)
        self.assertEqual(test_user.custom_data['tenant_id'], test_user_group.name)

        # ensure user is member of site_admin group
        member_site_admin = False
        for group in test_user.groups:
            if group.name == 'site_admin':
                member_site_admin = True
        self.assertTrue(member_site_admin)

        # delete user and group used for testing
        test_user_group.delete()
        test_user.delete()


class TestAddUser(PhotogTestCase):
    """Test add user functionality"""

    def test_add_user_page_loads(self):
        self.login(self.user.email, '4P@$$w0rd!')

        # ensure page loads properly
        resp = self.client.get('/add_user')
        assert 'Add Team Member' in resp.data

    @mock.patch('app.accounts.views.sendgrid.SendGridClient.send')
    def test_add_user_bad_input(self, mocked_send):
        
        self.login(self.user.email, '4P@$$w0rd!')

        # set sendgrid method to none
        mocked_send.return_value = None

        # submit add_user page
        resp = self.client.post('/add_user', data={
                'email': ''
            }, follow_redirects=True)
        assert 'Add Team Member' in resp.data

    # mock our sendgrid method so it does not send emails in test
    @mock.patch('app.accounts.views.sendgrid.SendGridClient.send')
    def test_add_user_valid_input(self, mocked_send):

        self.login(self.user.email, '4P@$$w0rd!')
        
        # set sendgrid method to none
        mocked_send.return_value = None
        
        # submit add_user page
        resp = self.client.post('/add_user', data={
                'email': 'joe@hotmail.com'
            }, follow_redirects=True)
        assert 'Invite sent successfully' in resp.data

        # create token for add_user_confirm view to consume
        token = self.create_token('joe@hotmail.com', self.user.custom_data['tenant_id'])

        # create new add on user
        resp = self.client.post('/add_user_confirm/' + token, data={
                'email': 'joe@hotmail.com',
                'password': 'TempPass123',
                'password_again': 'TempPass123'
            }, follow_redirects=True)
        assert 'Your account was created' in resp.data

        # get addon user objects
        user_add_on = self.get_test_user('joe@hotmail.com')
        group_admin = self.get_test_user_group('test_user2@example.com')

        for gms in user_add_on.group_memberships:
            if gms.group.description == 'test_user2@example.com':
                group_add_on = gms.group

        # check that added user is associated with tenant group
        self.assertEqual(self.user.custom_data['tenant_id'], user_add_on.custom_data['tenant_id'])
        self.assertEqual(group_add_on.name, group_admin.name)

        # ensure user is not in admin group
        member_site_admin = False
        for group in user_add_on.groups:
            if group.name == 'site_admin':
                member_site_admin = True
        self.assertFalse(member_site_admin)

        # delete added user
        user_add_on.delete()
