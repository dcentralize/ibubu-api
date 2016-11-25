"""
Define the classes for the user API.

"""
from flask import g
from flask_restful import reqparse, Resource
from swarm_intelligence_app.common import errors
from swarm_intelligence_app.common.authentication import auth
from swarm_intelligence_app.models import db
from swarm_intelligence_app.models.circle import Circle as CircleModel
from swarm_intelligence_app.models.organization import \
    Organization as OrganizationModel
from swarm_intelligence_app.models.partner import Partner as PartnerModel
from swarm_intelligence_app.models.partner import PartnerType
from swarm_intelligence_app.models.user import User as UserModel


class User(Resource):
    """
    Define the endpoints for the user node.

    """
    @auth.login_required
    def post(self):
        """
        Create a user.

        To create a user the data provided by google is taken into
        consideration. If a user with the provided google id does not exist,
        the user is created. If a user exists and is deactivated, the user is
        activated. If a user does not exist, the user is created with the data
        provided by google.

        """
        user = UserModel.query.filter_by(google_id=g.user['google_id']).first()

        if user is not None and user.is_deleted is False:
            raise errors.EntityAlreadyExistsError()

        if user is not None and user.is_deleted is True:
            user.is_deleted = False
        else:
            user = UserModel(
                g.user['google_id'],
                g.user['firstname'],
                g.user['lastname'],
                g.user['email']
            )
            db.session.add(user)

        db.session.commit()

        return {
            'success': True,
            'data': user.serialize
        }, 200

    @auth.login_required
    def get(self):
        """
        Retrieve the authenticated user.

        """
        user = UserModel.query.filter_by(google_id=g.user['google_id']).first()

        if user is None or user.is_deleted is True:
            raise errors.EntityNotFoundError('user', g.user['google_id'])

        return {
            'success': True,
            'data': user.serialize
        }, 200

    @auth.login_required
    def put(self):
        """
        Edit the authenticated user.

        Params:
            firstname: The firstname of the authenticated user
            lastname: The lastname of the authenticated user
            email: The email address of the authenticated user

        """
        user = UserModel.query.filter_by(google_id=g.user['google_id']).first()

        if user is None or user.is_deleted is True:
            raise errors.EntityNotFoundError('user', g.user['google_id'])

        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('firstname', required=True)
        parser.add_argument('lastname', required=True)
        parser.add_argument('email', required=True)
        args = parser.parse_args()

        user.firstname = args['firstname']
        user.lastname = args['lastname']
        user.email = args['email']
        db.session.commit()

        return {
            'success': True,
            'data': user.serialize
        }, 200

    @auth.login_required
    def delete(self):
        """
        Delete the authenticated user.

        This endpoint sets the authenticated user's account to 'closed' and
        the user's partnerships with organizations to 'inactive'. By signin-up
        again with the same google account, the user's account is reopened. To
        rejoin an organization, a new invitation is needed.

        """
        user = UserModel.query.filter_by(google_id=g.user['google_id']).first()

        if user is None or user.is_deleted is True:
            raise errors.EntityNotFoundError('user', g.user['google_id'])

        user.is_deleted = True

        for partner in user.partners:
            partner.is_deleted = True

        db.session.commit()

        return {
            'success': True,
            'data': user.serialize
        }, 200


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
        user = UserModel.query.filter_by(google_id=g.user['google_id']).first()

        if user is None or user.is_deleted is True:
            raise errors.EntityNotFoundError('user', g.user['google_id'])

        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('name', required=True)
        args = parser.parse_args()

        organization = OrganizationModel(args['name'])
        PartnerModel(PartnerType.ADMIN, user.firstname, user.lastname,
                     user.email, user, organization)
        db.session.commit()

        anchor_circle = CircleModel('General', None, None, organization.id,
                                    None)
        db.session.add(anchor_circle)
        db.session.commit()

        return {
            'success': True,
            'data': organization.serialize
        }, 200

    @auth.login_required
    def get(self):
        """
        List organizations for the authenticated user.

        This endpoint only lists organizations that the authenticated user is
        allowed to operate on as a member or an admin.

        """
        user = UserModel.query.filter_by(google_id=g.user['google_id']).first()

        if user is None or user.is_deleted is True:
            raise errors.EntityNotFoundError('user', g.user['google_id'])

        organizations = db.session.query(OrganizationModel).filter(
            OrganizationModel.partners.any(is_deleted=False, user=user))

        data = [item.serialize for item in organizations]
        return {
            'success': True,
            'data': data
        }, 200
