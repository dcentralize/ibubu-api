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
            self.post_circle_roles(client, jwtToken, circleId2)
            self.get_circle_roles(client, jwtToken, circleId2)
            roleId = self.get_role_id(client, jwtToken, circleId2)
            self.put_circle_subcircles(client, roleId, jwtToken)
            self.get_circle_subcircles(client, circleId2, jwtToken)
            self.get_circle_members(client, circleId2, jwtToken)
            partnerId = self.get_partner_id(client, id2, jwtToken)
            self.put_circle_partner(client, partnerId, circleId2, jwtToken)
            self.delete_circle_partner(client, partnerId, circleId2, jwtToken)
            self.post_circle_domain(client, circleId2, jwtToken)
            self.get_circle_domain(client, circleId2, jwtToken)
            self.post_circle_accountability(client, circleId2, jwtToken)
            self.get_circle_accountability(client, circleId2, jwtToken)

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
                                'purpose': 'Purpose2',
                                'strategy': 'Strategy2'}).status == '200 OK'

    def delete_circle(self, client, token, circleId):
        """
        Test if the delete request gets executed.
        """
        assert client.delete('/circles/' + circleId, headers={
            'Authorization': 'Bearer ' + token}).status == '200 OK'

    def post_circle_roles(self, client, token, circleId2):
        """
        Test if the post request gets executed.
        """
        assert client.post('/circles/' + circleId2 + '/roles', headers={
            'Authorization': 'Bearer ' + token},
                           data={'name': 'NewRole',
                                 'purpose': 'This is a new Role added to a '
                                            'Circle.'}).status \
            == '200 OK'

    def get_circle_roles(self, client, token, circleId2):
        """
        Test if the get request gets executed.
        """
        assert client.get('/circles/' + circleId2 + '/roles', headers={
            'Authorization': 'Bearer ' + token}).status == '200 OK'

    def get_role_id(self, client, token, circleId2):
        """
        Helper Method for getting the role Id
        """
        response = client.post('/circles/' + circleId2 + '/roles', headers={
            'Authorization': 'Bearer ' + token},
                           data={'name': 'NewRole',
                                 'purpose': 'This is a new Role added to a '
                                            'Circle.'})
        data = response.json['data']['id']
        role_id = str(data)
        return role_id

    def put_circle_subcircles(self, client, roleId, token):
        """
        Helper Method for creating a new subcircle.
        """
        assert client.put('/roles/' + roleId + '/circle', headers={
            'Authorization': 'Bearer ' + token}, data={'name': 'NewRole',
                                 'purpose': 'This is a new Role added to a '
                                            'Circle.',
                                 'strategy': 'NewStrategy'}).status == '200 OK'

    def get_circle_subcircles(self, client, circleId2, token):
        """
        Test if the get request gets executed.
        """
        assert client.get('/circles/' + circleId2 + '/subcircles', headers={
            'Authorization': 'Bearer ' + token}).status == '200 OK'

    def get_circle_members(self, client, circleId2, token):
        """
        Test if the get request gets executed.
        """
        assert client.get('/circles/' + circleId2 + '/members', headers={
            'Authorization': 'Bearer ' + token}).status == '200 OK'

    def get_partner_id(self, client, id2, token):
        """
        Helper Method for getting the partner id.
        """
        response = client.get('/organizations/' + id2 + '/members', headers={
            'Authorization': 'Bearer ' + token})
        data = response.json['data'][0]['id']
        partnerId = str(data)
        return partnerId

    def put_circle_partner(self, client, partnerId, circleId2, token):
        """
        Test if the put request gets executed.
        """
        assert client.put('/circles/' + circleId2 + '/members/' + partnerId,
                          headers={'Authorization': 'Bearer ' + token},
                          data={'firstname': 'Manuel', 'lastname':
                              'Neuer', 'email': 'm.neuer@mail.com'}).status \
            == '200 OK'

    def delete_circle_partner(self, client, partnerId, circleId2, token):
        """
        Test if the delete request gets executed.
        """
        assert client.delete('/circles/' + circleId2 + '/members/' + partnerId,
                             headers={'Authorization': 'Bearer ' + token}
                             ).status == '200 OK'

    def post_circle_domain(self, client, circleId2, token):
        """
        Test if the post request gets executed.
        """
        assert client.post('/circles/' + circleId2 + '/domains',
                           headers={'Authorization': 'Bearer ' + token},
                           data={'name': 'DomainName'}).status == '200 OK'

    def get_circle_domain(self, client, circleId2, token):
        """
        Test if the get request gets executed.
        """
        assert client.get('/circles/' + circleId2 + '/domains',
                          headers={'Authorization': 'Bearer ' +
                                   token}).status == '200 OK'

    def post_circle_accountability(self, client, circleId2, token):
        """
        Test if the post request gets executed.
        """
        assert client.post('/circles/' + circleId2 + '/accountabilities',
                           headers={'Authorization': 'Bearer ' + token},
                           data={'name': 'AccName'}).status == '200 OK'

    def get_circle_accountability(self, client, circleId2, token):
        """
        Test if the get request gets executed.
        """
        assert client.get('/circles/' + circleId2 + '/accountabilities',
                          headers={'Authorization': 'Bearer ' +
                                                    token}).status == '200 OK'