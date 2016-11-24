"""
Define classes for a association table for circle and partner.

"""
from swarm_intelligence_app.models import db

cm = \
    db.table('cm',
             db.column('circle_id', db.Integer, db.ForeignKey('circle.id')),
             db.column('partner_id', db.Integer, db.ForeignKey('partner.id')))


def __init__():
    """
    Initialize a circle.

    """