"""
Test user api-functionality.
"""

from swarm_intelligence_app.tests import test_helper
from swarm_intelligence_app.common import authentication
from swarm_intelligence_app.tests.user_tests import test_me
from swarm_intelligence_app.tests.organization_tests import test_organization
from swarm_intelligence_app.resources import invitation


class TestPartners:
    """
    Class for testing user api-functionality.
    """
    user1 = test_me.TestUser
    user2 = test_me.TestUser
    organization = test_organization.TestOrganization
    helper = test_helper.TestHelper
    tokens = authentication.get_mock_user()
    jwtToken = ''
    jwtToken2 = ''

    def test_partners(self, client):
        # TODO
        self.helper.set_up(test_helper, client)

        self.user1.me_post(test_me, client, 'mock_user_001')
        self.user2.me_post(test_me, client, 'mock_user_002')
        self.jwtToken = self.helper.login(test_helper, client,
                                          'mock_user_001')
        self.jwtToken2 = self.helper.login(test_helper, client,
                                           'mock_user_002')
        self.user1.me_organizations_post(test_me, client, self.jwtToken)
        organization_id = self.organization.get_organization_id(
            test_organization,
            client, self.jwtToken)
        self.add_user_to_organization(client, self.jwtToken2, organization_id)

        member_id = self.get_organization_members_id(client, self.jwtToken,
                                                     organization_id)
        print(member_id)
        partner_id = self.get_partner(client, self.jwtToken, member_id)
        self.put_partner(client, self.jwtToken, member_id)
        self.put_partner_admins(client, self.jwtToken, partner_id)

        # self.get_partner_metrics(client, self.jwtToken, organization_id)
        # self.get_partner_checklist(client, self.jwtToken, organization_id)

        # self.post_partner_checklist(client, self.jwtToken, organization_id)
        # self.post_partner_metrics(client, self.jwtToken, organization_id)
        self.delete_partner_admins(client, self.jwtToken, organization_id)
        self.delete_partner(client, self.jwtToken, organization_id)

    def get_organization_members_id(self, client, token, id):
        """
        Helper Method for getting an organization ID for further tests.
        """

        response = client.get('/organizations/' + id + '/members', headers={
            'Authorization': 'Bearer ' + token})
        json_response = response.json['data'][1]['id']
        return str(json_response)

    def get_partner(self, client, token, id):
        """
        Test if get request to API gets executed.
        """
        assert client.get('/partners/' + id, headers={
            'Authorization': 'Bearer ' + token}).status == '200 OK'

        json_response = client.get('/partners/' + id, headers={
            'Authorization': 'Bearer ' + token})

        partner_id = json_response.json['data']['id']
        print('Passed test for getting a Partner:' + str(partner_id))
        return str(partner_id)

    def put_partner(self, client, token, id):
        """
        Test if get request to API gets executed.
        """
        assert client.put('/partners/' + id, headers={
            'Authorization': 'Bearer ' + token},
                          data={'firstname': 'Daisy', 'lastname': 'Ducks',
                                'email': 'daisy' +
                                         token + '@tolli.com'})
        print('Passed test for editing a Partner.')

    def delete_partner(self, client, token, id):
        """
        Test if the delete request gets executed.
        """
        assert client.delete('/partners/' + id, headers={
            'Authorization': 'Bearer ' + token}).status == '200 OK'

    def post_partner_metrics(self, client, token, id):
        """
        Test if the get request gets executed.
        """
        # #TODO Implement Metrics
        # # assert client.get('/organizations/' + id + '/members', headers={
        # #   'Authorization': 'Bearer ' + token}).status == '200 OK'
        # assert client.post('/partners/' + id + '/metrics', headers={
        #     'Authorization': 'Bearer ' + token}) == '200 OK'

    def get_partner_metrics(self, client, token, id):
        """
        Test if the get request gets executed.
        """
        # #TODO Implement Metrics
        # # assert client.get('/organizations/' + id + '/members', headers={
        # #   'Authorization': 'Bearer ' + token}).status == '200 OK'
        # assert client.get('/partners/' + id + '/metrics', headers={
        #     'Authorization': 'Bearer ' + token}) == '200 OK'

    def put_partner_admins(self, client, token, id):
        """
        Test if the get request gets executed.
        """

        assert client.put('/partners/' + id + '/admin', headers={
            'Authorization': 'Bearer ' + token}).status == '200 OK'

    def delete_partner_admins(self, client, token, id):
        """
        Test if the get request gets executed.
        """

        assert client.delete('/partners/' + id + '/admin', headers={
            'Authorization': 'Bearer ' + token}).status == '200 OK'

    def post_partner_checklist(self, client, token, id):
        """
        Test if post request get executed.
        """
        # #TODO Implement Checklists
        # assert client.post('/partners/' + id + '/checklists', headers={
        #     'Authorization': 'Bearer ' + token}).status == '200 OK'

    def get_partner_checklist(self, client, token, id):
        """
        Test if the get request gets executed.
        """
        # #TODO Implement Checklists
        # assert client.get('/partners/' + id + '/checklists', headers={
        #     'Authorization': 'Bearer ' + token}).status == '200 OK'

    def add_user_to_organization(self, client, token, \
                                 id_organization):
        invitation_response = self.organization.post_organization_invitation(
            test_organization, client, self.jwtToken, id_organization)

        invitation_code = invitation_response.json['data']['code']
        assert client.get('/invitations/' + invitation_code + '/accept',
                          headers={
                              'Authorization': 'Bearer ' + token}).status == '200 OK'
