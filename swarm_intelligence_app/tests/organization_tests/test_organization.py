"""
Test user api-functionality.
"""

from swarm_intelligence_app.tests import test_helper
from swarm_intelligence_app.common import authentication
from swarm_intelligence_app.tests.user_tests import test_me


class TestOrganization:
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

            self.get_organization(client, jwtToken, id)
            self.put_organization(client, jwtToken, id)
            self.delete_organization(client, jwtToken, id)

            self.user.me_organizations_post(test_me, client, jwtToken)
            id2 = self.get_organization_id(client, jwtToken)

            self.get_organization_members(client, jwtToken, id2)
            self.get_organization_admins(client, jwtToken, id2)
            self.post_organization_invitation(client, jwtToken, id2)
            self.get_organization_invitations(client, jwtToken, id2)

    def get_organization_id(self, client, token):
        """
        Helper Method for getting an organization ID for further tests.
        """

        data = client.get('/me/organizations', headers={
            'Authorization': 'Bearer ' + token}).json['data'][0]['id']
        organization_id = str(data)
        return organization_id

    def get_organization(self, client, token, id):
        """
        Test if get request to API gets executed.
        """
        assert client.get('/organizations/' + id, headers={
            'Authorization': 'Bearer ' + token}).status == '200 OK'

        print('Passed test for getting an Organization.')

    def put_organization(self, client, token, id):
        """
        Test if get request to API gets executed.
        """
        assert client.put('/organizations/' + id, headers={
            'Authorization': 'Bearer ' + token},
                          data={'is_deleted': 'False', 'name': 'Tolli Empire',
                                'id': '1'}).status == '200 OK'

        print('Passed test for putting an Organization.')

    def delete_organization(self, client, token, id):
        """
        Test if the delete request gets executed.
        """
        assert client.delete('/organizations/' + id, headers={
            'Authorization': 'Bearer ' + token}).status == '200 OK'

    def get_organization_members(self, client, token, id):
        """
        Test if the get request gets executed.
        """

        # assert client.get('/organizations/' + id + '/members', headers={
        #   'Authorization': 'Bearer ' + token}).status == '200 OK'
        response = client.get('/organizations/' + id + '/members', headers={
            'Authorization': 'Bearer ' + token})
        #TODO PARTNERS?

        print("HIER KOMMEN DIE MEMBER TOLL!!")
        json_response = response.json['data']
        print(json_response)

    def get_organization_admins(self, client, token, id):
        """
        Test if the get request gets executed.
        """

        assert client.get('/organizations/' + id + '/admins', headers={
            'Authorization': 'Bearer ' + token}).status == '200 OK'

    def get_organization_invitations(self, client, token, id):
        """
        Test if the get request gets executed.
        """

        assert client.get('/organizations/' + id + '/invitations', headers={
            'Authorization': 'Bearer ' + token}).status == '200 OK'

    def post_organization_invitation(self, client, token, id):
        """
        Test if post request get executed.
        """
        assert client.post('/organizations/' + id + '/invitations', headers={
            'Authorization': 'Bearer ' + token}, data={
            'email': 'donaldo@ducko.com',
            'organization_id': id}).status == '200 OK'
