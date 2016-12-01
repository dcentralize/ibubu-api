from swarm_intelligence_app.models import db

role_members = db.Table(
    'role_member',
    db.column('partner_id', db.Integer, db.ForeignKey('partner_id')),
    db.column('role_id', db.Integer, db.ForeignKey('role_id')))
