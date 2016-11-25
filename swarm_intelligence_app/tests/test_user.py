"""
Test user api-functionality.
"""
from flask import url_for


class TestUser:
    """
    Class for testing user api-functionality.

    """
    token = 'mock_user_001'

    def test_signin(self, client):
        """
        Test if the signin-page returns a valid http status-code.
        """
        assert client.get(url_for('signin')).status == '200 OK'
        print('Passed test for sign in.')

    def test_setup(self, client):
        """
        Test if the setup-page returns a valid http status-code.
        """
        assert client.get(url_for('setup')).status == '200 OK'
        print('Passed test for setup.')

    def test_populate(self, client):
        """
        Test if the populate-page returns a valid http status-code.
        """
        assert client.get(url_for('populate')).status == '200 OK'
        print('Passed test for populating the database.')

    def test_me_post(self, client):
        """
        Test if the me-page returns a valid http status-code when posting.
        """
        assert client.post('/me', headers={
            'Authorization': 'Token ' + self.token}).status == '200 OK'
        print('Passed test for creating a new user.')

    # def test_me_postnologin(self, client):
    #     """
    #     Test if the me-page returns a valid http status-code when posting.
    #     """
    #     assert client.post('/me').status == '400 BAD REQUEST'
    #     print("Passed nologin-test for creating a new user.")

    def test_me_get(self, client):
        """
        Test if the me-page returns a valid http status-code when getting.
        """
        assert client.get('/me', headers={
            'Authorization': 'Token ' + self.token}).status == '200 OK'
        print('Passed test for getting a user.')

    # def test_me_getnologin(self, client):
    #     """
    #     Test if the me-page returns a valid http status-code when getting.
    #     """
    #     assert client.get('/me').status == '400 BAD REQUEST'
    #     print("Passed nologin-test for getting a user.")

    def test_me_put(self, client):
        """
        Test if the me-page returns a valid http status-code when putting.
        """
        assert client.put('/me', headers={
            'Authorization': 'Token ' + self.token},
                          data={'firstname': 'Daisy', 'lastname': 'Ducks',
                                'email': 'daisy@tolli.com'}).status == '200 OK'
        print('Passed test for updating a user.')

    # def test_me_putnologin(self, client):
    #     """
    #     Test if the me-page returns a valid http status-code when putting.
    #     """
    #     assert client.put('/me', headers={}, data={'firstname': 'Daisy',
    # 'lastname': 'Ducks',
    #                                 'email': 'daisy@tolli.com'}).status == \
    #                '400 BAD REQUEST'
    #     print("Passed nologin-test for updating a user.")

    def test_me_putnoparam(self, client):
        """
        Test if the me-page returns a valid http status-code when putting.
        """
        assert client.put('/me', headers={
            'Authorization': 'Token ' + self.token},
                          data={}).status == '400 BAD REQUEST'
        print('Passed noparam-test for updating a user.')

    def test_me_del(self, client):
        """
        Test if the me-page returns a valid http status-code when deleting.
        """
        assert client.delete('/me', headers={
            'Authorization': 'Token ' + self.token},
                             data={'email': 'daisy@tolli.com'}).status == \
               '200 OK'
        print('Passed test for deleting a user.')

    # def test_me_delnologin(self, client):
    #     """
    #     Test if the me-page returns a valid http status-code when deleting.
    #     """
    #     assert client.delete('/me', headers={},
    #                          data={'firstname': 'Daisy', 'lastname': 'Ducks',
    #                                'email': 'daisy@tolli.com'}).status == \
    #            '400 BAD REQUEST'
    #     print("Passed nologin-test for deleting a user.")

    # def test_me_delnoparam(self, client):
    #     """
    #     Test if the me-page returns a valid http status-code when deleting.
    #     """
    #     assert client.delete('/me', headers={
    #         'Authorization': 'Token ' + self.token},
    #                          data={}).status == '400 BAD REQUEST'
    #     print("Passed noparam-test for deleting a user.")

    def test_me_organizations_post(self, client):
        """
        Test if the me-organizations-page returns a valid http status-code.
        when posting.
        """
        self.test_me_post(client)
        assert client.post('/me/organizations', headers={
            'Authorization': 'Token ' + self.token},
                           data={'name': 'Dagoberts ' + 'Empire'}).status == \
               '200 OK'
        print('Passed test for creating a new organization.')

    # def test_me_organizations_postnologin(self, client):
    #     """
    #     Test if the me-organizations-page returns a valid http
    # status-code
    #     when posting.
    #     """
    #     self.test_me_post(client)
    #     assert client.post('/me/organizations', headers={},
    #                       data={'name': 'Dagoberts ' +
    # 'Empire'}).status == \
    #            '400 BAD REQUEST'
    #     print("Passed test for creating a new organization.")

    # def test_me_organizations_postnoparam(self, client):
    #     """
    #     Test if the me-organizations-page returns a valid http
    #     status-code
    #     when posting.
    #     """
    #     assert client.post('/me/organizations', headers={
    #         'Authorization': 'Token ' + self.token},
    #                        data={}).status == '200 OK'
    #     print("Passed noparam-test for creating a new organization.")
