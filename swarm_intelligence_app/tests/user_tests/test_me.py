"""
Test user api-functionality.
"""
import uuid
from swarm_intelligence_app.tests import test_helper
from swarm_intelligence_app.common import authentication


class TestUser:
    """
    Class for testing user api-functionality.

    """
    tokens = authentication.get_mock_user()
    helper = test_helper.TestHelper

    def test_me(self, client):
        self.helper.set_up(test_helper, client)
        for token in self.tokens:
            """
            Test /me Endpoint
            """

            self.me_post(client, token)
            jwtToken = self.helper.login(test_helper, client, token)
            self.me_get(client, jwtToken)
            self.me_put(client, jwtToken)
            self.me_del(client, jwtToken)

            """
            Test /me/organizations Endpoint
            """
            self.me_post(client, token)
            jwtToken = self.helper.login(test_helper, client, token)
            self.me_organizations_post(client, jwtToken)
            self.me_organizations_get(client, jwtToken)

    def me_post(self, client, token):
        """
        Test if the me-page returns a valid http status-code when posting.
        """
        assert client.post('/register', headers={
            'Authorization': 'Token ' + token}).status == '201 CREATED'

    def me_get(self, client, token):
        """
        Test if the me-page returns a valid http status-code when getting.
        """
        assert client.get('/me', headers={
            'Authorization': 'Bearer ' + token}).status == '200 OK'

    def me_put(self, client, token):
        """
        Test if the me-page returns a valid http status-code when putting.
        """
        assert client.put('/me', headers={
            'Authorization': 'Bearer ' + token},
                          data={'firstname': 'Daisy', 'lastname': 'Ducks',
                                'email': 'daisy' + str(uuid.uuid4()) +
                                         '@tolli.com'})
        print('Passed test for updating a user.')

    def me_del(self, client, token):
        """
        Test if the me-page returns a valid http status-code when deleting.
        """
        assert client.delete('/me', headers={
            'Authorization': 'Bearer ' + token}).status == '204 NO CONTENT'

    def me_organizations_post(self, client, token):
        """
        Test if the me-organizations-page returns a valid http status-code.
        when posting.
        """
        assert client.post('/me/organizations', headers={
            'Authorization': 'Bearer ' + token},
                           data={'name': str(uuid.uuid4()) + 'Dagoberts ' +
                                                 'Empire'}).status == \
               '201 CREATED'

    def me_organizations_get(self, client, token):
        """
        Test if the me-organizations-page returns a valid http status-code.
        when posting.
        """
        assert client.get('/me/organizations', headers={
            'Authorization': 'Bearer ' + token}, ).status == \
               '200 OK'
