"""
Define the main entry point for the app.

"""
from flask import Flask, render_template
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


def create_app():
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
    db.init_app(app)
    register_error_handlers(app)
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
    db.drop_all()
    db.create_all()
    return 'Setup Database Tables'


@application.route('/populate')
def populate():
    """
    Populate the database.

    """
    return 'Populate Database Tables'


if __name__ == '__main__':
    application.run(host='localhost', port=5432, debug=False)
