from flask import g
from flask_restful import Resource
from swarm_intelligence_app.models import db
from swarm_intelligence_app.models.invitation import \
    Invitation as InvitationModel
from swarm_intelligence_app.models.invitation import InvitationStatus
from swarm_intelligence_app.models.user import User as UserModel
from swarm_intelligence_app.models.partner import Partner as PartnerModel
from swarm_intelligence_app.models.partner import PartnerType
from swarm_intelligence_app.common import errors
from swarm_intelligence_app.common.authentication import auth


class Invitation(Resource):
    # get an invitation
    # permissions: login_required, organization_member
    @auth.login_required
    def get(self, invitation_id):
        invitation = InvitationModel.query.get(invitation_id)
        if invitation is None:
            raise errors.EntityNotFoundError('invitation', invitation_id)
        return {
            'success': True,
            'data': invitation.serialize
        }

    # set an invitation's status to deleted
    # permissions: login_required, organization_owner
    # conditions: invitation has not been accepted until now
    @auth.login_required
    def delete(self, invitation_id):
        invitation = InvitationModel.query.get(invitation_id)
        if invitation is None:
            raise errors.EntityNotFoundError('invitation', invitation_id)
        invitation.status = InvitationStatus.CANCELLED
        db.session.commit()
        data = invitation.serialize
        return {
            'success': True,
            'data': data
        }


class InvitationResend(Resource):
    # resend an invitation
    # permissions: login_required, organization_owner
    def get(self, invitation_id):
        raise errors.MethodNotImplementedError()


class InvitationAccept(Resource):
    # accept an invitation
    # permissions: login_required
    @auth.login_required
    def get(self, code):
        invitation = InvitationModel.query.filter_by(code=code).first()
        if invitation is None:
            raise errors.EntityNotFoundError('invitation', code)

        user = UserModel.query.filter_by(google_id=g.user['google_id']).first()
        if user is None:
            raise errors.EntityNotFoundError('user', g.user['google_id'])

        partner = PartnerModel(
            PartnerType.PARTNER,
            user.firstname,
            user.lastname,
            user.email,
            user.id,
            invitation.organization_id,
            invitation.id
        )
        db.session.add(partner)
        db.session.commit()

        invitation.status = InvitationStatus.ACCEPTED
        db.session.commit()

        data = invitation.serialize
        return {
            'success': True,
            'data': data
        }
