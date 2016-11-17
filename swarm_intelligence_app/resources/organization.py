from flask_restful import Resource, reqparse
from swarm_intelligence_app.models import db
from swarm_intelligence_app.models.organization import \
    Organization as OrganizationModel
from swarm_intelligence_app.models.invitation import \
    Invitation as InvitationModel
from swarm_intelligence_app.models.partner import Partner as PartnerModel
from swarm_intelligence_app.common import errors
from swarm_intelligence_app.common.authentication import auth


class Organization(Resource):
    # get an organization
    # permissions: login_required, organization_partner
    @auth.login_required
    def get(self, organization_id):
        organization = OrganizationModel.query.get(organization_id)
        if organization is None:
            raise errors.EntityNotFoundError('organization', organization_id)
        return {
            'success': True,
            'data': organization.serialize
        }

    # update an organization
    # permissions: login_required, organization_owner
    @auth.login_required
    def put(self, organization_id):
        organization = OrganizationModel.query.get(organization_id)
        if organization is None:
            raise errors.EntityNotFoundError('organization', organization_id)
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('name', required=True)
        args = parser.parse_args()
        organization.name = args['name']
        db.session.commit()
        return {
            'success': True,
            'data': organization.serialize
        }

    # delete an organization
    # permissions: login_required, organization_owner
    def delete(self, organization_id):
        raise errors.MethodNotImplementedError()


class OrganizationOwner(Resource):
    # change the owner of an organization
    # permissions: login_required, organization_owner
    def put(self, organization_id):
        raise errors.MethodNotImplementedError()


class OrganizationPartners(Resource):
    # get a list of partners of an organization
    # permissions: login_required, organization_partner
    @auth.login_required
    def get(self, organization_id):
        organization = OrganizationModel.query.get(organization_id)
        if organization is None:
            raise errors.EntityNotFoundError('organization', organization_id)
        partners = PartnerModel.query.filter_by(
            organization_id=organization.id)
        data = [i.serialize for i in partners]
        return {
            'success': True,
            'data': data
        }


class OrganizationInvitations(Resource):
    # create a new invitation to an organization
    # permissions: login_required, organization_owner
    @auth.login_required
    def post(self, organization_id):
        organization = OrganizationModel.query.get(organization_id)
        if organization is None:
            raise errors.EntityNotFoundError('organization', organization_id)

        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('email', required=True)
        args = parser.parse_args()

        invitation = InvitationModel(
            args['email'],
            organization.id
        )

        db.session.add(invitation)
        db.session.commit()

        return {
            'success': True,
            'data': invitation.serialize
        }

    # get a list of invitations to an organization
    # permissions: login_required, organization_partner
    @auth.login_required
    def get(self, organization_id):
        organization = OrganizationModel.query.get(organization_id)
        if organization is None:
            raise errors.EntityNotFoundError('organization', organization_id)
        invitations = InvitationModel.query.filter_by(
            organization_id=organization.id)
        data = [i.serialize for i in invitations]
        return {
            'success': True,
            'data': data
        }
