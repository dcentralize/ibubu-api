from swarm_intelligence_app.models import db
from swarm_intelligence_app.models import role_member
from enum import Enum


class RoleType(Enum):
    LEAD_LINK = 'lead_link'
    REP_LINK = 'rep_link'
    FACILITATOR = 'facilitator'
    SECRETARY = 'secretary'
    CUSTOM = "custom"


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    type = db.Column(db.Enum(RoleType), nullable=False)
    partners = db.relationship('partner', secondary=role_member,
                               back_populates='Role')

    def __init__(self,
                 name,
                 type):
        """
        Initialize a circle.

        """
        self.name = name
        self.type = type

    def __repr__(self):
        """
        Return a readable representation of a role.

        """
        return '<Role %r>' % self.id

    @property
    def serialize(self):
        """
        Return a JSON-encoded representation of a role.

        """
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
        }
