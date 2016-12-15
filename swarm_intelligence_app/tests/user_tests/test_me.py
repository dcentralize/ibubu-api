"""
Test user api-functionality.
"""
import uuid

from swarm_intelligence_app.common import authentication
from swarm_intelligence_app.tests import test_helper


class TestUser:
    """
    Class for testing user api-functionality.

    """
    tokens = authentication.get_mock_user()
    helper = test_helper.TestHelper

    def test_me(self, client):
        """
        Sets up the Database and checks the functionality for a given set of
        mock users.

        """
        self.helper.set_up(test_helper, client)
        for token in self.tokens:
            """
            Test /me Endpoint
            """

            self.me_post(client, token)
            jwt_token = self.helper.login(test_helper, client, token)
            self.me_get(client, jwt_token)
            self.me_put(client, jwt_token)
            self.me_del(client, jwt_token)

            """
            Test /me/organizations Endpoint
            """
            self.me_post(client, token)
            jwt_token = self.helper.login(test_helper, client, token)
            self.me_organizations_post(client, jwt_token)
            self.me_organizations_get(client, jwt_token)

    def me_post(self, client, token):
        """
        Test if the me-page returns the expected http status-code when posting.
        """
        assert client.post('/register', headers={
            'Authorization': 'Token ' + token}).status == '201 CREATED'

    def me_get(self, client, token):
        """
        Test if the me-page returns the expected http status-code when getting.
        """
        assert client.get('/me', headers={
            'Authorization': 'Bearer ' + token}).status == '200 OK'

    def me_put(self, client, token):
        """
        Test if the me-page returns the expected http status-code when putting.
        """
        assert client.put('/me', headers={
            'Authorization': 'Bearer ' + token},
                          data={'firstname': 'Daisy', 'lastname': 'Ducks',
                                'email': 'daisy' + str(uuid.uuid4()) +
                                         '@tolli.com'})
        print('Passed test for updating a user.')

    def me_del(self, client, token):
        """
        Test if the me-page returns the expected http status-code when
        deleting.
        """
        assert client.delete('/me', headers={
            'Authorization': 'Bearer ' + token}).status == '204 NO CONTENT'

    def me_organizations_post(self, client, token):
        """
        Test if the me-organizations-page returns the expected http status-code.
        when posting.
        """
        assert client.post('/me/organizations', headers={
            'Authorization': 'Bearer ' + token},
                           data={'name': str(uuid.uuid4()) + 'Dagoberts ' +
                                         'Empire'}).status == \
               '201 CREATED'

    def me_organizations_get(self, client, token):
        """
        Test if the me-organizations-page returns the expected http status-code.
        when getting.
        """
        assert client.get('/me/organizations', headers={
            'Authorization': 'Bearer ' + token}, ).status == \
               '200 OK'
