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

    partners = db.relationship(
        'Partner', secondary=circle_members, back_populates='circles')

    def __init__(self,
                 name):
        """
        Initialize a circle.

        """
        self.name = name

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
            'name': self.name
        }
