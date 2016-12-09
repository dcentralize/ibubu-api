"""
Define the classes for the user API.

"""
from datetime import datetime, timedelta

import jwt
import requests

from flask import g
from flask_restful import abort, reqparse, Resource
from flask_restful_swagger import swagger
from swarm_intelligence_app.common import errors
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

APP_SECRET = 'top_secret'
TOKEN_EXPIRATION = 3600

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
    @swagger.operation(
        # Parameters can be automatically extracted from URLs (e.g.
        # <string:id>)
        # but you could also override them here, or add other parameters.
        parameters=[
            {
                'name': 'Authorization',
                'defaultValue': ('Token + <mock_user_001>'),
                'in': 'header',
                'description': 'web-token to be passed as a header',
                'required': 'true',
                'paramType': 'header',
                'type': 'string'
            }
        ],
        responseMessages=[
            {
                'code': 400,
                'message': 'BAD REQUEST'
            },
            {
                'code': 401,
                'message': 'UNAUTHORIZED'
            }
        ],
    )
    def post(self):
        """
        Create a user.
        To create a user the data provided by google is taken into
        consideration.
        If a user with the provided google id does not exist,
        the user is created with the data provided by google.
        If a user exists and is deactivated, the user is reactivated.
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
            raise errors.EntityAlreadyExistsError()

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
            'exp': datetime.utcnow() + timedelta(seconds=TOKEN_EXPIRATION),
            'sub': user.google_id
        }

        encoded = jwt.encode(fields, APP_SECRET, algorithm='HS256')

        return {
            'success': True,
            'data': {
                'access_token': encoded.decode('utf-8')
            }
        }


class UserLogin(Resource):
    """
    Define the endpoints for the user login.
    """
    @swagger.operation(
        # Parameters can be automatically extracted from URLs (e.g.
        # <string:id>)
        # but you could also override them here, or add other parameters.
        parameters=[{
                'name': 'Authorization',
                'defaultValue': ('Bearer + <mock_user_001>'),
                'in': 'header',
                'description': 'JWT to be passed as a header',
                'required': 'true',
                'paramType': 'header',
                'type': 'string'
                    }],
        responseMessages=[
            {
                'code': 400,
                'message': 'BAD REQUEST'
            },
            {
                'code': 401,
                'message': 'UNAUTHORIZED'
            }
        ]
    )
    def get(self):
        """
        Login a user.
        In order to login a user, a valid JWT has to be provided to the server.
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
        if user is None:
            abort(401)

        fields = {
            'exp': datetime.utcnow() + timedelta(seconds=TOKEN_EXPIRATION),
            'sub': data['sub']
        }

        encoded = jwt.encode(fields, APP_SECRET, algorithm='HS256')

        return {
            'success': True,
            'data': {
                'access_token': encoded.decode('utf-8')
            }
        }


class User(Resource):
    """
    Define the endpoints for the user node.

    """
    @swagger.operation(
        # Parameters can be automatically extracted from URLs (e.g.
        # <string:id>)
        # but you could also override them here, or add other parameters.
        parameters=[{
                'name': 'Authorization',
                'defaultValue': ('Bearer + <mock_user_001>'),
                'in': 'header',
                'description': 'JWT to be passed as a header',
                'required': 'true',
                'paramType': 'header',
                'type': 'string'
                    }],
        responseMessages=[
            {
                'code': 400,
                'message': 'BAD REQUEST'
            },
            {
                'code': 401,
                'message': 'UNAUTHORIZED'
            }
        ]
    )
    @auth.login_required
    def get(self):
        """
        Retrieve the authenticated user.
        Retrieve the authenticated user from the database. A valid JWT must
        be provided.
        """
        return {
            'success': True,
            'data': g.user.serialize
        }, 200

    @swagger.operation(
        # Parameters can be automatically extracted from URLs (e.g.
        # <string:id>)
        # but you could also override them here, or add other parameters.
        parameters=[{
                'name': 'Authorization',
                'defaultValue': ('Bearer + <mock_user_001>'),
                'in': 'header',
                'description': 'JWT to be passed as a header',
                'required': 'true',
                'paramType': 'header',
                'type': 'string'
                    }, {
                'name': 'body',
                'defaultValue': ("{'firstname': 'Daisy', 'lastname': "
                                 "'Ducks', 'email': 'daisy' + token +  "
                                 "'@tolli.com'}"),
                'description': 'new user-data',
                'required': 'true',
                'type': 'JSON Object',
                'paramType': 'body'
        }],
        responseMessages=[
            {
                'code': 400,
                'message': 'BAD REQUEST'
            },
            {
                'code': 401,
                'message': 'UNAUTHORIZED'
            }
        ]
    )
    @auth.login_required
    def put(self):
        """
        Edit the authenticated user.
        The authenticated user will be updated, by providing the server with
        a valid JWT and the new user-data.
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

        return {
            'success': True,
            'data': g.user.serialize
        }, 200

    @swagger.operation(
        # Parameters can be automatically extracted from URLs (e.g.
        # <string:id>)
        # but you could also override them here, or add other parameters.
        parameters=[{
                'name': 'Authorization',
                'defaultValue': ('Bearer + <mock_user_001>'),
                'in': 'header',
                'description': 'JWT to be passed as a header',
                'required': 'true',
                'paramType': 'header',
                'type': 'string'
                    }],
        responseMessages=[
            {
                'code': 400,
                'message': 'BAD REQUEST'
            },
            {
                'code': 401,
                'message': 'UNAUTHORIZED'
            }
        ]
    )
    @auth.login_required
    def delete(self):
        """
        Delete the authenticated user.
        The state of the authenticated user will be set to 'closed' and the
        user's partnerships with organizations will be set to 'inactive'.
        The user's account will be reopened, as soon as a new user with the
        same google account has signed in. In order to rejoin an organization,
        a new invitation is needed. A valid JWT is needed.

        """
        g.user.is_deleted = True

        for partner in g.user.partners:
            partner.is_deleted = True

        db.session.commit()

        return {
            'success': True,
            'data': g.user.serialize
        }, 200


class UserOrganizations(Resource):
    """
    Define the endpoints for the organizations edge of the user node.

    """

    @swagger.operation(
        # Parameters can be automatically extracted from URLs (e.g.
        # <string:id>)
        # but you could also override them here, or add other parameters.
        parameters=[{
                'name': 'Authorization',
                'defaultValue': ('Bearer + <mock_user_001>'),
                'in': 'header',
                'description': 'JWT to be passed as a header',
                'required': 'true',
                'paramType': 'header',
                'type': 'string'
                    }, {
                'name': 'body',
                'defaultValue': ("{'name': token + ': Dagoberts ' + "
                                 "'Empire'}"),
                'description': 'name of the organization',
                'required': 'true',
                'type': 'JSON Object',
                'paramType': 'body'
                }
        ],
        responseMessages=[
            {
                'code': 400,
                'message': 'BAD REQUEST'
            },
            {
                'code': 401,
                'message': 'UNAUTHORIZED'
            }
        ]
    )
    @auth.login_required
    def post(self):
        """
        Create an organization.
        A new organization with an anchor circle will be created. The
        authenticated user becomes its admin. A valid JWT must be provided.
        """
        parser = reqparse.RequestParser()
        parser.add_argument('Authorization', location='headers', required=True)
        parser.add_argument('name', required=True)
        args = parser.parse_args()

        authorization = args['Authorization']
        credentials = authorization.split(' ')

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

        if user is None or user.is_deleted is True:
            raise errors.EntityNotFoundError('user', g.user['google_id'])

        organization = OrganizationModel(args['name'])
        partner = PartnerModel(PartnerType.ADMIN, user.firstname,
                               user.lastname, user.email, user, organization)
        db.session.add(partner)
        db.session.commit()

        role = RoleModel('General', 'Purpose', None, RoleType.CIRCLE)
        db.session.add(role)
        db.session.commit()

        anchor_circle = CircleModel('Strategy', organization.id, role.id)
        db.session.add(anchor_circle)
        db.session.commit()

        role_leadlink = RoleModel('LEAD_LINK', 'Purpose leadlink',
                                  anchor_circle.role_id, RoleType.LEAD_LINK)
        role_secretary = RoleModel('SECRETARY', 'Purpose secretary',
                                   anchor_circle.role_id, RoleType.SECRETARY)
        role_facilitator = RoleModel('FACILITATOR', 'Purpose facilitator',
                                     anchor_circle.role_id,
                                     RoleType.FACILITATOR)
        db.session.add(role_leadlink)
        db.session.add(role_secretary)
        db.session.add(role_facilitator)
        db.session.commit()

        partner.circles.append(anchor_circle)
        partner.roles.append(role_leadlink)
        db.session.commit()

        return {
            'success': True,
            'data': organization.serialize
        }, 200

    @swagger.operation(
        # Parameters can be automatically extracted from URLs (e.g.
        # <string:id>)
        # but you could also override them here, or add other parameters.
        parameters=[{
                'name': 'Authorization',
                'defaultValue': ('Bearer + <mock_user_001>'),
                'in': 'header',
                'description': 'JWT to be passed as a header',
                'required': 'true',
                'paramType': 'header',
                'type': 'string'
                    }],
        responseMessages=[
            {
                'code': 400,
                'message': 'BAD REQUEST'
            },
            {
                'code': 401,
                'message': 'UNAUTHORIZED'
            }
        ]
    )
    @auth.login_required
    def get(self):
        """
        List organizations for the authenticated user.
        A list of all organizations in which the authenticated user is
        allowed to operate in will be returned.
        """
        parser = reqparse.RequestParser()
        parser.add_argument('Authorization', location='headers', required=True)
        args = parser.parse_args()

        authorization = args['Authorization']
        credentials = authorization.split(' ')

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

        if user is None or user.is_deleted is True:
            raise errors.EntityNotFoundError('user', g.user['google_id'])

        organizations = db.session.query(OrganizationModel).filter(
            OrganizationModel.partners.any(is_deleted=False, user=user))

        data = [item.serialize for item in organizations]
        return {
            'success': True,
            'data': data
        }, 200
