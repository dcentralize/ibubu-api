"""
Define classes for a circle.

"""
from swarm_intelligence_app.models import db
from swarm_intelligence_app.models.circle_member import circle_members


class Circle(db.Model):
    """
    Define a mapping to the database for a circle.

    """
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'),
                        primary_key=True)
    strategy = db.Column(db.String(255), nullable=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'),
                                nullable=False)

    partners = db.relationship('Partner', secondary=circle_members,
                               back_populates='circles', cascade='all,delete')
    roles = db.relationship('Role', backref='circle',
                            primaryjoin='Role.circle_id==Circle.role_id',
                            cascade='all,delete')

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
            'strategy': self.strategy,
            'role_id': self.role_id,
            'organization_id': self.organization_id
        }
