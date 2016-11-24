"""
Define classes for a circle.

"""
from swarm_intelligence_app.models import db
from swarm_intelligence_app.models.circlemember import circle_members


class Circle(db.Model):
    """
    Define a mapping to the database for a circle.

    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    is_deleted = db.Column(db.Boolean(), nullable=False)

    """
      Partner Relationship
      ManyToMany
      """
    partners = \
        db.relationship('Partner', secondary=circle_members,
                        back_populates='circles')

    """
    Organization Relationship
    OneToOne
    """
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'),
                                nullable=False)
    organization = db.relationship('Organization', uselist=False,
                                   back_populates='circle')

    """
    Parent Circle Relationship
    OneToMany
    """
    child_circles = db.relationship('Circle',
                                    back_populates='parent_circle_id')

    """
    Child Circle Relationship
    ManyToOne
    """
    parent_circle_id = db.Column(db.Integer, db.ForeignKey('circle.id'),
                                 nullable=True)
    parent = db.relationship('Circle', back_populates='child_circles')

    def __init__(self, name, organization_id, parent_circle_id=None):
        """
        Initialize a circle.

        """
        self.name = name
        self.organization_id = organization_id
        self.parent_circle_id = parent_circle_id
        self.is_deleted = False

    def __repr__(self):
        """
        Return a readable representation of a circle.

        """
        return '<User %r>' % self.id

    @property
    def serialize(self):
        """
        Return a JSON-encoded representation of a circle.

        """
        return {
            'id': self.id,
            'name': self.name,
            'parent_circle_id': self.parent_circle_id,
            'organization_id': self.organization_id,
            'is_deleted': self.is_deleted
        }
