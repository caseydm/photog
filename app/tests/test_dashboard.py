from test_helpers import PhotogTestCase


class TestAddContact(PhotogTestCase):
    """Test our add contact view."""

    def test_add_contact_page_loads(self):
        self.login(self.user.email, self.test_password)

        # Page loads with correct text
        resp = self.client.get('/newcontact', follow_redirects=True)
        assert 'Add Contact' in resp.data

    def test_add_contact_page_bad_data(self):
        self.login(self.user.email, self.test_password)

        # Return error with bad data
        resp = self.client.post('/newcontact', data={
                'name': '',
                'email': 'test@hotmail.com'
            }, follow_redirects=True)
        assert 'Add Contact' in resp.data

        resp = self.client.post('/newcontact', data={
                'name': 'Joe',
                'email': ''
            }, follow_redirects=True)
        assert 'Add Contact' in resp.data

    def test_add_contact_page_good_data(self):
        self.login(self.user.email, self.test_password)

        # Return error with bad data
        resp = self.client.post('/newcontact', data={
                'name': 'Roger',
                'email': 'test@hotmail.com',
                'phone': '723-234-2343'
            }, follow_redirects=True)
        assert 'Dashboard' in resp.data
