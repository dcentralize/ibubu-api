"""
Define classes for a circle member.

"""
from swarm_intelligence_app.models import db


role_member = db.Table(
    'role_member',
    db.Column('partner_id', db.Integer, db.ForeignKey('partner.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)
