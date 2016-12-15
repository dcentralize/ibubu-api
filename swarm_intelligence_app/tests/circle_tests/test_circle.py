"""
Test user api-functionality.

"""

from swarm_intelligence_app.common import authentication
from swarm_intelligence_app.tests import test_helper
from swarm_intelligence_app.tests.user_tests import test_me


class TestCircle:
    """
    Class for testing user api-functionality.

    """
    user = test_me.TestUser
    helper = test_helper.TestHelper
    tokens = authentication.get_mock_user()

    def test_organization(self, client):
        """
        Test the endpoint /organization.

        """
        self.helper.set_up(test_helper, client)

        for token in self.tokens:
            self.user.me_post(test_me, client, token)
            jwt_token = self.helper.login(test_helper, client, token)
            self.user.me_organizations_post(test_me, client, jwt_token)
            id = self.get_organization_id(client, jwt_token)
            circle_id = self.get_circle_id(client, jwt_token, id)

            self.get_circle(client, jwt_token, circle_id)
            self.put_circle(client, jwt_token, id, circle_id)
            self.delete_organization(client, jwt_token, id)

            self.user.me_organizations_post(test_me, client, jwt_token)
            id2 = self.get_organization_id(client, jwt_token)
            circle_id2 = self.get_circle_id(client, jwt_token, id2)
            self.post_circle_roles(client, jwt_token, circle_id2)
            self.get_circle_roles(client, jwt_token, circle_id2)
            role_id = self.get_role_id(client, jwt_token, circle_id2)
            self.put_circle_subcircles(client, role_id, jwt_token)
            self.get_circle_members(client, circle_id2, jwt_token)
            partner_id = self.get_partner_id(client, id2, jwt_token)
            self.put_circle_partner(client, partner_id, circle_id2, jwt_token)
            self.delete_circle_partner(client, partner_id, circle_id2,
                                       jwt_token)

    def get_organization_id(self, client, token):
        """
        Helper Method for getting an organization ID for further tests.

        """

        data = client.get('/me/organizations', headers={
            'Authorization': 'Bearer ' + token}).json[0]['id']
        organization_id = str(data)
        return organization_id

    def get_circle_id(self, client, token, id):
        """
        Helper Method for getting a circle id for further tests.

        """

        data = client.get('/organizations/' + id + '/anchor_circle', headers={
            'Authorization': 'Bearer ' + token}).json['id']
        circle_id = str(data)
        return circle_id

    def delete_organization(self, client, token, id):
        """
        Test if the delete request gets executed.

        """
        assert client.delete('/organizations/' + id, headers={
            'Authorization': 'Bearer ' + token}).status == '204 NO CONTENT'

    def get_circle(self, client, token, circle_id):
        """
        Test if get request to API gets executed.

        """
        assert client.get('/circles/' + circle_id, headers={
            'Authorization': 'Bearer ' + token}).status == '200 OK'

        print('Passed test for getting a Circle.')

    def put_circle(self, client, token, id, circle_id):
        """
        Test if put request to API get executed.

        """
        assert client.put('/circles/' + circle_id, headers={
            'Authorization': 'Bearer ' + token},
                          data={'name': 'Name2',
                                'purpose': 'Purpose2',
                                'strategy': 'Strategy2'}).status == '200 OK'

    def post_circle_roles(self, client, token, circle_id2):
        """
        Test if the post request gets executed.

        """
        assert client.post('/circles/' + circle_id2 + '/roles', headers={
            'Authorization': 'Bearer ' + token},
                           data={'name': 'NewRole',
                                 'purpose': 'This is a new Role added to a '
                                            'Circle.'}).status \
            == '201 CREATED'

    def get_circle_roles(self, client, token, circle_id2):
        """
        Test if the get request gets executed.

        """
        assert client.get('/circles/' + circle_id2 + '/roles', headers={
            'Authorization': 'Bearer ' + token}).status == '200 OK'

    def get_role_id(self, client, token, circle_id2):
        """
        Helper Method for getting the role Id

        """
        response = client.post('/circles/' + circle_id2 + '/roles', headers={
            'Authorization': 'Bearer ' + token},
                               data={'name': 'NewRole',
                                     'purpose': 'This is a new Role added to '
                                                'a Circle.'})
        data = response.json['id']
        role_id = str(data)
        return role_id

    def put_circle_subcircles(self, client, role_id, token):
        """
        Helper Method for creating a new subcircle.

        """
        assert client.put('/roles/' + role_id + '/circle', headers={
            'Authorization': 'Bearer ' + token},
                          data={'name': 'NewRole',
                                'purpose': 'This is a new Role added to a '
                                           'Circle.',
                                'strategy': 'NewStrategy'}).status == \
            '204 NO CONTENT'

    def get_circle_members(self, client, circle_id2, token):
        """
        Test if the get request gets executed.

        """
        assert client.get('/circles/' + circle_id2 + '/members', headers={
            'Authorization': 'Bearer ' + token}).status == '200 OK'

    def get_partner_id(self, client, id2, token):
        """
        Helper Method for getting the partner id.

        """
        response = client.get('/organizations/' + id2 + '/members', headers={
            'Authorization': 'Bearer ' + token})
        data = response.json[0]['id']
        partner_id = str(data)
        return partner_id

    def put_circle_partner(self, client, partner_id, circle_id2, token):
        """
        Test if the put request gets executed.

        """
        assert client.put('/circles/' + circle_id2 + '/members/' + partner_id,
                          headers={'Authorization': 'Bearer ' + token},
                          data={'firstname': 'Manuel', 'lastname':
                                'Neuer', 'email': 'm.neuer@mail.com'}).status \
            == '204 NO CONTENT'

    def delete_circle_partner(self, client, partner_id, circle_id2, token):
        """
        Test if the delete request gets executed.

        """
        assert client.delete('/circles/' + circle_id2 + '/members/' +
                             partner_id,
                             headers={'Authorization': 'Bearer ' + token}
                             ).status == '204 NO CONTENT'
