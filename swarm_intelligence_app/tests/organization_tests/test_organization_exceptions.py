"""
Define Organization Exception Tests.

"""
from datetime import datetime, timedelta

import jwt

from swarm_intelligence_app.common import authentication
from swarm_intelligence_app.tests import test_helper
from swarm_intelligence_app.tests.organization_tests import test_organization
from swarm_intelligence_app.tests.user_tests import test_me


class TestOrganizationException:
    """
    Test API for exceptions.

    """
    helper = test_helper.TestHelper
    user = test_me.TestUser
    organization = test_organization.TestOrganization
    tokens = authentication.get_mock_user()

    def test_organization_exceptions(self, client):
        """
        Set up the Database and checks the functionality for a given set of
        mock users.

        """
        self.helper.set_up(test_helper, client)

        for jwt_token in self.tokens:
            self.user.me_post(test_me, client, jwt_token)
            jwt_token = self.helper.login(test_helper, client, jwt_token)
            self.user.me_organizations_post(test_me, client, jwt_token)
            id = self.organization.get_organization_id(
                test_organization,
                client, jwt_token)
            fields = {
                'exp': datetime.utcnow() - timedelta(
                    seconds=60
                ),
                'sub': 'mock_user_001'
            }
            encoded = jwt.encode(fields, 'top_secret', algorithm='HS256')
            expired_token = encoded.decode('utf-8')

            self.organization_post_not_allowed(client, id)
            self.organization_get_no_login(client, id)
            self.organization_get_expired_token(client, id, expired_token)
            self.organization_get_not_found(client, jwt_token)

            self.organization_put_no_login(client, id)
            self.organization_put_no_param(client, jwt_token, id)
            self.organization_put_wrong_params(client, jwt_token, id)
            self.organization_put_expired_token(client, expired_token, id)
            self.organization_put_not_found(client, jwt_token)

            self.organization_del_no_login(client, id)
            self.organization_del_no_param(client, jwt_token, id)
            self.organization_del_expired_token(client, expired_token, id)
            self.organization_del_not_found(client, jwt_token)

            self.organization_get_members_no_login(client, id)
            self.organization_get_members_expired_token(client, id,
                                                        expired_token)
            self.organization_get_members_not_found(client, jwt_token)

            self.organization_get_admins_no_login(client, id)
            self.organization_get_admins_expired_token(client, id,
                                                       expired_token)
            self.organization_get_admins_not_found(client, jwt_token)

            self.organization_post_invitation_no_login(client, id)
            self.organization_post_invitation_expired_token(client, id,
                                                            expired_token)
            self.organization_post_invitation_not_found(client, jwt_token)

            self.organization_get_invitation_no_login(client, id)
            self.organization_get_invitation_expired_token(client, id,
                                                           expired_token)
            self.organization_get_invitation_not_found(client, jwt_token)

    def organization_post_not_allowed(self, client, id):
        """
        Test if the organization api returns the expected http status-code
        when
        posting.

        """
        assert client.post(
            '/organizations/' + id).status == '405 METHOD NOT ALLOWED'

    def organization_get_no_login(self, client, id):
        """
        Test if the organization api returns the expected http status-code for
        getting
        without an authorization token.

        """
        assert client.get('/organizations/' + id).status == '400 BAD REQUEST'

    def organization_get_expired_token(self, client, id, expired_token):
        """
        Test if the get requests with an expired token returns a 401 status
        code.

        """
        assert client.get('/organizations/' + id, headers={
            'Authorization': 'Bearer ' + expired_token})\
            .status == '401 UNAUTHORIZED'

    def organization_get_not_found(self, client, jwt_token):
        """
        Test if the get requests to a non-existing organization returns a 404
        status code.

        """
        assert client.get('/organizations/' + '0',
                          headers={'Authorization': 'Bearer ' + jwt_token})\
            .status == '404 NOT FOUND'

    def organization_put_no_login(self, client, id):
        """
            Test if the organization api returns the expected http status-code
            for
            putting
        without an authorization token.

        """
        assert client.put('/organizations/' + id, headers={},
                          data={'name': 'Daisy'}).status == '400 BAD REQUEST'

    def organization_put_wrong_params(self, client, jwt_token, id):
        """
        Test if the organization api returns the expected http status-code
        when
        putting with wrong parameters.

        """
        assert client.put('/organizations/' + id,
                          headers={'Authorization': 'Bearer ' + jwt_token},
                          data={'firstname': 'Daisy',
                                'lastname': 'Ducks',
                                'email': 'daisy@tolli.com'}).status == \
            '400 BAD REQUEST'

    def organization_put_no_param(self, client, jwt_token, id):
        """
        Test if the organization api returns the expected http status-code
        when
        putting without parameters.

        """
        assert client.put('/organizations/' + id, headers={
            'Authorization': 'Bearer ' + jwt_token},
                          data={}).status == '400 BAD REQUEST'

    def organization_put_expired_token(self, client, expired_token, id):
        """
        Test if the put requests with an expired token returns a 401 status
        code.

        """
        assert client.put('/organizations/' + id, headers={
            'Authorization': 'Bearer ' + expired_token},
                          data={'firstname': 'Daisy',
                                'lastname': 'Ducks',
                                'email': 'daisy@tolli.com'}).status == \
            '401 UNAUTHORIZED'

    def organization_put_not_found(self, client, jwt_token):
        """
        Test if the put requests to a non-existing organization returns a 404
        status code.

        """
        assert client.put('/organizations/' + '0', headers={
            'Authorization': 'Bearer ' + jwt_token},
                          data={'firstname': 'Daisy',
                                'lastname': 'Ducks',
                                'email': 'daisy@tolli.com'}).status == \
            '404 NOT FOUND'

    def organization_del_no_login(self, client, id):
        """
        Test if the organization api returns the expected http status-code for
        deleting
        without an authorization token.

        """
        assert client.delete('/organizations/' + id, headers={},
                             data={'name': 'Daisy'}).status == \
            '400 BAD REQUEST'

    def organization_del_no_param(self, client, jwt_token, id):
        """
        Test if the organization api returns the expected http status-code
        when
        deleting without parameters.

        """
        assert client.delete('/organizations/' + id, headers={
            'Authorization': 'Bearer ' + jwt_token},
                             data={}).status == '204 NO CONTENT'

    def organization_del_expired_token(self, client, expired_token, id):
        """
        Test if the del requests with an expired token returns a 401
        status code.

        """
        assert client.delete('/organizations/' + id, headers={
            'Authorization': 'Bearer ' + expired_token},
                          data={}).status == '401 UNAUTHORIZED'

    def organization_del_not_found(self, client, jwt_token):
        """
        Test if the put requests to a non-existing organization
        returns a 404 status code.

        """
        assert client.delete('/organizations/' + '0', headers={
            'Authorization': 'Bearer ' + jwt_token},
                             data={}).status == '404 NOT FOUND'

    def organization_get_members_no_login(self, client, id):
        """
        Test if the organization api returns the expected http status-code for
        getting
        without an authorization token.

        """
        assert client.get('/organizations/' + id + '/members',
                          headers={}).status == '400 BAD REQUEST'

    def organization_get_members_expired_token(self, client, id,
                                               expired_token):
        """
        Test if the get requests with an expired token returns a 401
        status code.

        """
        assert client.get('/organizations/' + id + '/members', headers={
            'Authorization': 'Bearer ' + expired_token},
                             data={}).status == '401 UNAUTHORIZED'

    def organization_get_members_not_found(self, client, jwt_token):
        """
        Test if the get requests to a non-existing organization
        returns a 404 status code.

        """
        assert client.get('/organizations/' + '0' + '/members', headers={
            'Authorization': 'Bearer ' + jwt_token},
                             data={}).status == '404 NOT FOUND'

    def organization_get_admins_no_login(self, client, id):
        """
        Test if the organization api returns a valid http status-code for
        getting
        without an authorization token.
        """
        assert client.get('/organizations/' + id + '/admins',
                          headers={}).status == '400 BAD REQUEST'

    def organization_get_admins_expired_token(self, client, id,
                                               expired_token):
        """
        Test if the get requests with an expired token returns a 401
        status code.

        """
        assert client.get('/organizations/' + id + '/admins', headers={
            'Authorization': 'Bearer ' + expired_token},
                             data={}).status == '401 UNAUTHORIZED'

    def organization_get_admins_not_found(self, client, jwt_token):
        """
        Test if the get requests to a non-existing organization
        returns a 404 status code.

        """
        assert client.get('/organizations/' + '0' + '/admins', headers={
            'Authorization': 'Bearer ' + jwt_token},
                             data={}).status == '404 NOT FOUND'

    def organization_post_invitation_no_login(self, client, id):
        """
        Test if the organization api returns a valid http status-code for
        getting
        without an authorization token.

        """
        assert client.post('/organizations/' + id + '/invitations', headers={},
                           data={
                               'email': 'donaldo@ducko.com',
                               'organization_id': id}).status == '400 BAD ' \
                                                                 'REQUEST'

    def organization_post_invitation_expired_token(self, client, id,
                                                   expired_token):
        """
        Test if the post requests with an expired token returns a 401
        status code.

        """
        assert client.post('/organizations/' + id + '/invitations', headers={
            'Authorization': 'Bearer ' + expired_token},
                           data={
                               'email': 'donaldo@ducko.com',
                               'organization_id': id})\
            .status == '401 UNAUTHORIZED'

    def organization_post_invitation_not_found(self, client, jwt_token):
        """
        Test if the post requests to a non-existing organization
        returns a 404 status code.

        """
        assert client.post('/organizations/' + '0' + '/invitations', headers={
            'Authorization': 'Bearer ' + jwt_token},
                          data={
                              'email': 'donaldo@ducko.com',
                              'organization_id': id})\
            .status == '404 NOT FOUND'

    def organization_get_invitation_no_login(self, client, id):
        """
        Test if the organization api returns a valid http status-code for
        getting
        without an authorization token.

        """
        assert client.get('/organizations/' + id + '/invitations',
                          headers={}).status == '400 BAD REQUEST'

    def organization_get_invitation_expired_token(self, client, id,
                                                   expired_token):
        """
        Test if the get requests with an expired token returns a 401
        status code.

        """
        assert client.get('/organizations/' + id + '/invitations', headers={
            'Authorization': 'Bearer ' + expired_token},
                           data={}).status == '401 UNAUTHORIZED'

    def organization_get_invitation_not_found(self, client, jwt_token):
        """
        Test if the get requests to a non-existing organization
        returns a 404 status code.

        """
        assert client.get('/organizations/' + '0' + '/invitations', headers={
            'Authorization': 'Bearer ' + jwt_token},
                          data={}).status == '404 NOT FOUND'
