"""
Test organization api-functionality.
"""
from swarm_intelligence_app.tests import test_helper, test_user


class TestOrganization:
    """
    Class for testing API-Endpoint /organizations.

    """
    token = 'mock_user_001'
    helper = test_helper.TestHelper

    def get_organization_id(self, client):
        client.get('/organizations', headers={
            'Authorization': 'Token ' + self.token}).json['data'][0]['id']

    def test_organizations_get(self, client):
        """
        Test if the endpoint /organizations returns the Status-Code '200' when
        an existing organization is requested with a valid token.
        """
        self.helper.set_up(test_helper, client)
        test_user.TestUserOrganization.test_me_organizations_post(self, client)
        assert client.get('/organizations', headers={
            'Authorization': 'Token ' + self.token}).status == '200 OK'
