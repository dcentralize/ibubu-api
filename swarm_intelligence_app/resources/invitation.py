"""
Define the classes for the invitation API.

"""
from flask import abort, g
from flask_restful import Resource
from swarm_intelligence_app.common.authentication import auth
from swarm_intelligence_app.models import db
from swarm_intelligence_app.models.invitation import \
    Invitation as InvitationModel
from swarm_intelligence_app.models.invitation import InvitationStatus
from swarm_intelligence_app.models.partner import Partner as PartnerModel
from swarm_intelligence_app.models.partner import PartnerType


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
            abort(404)

        return invitation.serialize, 200


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
            abort(404)

        PartnerModel(PartnerType.member, g.user.firstname, g.user.lastname,
                     g.user.email, g.user, invitation.organization)

        invitation.status = InvitationStatus.accepted
        db.session.commit()

        return invitation.serialize, 200


class InvitationCancel(Resource):
    """
    Define the endpoints for the cancel edge of the invitation node.

    """
    @auth.login_required
    def put(self,
            invitation_id):
        """
        Cancel an invitation.

        If an invitation's state is 'pending', this endpoint will set the
        invitation's state to 'cancelled'. If an invitation's state is
        'accepted' or 'cancelled', the invitation cannot be cancelled at all or
        cancelled again. In order to cancel an invitation, the authenticated
        user must be an admin of the organization that the invitation is
        associated with.

        Params:
            invitation_id: The id of the invitation to cancel

        """
        invitation = InvitationModel.query.get(invitation_id)

        if invitation is None:
            abort(404)

        if invitation.status == InvitationStatus.accepted:
            abort(409, 'The invitation has already '
                       'been accepted and cannot be '
                       'cancelled.')

        invitation.status = InvitationStatus.cancelled
        db.session.commit()

        return None, 204


class InvitationResend(Resource):
    """
    Define the endpoints for the resend edge of the invitation node.

    """
    @auth.login_required
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
        abort(501)
