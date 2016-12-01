"""
Define classes for a circle.

"""
from swarm_intelligence_app.models import db
from swarm_intelligence_app.models.circle_member import circle_members


class Circle(db.Model):
    """
    Define a mapping to the database for a circle.

    """
    id = db.Column(db.Integer, primary_key=True)
    strategy = db.Column(db.String(255), nullable=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'),
                                nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=True)
    partners = db.relationship(
        'Partner', secondary=circle_members, back_populates='circles')
    roles = db.relationship('Role', backref='circle')

    # subcircles = db.relationship('Circle')
    # parent_circle = db.relationship('Circle', remote_side=[id])

    def __init__(self,
                 strategy,
                 organization_id,
                 role_id):
        """
        Initialize a circle.

        """
        self.strategy = strategy
        self.role_id = role_id
        self.organization_id = organization_id

    def __repr__(self):
        """
        Return a readable representation of a circle.

        """
        return '<Circle %r>' % self.id

    @property
    def serialize(self):
        """
        Return a JSON-encoded representation of a circle.

        """
        return {
            'id': self.id,
            'strategy': self.strategy,
            'role_id': self.role_id,
            'organization_id': self.organization_id
        }
