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
        .. :quickref: Invitation; Retrieve an invitation.

        Retrieve an invitation.

        In order to retrieve an invitation, the authenticated user must be a
        partner of the organization that the invitation is associated with.

        **Example request**:

        .. sourcecode:: http

            GET /invitations/1 HTTP/1.1
            Host: example.com
            Authorization: Bearer <token>

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: application/json

            {
                'id': 1,
                'code': '12345678-1234-1234-1234-123456789012',
                'email': 'john@example.org',
                'status': 'pending',
                'organization_id': 1
            }

        :param int invitation_id: the invitation to retrieve

        :reqheader Authorization: JSON Web Token to authenticate

        :resheader Content-Type: data is received as application/json

        :>json int id: the invitation's unique id
        :>json string code: the invitation's unique code
        :>json string email: the email address the invitation is sent to
        :>json string status: the invitation's status
        :>json int organization_id: the organization the invitation is related
                                    to

        :status 200: Invitation is retrieved
        :status 400: Token is not well-formed
        :status 401: Token has expired
        :status 401: User is not authorized
        :status 404: Invitation is not found

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
        .. :quickref: Invitation; Accept an invitation.

        Accept an invitation.

        If an invitation's state is 'pending', this endpoint will set the
        invitation's state to 'accepted' and the authenticated user will be
        added as a partner to the associated organization. If an invitation's
        state is 'accepted' or 'cancelled', the invitation cannot be
        accepted again or accepted at all. In order to accept an invitation,
        the user must be an authenticated user.

        **Example request**:

        .. sourcecode:: http

            GET /invitations/12345678-1234-1234-1234-123456789012/accept
            HTTP/1.1
            Host: example.com
            Authorization: Bearer <token>

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: application/json

            {
                'id': 1,
                'code': '12345678-1234-1234-1234-123456789012',
                'email': 'john@example.org',
                'status': 'accepted',
                'organization_id': 1
            }

        :param int invitation_id: the invitation to accept

        :reqheader Authorization: JSON Web Token to authenticate

        :resheader Content-Type: data is received as application/json

        :>json int id: the invitation's unique id
        :>json string code: the invitation's unique code
        :>json string email: the email address the invitation is sent to
        :>json string status: the invitation's status
        :>json int organization_id: the organization the invitation is related
                                    to

        :status 200: Invitation is accepted
        :status 400: Token is not well-formed
        :status 401: Token has expired
        :status 401: User is not authorized
        :status 404: Invitation is not found
        :status 409: Invitation status is cancelled

        """
        invitation = InvitationModel.query.filter_by(code=code).first()

        if invitation is None:
            abort(404)

        if invitation.status == InvitationStatus.cancelled:
            abort(409, 'The invitation has been cancelled and cannot be '
                       'accepted.')

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
        .. :quickref: Invitation; Cancel an invitation.

        Cancel an invitation.

        If an invitation's state is 'pending', this endpoint will set the
        invitation's state to 'cancelled'. If an invitation's state is
        'accepted' or 'cancelled', the invitation cannot be cancelled at all or
        cancelled again. In order to cancel an invitation, the authenticated
        user must be an admin of the organization that the invitation is
        associated with.

        **Example request**:

        .. sourcecode:: http

            GET /invitations/1/cancel HTTP/1.1
            Host: example.com
            Authorization: Bearer <token>

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: application/json

            {
                'id': 1,
                'code': '12345678-1234-1234-1234-123456789012',
                'email': 'john@example.org',
                'status': 'cancelled',
                'organization_id': 1
            }

        :param int invitation_id: the invitation to cancel

        :reqheader Authorization: JSON Web Token to authenticate

        :resheader Content-Type: data is received as application/json

        :>json int id: the invitation's unique id
        :>json string code: the invitation's unique code
        :>json string email: the email address the invitation is sent to
        :>json string status: the invitation's status
        :>json int organization_id: the organization the invitation is related
                                    to

        :status 200: Invitation is cancelled
        :status 400: Token is not well-formed
        :status 401: Token has expired
        :status 401: User is not authorized
        :status 404: Invitation is not found
        :status 409: Invitation status is accepted

        """
        invitation = InvitationModel.query.get(invitation_id)

        if invitation is None:
            abort(404)

        if invitation.status == InvitationStatus.accepted:
            abort(409, 'The invitation has been accepted and cannot be '
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
        .. :quickref: Invitation; Resend an invitation.

        Resend an invitation.

        If an invitation's state is 'pending', this endpoint will resend the
        invitation to the associated email address. If an invitation's state
        is 'accepted' or 'cancelled', the invitation cannot be resent. In
        order to resend an invitation, the authenticated user must be an admin
        of the organization that the invitation is associated with.

        """
        abort(501)
