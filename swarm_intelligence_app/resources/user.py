"""
Define the classes for the user API.

"""
from datetime import datetime, timedelta

import jwt
import requests

from flask import abort, current_app, g
from flask_restful import reqparse, Resource
from swarm_intelligence_app.common.authentication import auth
from swarm_intelligence_app.models import db
from swarm_intelligence_app.models.circle import Circle as CircleModel
from swarm_intelligence_app.models.organization import Organization as \
    OrganizationModel
from swarm_intelligence_app.models.partner import Partner as PartnerModel
from swarm_intelligence_app.models.partner import PartnerType
from swarm_intelligence_app.models.role import Role as RoleModel
from swarm_intelligence_app.models.role import RoleType
from swarm_intelligence_app.models.user import User as UserModel

mock_users = {
    'mock_user_001': {
        'sub': 'mock_user_001',
        'given_name': 'Donald',
        'family_name': 'Duck',
        'email': 'donald@gmail.de'
    },
    'mock_user_002': {
        'sub': 'mock_user_002',
        'given_name': 'Dagobert',
        'family_name': 'Duck',
        'email': 'dagobert@gmail.de'
    }
}


class UserRegistration(Resource):
    """
    Define the endpoints for the user registration.

    """
    def post(self):
        """
        .. :quickref: User; Register a user.

        Register a user.

        To create a user the data provided by google is taken into
        consideration. If a user with the provided google id does not exist, 
        the user is created. If a user exists and is deactivated, the user is 
        activated. If a user does not exist, the user is created with the data 
        provided by google.

        **Example request**:

        .. sourcecode:: http

            POST /register HTTP/1.1
            Host: example.com
            Authorization: Token <token>

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 201 Created
            Content-Type: application/json

            {
                'access_token': <token>
            }

        :reqheader Authorization: Google ID token to authenticate

        :resheader Content-Type: data is received as application/json

        :>json string access_token: A JSON Web Token

        :status 201: User is created
        :status 400: Token is not well-formed
        :status 401: Token is not authorized by google
        :status 409: User already exists

        """
        parser = reqparse.RequestParser()
        parser.add_argument('Authorization', location='headers', required=True)
        args = parser.parse_args()

        authorization = args['Authorization']
        credentials = authorization.split(' ')

        if len(credentials) != 2:
            abort(400)

        if credentials[0] != 'Token':
            abort(400)

        if credentials[1] == 'mock_user_001':
            data = mock_users['mock_user_001']
        elif credentials[1] == 'mock_user_002':
            data = mock_users['mock_user_002']
        else:
            response = requests.get('https://www.googleapis.com/oauth2/v3/'
                                    'tokeninfo?id_token=' + credentials[1])

            if response.status_code != 200:
                abort(401)

            data = response.json()
            if data['aud'] != '806916571874-7tnsbrr22526ioo36l8njtqj2st8nn54' \
                              '.apps.googleusercontent.com':
                abort(401)

        user = UserModel.query.filter_by(google_id=data['sub']).first()

        if user is not None and user.is_active is True:
            abort(409, 'Cannot create user. The user already exists.')

        if user is not None and user.is_active is False:
            user.is_active = True
        else:
            user = UserModel(
                data['sub'],
                data['given_name'],
                data['family_name'],
                data['email']
            )
            db.session.add(user)

        db.session.commit()

        fields = {
            'exp': datetime.utcnow() + timedelta(
                seconds=current_app.config['SI_JWT_EXPIRATION']),
            'sub': user.google_id
        }

        encoded = jwt.encode(
            fields, current_app.config['SI_JWT_SECRET'], algorithm='HS256')

        return {
            'access_token': encoded.decode('utf-8')
        }, 201


class UserLogin(Resource):
    """
    Define the endpoints for the user login.

    """
    def get(self):
        """
        .. :quickref: User; Login a user.

        Login a user.

        **Example request**:

        .. sourcecode:: http

            GET /login HTTP/1.1
            Host: example.com
            Authorization: Token <token>

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: application/json

            {
                'access_token': <token>
            }

        :reqheader Authorization: Google ID token to authenticate

        :resheader Content-Type: data is received as application/json

        :>json string access_token: A JSON Web Token

        :status 200: User is logged in
        :status 400: Token is not well-formed
        :status 401: Token is not authorized by google
        :status 401: User is not authorized

        """
        parser = reqparse.RequestParser()
        parser.add_argument('Authorization', location='headers', required=True)
        args = parser.parse_args()

        authorization = args['Authorization']
        credentials = authorization.split(' ')

        if len(credentials) != 2:
            abort(400)

        if credentials[0] != 'Token':
            abort(400)

        if credentials[1] == 'mock_user_001':
            data = mock_users['mock_user_001']
        elif credentials[1] == 'mock_user_002':
            data = mock_users['mock_user_002']
        else:
            response = requests.get('https://www.googleapis.com/oauth2/v3/'
                                    'tokeninfo?id_token=' + credentials[1])

            if response.status_code != 200:
                abort(401)

            data = response.json()
            if data['aud'] != '806916571874-7tnsbrr22526ioo36l8njtqj2st8nn54' \
                              '.apps.googleusercontent.com':
                abort(401)

        user = UserModel.query.filter_by(
            google_id=data['sub'], is_active=True).first()

        if user is None:
            abort(401)

        fields = {
            'exp': datetime.utcnow() + timedelta(
                seconds=current_app.config['SI_JWT_EXPIRATION']),
            'sub': data['sub']
        }

        encoded = jwt.encode(
            fields, current_app.config['SI_JWT_SECRET'], algorithm='HS256')

        return {
            'access_token': encoded.decode('utf-8')
        }, 200


class User(Resource):
    """
    Define the endpoints for the user node.

    """
    @auth.login_required
    def get(self):
        """
        .. :quickref: User; Retrieve the authenticated user.

        Retrieve the authenticated user.

        **Example request**:

        .. sourcecode:: http

            GET /me HTTP/1.1
            Host: example.com
            Authorization: Bearer <token>

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: application/json

            {
                'id': 1,
                'google_id': '123456789',
                'firstname': 'John',
                'lastname': 'Doe',
                'email': 'john@example.org',
                'is_active': True
            }

        :reqheader Authorization: JSON Web Token to authenticate

        :resheader Content-Type: data is received as application/json

        :>json int id: the user's id
        :>json string google_id: the user's google id
        :>json string firstname: the user's firstname
        :>json string lastname: the user's lastname
        :>json string email: the user's email
        :>json boolean is_active: the user's status

        :status 200: User is retrieved
        :status 400: Token is not well-formed
        :status 401: Token has expired
        :status 401: User is not authorized

        """
        return g.user.serialize, 200

    @auth.login_required
    def put(self):
        """
        .. :quickref: User; Update the authenticated user.

        Update the authenticated user.

        **Example request**:

        .. sourcecode:: http

            PUT /me HTTP/1.1
            Host: example.com
            Authorization: Bearer <token>
            Content-Type: application/json

            {
                'firstname': 'John',
                'lastname': 'Doe',
                'email': 'john@example.org'
            }

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: application/json

            {
                'id': 1,
                'google_id': '123456789',
                'firstname': 'John',
                'lastname': 'Doe',
                'email': 'john@example.org',
                'is_active': True
            }

        :reqheader Authorization: JSON Web Token to authenticate
        :reqheader Content-Type: data is sent as application/json or
                                 application/x-www-form-urlencoded

        :<json string firstname: the user's firstname
        :<json string lastname: the user's lastname
        :<json string email: the user's email

        :resheader Content-Type: data is received as application/json

        :>json int id: the user's id
        :>json string google_id: the user's google id
        :>json string firstname: the user's firstname
        :>json string lastname: the user's lastname
        :>json string email: the user's email
        :>json boolean is_active: the user's status

        :status 200: User is updated
        :status 400: Parameters are missing
        :status 400: Token is not well-formed
        :status 401: Token has expired
        :status 401: User is not authorized

        """
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('firstname', required=True)
        parser.add_argument('lastname', required=True)
        parser.add_argument('email', required=True)
        args = parser.parse_args()

        g.user.firstname = args['firstname']
        g.user.lastname = args['lastname']
        g.user.email = args['email']
        db.session.commit()

        return g.user.serialize, 200

    @auth.login_required
    def delete(self):
        """
        .. :quickref: User; Delete the authenticated user.

        Delete the authenticated user.

        This endpoint sets the authenticated user's account and partnerships
        with organizations to 'inactive'. By signin-up again with the same
        google account, the user's account is reactivated. To rejoin an
        organization, a new invitation is needed.

        **Example request**:

        .. sourcecode:: http

            DELETE /me HTTP/1.1
            Host: example.com
            Authorization: Bearer <token>

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 204 No Content

        :reqheader Authorization: JSON Web Token to authenticate

        :status 204: User is deleted
        :status 400: Token is not well-formed
        :status 401: Token has expired
        :status 401: User is not authorized

        """
        g.user.is_active = False

        for partner in g.user.partners:
            partner.is_active = False

        db.session.commit()

        return None, 204


class UserOrganizations(Resource):
    """
    Define the endpoints for the organizations edge of the user node.

    """

    @auth.login_required
    def post(self):
        """
        .. :quickref: User Organizations; Create an organization.

        Create an organization.

        This endpoint creates a new organization with an anchor circle and
        adds the authenticated user as an admin to the organization.

        **Example request**:

        .. sourcecode:: http

            POST /me/organizations HTTP/1.1
            Host: example.com
            Authorization: Bearer <token>
            Content-Type: application/json

            {
                'name': 'My Organization'
            }

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 201 Created
            Content-Type: application/json

            {
                'id': 1,
                'name': 'My Organization'
            }

        :reqheader Authorization: JSON Web Token to authenticate
        :reqheader Content-Type: data is sent as application/json or
                                 application/x-www-form-urlencoded

        :<json string name: the organization's name

        :resheader Content-Type: data is received as application/json

        :>json int id: the organization's id
        :>json string name: the organization's name

        :status 201: Organization is created
        :status 400: Parameters are missing
        :status 400: Token is not well-formed
        :status 401: Token has expired
        :status 401: User is not authorized
        :status 409: Organization cannot be created

        """
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('name', required=True)
        args = parser.parse_args()

        try:
            organization = OrganizationModel(args['name'])

            partner = PartnerModel(PartnerType.admin, g.user.firstname,
                                   g.user.lastname, g.user.email,
                                   g.user, organization)
            db.session.add(partner)
            db.session.flush()

            role = RoleModel(RoleType.circle, 'General', 'General\'s Purpose',
                             None, organization.id)
            db.session.add(role)
            db.session.flush()

            circle = CircleModel(role.id, None)
            db.session.add(circle)
            db.session.flush()

            lead_link = RoleModel(RoleType.lead_link, 'Lead Link',
                                  'Lead Link\'s Purpose', role.id,
                                  role.organization_id)
            db.session.add(lead_link)
            db.session.flush()

            secretary = RoleModel(RoleType.secretary, 'Secretary',
                                  'Secretary\'s Purpose', role.id,
                                  role.organization_id)
            db.session.add(secretary)
            db.session.flush()

            facilitator = RoleModel(RoleType.facilitator, 'Facilitator',
                                    'Facilitator\'s Purpose', role.id,
                                    role.organization_id)
            db.session.add(facilitator)
            db.session.flush()

            partner.memberships.append(role)
            partner.memberships.append(lead_link)

            db.session.commit()
        except:
            db.session.rollback()
            abort(409)

        return organization.serialize, 201

    @auth.login_required
    def get(self):
        """
        .. :quickref: User Organizations; List the user's organizations.

        List organizations for the authenticated user.

        This endpoint only lists organizations that the authenticated user is
        allowed to operate on as a member or an admin.

        **Example request**:

        .. sourcecode:: http

            GET /me/organizations HTTP/1.1
            Host: example.com
            Authorization: Bearer <token>

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: application/json

            [
                {
                    'id': 1,
                    'name': 'My Organization'
                }
            ]

        :reqheader Authorization: JSON Web Token to authenticate

        :resheader Content-Type: data is received as application/json

        :>jsonarr int id: the organization's id
        :>jsonarr string name: the organization's name

        :status 200: Organizations are listed
        :status 400: Token is not well-formed
        :status 401: Token has expired
        :status 401: User is not authorized

        """
        organizations = db.session.query(OrganizationModel).filter(
            OrganizationModel.partners.any(is_active=True, user=g.user))

        data = [item.serialize for item in organizations]

        return data, 200
