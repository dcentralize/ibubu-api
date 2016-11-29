from unittest import TestCase
from flask import Flask, url_for, jsonify
import urllib
import requests
import json


class TestCircle:
    token_user1 = "mock_user_001"
    token_user2 = "mock_user_002"

    def setUp(self, client):
        assert client.get(url_for('setup')).status == '200 OK'

        assert client.post("/me", headers={
            'Authorization': 'Token  ' + self.token_user1}).status == '200 OK'

        assert client.post("/me", headers={
            'Authorization': 'Token  ' + self.token_user2}).status == '200 OK'
        assert client.post("/me/organizations",
                           headers={
                               'Authorization': 'Token ' + self.token_user1},
                           data={
                               'name': 'CheGuevara GmbH'}).status == '200 OK'

    def test_get_circle(self, client):
        self.setUp(client)

        assert client.get("/circles/1", headers={
            'Authorization': 'Token ' + self.token_user1}).status == '200 OK'
        assert client.get("/circles/2",
                          headers={
                              'Authorization': 'Token ' +
                                               self.token_user1}).status == \
               '404 NOT FOUND'
        data_circle1 = client.get("/circles/1", headers={'Authorization':
                                                             'Token ' +
                                                             self.token_user1}
                                  ).json['data']
        assert data_circle1['organization_id'] == 1
        assert data_circle1['name'] == 'General'
        assert data_circle1['id'] == 1
        assert data_circle1['purpose'] is None
        assert data_circle1['strategy'] is None

    def test_put_circle(self, client):
        self.setUp(client)
        data_circle1 = client.get("/circles/1", headers={'Authorization':
                                                             'Token ' +
                                                             self.token_user1}
                                  ).json['data']
        assert data_circle1['organization_id'] == 1
        assert data_circle1['name'] == 'General'
        assert data_circle1['id'] == 1
        assert data_circle1['purpose'] is None
        assert data_circle1['strategy'] is None

        assert client.put("/circles/1", headers={
            'Authorization': 'Token ' + self.token_user1},
                          data={'name': 'changeCircleName'}).status == '200 OK'
        data_circle1 = client.get("/circles/1", headers={'Authorization':
                                                             'Token ' +
                                                             self.token_user1}
                                  ).json['data']
        assert data_circle1['organization_id'] == 1
        assert data_circle1['name'] == 'changeCircleName'
        assert data_circle1['id'] == 1
        assert data_circle1['purpose'] is None
        assert data_circle1['strategy'] is None

    def test_delete_circle(self, client):
        self.setUp(client)
        assert client.get("/circles/1", headers={'Authorization': 'Token ' +

                                                                  self.token_user1}).status == '200 OK'
        assert client.delete("/circles/1", headers={
            'Authorization': 'Token ' + self.token_user1}).status == '200 OK'
        assert client.get("/circles/1", headers={'Authorization': 'Token ' +

                                                                  self.token_user1}).status == '404 NOT FOUND'

    def test_post_subcircle(self, client):
        self.setUp(client)
        assert client.get("circles/1", headers={'Authorization': 'Token ' +
                                                                 self.token_user1}).status == \
               '200 OK'

        assert client.post("/circles/1/subcircles",
                           headers={'Authorization': 'Token ' +
                                                     self.token_user1},
                           data={'name': 'blabla subcircle'}
                           ).status == '200 OK'
        sub_circle = client.get("/circles/1/subcircles",
                                headers={'Authorization': 'Token ' +
                                                          self.token_user1}).json[
            'data'][0]

        assert sub_circle['name'] == 'blabla subcircle'
        assert sub_circle['circle_id'] == 1
        assert sub_circle['purpose'] is None
        assert sub_circle['strategy'] is None
        assert sub_circle['id'] == 2
        assert client.post("/circles/1/subcircles",
                           headers={'Authorization': 'Token ' +
                                                     self.token_user1},
                           data={'name': 'blabla subcircle2'})
        sub_circle = client.get("/circles/1/subcircles",
                                headers={'Authorization': 'Token ' +
                                                          self.token_user1}).json[
            'data'][1]

        assert sub_circle['name'] == 'blabla subcircle2'
        assert sub_circle['circle_id'] == 1
        assert sub_circle['purpose'] is None
        assert sub_circle['strategy'] is None
        assert sub_circle['id'] == 3

    def test_put_circle_member(self, client):
        self.setUp(client)
        client.post("/me/organizations", headers={'Authorization': 'Token ' +
                                                                   self.token_user1},
                    data={'name': 'OrganizationName GmbH'})
        invitation_code = client.post("/organizations/1/invitations",
                                      headers={
                                          'Authorization': 'Token ' + self.token_user1},
                                      data={
                                          'email': 'dagobert@gmail.de'}).json[
            'data']['code']

        assert client.get("/invitations/" + invitation_code + "/accept",
                          headers={'Authorization': 'Token ' +
                                                    self.token_user2}).status == '200 OK'
        assert client.get("/organizations/1/members", headers={
            'Authorization': 'Token ' + self.token_user1}).json['data'][1][
                   'email'] == 'dagobert@gmail.de'
        partner_id = client.get("/organizations/1/members", headers={
            'Authorization': 'Token ' + self.token_user1}).json['data'][1][
            'id']
        assert client.put("/circles/1/members/" + str(partner_id), headers={
            'Authorization': 'Token ' + self.token_user1}).status == '200 OK'

        assert len(client.get("circles/1/members",
                              headers={'Authorization': 'Token ' +
                                                        self.token_user1}).json[
                       'data']) == 1

        assert \
            client.get("circles/1/members", headers={
                'Authorization': 'Token ' + self.token_user1}).json[
                'data'][0]['email'] == "dagobert@gmail.de"

    def test_put_circle_member_wrong_auth(self, client):
        self.setUp(client)
        client.post("/me/organizations", headers={'Authorization': 'Token ' +
                                                                   self.token_user1},
                    data={'name': 'OrganizationName GmbH'})
        invitation_code = client.post("/organizations/1/invitations",
                                      headers={
                                          'Authorization': 'Token ' + self.token_user1},
                                      data={
                                          'email': 'dagobert@gmail.de'}).json[
            'data']['code']

        assert client.get("/invitations/" + invitation_code + "/accept",
                          headers={'Authorization': 'Token ' +
                                                    self.token_user2}).status == '200 OK'
        assert client.get("/organizations/1/members", headers={
            'Authorization': 'Token ' + self.token_user1}).json['data'][1][
                   'email'] == 'dagobert@gmail.de'
        partner_id = client.get("/organizations/1/members", headers={
            'Authorization': 'Token ' + self.token_user1}).json['data'][1][
            'id']
        assert client.put("/circles/1/members/" + str(partner_id), headers={
            'Authorization': 'Token ' + 'wrongAuth'}).status == '400 BAD ' \
                                                                'REQUEST'


    def test_delete_unknown_circle_member(self, client):
        self.setUp(client)

        client.post("/me/organizations",
                    headers={'Authorization': 'Token ' +
                                              self.token_user1},
                    data={'name': 'OrganizationName GmbH'})
        invitation_code = client.post("/organizations/1/invitations",
                                      headers={
                                          'Authorization': 'Token ' + self.token_user1},
                                      data={
                                          'email': 'dagobert@gmail.de'}).json[
            'data']['code']

        assert client.get("/invitations/" + invitation_code + "/accept",
                          headers={'Authorization': 'Token ' +
                                                    self.token_user2}).status == '200 OK'
        assert client.get("/organizations/1/members", headers={
            'Authorization': 'Token ' + self.token_user1}).json['data'][1][
                   'email'] == 'dagobert@gmail.de'
        partner_id = client.get("/organizations/1/members", headers={
            'Authorization': 'Token ' + self.token_user1}).json['data'][1][
            'id']
        assert client.put("/circles/1/members/" + str(partner_id),
                          headers={
                              'Authorization': 'Token ' + self.token_user1}).status == '200 OK'

        assert client.delete("circles/1/members/10", headers={
            'Authorization': 'Token ' + self.token_user1}).status == '404 ' \
                                                                     'NOT ' \
                                                                     'FOUND'

    def test_delete_circle_member_wrong_auth(self, client):
        self.setUp(client)

        client.post("/me/organizations",
                    headers={'Authorization': 'Token ' +
                                              self.token_user1},
                    data={'name': 'OrganizationName GmbH'})
        invitation_code = client.post("/organizations/1/invitations",
                                      headers={
                                          'Authorization': 'Token ' + self.token_user1},
                                      data={
                                          'email': 'dagobert@gmail.de'}).json[
            'data']['code']

        assert client.get("/invitations/" + invitation_code + "/accept",
                          headers={'Authorization': 'Token ' +
                                                    self.token_user2}).status == '200 OK'
        assert client.get("/organizations/1/members", headers={
            'Authorization': 'Token ' + self.token_user1}).json['data'][1][
                   'email'] == 'dagobert@gmail.de'
        partner_id = client.get("/organizations/1/members", headers={
            'Authorization': 'Token ' + self.token_user1}).json['data'][1][
            'id']
        assert client.put("/circles/1/members/" + str(partner_id),
                          headers={
                              'Authorization': 'Token ' + self.token_user1}).status == '200 OK'

        assert client.delete("circles/1/members/" + str(partner_id),
                               headers={
            'Authorization': 'Token ' + "4334"}).status == '400 BAD REQUEST'

    def test_delete_circle_member(self, client):
        self.setUp(client)
        client.post("/me/organizations",
                    headers={'Authorization': 'Token ' +
                                              self.token_user1},
                    data={'name': 'OrganizationName GmbH'})
        invitation_code = client.post("/organizations/1/invitations",
                                      headers={
                                          'Authorization': 'Token ' + self.token_user1},
                                      data={
                                          'email': 'dagobert@gmail.de'}).json[
            'data']['code']

        assert client.get("/invitations/" + invitation_code + "/accept",
                          headers={'Authorization': 'Token ' +
                                                    self.token_user2}).status == '200 OK'
        assert client.get("/organizations/1/members", headers={
            'Authorization': 'Token ' + self.token_user1}).json['data'][1][
                   'email'] == 'dagobert@gmail.de'
        partner_id = client.get("/organizations/1/members", headers={
            'Authorization': 'Token ' + self.token_user1}).json['data'][1][
            'id']
        assert client.put("/circles/1/members/" + str(partner_id),
                          headers={
                              'Authorization': 'Token ' + self.token_user1}).status == '200 OK'

        assert client.delete("circles/1/members/" + str(partner_id), headers={
            'Authorization': 'Token ' + self.token_user1}).status == \
               '200 OK'
        assert len(client.get("circles/1/members",
                              headers={'Authorization': 'Token ' +
                                                        self.token_user1}).json[
                       'data']) == 0

    def test_delete_deleted_circle_member(self, client):
        self.setUp(client)
        client.post("/me/organizations",
                    headers={'Authorization': 'Token ' +
                                              self.token_user1},
                    data={'name': 'OrganizationName GmbH'})
        invitation_code = client.post("/organizations/1/invitations",
                                      headers={
                                          'Authorization': 'Token ' + self.token_user1},
                                      data={
                                          'email': 'dagobert@gmail.de'}).json[
            'data']['code']

        assert client.get("/invitations/" + invitation_code + "/accept",
                          headers={'Authorization': 'Token ' +
                                                    self.token_user2}).status == '200 OK'
        assert client.get("/organizations/1/members", headers={
            'Authorization': 'Token ' + self.token_user1}).json['data'][1][
                   'email'] == 'dagobert@gmail.de'
        partner_id = client.get("/organizations/1/members", headers={
            'Authorization': 'Token ' + self.token_user1}).json['data'][1][
            'id']
        assert client.put("/circles/1/members/" + str(partner_id),
                          headers={
                              'Authorization': 'Token ' + self.token_user1}).status == '200 OK'

        assert client.delete("circles/1/members/" + str(partner_id), headers={
            'Authorization': 'Token ' + self.token_user1}).status == \
               '200 OK'
        assert len(client.get("circles/1/members",
                              headers={'Authorization': 'Token ' +
                                                        self.token_user1}).json[
                       'data']) == 0
        print(client.delete("circles/1/members/" + str(partner_id),
                            headers={'Authorization': 'Token ' +
                                                      self.token_user1}).status)
