"""Run tests against our custom views."""

from test_helpers import PhotogTestCase


class TestRegister(PhotogTestCase):
    """Test our registration view."""

    def test_register_user(self):
        # Page loads with correct text
        resp = self.client.get('/register')
        assert 'Register for an Account' in resp.data

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

        # Valid data results in success
        resp = self.client.post('/register', data={
            'email': self.test_email,
            'password': 'TempPass123',
            'password_again': 'TempPass123',
            }, follow_redirects=True)
        assert 'Dashboard' in resp.data

        self.remove_test_user_tenant_group(self.test_email)
        self.remove_test_user(self.test_email)


class TestLogin(PhotogTestCase):
    """Test login view."""

    # Page loads with correct text
    def test_login_user(self):
        resp = self.client.get('/login')
        assert 'Log in to your Account' in resp.data
