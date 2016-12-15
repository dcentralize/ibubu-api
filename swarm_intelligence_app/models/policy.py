"""
Define classes for a policy.

"""
from swarm_intelligence_app.models import db


class Policy(db.Model):
    """
    Define a mapping to the database for a policy.

    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    domain_id = db.Column(db.Integer, db.ForeignKey('domain.id'),
        nullable=False)

    def __init__(self, title, description, domain_id):
        """
        Initialize a policy.

        """
        self.title = title
        self.description = description
        self.domain_id = domain_id

    def __repr__(self):
        """
        Return a readable representation of a policy.

        """
        return '<Policy %r>' % self.id

    @property
    def serialize(self):
        """
        Return a JSON-encoded representation of a policy.

        """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'domain': self.domain_id
        }
