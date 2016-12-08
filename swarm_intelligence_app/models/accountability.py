"""
Define classes for a accountability.

"""
from swarm_intelligence_app.models import db


class Accountability(db.Model):
    """
    Define a mapping to the database for a accountability.

    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=True)

    def __init__(self, title, description, role_id):
        """
        Initialize a accountability.

        """
        self.title = title
        self.description = description
        self.role_id = role_id

    def __repr__(self):
        """
        Return a readable representation of a accountability.

        """
        return '<Accountability %r>' % self.id

    @property
    def serialize(self):
        """
        Return a JSON-encoded representation of a accountability.

        """
        return {
            'id': self.id,
            'title': self.name,
            'role_id': self.role_id
        }
