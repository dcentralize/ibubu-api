"""
Define classes for an invitation.

"""
import uuid
from enum import Enum

from swarm_intelligence_app.models import db


class InvitationStatus(Enum):
    """
    Define values for an invitation's status.

    """
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    CANCELLED = 'cancelled'


class Invitation(db.Model):
    """
    Define a mapping to the database for an invitation.

    """
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(36), unique=True, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    status = db.Column(db.Enum(InvitationStatus), nullable=False)
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'),
                                nullable=False)

    def __init__(self,
                 email,
                 organization_id):
        """
        Initialize an invitation.

        """
        self.code = str(uuid.uuid4())
        self.email = email
        self.status = InvitationStatus.PENDING
        self.organization_id = organization_id

    def __repr__(self):
        """
        Return a readable representation of an invitation.

        """
        return '<Invitation %r>' % self.id

    @property
    def serialize(self):
        """
        Return a JSON-encoded representation of an invitation.

        """
        return {
            'id': self.id,
            'code': self.code,
            'email': self.email,
            'status': self.status.value,
            'organization_id': self.organization_id
        }