"""
Define classes for an accountability.

"""
from swarm_intelligence_app.models import db


class Accountability(db.Model):
    """
    Define a mapping to the database for an accountability.

    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)

    def __init__(self, title, role_id):
        """
        Initialize an accountability.

        """
        self.title = title
        self.role_id = role_id

    def __repr__(self):
        """
        Return a readable representation of an accountability.

        """
        return '<Accountability %r>' % self.id

    @property
    def serialize(self):
        """
        Return a JSON-encoded representation of an accountability.

        """
        return {
            'id': self.id,
            'title': self.title,
            'role_id': self.role_id
        }
