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
    name = db.Column(db.String(100), nullable=False)
    purpose = db.Column(db.String(100), nullable=True)
    strategy = db.Column(db.String(255), nullable=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'),
                                nullable=False)
    circle_id = db.Column(db.Integer,
                          db.ForeignKey('circle.id',
                                        onupdate='CASCADE',
                                        ondelete='CASCADE'),
                          nullable=True)

    partners = db.relationship(
        'Partner', secondary=circle_members, back_populates='circles')

    # subcircles = db.relationship('Circle')
    # parent_circle = db.relationship('Circle', remote_side=[id])

    def __init__(self,
                 name,
                 purpose,
                 strategy,
                 organization_id,
                 circle_id):
        """
        Initialize a circle.

        """
        self.name = name
        self.purpose = purpose
        self.strategy = strategy
        self.organization_id = organization_id
        self.circle_id = circle_id

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
            'name': self.name,
            'purpose': self.purpose,
            'strategy': self.strategy,
            'organization_id': self.organization_id,
            'circle_id': self.circle_id
        }
