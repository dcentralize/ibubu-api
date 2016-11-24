"""
Define the classes for the invitation API.

"""
from flask import g
from flask_restful import Resource
from swarm_intelligence_app.common import errors
from swarm_intelligence_app.common.authentication import auth
from swarm_intelligence_app.models import db
from swarm_intelligence_app.models.invitation import \
    Invitation as InvitationModel
from swarm_intelligence_app.models.invitation import InvitationStatus
from swarm_intelligence_app.models.partner import Partner as PartnerModel
from swarm_intelligence_app.models.partner import PartnerType
from swarm_intelligence_app.models.user import User as UserModel


class Invitation(Resource):
    """
    Define the endpoints for the invitation node.

    """
    @auth.login_required
    def get(self,
            invitation_id):
        """
        Retrieve an invitation.

        In order to retrieve an invitation, the authenticated user must be a
        member or an admin of the organization that the invitation is
        associated with.

        Params:
            invitation_id: The id of the invitation to retrieve

        """
        invitation = InvitationModel.query.get(invitation_id)

        if invitation is None:
            raise errors.EntityNotFoundError('invitation', invitation_id)

        return {
            'success': True,
            'data': invitation.serialize
        }, 200

    @auth.login_required
    def delete(self,
               invitation_id):
        """
        Delete an invitation.

        If an invitation's state is 'pending', this endpoint will set the
        invitation's state to 'cancelled'. If an invitation's state is
        'accepted' or 'cancelled', the invitation cannot be deleted at all or
        deleted again. In order to delete an invitation, the authenticated
        user must be an admin of the organization that the invitation is
        associated with.

        Params:
            invitation_id: The id of the invitation to delete

        """
        invitation = InvitationModel.query.get(invitation_id)

        if invitation is None:
            raise errors.EntityNotFoundError('invitation', invitation_id)

        if invitation.status == InvitationStatus.ACCEPTED:
            raise errors.EntityNotModifiedError('The invitation has already '
                                                'been accepted and cannot be '
                                                'deleted.')

        invitation.status = InvitationStatus.CANCELLED
        db.session.commit()

        data = invitation.serialize
        return {
            'success': True,
            'data': data
        }, 200


class InvitationResend(Resource):
    """
    Define the endpoints for the resend edge of the invitation node.

    """
    def get(self,
            invitation_id):
        """
        Resend an invitation.

        If an invitation's state is 'pending', this endpoint will resend the
        invitation to the associated email address. If an invitation's state
        is 'accepted' or 'cancelled', the invitation cannot be resent. In
        order to resend an invitation, the authenticated user must be an admin
        of the organization that the invitation is associated with.

        Params:
            invitation_id: The id of the invitation to resend

        """
        raise errors.MethodNotImplementedError()


class InvitationAccept(Resource):
    """
    Define the endpoints for the accept edge of the invitation node.

    """
    @auth.login_required
    def get(self,
            code):
        """
        Accept an invitation.

        If an invitation's state is 'pending', this endpoint will set the
        invitation's state to 'accepted' and the authenticated user will be
        added as a partner to the associated organization. If an invitation's
        state is 'accepted' or 'cancelled', the invitation cannot be
        accepted again or accepted at all. In order to accept an invitation,
        the user must be an authenticated user.

        Params:
            code: The code of the invitation to accept

        """
        invitation = InvitationModel.query.filter_by(code=code).first()

        if invitation is None:
            raise errors.EntityNotFoundError('invitation', code)

        user = UserModel.query.filter_by(google_id=g.user['google_id']).first()

        if user is None:
            raise errors.EntityNotFoundError('user', g.user['google_id'])

        PartnerModel(PartnerType.MEMBER, user.firstname, user.lastname,
                     user.email, user, invitation.organization, invitation.id)

        invitation.status = InvitationStatus.ACCEPTED
        db.session.commit()

        data = invitation.serialize
        return {
            'success': True,
            'data': data
        }, 200
