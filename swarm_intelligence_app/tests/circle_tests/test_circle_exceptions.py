"""
Test user api-functionality.
"""

from swarm_intelligence_app.tests import test_helper
from swarm_intelligence_app.common import authentication
from swarm_intelligence_app.tests.user_tests import test_me
from swarm_intelligence_app.tests.circle_tests import test_circle


class TestCircle:
    """
    Class for testing user api-functionality.
    """
    user = test_me.TestUser
    helper = test_helper.TestHelper
    circle = test_circle.TestCircle
    tokens = authentication.get_mock_user()

    def test_organization(self, client):
        self.helper.set_up(test_helper, client)

        for token in self.tokens:
            self.user.me_post(test_me, client, token)
            jwtToken = self.helper.login(test_helper, client, token)
            self.user.me_organizations_post(test_me, client, jwtToken)
            id = self.circle.get_organization_id(test_circle, client, jwtToken)
            circleId = self.circle.get_circle_id(test_circle, client, jwtToken,
                                                 id)
            partnerId = self.circle.get_partner_id(test_circle, client, id,
                                                   jwtToken)
            roleId = self.circle.get_role_id(test_circle, client, jwtToken,
                                             circleId)

            self.circle_get_no_login(client, circleId)
            self.circle_put_no_login(client, circleId)
            self.circle_put_no_param(client, circleId, jwtToken)
            self.circle_put_wrong_param(client, circleId, jwtToken)
            self.circle_delete_no_login(client, circleId)
            self.circle_post_roles_no_login(client, circleId)
            self.circle_post_roles_no_param(client, circleId, jwtToken)
            self.circle_post_roles_wrong_param(client, circleId, jwtToken)
            self.circle_get_roles_no_login(client, circleId)
            self.circle_put_subcircles_no_login(client, roleId)
            self.circle_put_subcircles_no_param(client, circleId, jwtToken)
            self.circle_put_subcircles_wrong_param(client, circleId, jwtToken)
            self.circle_get_subcircles_no_login(client, circleId)
            self.circle_get_members_no_login(client, circleId)
            self.circle_put_partner_no_login(client, circleId, partnerId)
            self.circle_delete_partner_no_login(client, circleId, partnerId)
            self.circle_post_domain_no_login(client, circleId)
            self.circle_post_domain_no_param(client, circleId, jwtToken)
            self.circle_get_domain_no_login(client, circleId)
            self.circle_post_accountability_no_login(client, circleId)
            self.circle_post_accountability_no_param(client, circleId,
                                                      jwtToken)
            self.circle_get_accountability_no_login(client, circleId)

    def circle_get_no_login(self, client, circleId):
        """
        Test if the get requests without a valid token returns a 400 status
        code.
        """
        assert client.get('/circles/' + circleId).status == '400 BAD REQUEST'

    def circle_put_no_login(self, client, circleId):
        """
        Test if the put request without a valid token returns a 400 status
        code.
        """
        assert client.put('/circles/' + circleId, headers={},
                          data={'name': 'Name2',
                                'purpose': 'Purpose2',
                                'strategy': 'Strategy2'})\
                   .status == '400 BAD REQUEST'

    def circle_put_no_param(self, client, circleId, token):
        """
        Test if the put request with a missing body returns a 400 status code.
        """
        assert client.put('/circles/' + circleId, headers={
            'Authorization': 'Bearer ' + token},
                          data={}) \
                   .status == '400 BAD REQUEST'

    def circle_put_wrong_param(self, client, circleId, token):
        """
        Test if the put request without a correct body returns a 400 status
        code.
        """
        assert client.put('/circles/' + circleId, headers={
            'Authorization': 'Bearer ' + token},
                          data={'purpose': 'Purpose2',
                                'strategy': 'Strategy2'}) \
            .status == '400 BAD REQUEST'

    def circle_delete_no_login(self, client, circleId):
        """
        Test if the delete request without a valid token returns a 400
        status code.
        """
        assert client.delete('/circles/' + circleId, headers={},
                             data={}).status == '400 BAD REQUEST'

    def circle_post_roles_no_login(self, client, circleId):
        """
        Test if the post request without a valid token returns a 400 status
        code.
        """
        assert client.post('/circles/' + circleId + '/roles', headers={},
                           data={'name': 'NewRole',
                                 'purpose': 'This is a new Role added to a '
                                            'Circle.'}).status \
            == '400 BAD REQUEST'

    def circle_post_roles_no_param(self, client, circleId, token):
        """
        Test if the post request with a missing body returns a 400 status code.
        """
        assert client.post('/circles/' + circleId + '/roles', headers={
            'Authorization': 'Bearer ' + token},
                           data={}).status \
               == '400 BAD REQUEST'

    def circle_post_roles_wrong_param(self, client, circleId, token):
        """
        Test if the post request without a correct body returns a 400 status
        code.
        """
        assert client.post('/circles/' + circleId + '/roles', headers={
            'Authorization': 'Bearer ' + token},
                           data={'purpose': 'This is a new Role added to a '
                                            'Circle.'}).status \
               == '400 BAD REQUEST'

    def circle_get_roles_no_login(self, client, circleId):
        """
        Test if the get request without a valid token returns a 400 status
        code.
        """
        assert client.get('/circles/' + circleId + '/roles', headers={},
                           data={}).status == '400 BAD REQUEST'

    def circle_put_subcircles_no_login(self, client, roleId):
        """
        Test if the put request without a valid token returns a 400 status
        code.
        """
        assert client.put('/roles/' + roleId + '/circle', headers={},
                          data={'name': 'NewRole',
                                'purpose': 'This is a new Role added to a '
                                           'Circle.',
                                'strategy': 'NewStrategy'})\
            .status == '400 BAD REQUEST'

    def circle_put_subcircles_no_param(self, client, roleId, token):
        """
        Test if the put request with a missing body returns a 400 status code.
        """
        assert client.put('/roles/' + roleId + '/circle', headers={
            'Authorization': 'Bearer ' + token}, data={}).status ==\
            '400 BAD REQUEST'

    def circle_put_subcircles_wrong_param(self, client, roleId, token):
        """
        Test if the put request without a correct body returns a 400 status
        code.
        """
        assert client.put('/roles/' + roleId + '/circle', headers={
            'Authorization': 'Bearer ' + token},
                          data={'name': 'NewRole', 'strategy': 'NewStrategy'})\
            .status == '400 BAD REQUEST'

    def circle_get_subcircles_no_login(self, client, roleId):
        """
        Test if the get request without a valid token returns a 400 status
        code.
        """
        assert client.put('/roles/' + roleId + '/circle', headers={
        }).status == '400 BAD REQUEST'

    def circle_get_members_no_login(self, client, circleId):
        """
        Test if the get request without a valid token returns a 400 status
        code.
        """
        assert client.get('/circles/' + circleId + '/members',
                          headers={}).status == '400 BAD REQUEST'

    def circle_put_partner_no_login(self, client, circleId, partnerId):
        """
        Test if the put request without a valid token returns a 400 status
        code.
        """
        assert client.put('/circles/' + circleId + '/members/' + partnerId,
                          headers={},
                          data={'firstname': 'Manuel', 'lastname':
                              'Neuer', 'email': 'm.neuer@mail.com'}).status \
               == '400 BAD REQUEST'

    def circle_delete_partner_no_login(self, client, circleId, partnerId):
        """
        Test if the delete request without a valid token returns a 400 status
        code.
        """
        assert client.delete('/circles/' + circleId + '/members/' + partnerId,
                             headers={}
                             ).status == '400 BAD REQUEST'

    def circle_post_domain_no_login(self, client, circleId):
        """
        Test if the post request without a valid token returns a 400 status
        code.
        """
        assert client.post('/circles/' + circleId + '/domains',
                           headers={},
                           data={'name': 'DomainName'}).status == '400 BAD ' \
                                                                  'REQUEST'
    def circle_post_domain_no_param(self, client, circleId, token):
        """
        Test if the post request with a missing body returns a 400 status
        code.
        """
        assert client.post('/circles/' + circleId + '/domains',
                           headers={'Authorization': 'Bearer ' + token},
                           data={}).status == '400 BAD REQUEST'

    def circle_get_domain_no_login(self, client, circleId):
        """
        Test if the get request without a valid token returns a 400 status
        code.
        """
        assert client.get('/circles/' + circleId + '/domains',
                          headers={}).status == '400 BAD REQUEST'

    def circle_post_accountability_no_login(self, client, circleId):
        """
        Test if the post request without a valid token returns a 400
        status code.
        """
        assert client.post('/circles/' + circleId + '/accountabilities',
                           headers={},
                           data={'name': 'AccName'}).status == '400 BAD ' \
                                                               'REQUEST'

    def circle_post_accountability_no_param(self, client, circleId, token):
        """
        Test if the post request with a missing body returns a 400 status code.
        """
        assert client.post('/circles/' + circleId + '/accountabilities',
                           headers={'Authorization': 'Bearer ' + token},
                           data={}).status == '400 BAD REQUEST'

    def circle_get_accountability_no_login(self, client, circleId):
        """
        Test if the get request without a valid token returns a 400 status
        code.
        """
        assert client.get('/circles/' + circleId + '/accountabilities',
                          headers={}).status == '400 BAD REQUEST'
