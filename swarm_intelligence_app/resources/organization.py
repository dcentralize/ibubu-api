"""
Define the classes for the organization API.

"""
from flask import abort
from flask_restful import reqparse, Resource
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
from swarm_intelligence_app.models.role import Role as RoleModel


class Organization(Resource):
    """
    Define the endpoints for the organization node.

    """
    # @permission_required('read_organization')
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

        if organization is None or organization.is_deleted is True:
            abort(404)

        return organization.serialize, 200

    # @permission_required('manage_organization')
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

        if organization is None or organization.is_deleted is True:
            abort(404)

        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('name', required=True)
        args = parser.parse_args()

        organization.name = args['name']
        db.session.commit()

        return organization.serialize, 200

    # @permission_required('manage_organization')
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

        #if organization is None or organization.is_deleted is True:
        if organization is None:
            abort(404)

        #organization.is_deleted = True

        #for partner in organization.partners:
        #    partner.is_deleted = True

        db.session.delete(organization)
        db.session.commit()

        return None, 204


class OrganizationAnchorCircle(Resource):
    """
    Define the endpoints for the anchor circle edge of the organization node.

    """
    # @permission_required('read_organization')
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

        if organization is None or organization.is_deleted is True:
            abort(404)

        role, circle = db.session.query(
            RoleModel, CircleModel).join(
            CircleModel, RoleModel.id == CircleModel.id).filter(
            RoleModel.organization_id == organization.id).filter(
            RoleModel.parent_circle_id == None).first()

        if role is None or circle is None:
            abort(404)

        data = {}
        data.update(role.serialize)
        data.update(circle.serialize)

        return data, 200


class OrganizationMembers(Resource):
    """
    Define the endpoints for the members edge of the organization node.

    """
    # @permission_required('read_organization')
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

        if organization is None or organization.is_deleted is True:
            abort(404)

        data = [i.serialize for i in organization.partners]

        return data, 200


class OrganizationAdmins(Resource):
    """
    Define the endpoints for the admins edge of the organization node.

    """
    # @permission_required('read_organization')
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

        if organization is None or organization.is_deleted is True:
            abort(404)

        admins = PartnerModel.query.filter_by(organization=organization,
                                              type=PartnerType.admin).all()

        data = [i.serialize for i in admins]

        return data, 200


class OrganizationInvitations(Resource):
    """
    Define the endpoints for the invitations edge of the organization node.

    """
    # @permission_required('manage_organization')
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

        if organization is None or organization.is_deleted is True:
            abort(404)

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

        return invitation.serialize, 201

    # @permission_required('read_organization')
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

        if organization is None or organization.is_deleted is True:
            abort(404)

        invitations = InvitationModel.query.filter_by(
            organization_id=organization.id)

        data = [i.serialize for i in invitations]

        return data, 200
