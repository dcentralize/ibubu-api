from swarm_intelligence_app.models import db

role_members = db.Table(
    'role_members',
  #  db.Column('role_id', db.Integer, db.ForeignKey('role.id')),
    db.Column('partner_id', db.Integer, db.ForeignKey('partner.id')))

