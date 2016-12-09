"""
Define the main entry point for the tests.

"""
import pytest
from flask import Blueprint, Flask, render_template
from flask_restful import Api
from flask_restful_swagger import swagger
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists
from swarm_intelligence_app.common import errors
from swarm_intelligence_app.common import handlers
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
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        'mysql+pymysql://root@localhost:3306/swarm_intelligence'
    app.config['GOOGLE_CLIENT_ID'] = \
        '806916571874-7tnsbrr22526ioo36l8njtqj2st8nn54.apps' \
        '.googleusercontent.com'


def register_error_handlers(app):
    """
    Register error handlers for the given app.

    """
    app.register_error_handler(errors.EntityNotFoundError,
                               handlers.handle_entity_not_found)
    app.register_error_handler(errors.EntityAlreadyExistsError,
                               handlers.handle_entity_already_exists)
    app.register_error_handler(errors.EntityNotModifiedError,
                               handlers.handle_entity_not_modified)
    app.register_error_handler(errors.MethodNotImplementedError,
                               handlers.handle_method_not_implemented)


@pytest.fixture
def app():
    """
    Create the main flask app.

    """
    app = Flask('pytest')
    app.config.update(DEBUG=True)
    load_config(app)
    api = Api(app)
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
    api.add_resource(organization.OrganizationRoles,
                     '/organizations/<organization_id>/roles')
    api.add_resource(partner.Partner,
                     '/partners/<partner_id>')
    api.add_resource(partner.PartnerCircles,
                     '/partners/<partner_id>/circles')
    api.add_resource(partner.PartnerAdmin,
                     '/partners/<partner_id>/admin')
    api.add_resource(partner.PartnerMetrics,
                     '/partners/<partner_id>/metrics')
    api.add_resource(partner.PartnerChecklists,
                     '/partners/<partner_id>/checklists')
    api.add_resource(partner.PartnerRoles,
                     '/partners/<partner_id>/roles')
    api.add_resource(invitation.Invitation,
                     '/invitations/<invitation_id>')
    api.add_resource(invitation.InvitationResend,
                     '/invitations/<invitation_id>/resend')
    api.add_resource(invitation.InvitationAccept,
                     '/invitations/<code>/accept')
    api.add_resource(circle.Circle,
                     '/circles/<circle_id>')
    api.add_resource(circle.CircleSubcircles,
                     '/circles/<circle_id>/subcircles')
    api.add_resource(circle.CircleRole,
                     '/circles/<circle_id>/role')
    api.add_resource(circle.CircleRoles,
                     '/circles/<circle_id>/roles')
    api.add_resource(circle.CircleMembers,
                     '/circles/<circle_id>/members',
                     '/circles/<circle_id>/members/<partner_id>')
    api.add_resource(circle.CircleDomains,
                     '/circles/<circle_id>/domains')
    api.add_resource(circle.CircleAccountabilities,
                     '/circles/<circle_id>/accountabilities')
    api.add_resource(role.Role,
                     '/roles/<role_id>')
    api.add_resource(role.RoleMembers,
                     '/roles/<role_id>/members',
                     '/roles/<role_id>/members/<partner_id>')
    api.add_resource(role.RoleCircles,
                     '/roles/<role_id>/circle')
    api.add_resource(role.RoleDomains,
                     '/roles/<role_id>/domains')
    api.add_resource(role.RoleAccountabilities,
                     '/roles/<role_id>/accountabilities')
    api.add_resource(policy.Policy,
                     '/policies/<policy_id>')
    api.add_resource(accountability.Accountability,
                     '/accountabilities/<accountability_id>')
    api.add_resource(domain.Domain,
                     '/domains/<domain_id>')
    api.add_resource(domain.DomainPolicies,
                     '/domains/<domain_id>/policies')
    db.init_app(app)
    register_error_handlers(app)

    @app.route('/signin')
    def signin():
        """
        Provide a Google Sign-In Page.

        """
        return render_template('google_signin.html')

    @app.route('/setup')
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

    @app.route('/populate')
    def populate():
        """
        Populate the database.

        """
        return 'Populate Database Tables'

    return app