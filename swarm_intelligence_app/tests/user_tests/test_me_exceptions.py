"""
Test User-Api exceptions.

"""

from swarm_intelligence_app.common import authentication
from swarm_intelligence_app.tests import test_helper
from swarm_intelligence_app.tests.user_tests import test_me


class TestUserExceptions:
    """
    Class for testing exceptions at the /me(/*) endpoint.

    """
    tokens = authentication.get_mock_user()
    endpoint_me = test_me.TestUser
    helper = test_helper.TestHelper

    def test_me_exceptions(self, client):
        """
        Sets up the Database and checks the functionality for a given set of
        mock users.

        """
        self.helper.set_up(test_helper, client)

        self.me_put_no_login(client)
        self.me_del_no_login(client)
        self.me_organizations_post_no_login(client)

        for token in self.tokens:
            self.endpoint_me.me_post(test_me, client, token)
            jwt_token = self.helper.login(test_helper, client, token)
            self.me_organizations_post_no_param(client, jwt_token)
            self.me_del_no_param(client, jwt_token)
            self.me_delete_deleted_user(client, jwt_token)

    def me_post_no_login(self, client):
        """
        Test if the me-page returns the expected http status-code when posting
        without an authorization token.

        """
        assert client.post('/me').status == '400 BAD REQUEST'

    def me_get_no_login(self, client):
        """
        Test if the me-page returns the expected http status-code when getting
        without an authorization token.

        """
        assert client.get('/me').status == '400 BAD REQUEST'

    def me_put_no_login(self, client):
        """
        Test if the me-page returns the expected http status-code when putting
        without an authorization token.

        """
        assert client.put('/me', headers={},
                          data={'firstname': 'Daisy',
                                'lastname': 'Ducks',
                                'email': 'daisy@tolli.com'}).status == \
               '400 BAD REQUEST'

    def me_put_no_param(self, client, token):
        """
        Test if the me-page returns the expected http status-code when putting.

        """
        assert client.put('/me', headers={
            'Authorization': 'Bearer ' + token},
                          data={}).status == '400 BAD REQUEST'

    def me_del_no_login(self, client):
        """
        Test if the me-page returns the expected http status-code when deleting
        without an authorization token.

        """
        assert client.delete('/me', headers={},
                             data={'firstname': 'Daisy', 'lastname': 'Ducks',
                                   'email': 'daisy@tolli.com'}).status == \
               '400 BAD REQUEST'

    def me_del_no_param(self, client, token):
        """
        Test if the me-page returns the expected http status-code
        when deleting.

        """
        assert client.delete('/me', headers={
            'Authorization': 'Bearer ' + token},
                             data={}).status == '204 NO CONTENT'

    def me_organizations_post_no_login(self, client):
        """
        Test if the me-organizations-page returns the expected http status-code
        when posting without an authorization token.

        """
        assert client.post('/me/organizations', headers={},
                           data={'name': 'Dagoberts ' +
                                         'Empire'}).status == \
               '400 BAD REQUEST'

    def me_organizations_post_no_param(self, client, token):
        """
        Test if the me-organizations-page returns the expected http
        status-code when posting.

        """
        assert client.post('/me/organizations', headers={
            'Authorization': 'Bearer ' + token},
                           data={}).status == '400 BAD REQUEST'

    def me_delete_deleted_user(self, client, token):
        """
        Test if the delete request works on a deleted user.

        """
        assert client.delete('/me', headers={
            'Authorization': 'Bearer ' + token}).status == '401 UNAUTHORIZED'
