"""
Define the classes for the user API.

"""
from datetime import datetime, timedelta

import jwt
import requests

from flask import current_app, g
from flask_restful import abort, reqparse, Resource
from swarm_intelligence_app.common.authentication import auth
from swarm_intelligence_app.models import db
from swarm_intelligence_app.models.circle import Circle as CircleModel
from swarm_intelligence_app.models.organization import \
    Organization as OrganizationModel
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
        Create a user.

        To create a user the data provided by google is taken into
        consideration. If a user with the provided google id does not exist,
        the user is created. If a user exists and is deactivated, the user is
        activated. If a user does not exist, the user is created with the data
        provided by google.

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

        if user is not None and user.is_deleted is False:
            abort(409, 'Cannot create user. The user already exists.')

        if user is not None and user.is_deleted is True:
            user.is_deleted = False
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
            'success': True,
            'data': {
                'access_token': encoded.decode('utf-8')
            }
        }, 201


class UserLogin(Resource):
    """
    Define the endpoints for the user login.
    """
    def get(self):
        """
        Login a user.
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
            google_id=data['sub'], is_deleted=False).first()

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
            'success': True,
            'data': {
                'access_token': encoded.decode('utf-8')
            }
        }, 200


class User(Resource):
    """
    Define the endpoints for the user node.

    """
    @auth.login_required
    def get(self):
        """
        Retrieve the authenticated user.

        """
        return g.user.serialize, 200

    @auth.login_required
    def put(self):
        """
        Edit the authenticated user.

        Params:
            firstname: The firstname of the authenticated user
            lastname: The lastname of the authenticated user
            email: The email address of the authenticated user

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
        Delete the authenticated user.

        This endpoint sets the authenticated user's account to 'closed' and
        the user's partnerships with organizations to 'inactive'. By signin-up
        again with the same google account, the user's account is reopened. To
        rejoin an organization, a new invitation is needed.

        """
        g.user.is_deleted = True

        for partner in g.user.partners:
            partner.is_deleted = True

        db.session.commit()

        return None, 204


class UserOrganizations(Resource):
    """
    Define the endpoints for the organizations edge of the user node.

    """
    @auth.login_required
    def post(self):
        """
        Create an organization.

        This endpoint creates a new organization with an anchor circle and
        adds the authenticated user as an admin to the organization.

        Params:
            name: The name of the organization

        """
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('name', required=True)
        args = parser.parse_args()

        try:
            organization = OrganizationModel(args['name'])

            partner = PartnerModel(PartnerType.admin, g.user.firstname,
                g.user.lastname, g.user.email, g.user, organization)
            db.session.add(partner)
            db.session.flush()

            role = RoleModel(RoleType.circle, 'General', 'General\'s Purpose',
                None, organization.id)
            db.session.add(role)
            db.session.flush()

            circle = CircleModel(role.id, None)
            db.session.add(circle)
            db.session.flush()

            lead_link = RoleModel(RoleType.lead_link,'Lead Link',
                'Lead Link\'s Purpose', role.id, role.organization_id)
            db.session.add(lead_link)
            db.session.flush()

            secretary = RoleModel(RoleType.secretary, 'Secretary',
                'Secretary\'s Purpose', role.id, role.organization_id)
            db.session.add(secretary)
            db.session.flush()

            facilitator = RoleModel(RoleType.facilitator, 'Facilitator',
                'Facilitator\'s Purpose', role.id, role.organization_id)
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
        List organizations for the authenticated user.

        This endpoint only lists organizations that the authenticated user is
        allowed to operate on as a member or an admin.

        """
        organizations = db.session.query(OrganizationModel).filter(
            OrganizationModel.partners.any(is_deleted=False, user=g.user))

        data = [item.serialize for item in organizations]

        return data, 200
