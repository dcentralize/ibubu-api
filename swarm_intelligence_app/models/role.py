"""
Define classes for a role.

"""
from enum import Enum

from swarm_intelligence_app.models import db


class RoleType(Enum):
    """
    Define values for a role's type.

    """
    lead_link = 'lead_link'
    rep_link = 'rep_link'
    cross_link = 'cross_link'
    facilitator = 'facilitator'
    secretary = 'secretary'
    circle = 'circle'
    custom = 'custom'


class Role(db.Model):
    """
    Define a mapping to the database for a role.

    """
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Enum(RoleType), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    purpose = db.Column(db.String(255), nullable=False)
    parent_circle_id = db.Column(db.Integer, db.ForeignKey('circle.id'),
                                 nullable=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'),
                                nullable=False)

    members = db.relationship('Partner',
                              secondary='role_member',
                              back_populates='memberships')
    #                         cascade='all, delete-orphan')

    domains = db.relationship('Domain',
                              backref='role',
                              cascade='all, delete-orphan')

    accountabilities = db.relationship('Accountability',
                                       backref='role',
                                       cascade='all, delete-orphan')

    # implement inheritance, circle extends role
    derived_circle = db.relationship('Circle',
                                     back_populates='super',
                                     foreign_keys='Circle.id',
                                     uselist=False,
                                     cascade='all, delete-orphan')

    def __init__(self,
                 type,
                 name,
                 purpose,
                 parent_circle_id,
                 organization_id):
        """
        Initialize a role.

        """
        self.type = type
        self.name = name
        self.purpose = purpose
        self.parent_circle_id = parent_circle_id
        self.organization_id = organization_id

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
            'type': self.type.value,
            'name': self.name,
            'purpose': self.purpose,
            'parent_circle_id': self.parent_circle_id,
            'organization_id': self.organization_id
        }
