"""
Define Organization Exception Tests.
"""

from swarm_intelligence_app.common import authentication
from swarm_intelligence_app.tests.user_tests import test_me
from swarm_intelligence_app.tests.organization_tests import test_organization
from swarm_intelligence_app.tests import test_helper
from swarm_intelligence_app.tests.partner_tests import test_partners


class TestPartnerException:
    """
    Test API for exceptions.
    """
    partner_helper = test_partners.TestPartners
    helper = test_helper.TestHelper
    user1 = test_me.TestUser
    user2 = test_me.TestUser
    organization = test_organization.TestOrganization
    tokens = authentication.get_mock_user()
    jwtToken = ''
    jwtToken2 = ''

    def test_organization_exceptions(self, client):
        """
        Test with multiple token.
        """
        self.helper.set_up(test_helper, client)

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

        self.add_user_to_organization(client, self.jwtToken2,
                                      organization_id)

        member_id = self.partner_helper.get_organization_members_id \
            (test_partners, client,
             self.jwtToken,
             organization_id)

        partner_id = self.partner_helper.get_partner(test_partners, client,
                                                     self.jwtToken,
                                                     member_id)

        self.partner_post_not_allowed(client, partner_id)
        self.partner_put_no_login(client, partner_id)
        self.partner_put_no_param(client, self.jwtToken, partner_id)
        self.partner_put_wrong_params(client, self.jwtToken, partner_id)
        self.partner_get_no_id(client, self.jwtToken)
        self.partner_get_no_login(client, partner_id)
        self.partner_get_wrong_id(client, self.jwtToken, '1234567890')
        self.partner_put_admin_no_id(client, self.jwtToken)
        self.partner_put_admin_no_login(client, partner_id)
        self.partner_put_admin_wrong_id(client, self.jwtToken, '1234567890')
        self.partner_del_admins_no_id(client, self.jwtToken)
        self.partner_del_admins_no_login(client, partner_id)
        self.partner_del_admins_wrong_id(client, self.jwtToken, '1234567890')
        self.partner_del_no_id(client, self.jwtToken)
        self.partner_del_no_login(client, partner_id)
        self.partner_del_wrong_id(client, self.jwtToken, '1234567890')

    def partner_post_not_allowed(self, client, id):
        """
        Test if the me-page returns a valid http status-code when posting.
        """
        assert client.post(
            '/partners/' + id).status == '405 METHOD NOT ALLOWED'

    def partner_put_no_login(self, client, id):
        """
        Test if the me-page returns a valid http status-code when getting.
        """
        assert client.put('/partners/' + id, headers={},
                          data={'firstname': 'Daisy', 'lastname': 'Ducks',
                                'email': 'daisy@tolli.com'}).status == \
            '400 BAD REQUEST'

    def partner_put_no_param(self, client, token, id):
        """
            Test if the me-page returns a valid http status-code when putting.
            """
        assert client.put('/partners/' + id,
                          headers={'Authorization': 'Bearer ' + token},
                          data={}).status == '400 BAD REQUEST'

    def partner_put_wrong_params(self, client, token, id):
        """
        Test if the me-page returns a valid http status-code when putting.
        """
        assert client.put('/partners/' + id,
                          headers={'Authorization': 'Bearer ' + token},
                          data={'google_id': 'Daisy',
                                'lastname': 'Ducks',
                                'email': 'daisy@tolli.com'}).status == \
            '400 BAD REQUEST'

    def partner_get_no_login(self, client, id):
        assert client.get('/partners/' + id, headers={}).status == '400 BAD ' \
                                                                   'REQUEST'

    def partner_get_no_id(self, client, token):
        assert client.get('/partners/', headers={
            'Authorization': 'Bearer ' + token}).status == '404 NOT FOUND'

    def partner_get_wrong_id(self, client, token, id):
        assert client.get('/partners/' + id, headers={
            'Authorization': 'Bearer ' + token}).status == '404 NOT FOUND'

    def partner_put_admin_no_login(self, client, id):
        assert client.put('/partners/' + id + '/admin', headers={}).status \
               == '400 BAD REQUEST'

    def partner_put_admin_no_id(self, client, token):
        assert client.put('/partners/admin', headers={
            'Authorization': 'Bearer ' + token}).status == '404 NOT FOUND'

    def partner_put_admin_wrong_id(self, client, token, id):
        assert client.put('/partners/' + id + '/admin', headers={
            'Authorization': 'Bearer ' + token}).status == '404 NOT FOUND'

    def partner_del_admins_no_login(self, client, id):
        assert client.delete('/partners/' + id + '/admin', headers={

        }).status == '400 BAD REQUEST'

    def partner_del_admins_no_id(self, client, token):
        assert client.delete('/partners/admin', headers={
            'Authorization': 'Bearer ' + token}).status == '404 NOT FOUND'

    def partner_del_admins_wrong_id(self, client, token, id):
        assert client.delete('/partners/' + id + '/admin', headers={
            'Authorization': 'Bearer ' + token}).status == '404 NOT FOUND'

    def partner_operation_with_deleted_user(self, client, token, id):
        assert client.delete('/partners/' + id, headers={
            'Authorization': 'Bearer ' + token}).status == '200 OK'

        assert client.put('/partners/' + id,
                          headers={'Authorization': 'Bearer ' + token},
                          data={'firstname': 'Daisy',
                                'lastname': 'Ducks',
                                'email': 'daisy@tolli.com'}).status == \
            '400 BAD REQUEST'

    def partner_del_no_login(self, client, id):
        assert client.delete('/partners/' + id,
                             headers={}).status == '400 BAD REQUEST'

    def partner_del_no_id(self, client, token):
        assert client.delete('/partners/', headers={
            'Authorization': 'Bearer ' + token}).status == '404 NOT FOUND'

    def partner_del_wrong_id(self, client, token, id):
        assert client.delete('/partners/' + id, headers={
            'Authorization': 'Bearer ' + token}).status == '404 NOT FOUND'

    def add_user_to_organization(self, client, token, id_organization):
        invitation_response = self.organization.post_organization_invitation(
            test_organization, client, self.jwtToken, id_organization)

        invitation_code = invitation_response.json['code']
        assert client.get('/invitations/' + invitation_code + '/accept',
                          headers={
                              'Authorization': 'Bearer ' + token}).status == \
            '200 OK'
