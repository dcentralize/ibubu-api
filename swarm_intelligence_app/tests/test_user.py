"""
Test user api-functionality.
"""
from flask import url_for


class TestUser:
    """
    Class for testing user api-functionality.

    """
    token = 'mock_user_001'

    def test_signin(self, client):
        """
        Test if the signin-page returns a valid http status-code.
        """
        assert client.get(url_for('signin')).status == '200 OK'

    def test_setup(self, client):
        """
        Test if the setup-page returns a valid http status-code.
        """
        assert client.get(url_for('setup')).status == '200 OK'

    def test_populate(self, client):
        """
        Test if the populate-page returns a valid http status-code.
        """
        assert client.get(url_for('populate')).status == '200 OK'

    def test_me_post(self, client):
        """
        Test if the me-page returns a valid http status-code.
        """
        assert client.post('/me', headers={
            'Authorization': 'Token ' + self.token}).status == '200 OK'

    def test_me_get(self, client):
        """
        Test if the me-page returns a valid http status-code.
        """
        assert client.get('/me', headers={
            'Authorization': 'Token ' + self.token}).status == '200 OK'

    def test_me_put(self, client):
        """
        Test if the me-page returns a valid http status-code.
        """
        assert client.put('/me', headers={
            'Authorization': 'Token ' + self.token}).status == '200 OK'
