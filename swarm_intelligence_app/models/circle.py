"""
Define classes for a circle.

"""
from swarm_intelligence_app.models import db


class Circle(db.Model):
    """
    Define a mapping to the database for a circle.

    """
    id = db.Column(db.Integer, db.ForeignKey('role.id'), primary_key=True)
    strategy = db.Column(db.String(255), nullable=True)

    roles = db.relationship('Role',
                            backref='parent_circle',
                            foreign_keys='Role.parent_circle_id',
                            cascade='all, delete-orphan')

    # implement inheritance, circle extends role
    super = db.relationship('Role',
                            back_populates='derived_circle',
                            foreign_keys='Circle.id',
                            single_parent=True)

    def __init__(self,
                 id,
                 strategy):
        """
        Initialize a circle.

        """
        self.id = id
        self.strategy = strategy

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
            'strategy': self.strategy
        }
