"""
Test user api-functionality.
"""
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
            # self.me_put(client, jwtToken)
            # self.me_del(client, jwtToken)

            """
            Test /me/organizations Endpoint
            """
            # self.me_organizations_post(client, token)

    def me_post(self, client, token):
        """
        Test if the me-page returns a valid http status-code when posting.
        """
        print('Passed test for creating a new user: ' + token)

        assert client.post('/register', headers={
            'Authorization': 'Token ' + token}).status == '200 OK'

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
                                'email': 'daisy' +
                                         token + '@tolli.com'})
        print('Passed test for updating a user:' + token)

    def me_del(self, client, token):
        """
        Test if the me-page returns a valid http status-code when deleting.
        """
        assert client.delete('/me', headers={
            'Authorization': 'Bearer ' + token})
        print('Passed test for deleting a user: ' + token)

        # def me_organizations_post(self, client, token):
        #     """
        #     Test if the me-organizations-page returns a valid http status-code.
        #     when posting.
        #     """
        #     assert client.post('/me/organizations', headers={
        #         'Authorization': 'Bearer ' + token},
        #                        data={'name': token + ': Dagoberts ' +
        #                                      'Empire'}).status == \
        #            '200 OK'
        #     print('Passed test for creating a new organization: ' + token)
