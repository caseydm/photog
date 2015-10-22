"""Run tests against our custom views."""

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
        self.remove_test_user_tenant_group(self.test_email)
        self.remove_test_user(self.test_email)


class TestLogin(PhotogTestCase):
    """Test login view."""

    # Page loads with correct text
    def test_login_user(self):
        resp = self.client.get('/login')
        assert 'Log in to your Account' in resp.data
