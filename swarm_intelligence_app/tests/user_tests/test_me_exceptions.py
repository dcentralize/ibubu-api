"""
Test User-Api exceptions
"""

from swarm_intelligence_app.tests import test_helper
from swarm_intelligence_app.common import authentication
from swarm_intelligence_app.tests.user_tests import test_me


class TestUserExceptions:
    """
    Class for testing exceptions at the /me(/*) endpoint
    """
    tokens = authentication.get_mock_user()
    endpoint_me = test_me.TestUser
    helper = test_helper.TestHelper

    def test_me_exceptions(self, client):
        self.helper.set_up(test_helper, client)

        self.me_put_no_login(client)
        self.me_del_no_login(client)
        self.me_organizations_post_no_login(client)

        for token in self.tokens:
            self.endpoint_me.me_post(test_me, client, token)
            jwtToken = self.helper.login(test_helper, client, token)
            self.me_organizations_post_no_param(client, jwtToken)
            self.me_del_no_param(client, jwtToken)
            self.me_delete_deleted_user(client, jwtToken)

    def me_post_no_login(self, client):
        """
        Test if the me-page returns a valid http status-code when posting.
        """
        assert client.post('/me').status == '400 BAD REQUEST'
        print("Passed nologin-test for creating a new user.")

    def me_get_no_login(self, client):
        """
        Test if the me-page returns a valid http status-code when getting.
        """
        assert client.get('/me').status == '400 BAD REQUEST'
        print("Passed nologin-test for getting a user.")

    def me_put_no_login(self, client):
        """
        Test if the me-page returns a valid http status-code when putting.
        """
        assert client.put('/me', headers={},
                          data={'firstname': 'Daisy',
                                'lastname': 'Ducks',
                                'email': 'daisy@tolli.com'}).status == \
               '400 BAD REQUEST'
        print("Passed nologin-test for updating a user.")

    def me_put_no_param(self, client, token):
        """
        Test if the me-page returns a valid http status-code when putting.
        """
        assert client.put('/me', headers={
            'Authorization': 'Bearer ' + token},
                          data={}).status == '400 BAD REQUEST'
        print('Passed noparam-test for updating a user: ' + token)

    def me_del_no_login(self, client):
        """
        Test if the me-page returns a valid http status-code when deleting.
        """
        assert client.delete('/me', headers={},
                             data={'firstname': 'Daisy', 'lastname': 'Ducks',
                                   'email': 'daisy@tolli.com'}).status == \
               '400 BAD REQUEST'
        print("Passed nologin-test for deleting a user.")

    def me_del_no_param(self, client, token):
        """
        Test if the me-page returns a valid http status-code when deleting.
        """
        assert client.delete('/me', headers={
            'Authorization': 'Bearer ' + token},
                             data={}).status == '200 OK'
        #TODO 400 oder 200?
        print("Passed noparam-test for deleting a user.")

    def me_organizations_post_no_login(self, client):
        """
        Test if the me-organizations-page returns a valid http status-code
        when posting.
        """
        assert client.post('/me/organizations', headers={},
                           data={'name': 'Dagoberts ' +
                                         'Empire'}).status == \
               '400 BAD REQUEST'
        print("Passed test for creating a new organization.")

    def me_organizations_post_no_param(self, client, token):
        """
        Test if the me-organizations-page returns a valid http
        status-code
        when posting.
        """
        assert client.post('/me/organizations', headers={
            'Authorization': 'Bearer ' + token},
                           data={}).status == '400 BAD REQUEST'
        print("Passed noparam-test for creating a new organization.")

    def me_delete_deleted_user(self, client, token):

        assert client.delete('/me', headers={
            'Authorization': 'Bearer ' + token}).status == '401 UNAUTHORIZED'
