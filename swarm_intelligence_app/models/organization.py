"""
Define classes for an organization.

"""
from swarm_intelligence_app.models import db


class Organization(db.Model):
    """
    Define a mapping to the database for an organization.

    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    partners = db.relationship('Partner',
                               backref='organization',
                               cascade='all, delete-orphan')

    invitations = db.relationship('Invitation',
                                  backref='organization',
                                  cascade='all, delete-orphan')

    roles = db.relationship('Role',
                            backref='organization',
                            cascade='all, delete-orphan')

    def __init__(self,
                 name):
        """
        Initialize an organization.

        """
        self.name = name

    def __repr__(self):
        """
        Return a readable representation of an organization.

        """
        return '<Organization %r>' % self.id

    @property
    def serialize(self):
        """
        Return a JSON-encoded representation of an organization.

        """
        return {
            'id': self.id,
            'name': self.name,
        }
