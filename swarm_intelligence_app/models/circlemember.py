"""
Define classes for a association table for circle and partner.

"""
from swarm_intelligence_app.models import db

circle_members = \
    db.Table('circle_members',
             db.Column('partner_id', db.Integer, db.ForeignKey('partner.id')),
             db.Column('circle_id', db.Integer, db.ForeignKey('circle.id'))

             )
