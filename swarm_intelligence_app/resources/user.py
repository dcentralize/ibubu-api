from flask import g
from flask_restful import Resource, reqparse
from swarm_intelligence_app.models import db
from swarm_intelligence_app.models.user import User as UserModel
from swarm_intelligence_app.models.organization import \
    Organization as OrganizationModel
from swarm_intelligence_app.models.partner import Partner as PartnerModel
from swarm_intelligence_app.models.partner import PartnerType
from swarm_intelligence_app.common import errors
from swarm_intelligence_app.common.authentication import auth


class User(Resource):
    # create a new user
    # permissions: login_required
    @auth.login_required
    def post(self):
        user = UserModel.query.filter_by(google_id=g.user['google_id']).first()
        if user is not None:
            return 'User already exists.'

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
        }

    # get the authenticated user
    # permissions: login_required
    @auth.login_required
    def get(self):
        user = UserModel.query.filter_by(google_id=g.user['google_id']).first()
        if user is None:
            raise errors.EntityNotFoundError('user', g.user['google_id'])
        return {
            'success': True,
            'data': user.serialize
        }

    # update the authenticated user
    # permissions: login_required
    @auth.login_required
    def put(self):
        user = UserModel.query.filter_by(google_id=g.user['google_id']).first()
        if user is None:
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
        }

    # delete the authenticated user
    # permissions: login_required
    @auth.login_required
    def delete(self):
        user = UserModel.query.filter_by(google_id=g.user['google_id']).first()
        if user is None:
            raise errors.EntityNotFoundError('user', g.user['google_id'])

        user.is_deleted = True
        db.session.commit()

        return {
            'success': True,
            'data': user.serialize
        }


class UserOrganizations(Resource):
    # add a new organization to the authenticated user as owner
    # permissions: login_required
    @auth.login_required
    def post(self):
        user = UserModel.query.filter_by(google_id=g.user['google_id']).first()
        if user is None:
            raise errors.EntityNotFoundError('user', g.user['google_id'])

        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('name', required=True)
        args = parser.parse_args()

        organization = OrganizationModel(
            args['name']
        )
        db.session.add(organization)
        db.session.commit()

        partner = PartnerModel(
            PartnerType.OWNER,
            user.firstname,
            user.lastname,
            user.email,
            user.id,
            organization.id
        )
        db.session.add(partner)
        db.session.commit()

        return {
            'success': True,
            'data': organization.serialize
        }

    # get a list of organizations with the authenticated user as its owner
    # or partner
    # permissions: login_required
    @auth.login_required
    def get(self):
        user = UserModel.query.filter_by(google_id=g.user['google_id']).first()
        if user is None:
            raise errors.EntityNotFoundError('user', g.user['google_id'])

        organizations = OrganizationModel.query.join(PartnerModel, (
            PartnerModel.organization_id == OrganizationModel.id)).filter(
            PartnerModel.user_id == user.id).all()

        data = [i.serialize for i in organizations]
        return {
            'success': True,
            'data': data
        }
