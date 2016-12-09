"""
Test user api-functionality.
"""

from swarm_intelligence_app.tests import test_helper
from swarm_intelligence_app.common import authentication
from swarm_intelligence_app.tests.user_tests import test_me


class TestCircle:
    """
    Class for testing user api-functionality.
    """
    user = test_me.TestUser
    helper = test_helper.TestHelper
    tokens = authentication.get_mock_user()

    def test_organization(self, client):
        self.helper.set_up(test_helper, client)

        for token in self.tokens:
            self.user.me_post(test_me, client, token)
            jwtToken = self.helper.login(test_helper, client, token)
            self.user.me_organizations_post(test_me, client, jwtToken)
            id = self.get_organization_id(client, jwtToken)
            circleId = self.get_circle_id(client, jwtToken, id)

            self.get_circle(client, jwtToken, circleId)
            self.put_circle(client, jwtToken, id, circleId)
            self.delete_circle(client, jwtToken, circleId)
            self.delete_organization(client, jwtToken, id)

            self.user.me_organizations_post(test_me, client, jwtToken)
            id2 = self.get_organization_id(client, jwtToken)
            circleId2 = self.get_circle_id(client, jwtToken, id2)
            #self.post_roles(client, token, circleId2)

    def get_organization_id(self, client, token):
        """
        Helper Method for getting an organization ID for further tests.
        """

        data = client.get('/me/organizations', headers={
            'Authorization': 'Bearer ' + token}).json['data'][0]['id']
        organization_id = str(data)
        return organization_id

    def get_circle_id(self, client, token, id):
        """
        Helper Method for getting a circle id for further tests.
        """

        data = client.get('/organizations/' + id + '/anchor_circle', headers={
            'Authorization': 'Bearer ' + token}).json['data'][0]['role_id']
        circle_id = str(data)
        return circle_id

    def delete_organization(self, client, token, id):
        """
        Test if the delete request gets executed.
        """
        assert client.delete('/organizations/' + id, headers={
            'Authorization': 'Bearer ' + token}).status == '200 OK'

    def get_circle(self, client, token, circleId):
        """
        Test if get request to API gets executed.
        """
        assert client.get('/circles/' + circleId, headers={
            'Authorization': 'Bearer ' + token}).status == '200 OK'

        print('Passed test for getting a Circle.')

    def put_circle(self, client, token, id, circleId):
        """
        Test if put request to API get executed.
        """
        assert client.put('/circles/' + circleId, headers={
            'Authorization': 'Bearer ' + token},
                          data={'name': 'Name2',
                                'purpose': "Purpose2",
                                'strategy': 'Strategy2'}).status == '200 OK'

        print('Passed test for putting a Circle.')

    def delete_circle(self, client, token, circleId):
        """
        Test if the delete request gets executed.
        """
        assert client.delete('/circles/' + circleId, headers={
            'Authorization': 'Bearer ' + token}).status == '200 OK'

    def post_roles(self, client, token, circleId2):
        """
        Tst if the post request gets executed.
        """
        assert client.post('/circles' + circleId2 + '/roles', headers={
            'Authorization': 'Bearer ' + token},
                           data={'name': 'NewCircle',
                                 'purpose': 'This is a new Circle'}).status \
                            == '200 OK'
