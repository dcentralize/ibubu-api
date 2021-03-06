"""
Define classes for a domain.

"""
from swarm_intelligence_app.models import db


class Domain(db.Model):
    """
    Define a mapping to the database for a domain.

    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)

    policies = db.relationship('Policy',
                               backref='domain',
                               cascade='all, delete-orphan')

    def __init__(self, title, role_id):
        """
        Initialize a domain.

        """
        self.title = title
        self.role_id = role_id

    def __repr__(self):
        """
        Return a readable representation of a domain.

        """
        return '<Domain %r>' % self.id

    @property
    def serialize(self):
        """
        Return a JSON-encoded representation of a domain.

        """
        return {
            'id': self.id,
            'title': self.title,
            'role_id': self.role_id
        }
