from enum import Enum
from swarm_intelligence_app.models import db


class PartnerType(Enum):
    OWNER = 'owner'
    PARTNER = 'partner'


class Partner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Enum(PartnerType), nullable=False)
    firstname = db.Column(db.String(45), nullable=False)
    lastname = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    is_deleted = db.Column(db.Boolean(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'),
                                nullable=False)
    invitation_id = db.Column(db.Integer, db.ForeignKey('invitation.id'),
                              nullable=True)

    __table_args__ = (db.UniqueConstraint('user_id', 'organization_id',
                                          name='UNIQUE_organization_id_user_id'
                                          ),)

    def __init__(self, type, firstname, lastname, email, user_id,
                 organization_id, invitation_id=None):
        self.type = type
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.is_deleted = False
        self.user_id = user_id
        self.organization_id = organization_id
        self.invitation_id = invitation_id

    def __repr__(self):
        return '<Partner %r>' % self.id

    @property
    def serialize(self):
        return {
            'id': self.id,
            'type': self.type.value,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'email': self.email,
            'is_deleted': self.is_deleted,
            'user_id': self.user_id,
            'organization_id': self.organization_id,
            'invitation_id': self.invitation_id
        }
