# """
# Test user api-functionality.
# """
# import pytest
# from swarm_intelligence_app.tests import test_helper
#
#
# class TestUser:
#     """
#     Class for testing API-Endpoint /me.
#
#     """
#     token = 'mock_user_001'
#     helper = test_helper.TestHelper
#
#     #@pytest.fixture
#     #def user_data(self):
#
#
#
#     def test_me_post(self, client):
#         """
#         Test if the endpoint /me returns the Status-Code '200' when a new
#         user is created with a valid token.
#         """
#         self.helper.set_up(test_helper, client)
#         assert client.post('/me', headers={
#             'Authorization': 'Token ' + self.token}).status == '200 OK'
#
#         print('Passed test for creating a new user.')
#
#     def test_me_post_activate_user(self, client):
#         """
#         Test if the endpoint /me returns the Status-Code '200' when a new
#         user is created again, after it has been deleted before
#         """
#         self.helper.set_up(test_helper, client)
#         self.test_me_post(client)
#         assert client.delete('/me', headers={
#             'Authorization': 'Token ' + self.token},
#                              data={'email': 'daisy@tolli.com'}).status == \
#                '200 OK'
#         assert client.post('/me', headers={
#             'Authorization': 'Token ' + self.token}).status == '200 OK'
#
#         print('Passed test for re-activating a new user.')
#
#     def test_me_get(self, client):
#         """
#         Test if the endpoint /me returns the Status-Code '200' when existing
#         user-data is requested with a valid token.
#         """
#         self.helper.set_up(test_helper, client)
#         self.test_me_post(client)
#         assert client.get('/me', headers={
#             'Authorization': 'Token ' + self.token}).status == '200 OK'
#         print('Passed test for getting a user.')
#
#     def test_me_put(self, client):
#         """
#         Test if the endpoint /me returns the Status-Code '200' when existing
#         user-data is updated with a valid token and valid input.
#         """
#         self.helper.set_up(test_helper, client)
#         self.test_me_post(client)
#         assert client.put('/me', headers={
#             'Authorization': 'Token ' + self.token},
#                           data={'firstname': 'Daisy', 'lastname': 'Ducks',
#                                 'email': 'daisy@tolli.com'}).status == '200 OK'
#         print('Passed test for updating a user.')
#
#     def test_me_del(self, client):
#         """
#         Test if the endpoint /me returns the Status-Code '200' when existing
#         user-data is deleted with a valid token and valid input.
#         """
#         self.helper.set_up(test_helper, client)
#         self.test_me_post(client)
#         assert client.delete('/me', headers={
#             'Authorization': 'Token ' + self.token},
#                              data={'email': 'daisy@tolli.com'}).status == \
#                '200 OK'
#         print('Passed test for deleting a user.')
#
#
# class TestUserOrganization:
#     """
#     Class for testing API-Endpoint /me/organizations.
#
#     """
#     token = 'mock_user_001'
#     helper = test_helper.TestHelper
#
#     def test_me_organizations_post(self, client):
#         """
#         Test if the endpoint /me/organization returns the Status-Code '200'
#         when a new organization is created with a valid token and valid input.
#         """
#         self.helper.set_up(test_helper, client)
#         TestUser.test_me_post(self, client)
#         assert client.post('/me/organizations', headers={
#             'Authorization': 'Token ' + self.token},
#                            data={'name': 'Dagoberts ' + 'Empire'}).status == \
#                '200 OK'
#         print('Passed test for creating a new organization.')
#
#     def test_me_organizations_get(self, client):
#         """
#         Test if the endpoint /me/organization returns the Status-Code '200'
#         when a new organization is requested with a valid token and valid
#         input.
#         """
#         self.helper.set_up(test_helper, client)
#         TestUser.test_me_post(self, client)
#         assert client.get('/me/organizations', headers={
#             'Authorization': 'Token ' + self.token}).status == \
#                '200 OK'
#         print('Passed test for getting an organization.')
#
#
# class TestUserExceptions:
#     """
#     Class for testing exceptions for API-Endpoint /me.
#
#     """
#
#     token = 'mock_user_001'
#     helper = test_helper.TestHelper
#
#     def test_me_post_no_login(self, client):
#         """
#         Test if the endpoint /me returns the Status-Code '400' when a new
#         user is created without a token.
#         """
#         self.helper.set_up(test_helper, client)
#         assert client.post('/me').status == '400 BAD REQUEST'
#         print('Passed nologin-test for creating a new user.')
#
#     def test_me_post_invalid_login(self, client):
#         """
#         Test if the endpoint /me returns the Status-Code '400' when a new
#         user is created with an invalid token.
#         """
#         self.helper.set_up(test_helper, client)
#         assert client.post('/me', headers={
#             'Authorization': 'Token ' + '2'}).status == '400 BAD REQUEST'
#         print('Passed invalid-login-test for creating a new user.')
#
#     def test_me_post_user_already_exists(self, client):
#         """
#         Test if the endpoint /me returns the Status-Code '409' while
#         creating when a user already exists.
#         """
#         self.helper.set_up(test_helper, client)
#         TestUser.test_me_post(self, client)
#         assert client.post('/me', headers={
#             'Authorization': 'Token ' + self.token}).status == '409 CONFLICT'
#         print('Passed user-already-exists-test for creating a new user.')
#
#     def test_me_get_no_login(self, client):
#         """
#         Test if the endpoint /me returns the Status-Code '400' when existing
#         user-data is requested without a token.
#         """
#         self.helper.set_up(test_helper, client)
#         TestUser.test_me_post(self, client)
#         assert client.get('/me').status == '400 BAD REQUEST'
#         print('Passed nologin-test for getting a user.')
#
#     def test_me_get_invalid_login(self, client):
#         """
#         Test if the endpoint /me returns the Status-Code '400' when existing
#         user-data is requested with an invalid token.
#         """
#         self.helper.set_up(test_helper, client)
#         TestUser.test_me_post(self, client)
#         assert client.get('/me', headers={
#             'Authorization': 'Token ' + '2'}).status == '400 BAD REQUEST'
#         print('Passed invalid-login-test for creating a new user.')
#
#     def test_me_get_no_data(self, client):
#         """
#         Test if the endpoint /me returns the Status-Code '404' when
#         non-existing user-data is requested with a valid token.
#         """
#         self.helper.set_up(test_helper, client)
#         assert client.get('/me', headers={
#             'Authorization': 'Token ' + self.token}).status == \
#                '404 NOT FOUND'
#         print('Passed no-data-test for creating a new user.')
#
#     def test_me_get_deleted_user(self, client):
#         """
#         Test if the endpoint /me returns the Status-Code '404' when
#         deleted user-data is requested with a valid token.
#         """
#         self.helper.set_up(test_helper, client)
#         TestUser.test_me_post(self, client)
#         assert client.delete('/me', headers={
#             'Authorization': 'Token ' + self.token},
#                              data={'email': 'daisy@tolli.com'}).status == \
#                '200 OK'
#         assert client.get('/me', headers={
#             'Authorization': 'Token ' + self.token}).status == \
#                '404 NOT FOUND'
#         print('Passed deleted-user-test for creating a new user.')
#
#     def test_me_put_no_login(self, client):
#         """
#         Test if the endpoint /me returns the Status-Code '400' when existing
#         user-data is updated with a missing token and valid input.
#         """
#         self.helper.set_up(test_helper, client)
#         TestUser.test_me_post(self, client)
#         assert client.put('/me',
#                           data={'firstname': 'Daisy', 'lastname': 'Ducks',
#                                 'email': 'daisy@tolli.com'}).status == \
#                '400 BAD REQUEST'
#         print('Passed nologin-test for updating a user.')
#
#     def test_me_put_invalid_login(self, client):
#         """
#         Test if the endpoint /me returns the Status-Code '400' when existing
#         user-data is updated with an invalid token and valid input.
#         """
#         self.helper.set_up(test_helper, client)
#         TestUser.test_me_post(self, client)
#         assert client.put('/me', headers={
#             'Authorization': 'Token ' + '2'},
#                           data={'firstname': 'Daisy', 'lastname': 'Ducks',
#                                 'email': 'daisy@tolli.com'}).status == \
#                '400 BAD REQUEST'
#         print('Passed invalid-login-test for updating a user.')
#
#     def test_me_put_no_data(self, client):
#         """
#         Test if the endpoint /me returns the Status-Code '404' when
#         non-existing user-data is requested with a valid token.
#         """
#         self.helper.set_up(test_helper, client)
#         assert client.put('/me', headers={
#             'Authorization': 'Token ' + self.token},
#                           data={'firstname': 'Daisy', 'lastname': 'Ducks',
#                                 'email': 'daisy@tolli.com'}).status == \
#                '404 NOT FOUND'
#         print('Passed no-data-test for updating a user.')
#
#     def test_me_put_deleted_user(self, client):
#         """
#         Test if the endpoint /me returns the Status-Code '404' when
#         deleted user-data is requested with a valid token.
#         """
#         self.helper.set_up(test_helper, client)
#         TestUser.test_me_post(self, client)
#         assert client.delete('/me', headers={
#             'Authorization': 'Token ' + self.token},
#                              data={'email': 'daisy@tolli.com'}).status == \
#                '200 OK'
#         assert client.put('/me', headers={
#             'Authorization': 'Token ' + self.token},
#                           data={'firstname': 'Daisy', 'lastname': 'Ducks',
#                                 'email': 'daisy@tolli.com'}).status == \
#                '404 NOT FOUND'
#         print('Passed deleted-user-test for updating a user.')
#
#     def test_me_del_no_login(self, client):
#         """
#         Test if the endpoint /me returns the Status-Code '400' when
#         existing user-data is deleted with a missing token and valid input.
#         """
#         self.helper.set_up(test_helper, client)
#         TestUser.test_me_post(self, client)
#         assert client.delete('/me',
#                              data={'email': 'daisy@tolli.com'}).status == \
#                '400 BAD REQUEST'
#         print('Passed nologin-test for deleting a user.')
#
#     def test_me_del_invalid_login(self, client):
#         """
#         Test if the endpoint /me returns the Status-Code '400' when existing
#         user-data is updated with an invalid token and valid input.
#         """
#         self.helper.set_up(test_helper, client)
#         TestUser.test_me_post(self, client)
#         assert client.delete('/me', headers={
#             'Authorization': 'Token ' + '2'},
#                              data={'email': 'daisy@tolli.com'}).status == \
#                '400 BAD REQUEST'
#         print('Passed invalid-login-test for deleting a user.')
#
#     def test_me_del_no_data(self, client):
#         """
#         Test if the endpoint /me returns the Status-Code '404' when
#         non-existing user-data is deleted with a valid token.
#         """
#         self.helper.set_up(test_helper, client)
#         assert client.delete('/me', headers={
#             'Authorization': 'Token ' + self.token},
#                              data={'email': 'daisy@tolli.com'}).status == \
#                '404 NOT FOUND'
#         print('Passed no-data-test for deleting a user.')
#
#     def test_me_del_deleted_user(self, client):
#         """
#         Test if the endpoint /me returns the Status-Code '404' when
#         deleted user-data is deleted with a valid token.
#         """
#         self.helper.set_up(test_helper, client)
#         TestUser.test_me_post(self, client)
#         assert client.delete('/me', headers={
#             'Authorization': 'Token ' + self.token},
#                              data={'email': 'daisy@tolli.com'}).status == \
#                '200 OK'
#         assert client.delete('/me', headers={
#             'Authorization': 'Token ' + self.token},
#                              data={'email': 'daisy@tolli.com'}).status == \
#                '404 NOT FOUND'
#         print('Passed deleted-user-test for deleting a user.')
#
#
# class TestUserOrganizationExceptions:
#     """
#     Class for testing exceptions for API-Endpoint /me/organizations.
#
#     """
#     token = 'mock_user_001'
#     helper = test_helper.TestHelper
#
#     def test_me_organizations_post_no_login(self, client):
#         """
#         Test if the endpoint /me/organizations returns the Status-Code '400'
#         when a new organization is created with a missing token and valid
#         input.
#         """
#         self.helper.set_up(test_helper, client)
#         TestUser.test_me_post(self, client)
#         assert client.post('/me/organizations',
#                            data={'name': 'Dagoberts ' + 'Empire'}).status == \
#                '400 BAD REQUEST'
#         print('Passed nologin-test for creating a new organization.')
#
#     def test_me_organizations_post_invalid_login(self, client):
#         """
#         Test if the endpoint /me/organizations returns the Status-Code '400'
#         when a new organization is created with an invalid token and valid
#         input.
#         """
#         self.helper.set_up(test_helper, client)
#         TestUser.test_me_post(self, client)
#         assert client.post('/me/organizations', headers={
#             'Authorization': 'Token ' + '2'},
#                            data={'name': 'Dagoberts ' + 'Empire'}).status == \
#                '400 BAD REQUEST'
#         print('Passed invalid-login-test for creating a new organization.')
#
#     def test_me_organizations_get_no_login(self, client):
#         """
#         Test if the endpoint /me/organizations returns the Status-Code '400'
#         when an organization is requested with a missing token and valid
#         input.
#         """
#         self.helper.set_up(test_helper, client)
#         TestUser.test_me_post(self, client)
#         assert client.get('/me/organizations').status == '400 BAD REQUEST'
#         print('Passed nologin-test for getting an organization.')
#
#     def test_me_organizations_get_invalid_login(self, client):
#         """
#         Test if the endpoint /me/organizations returns the Status-Code '400'
#         when an existing organization is requested with an invalid token.
#         """
#         self.helper.set_up(test_helper, client)
#         TestUser.test_me_post(self, client)
#         assert client.get('/me/organizations', headers={
#             'Authorization': 'Token ' + '2'}).status == '400 BAD REQUEST'
#         print('Passed invalid-login-test for getting an organization.')
#
#     def test_me_organizations_get_no_data(self, client):
#         """
#         Test if the endpoint /me/organizations returns the Status-Code '404'
#         when an non-existing organization is requested with a valid token.
#         """
#         self.helper.set_up(test_helper, client)
#         assert client.get('/me/organizations', headers={
#             'Authorization': 'Token ' + self.token}).status == \
#                '404 NOT FOUND'
#         print('Passed no-data-test for getting an organization.')
