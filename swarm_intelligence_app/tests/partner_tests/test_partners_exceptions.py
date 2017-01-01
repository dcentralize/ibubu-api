"""
Define Partners Exception Tests.

"""
import uuid

import jwt

from datetime import datetime, timedelta

from swarm_intelligence_app.common import authentication
from swarm_intelligence_app.tests import test_helper
from swarm_intelligence_app.tests.organization_tests import test_organization
from swarm_intelligence_app.tests.partner_tests import test_partners
from swarm_intelligence_app.tests.user_tests import test_me


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
        Set up the Database and checks the functionality for a given set of
        mock users.

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

        member_id = self.partner_helper.get_organization_members_id(
            test_partners, client,
            self.jwtToken,
            organization_id)

        partner_id = self.partner_helper.get_partner(test_partners, client,
                                                     self.jwtToken,
                                                     member_id)

        fields = {
            'exp': datetime.utcnow() - timedelta(
                seconds=60
            ),
            'sub': 'mock_user_001'
        }
        encoded = jwt.encode(fields, 'top_secret', algorithm='HS256')
        expired_token = encoded.decode('utf-8')

        self.partner_post_not_allowed(client, partner_id)
        self.partner_get_no_login(client, partner_id)
        self.partner_get_expired_token(client, expired_token, partner_id)
        self.partner_get_not_found(client, self.jwtToken)

        self.partner_put_no_login(client, partner_id)
        self.partner_put_no_param(client, self.jwtToken, partner_id)
        self.partner_put_wrong_params(client, self.jwtToken, partner_id)
        self.partner_put_expired_token(client, expired_token, partner_id)
        self.partner_put_not_found(client, self.jwtToken)

        self.partner_del_no_login(client, partner_id)
        self.partner_del_expired_token(client, expired_token, partner_id)
        self.partner_del_not_found(client, self.jwtToken)

        self.partner_put_admin_no_login(client, partner_id)
        self.partner_put_admin_expired_token(client, expired_token, partner_id)
        self.partner_put_admin_not_found(client, self.jwtToken)

        self.partner_del_admin_no_login(client, partner_id)
        self.partner_del_admin_expired_token(client, expired_token, partner_id)
        self.partner_del_admin_not_found(client, self.jwtToken)

    def partner_post_not_allowed(self, client, partner_id):
        """
        Test if the partner api returns the expected http status-code
        when posting.

        """
        assert client.post(
            '/partners/' + partner_id).status == '405 METHOD NOT ALLOWED'

    def partner_get_no_login(self, client, partner_id):
        """
        Test if the partner api returns the expected http status-code
        when getting without an authorization token.

        """
        assert client.get('/partners/' + partner_id, headers={}).status == \
            '400 BAD REQUEST'

    def partner_get_expired_token(self, client, expired_token, partner_id):
        """
        Test if the get requests with an expired token returns a 401 status
        code.

        """
        assert client.get('/partners/' + partner_id, headers={
            'Authorization': 'Bearer ' + expired_token}).status == \
            '401 UNAUTHORIZED'

    def partner_get_not_found(self, client, jwt_token):
        """
        Test if the get requests to a non-existing partner returns a 404
        status code.

        """
        assert client.get('/partners/' + '0', headers={
            'Authorization': 'Bearer ' + jwt_token}).status == '404 NOT FOUND'

    def partner_put_no_login(self, client, partner_id):
        """
        Test if the partner api returns the expected http status-code
        when putting without an authorization token.

        """
        assert client.put('/partners/' + partner_id, headers={},
                          data={'firstname': 'Daisy', 'lastname': 'Ducks',
                                'email': 'daisy@tolli.com'}).status == \
            '400 BAD REQUEST'

    def partner_put_no_param(self, client, token, partner_id):
        """
        Test if the partner api returns the expected http status-code
        when putting without parameters.

        """
        assert client.put('/partners/' + partner_id,
                          headers={'Authorization': 'Bearer ' + token},
                          data={}).status == '400 BAD REQUEST'

    def partner_put_wrong_params(self, client, token, partner_id):
        """
        Test if the partner api returns the expected http status-code
        when putting with wrong parameters.

        """
        assert client.put('/partners/' + partner_id,
                          headers={'Authorization': 'Bearer ' + token},
                          data={'google_id': 'Daisy',
                                'lastname': 'Ducks',
                                'email': 'daisy@tolli.com'}).status == \
            '400 BAD REQUEST'

    def partner_put_expired_token(self, client, expired_token, partner_id):
        """
        Test if the put requests with an expired token returns a 401 status
        code.

        """
        assert client.put('/partners/' + partner_id,
                          headers={'Authorization': 'Bearer ' + expired_token},
                          data={'firstname': 'Daisy', 'lastname': 'Ducks',
                                'email': 'daisy' + str(uuid.uuid4()) +
                                         '@tolli.com'}).status == \
            '401 UNAUTHORIZED'

    def partner_put_not_found(self, client, jwt_token):
        """
        Test if the put requests to a non-existing partner returns a 404
        status code.

        """
        assert client.put('/partners/' + '0',
                          headers={'Authorization': 'Bearer ' + jwt_token},
                          data={'firstname': 'Daisy', 'lastname': 'Ducks',
                                'email': 'daisy' + str(uuid.uuid4()) +
                                         '@tolli.com'}).status == \
            '404 NOT FOUND'

    def partner_del_no_login(self, client, partner_id):
        """
        Test if the partner api returns the expected http status-code
        when deleting without an authorization token.

        """
        assert client.delete('/partners/' + partner_id,
                             headers={}).status == '400 BAD REQUEST'

    def partner_del_expired_token(self, client, expired_token, partner_id):
        """
        Test if the put requests with an expired token returns a 401 status
        code.

        """
        assert client.delete('/partners/' + partner_id, headers={
            'Authorization': 'Bearer ' + expired_token}).status == \
            '401 UNAUTHORIZED'

    def partner_del_not_found(self, client, token):
        """
        Test if the delete requests to a non-existing partner returns a 404
        status code.

        """
        assert client.delete('/partners/' + '0', headers={
            'Authorization': 'Bearer ' + token}).status == '404 NOT FOUND'

    def partner_put_admin_no_login(self, client, partner_id):
        """
        Test if the partner api returns the expected http status-code
        when putting without an authorization token.

        """
        assert client.put('/partners/' + partner_id + '/admin',
                          headers={}).status == '400 BAD REQUEST'

    def partner_put_admin_expired_token(self, client, expired_token,
                                        partner_id):
        """
        Test if the put requests with an expired token returns a 401 status
        code.

        """
        assert client.put('/partners/' + partner_id + '/admin', headers={
            'Authorization': 'Bearer ' + expired_token}).status == \
            '401 UNAUTHORIZED'

    def partner_put_admin_not_found(self, client, token):
        """
        Test if the partner api returns the expected http status-code
        when putting without an ID.

        """
        assert client.put('/partners/admin', headers={
            'Authorization': 'Bearer ' + token}).status == '404 NOT FOUND'

    def partner_del_admin_no_login(self, client, id):
        """
        Test if the partner api returns the expected http status-code
        when deleting without an authorization token.

        """
        assert client.delete('/partners/' + id + '/admin',
                             headers={}).status == '400 BAD REQUEST'

    def partner_del_admin_expired_token(self, client, expired_token,
                                        partner_id):
        """
        Test if the del requests with an expired token returns a 401 status
        code.

        """
        assert client.delete('/partners/' + partner_id + '/admin', headers={
            'Authorization': 'Bearer ' + expired_token}).status == \
            '401 UNAUTHORIZED'

    def partner_del_admin_not_found(self, client, token):
        """
        Test if the partner api returns the expected http status-code
        when deleting without an ID.

        """
        assert client.delete('/partners/' + '0' + '/admin', headers={
            'Authorization': 'Bearer ' + token}).status == '404 NOT FOUND'

    def partner_operation_with_deleted_user(self, client, token, id):
        """
        Test if the partner api returns the expected http status-code
        when posting.

        """
        assert client.delete('/partners/' + id, headers={
            'Authorization': 'Bearer ' + token}).status == '200 OK'

        assert client.put('/partners/' + id,
                          headers={'Authorization': 'Bearer ' + token},
                          data={'firstname': 'Daisy',
                                'lastname': 'Ducks',
                                'email': 'daisy@tolli.com'}).status == \
            '400 BAD REQUEST'

    def add_user_to_organization(self, client, token, id_organization):
        """
        Helper Method adding a User to an Organization
        """
        invitation_response = self.organization.post_organization_invitation(
            test_organization, client, self.jwtToken, id_organization)

        invitation_code = invitation_response.json['code']
        assert client.get('/invitations/' + invitation_code + '/accept',
                          headers={
                              'Authorization': 'Bearer ' + token}).status == \
            '200 OK'
