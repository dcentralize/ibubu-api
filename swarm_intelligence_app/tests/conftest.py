"""
Define the main entry point for the tests.

"""
import pytest
from flask import Flask, render_template, jsonify
from flask_restful import Api
from swarm_intelligence_app.common import errors
from swarm_intelligence_app.common import handlers
from swarm_intelligence_app.models import db
from swarm_intelligence_app.resources import circle
from swarm_intelligence_app.resources import invitation
from swarm_intelligence_app.resources import organization
from swarm_intelligence_app.resources import partner
from swarm_intelligence_app.resources import role
from swarm_intelligence_app.resources import user


def load_config(app):
    """
    Load configuration for the given app.

    """
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        'mysql+pymysql://root:1111@localhost:3306/swarm_intelligence'
    app.config['GOOGLE_CLIENT_ID'] = \
        '806916571874-7tnsbrr22526ioo36l8njtqj2st8nn54.apps' \
        '.googleusercontent.com'
    app.config['DEBUG'] = True


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
    app = Flask(__name__)

    load_config(app)
    api = Api(app)
    api.add_resource(user.User,
                     '/me')
    api.add_resource(user.UserOrganizations,
                     '/me/organizations')
    api.add_resource(organization.Organization,
                     '/organizations/<organization_id>')
    api.add_resource(organization.OrganizationMembers,
                     '/organizations/<organization_id>/members')
    api.add_resource(organization.OrganizationAdmins,
                     '/organizations/<organization_id>/admins')
    api.add_resource(organization.OrganizationInvitations,
                     '/organizations/<organization_id>/invitations')
    api.add_resource(partner.Partner,
                     '/partners/<partner_id>')
    #    api.add_resource(partner.PartnerAdmin,
    #                    '/partners/<partner_id>/admin')
    api.add_resource(partner.PartnerMetrics,
                     '/partners/<partner_id>/metrics')
    api.add_resource(partner.PartnerChecklists,
                     '/partners/<partner_id>/checklists')
    api.add_resource(invitation.Invitation,
                     '/invitations/<invitation_id>')
    api.add_resource(invitation.InvitationResend,
                     '/invitations/<invitation_id>/resend')
    api.add_resource(invitation.InvitationAccept,
                     '/invitations/<code>/accept')
    api.add_resource(circle.Circle,
                     '/circles/<circle_id>')
    api.add_resource(circle.CircleRoles,
                     '/circles/<circle_id>/roles')
    api.add_resource(circle.CircleMembers,
                     '/circles/<circle_id>/members')
    api.add_resource(role.Role,
                     '/roles/<role_id>')
    api.add_resource(role.RoleMembers,
                     '/roles/<role_id>/members')

    register_error_handlers(app)
    db.init_app(app)

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
        print("setup")
        db.drop_all()
        db.create_all()
        return 'Setup Database Tables'

    @app.route('/populate')
    def populate():
        """
        Populate the database.

        """
        return 'Populate Database Tables'

    return app
