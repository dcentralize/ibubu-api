from flask_restful import Resource, reqparse
from swarm_intelligence_app.models import db
from swarm_intelligence_app.models.organization import \
    Organization as OrganizationModel
from swarm_intelligence_app.models.partner import \
    Partner as PartnerModel
from swarm_intelligence_app.models.partner import PartnerType
from swarm_intelligence_app.models.invitation import \
    Invitation as InvitationModel
from swarm_intelligence_app.common import errors
from swarm_intelligence_app.common.authentication import auth


class Organization(Resource):
    @auth.login_required
    def get(self,
            organization_id):
        """
        Retrieve an organization

        In order to retrieve an organization, the authenticated user must be a
        member or an admin of the organization.

        Params:
            organization_id: The id of the organization to retrieve
        """
        organization = OrganizationModel.query.get(organization_id)

        if organization is None:
            raise errors.EntityNotFoundError('organization', organization_id)

        return {
            'success': True,
            'data': organization.serialize
        }, 200

    @auth.login_required
    def put(self,
            organization_id):
        """
        Edit an organization

        In order to edit an organization, the authenticated user must be an
        admin of the organization.

        Params:
            organization_id: The id of the organization to edit
            name: The name of the organization
        """
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
        }, 200

    def delete(self,
               organization_id):
        """
        Delete an organization

        This endpoint sets the organization's state to 'deleted', so that it
        cannot be accessed by its members or admins in any way. In order to
        delete an organization, the authenticated user must be an admin of the
        organization.

        Params:
            organization_id: The id of the organization to delete
        """
        organization = OrganizationModel.query.get(organization_id)

        if organization is None:
            raise errors.EntityNotFoundError('organization', organization_id)

        organization.is_deleted = True

        for partner in organization.partners:
            partner.is_deleted = True

        db.session.commit()

        return {
            'success': True,
            'data': organization.serialize
        }, 200


class OrganizationMembers(Resource):
    @auth.login_required
    def get(self,
            organization_id):
        """
        List members of an organization

        This endpoint lists all partners with access through membership or with
        admin access to the organization, whether their state is 'active' or
        not. In order to list the members of an organization, the
        authenticated user must be a member or an admin of the organization.

        Params:
            organization_id: The id of the organization for which to list the
            members
        """
        organization = OrganizationModel.query.get(organization_id)

        if organization is None:
            raise errors.EntityNotFoundError('organization', organization_id)

        data = [i.serialize for i in organization.partners]
        return {
            'success': True,
            'data': data
        }, 200


class OrganizationAdmins(Resource):
    @auth.login_required
    def get(self,
            organization_id):
        """
        List admins of an organization

        This endpoint lists all partners of an organization with admin access
        to the organization, wether their state is 'active' or not. In order
        to list the admins of an organization, the authenticated user must be
        a member or an admin of the organization.

        Params:
            organization_id: The id of the organization for which to list the
            admins
        """
        organization = OrganizationModel.query.get(organization_id)

        if organization is None:
            raise errors.EntityNotFoundError('organization', organization_id)

        admins = PartnerModel.query.filter_by(organization=organization,
                                              type=PartnerType.ADMIN)

        data = [i.serialize for i in admins]
        return {
            'success': True,
            'data': data
        }, 200


class OrganizationInvitations(Resource):
    @auth.login_required
    def post(self,
             organization_id):
        """
        Invite a user to an organization

        This endpoint will send an invitation to a given email address. The
        newly-created invitation will be in the 'pending' state until the user
        accepts the invitation. At this point the invitation will transition
        to the 'accepted' state and the user will be added as a new partner to
        the organization. In order to invite a user to an organization, the
        authenticated user must be an admin of the organization.

        Params:
            organization_id: The id of the organization for which to invite
            the user
            email: The email address the invitation will be sent to
        """
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
        organization.invitations.append(invitation)

        db.session.add(invitation)
        db.session.commit()

        return {
            'success': True,
            'data': invitation.serialize
        }, 200

    @auth.login_required
    def get(self,
            organization_id):
        """
        List invitations to an organization

        This endpoint lists all 'pending', 'accepted' and 'cancelled'
        invitations to an organization. In order to list invitations to an
        organization, the authenticated user must be a member or an admin of
        the organization.

        Params:
            organization_id: The id of the organization for which to list the
            invitations
        """
        organization = OrganizationModel.query.get(organization_id)

        if organization is None:
            raise errors.EntityNotFoundError('organization', organization_id)

        invitations = InvitationModel.query.filter_by(
            organization_id=organization.id)

        data = [i.serialize for i in invitations]
        return {
            'success': True,
            'data': data
        }, 200
