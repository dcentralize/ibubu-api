"""
Define classes for a user.

"""
from sqlalchemy.ext.associationproxy import association_proxy
from swarm_intelligence_app.models import db


class User(db.Model):
    """
    Define a mapping to the database for a user.

    """
    id = db.Column(db.Integer, primary_key=True)
    google_id = db.Column(db.String(100), unique=True, nullable=False)
    firstname = db.Column(db.String(45), nullable=False)
    lastname = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    is_deleted = db.Column(db.Boolean(), nullable=False)

    partners = db.relationship('Partner', backref='user')
    organizations = association_proxy('partners', 'organization')

    def __init__(self,
                 google_id,
                 firstname,
                 lastname,
                 email):
        """
        Initialize a user.

        """
        self.google_id = google_id
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.is_deleted = False

    def __repr__(self):
        """
        Return a readable representation of a user including its id.

        """
        return '<User %r>' % self.id

    @property
    def serialize(self):
        return {
            'id': self.id,
            'google_id': self.google_id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'email': self.email,
            'is_deleted': self.is_deleted
        }
