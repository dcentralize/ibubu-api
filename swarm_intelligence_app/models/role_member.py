"""
Define the table for the relationship role and member API.

"""
from swarm_intelligence_app.models import db

role_members = db.Table(
    'role_members',
    db.Column('partner_id', db.Integer, db.ForeignKey('partner.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id',
                                                   onupdate='CASCADE',
                                                   ondelete='CASCADE'))
)
