"""
Define classes for a circle member.

"""
from swarm_intelligence_app.models import db


circle_members = db.Table(
    'circle_members',
    db.Column('partner_id', db.Integer, db.ForeignKey('partner.id')),
    db.Column('circle_id', db.Integer, db.ForeignKey(
        'circle.id', onupdate='CASCADE', ondelete='CASCADE'))
)
