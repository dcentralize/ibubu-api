"""
Define classes for a circle.

"""
from swarm_intelligence_app.models import db


class Circle(db.Model):
    """
    Define a mapping to the database for a circle.

    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    is_deleted = db.Column(db.Boolean(), nullable=False)
    parent_circle_id = db.Column(db.Integer, db.ForeignKey('circle.id'),
                                 nullable=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'),
                                nullable=False)

    partners = db.relationship('Partner', backref='organization')
    child_circles = db.relationship('Circle', backref='circle', lazy='dynamic')

    def __init__(self, name, organization_id, parent_circle_id=None):
        """
        Initialize a circle.

        """
        self.name = name
        self.organization_id = organization_id
        self.parent_circle_id = parent_circle_id
        self.is_deleted = False

    def __repr__(self):
        """
        Return a readable representation of a circle.

        """
        return '<User %r>' % self.id

    @property
    def serialize(self):
        """
        Return a JSON-encoded representation of a circle.

        """
        return {
            'id': self.id,
            'name': self.name,
            'parent_circle_id': self.parent_circle_id,
            'organization_id': self.organization_id,
            'is_deleted': self.is_deleted
        }
