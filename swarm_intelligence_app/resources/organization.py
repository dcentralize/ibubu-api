"""
Define the classes for the organization API.

"""
from flask_restful import reqparse, Resource
from swarm_intelligence_app.common import errors
from swarm_intelligence_app.common.authentication import auth
from swarm_intelligence_app.models import db
from swarm_intelligence_app.models.circle import Circle as CircleModel
from swarm_intelligence_app.models.invitation import \
    Invitation as InvitationModel
from swarm_intelligence_app.models.organization import \
    Organization as OrganizationModel
from swarm_intelligence_app.models.partner import \
    Partner as PartnerModel
from swarm_intelligence_app.models.partner import PartnerType
from swarm_intelligence_app.models.role import RoleType


class Organization(Resource):
    """
    Define the endpoints for the organization node.

    """
    @auth.login_required
    def get(self,
            organization_id):
        """
        Retrieve an organization.

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
        Edit an organization.

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

    @auth.login_required
    def delete(self,
               organization_id):
        """
        Delete an organization.

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


class OrganizationAnchorCircle(Resource):
    """
    Define the endpoints for the anchor circle edge of the organization node.

    """
    @auth.login_required
    def get(self,
            organization_id):
        """
        Retrieve the anchor circle of an organization.

        This endpoint retrieves the anchor circle of an organization. Each
        organization has exactly one circle as its anchor circle. In order to
        retrieve the anchor circle of an organization, the authenticated user
        must be a member or an admin of the organization.

        Params:
            organization_id: The id of the organization for which to retrieve
            the anchor circle

        """
        organization = OrganizationModel.query.get(organization_id)

        if organization is None:
            raise errors.EntityNotFoundError('organization', organization_id)

        anchor_circle = CircleModel.query.filter_by(
            organization_id=organization.id).first()

        if anchor_circle is None:
            raise errors.EntityNotFoundError('circle', '')

        return {
            'sucess': True,
            'data': anchor_circle.serialize
        }, 200


class OrganizationRoles(Resource):
    """
    Define the endpoints for the anchor circle edge of the organization node.

    """
    @auth.login_required
    def get(self, organization_id):
        """
        List of all roles in a organization.

        This endpoint retrieves a list of all roles in a organization.

        Params:
            organization_id: The id of the organization for which to retrieve
            the anchor circle

        """
        organization = OrganizationModel.query.get(organization_id)

        if organization is None:
            raise errors.EntityNotFoundError('organization', organization_id)

        circles = CircleModel.query.filter_by(organization_id=organization.id)

        data = []
        for circle in circles:
            for role in circle.roles:
                if role.type != RoleType.CIRCLE:
                    data.append(role.serialize)

        return {
            'sucess': True,
            'data': data
        }, 200


class OrganizationMembers(Resource):
    """
    Define the endpoints for the members edge of the organization node.

    """
    @auth.login_required
    def get(self,
            organization_id):
        """
        List members of an organization.

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
    """
    Define the endpoints for the admins edge of the organization node.

    """
    @auth.login_required
    def get(self,
            organization_id):
        """
        List admins of an organization.

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
                                              type=PartnerType.ADMIN).all()

        data = [i.serialize for i in admins]
        return {
            'success': True,
            'data': data
        }, 200


class OrganizationInvitations(Resource):
    """
    Define the endpoints for the invitations edge of the organization node.

    """
    @auth.login_required
    def post(self,
             organization_id):
        """
        Invite a user to an organization.

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
        List invitations to an organization.

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
