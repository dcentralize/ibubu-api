"""
Test Organization api-functionality.

"""

from swarm_intelligence_app.common import authentication
from swarm_intelligence_app.tests import test_helper
from swarm_intelligence_app.tests.user_tests import test_me


class TestOrganization:
    """
    Class for testing Organization api-functionality.

    """
    user = test_me.TestUser
    helper = test_helper.TestHelper
    tokens = authentication.get_mock_user()

    def test_organization(self, client):
        """
        Set up the Database and checks the functionality for a given set of
        mock users.

        """
        self.helper.set_up(test_helper, client)

        for token in self.tokens:
            self.user.me_post(test_me, client, token)
            jwt_token = self.helper.login(test_helper, client, token)
            self.user.me_organizations_post(test_me, client, jwt_token)
            id = self.get_organization_id(client, jwt_token)

            self.get_organization(client, jwt_token, id)
            self.put_organization(client, jwt_token, id)
            self.delete_organization(client, jwt_token, id)

            self.user.me_organizations_post(test_me, client, jwt_token)
            id2 = self.get_organization_id(client, jwt_token)

            self.get_organization_members(client, jwt_token, id2)
            self.get_organization_admins(client, jwt_token, id2)
            self.post_organization_invitation(client, jwt_token, id2)
            self.get_organization_invitations(client, jwt_token, id2)

    def get_organization_id(self, client, token):
        """
        Helper Method for getting an organization ID for further tests.
        :return Organization-ID as String.

        """
        data = client.get('/me/organizations', headers={
            'Authorization': 'Bearer ' + token}).json[0]['id']
        organization_id = str(data)
        return organization_id

    def get_organization(self, client, token, id):
        """
        Test if get request to API gets executed.

        """
        assert client.get('/organizations/' + id, headers={
            'Authorization': 'Bearer ' + token}).status == '200 OK'

    def put_organization(self, client, token, id):
        """
        Test if put request to API gets executed.

        """
        assert client.put('/organizations/' + id, headers={
            'Authorization': 'Bearer ' + token},
                          data={'is_deleted': 'False', 'name': 'Tolli Empire',
                                'id': '1'}).status == '200 OK'

    def delete_organization(self, client, token, id):
        """
        Test if the delete request gets executed.

        """
        assert client.delete('/organizations/' + id, headers={
            'Authorization': 'Bearer ' + token}).status == '204 NO CONTENT'

    def get_organization_members(self, client, token, id):
        """
        Get all organization members for further testing.
        :return JSON object with all members.

        """
        response = client.get('/organizations/' + id + '/members', headers={
            'Authorization': 'Bearer ' + token})
        json_response = response.json
        return json_response

    def get_organization_admins(self, client, token, id):
        """
        Test if the get request for Admins of an organization gets executed.
        :return JSON Object with all admins of an Organization.

        """
        assert client.get('/organizations/' + id + '/admins', headers={
            'Authorization': 'Bearer ' + token}).status == '200 OK'

        return client.get('/organizations/' + id + '/admins', headers={
            'Authorization': 'Bearer ' + token})

    def get_organization_invitations(self, client, token, id):
        """
        Test if the get request for Invitations gets executed.

        """
        assert client.get('/organizations/' + id + '/invitations', headers={
            'Authorization': 'Bearer ' + token}).status == '200 OK'

    def post_organization_invitation(self, client, token, id):
        """
        Post a Mock Invitation to an Organization.

        """
        return client.post('/organizations/' + id + '/invitations', headers={
            'Authorization': 'Bearer ' + token}, data={
            'email': 'dagobert@gmail.de',
            'organization_id': id})
