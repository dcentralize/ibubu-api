"""
Define the main entry point for the app.

"""
import os

from flask import Flask, render_template
from flask_cors import CORS
from flask_restful import Api
from flask_restful_swagger import swagger
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists
from swarm_intelligence_app.config import config
from swarm_intelligence_app.models import db
from swarm_intelligence_app.resources import accountability
from swarm_intelligence_app.resources import circle
from swarm_intelligence_app.resources import domain
from swarm_intelligence_app.resources import invitation
from swarm_intelligence_app.resources import organization
from swarm_intelligence_app.resources import partner
from swarm_intelligence_app.resources import policy
from swarm_intelligence_app.resources import role
from swarm_intelligence_app.resources import user


def load_config(app):
    """
    Load configuration for the given app.

    """
    config_name = os.environ.get('SI_CONFIG_NAME') or 'default'
    app.config.from_object(config[config_name])


def create_app():
    """
    Create the main flask app.

    """
    app = Flask(__name__)
    CORS(app)
    api = Api(app)
    load_config(app)
    api.add_resource(user.UserRegistration,
                     '/register')
    api.add_resource(user.UserLogin,
                     '/login')
    api.add_resource(user.User,
                     '/me')
    api.add_resource(user.UserOrganizations,
                     '/me/organizations')
    api.add_resource(organization.Organization,
                     '/organizations/<organization_id>')
    api.add_resource(organization.OrganizationAnchorCircle,
                     '/organizations/<organization_id>/anchor_circle')
    api.add_resource(organization.OrganizationMembers,
                     '/organizations/<organization_id>/members')
    api.add_resource(organization.OrganizationAdmins,
                     '/organizations/<organization_id>/admins')
    api.add_resource(organization.OrganizationInvitations,
                     '/organizations/<organization_id>/invitations')
    api.add_resource(partner.Partner,
                     '/partners/<partner_id>')
    api.add_resource(partner.PartnerAdmin,
                     '/partners/<partner_id>/admin')
    api.add_resource(partner.PartnerMemberships,
                     '/partners/<partner_id>/memberships')
    api.add_resource(partner.PartnerMetrics,
                     '/partners/<partner_id>/metrics')
    api.add_resource(partner.PartnerChecklists,
                     '/partners/<partner_id>/checklists')
    api.add_resource(invitation.Invitation,
                     '/invitations/<invitation_id>')
    api.add_resource(invitation.InvitationAccept,
                     '/invitations/<code>/accept')
    api.add_resource(invitation.InvitationCancel,
                     '/invitations/<invitation_id>/cancel')
    api.add_resource(invitation.InvitationResend,
                     '/invitations/<invitation_id>/resend')
    api.add_resource(role.Role,
                     '/roles/<role_id>')
    api.add_resource(role.RoleMembers,
                     '/roles/<role_id>/members')
    api.add_resource(role.RoleMembersAssociation,
                     '/roles/<role_id>/members/<partner_id>')
    api.add_resource(role.RoleDomains,
                     '/roles/<role_id>/domains')
    api.add_resource(role.RoleAccountabilities,
                     '/roles/<role_id>/accountabilities')
    api.add_resource(role.RoleCircle,
                     '/roles/<role_id>/circle')
    api.add_resource(circle.Circle,
                     '/circles/<circle_id>')
    api.add_resource(circle.CircleRoles,
                     '/circles/<circle_id>/roles')
    api.add_resource(circle.CircleMembers,
                     '/circles/<circle_id>/members')
    api.add_resource(circle.CircleMembersAssociation,
                     '/circles/<circle_id>/members/<partner_id>')
    api.add_resource(domain.Domain,
                     '/domains/<domain_id>')
    api.add_resource(domain.DomainPolicies,
                     '/domains/<domain_id>/policies')
    api.add_resource(policy.Policy,
                     '/policies/<policy_id>')
    api.add_resource(accountability.Accountability,
                     '/accountabilities/<accountability_id>')
    db.init_app(app)
    return app


application = create_app()


@application.route('/signin')
def signin():
    """
    Provide a Google Sign-In Page.

    """
    return render_template('google_signin.html')


@application.route('/setup')
def setup():
    """
    Setup the database.

    """
    engine = create_engine(
        'mysql+pymysql://root@localhost:3306/swarm_intelligence')
    conn = engine.connect()
    conn.execute('COMMIT')
    # Do not substitute user-supplied database names here.
    conn.execute('DROP DATABASE swarm_intelligence')
    conn.close()
    if not database_exists(engine.url):
        create_database(engine.url)

    db.create_all()
    return 'Setup Database Tables'


if __name__ == '__main__':
    application.run()
