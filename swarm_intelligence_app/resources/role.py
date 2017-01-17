"""
Define the classes for the role API.

"""
from flask import abort
from flask_restful import reqparse, Resource
from swarm_intelligence_app.common.authentication import auth
from swarm_intelligence_app.models import db
from swarm_intelligence_app.models.accountability import Accountability as \
    AccountabilityModel
from swarm_intelligence_app.models.circle import Circle as CircleModel
from swarm_intelligence_app.models.domain import Domain as DomainModel
from swarm_intelligence_app.models.partner import Partner as PartnerModel
from swarm_intelligence_app.models.role import Role as RoleModel
from swarm_intelligence_app.models.role import RoleType


class Role(Resource):
    """
    Define the endpoints for the role node.

    """
    @auth.login_required
    def get(self, role_id):
        """
        .. :quickref: Role; Retrieve a role.

        Retrieve a role.

        **Example request**:

        .. sourcecode:: http

            GET /roles/1 HTTP/1.1
            Host: example.com
            Authorization: Bearer <token>

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: application/json

            {
                'id': 5,
                'type': 'custom',
                'name': 'My Role\'s name',
                'purpose': 'My Role\'s purpose',
                'parent_role_id': 1,
                'organization_id': 1
            }

        :param int role_id: the role to retrieve

        :reqheader Authorization: JSON Web Token to authenticate

        :resheader Content-Type: data is received as application/json

        :>json int id: the role's unique id
        :>json string type: the role's type
        :>json string name: the role's name
        :>json string purpose: the role's purpose
        :>json int parent_role_id: the parent role the role is related to
        :>json int organization_id: the organization the role is related to

        :status 200: Role is retrieved
        :status 400: Token is not well-formed
        :status 401: Token has expired
        :status 401: User is not authorized
        :status 404: Role is not found

        """
        role = RoleModel.query.get(role_id)

        if role is None:
            abort(404)

        return role.serialize, 200

    @auth.login_required
    def put(self, role_id):
        """
        .. :quickref: Role; Update a role.

        Update a role.

        **Example request**:

        .. sourcecode:: http

            PUT /roles/5 HTTP/1.1
            Host: example.com
            Authorization: Bearer <token>
            Content-Type: application/json

            {
                'name': 'My Role\'s new name',
                'purpose': 'My Role\'s new purpose'
            }

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: application/json

            {
                'id': 5,
                'type': 'custom',
                'name': 'My Role\'s new name',
                'purpose': 'My Role\'s new purpose',
                'parent_role_id': 1,
                'organization_id': 1
            }

        :param int role_id: the role to update

        :reqheader Authorization: JSON Web Token to authenticate
        :reqheader Content-Type: data is sent as application/json or
                                 application/x-www-form-urlencoded

        :<json string name: the role's name
        :<json string purpose: the role's purpose

        :resheader Content-Type: data is received as application/json

        :>json int id: the role's unique id
        :>json string type: the role's type
        :>json string name: the role's name
        :>json string purpose: the role's purpose
        :>json int parent_role_id: the parent role the role is related to
        :>json int organization_id: the organization the role is related to

        :status 200: Role is updated
        :status 400: Parameters are missing
        :status 400: Token is not well-formed
        :status 401: Token has expired
        :status 401: User is not authorized
        :status 404: Role is not found

        """
        role = RoleModel.query.get(role_id)

        if role is None:
            abort(404)

        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('name', required=True)
        parser.add_argument('purpose', required=True)
        args = parser.parse_args()

        role.name = args['name']
        role.purpose = args['purpose']
        db.session.commit()

        return role.serialize, 200

    @auth.login_required
    def delete(self, role_id):
        """
        .. :quickref: Role; Delete a role.

        Delete a role.

        **Example request**:

        .. sourcecode:: http

            DELETE /roles/5 HTTP/1.1
            Host: example.com
            Authorization: Bearer <token>

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 204 No Content

        :param int role_id: the role to delete

        :reqheader Authorization: JSON Web Token to authenticate

        :status 204: Role is deleted
        :status 400: Token is not well-formed
        :status 401: Token has expired
        :status 401: User is not authorized
        :status 404: Role is not found
        :status 409: Role type is other than custom
        :status 409: Role is an anchor circle of an organization

        """
        role = RoleModel.query.get(role_id)

        if role is None:
            abort(404)

        if role.type != RoleType.custom:
            abort(409, 'Cannot delete role of type other than custom circle.')

        if role.parent_circle_id is None:
            abort(409, 'The anchor circle of an organization cannot be '
                       'deleted.')

        db.session.delete(role)
        db.session.commit()

        return None, 204


class RoleMembers(Resource):
    """
    Define the endpoints for the members edge of the role node.

    """
    def get(self,
            role_id):
        """
        .. :quickref: Role Members; List members of a role.

        List members of a role.

        **Example request**:

        .. sourcecode:: http

            GET /roles/1/members HTTP/1.1
            Host: example.com
            Authorization: Bearer <token>

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: application/json

            [
                {
                    'id': 1,
                    'type': 'admin',
                    'firstname': 'John',
                    'lastname': 'Doe',
                    'email': 'john@example.org',
                    'is_active': True,
                    'user_id': 1,
                    'organization_id': 1,
                    'invitation_id': null
                }
            ]

        :param int role_id: the role the members are listed for

        :reqheader Authorization: JSON Web Token to authenticate

        :resheader Content-Type: data is received as application/json

        :>jsonarr int id: the partner's unique id
        :>jsonarr string type: the partner's type
        :>jsonarr string firstname: the partner's firstname
        :>jsonarr string lastname: the partner's lastname
        :>jsonarr string email: the partner's email address
        :>jsonarr boolean is_active: the partner's status
        :>jsonarr int user_id: the user account the partner is related to
        :>jsonarr int organization_id: the organization the partner is
                                       related to
        :>jsonarr int invitation_id: the invitation the partner is related to

        :status 200: Members are listed
        :status 400: Token is not well-formed
        :status 401: Token has expired
        :status 401: User is not authorized
        :status 404: Role is not found

        """
        role = RoleModel.query.get(role_id)

        if role is None:
            abort(404)

        data = [i.serialize for i in role.members]

        return data, 200


class RoleMembersAssociation(Resource):
    """
    Define the endpoints for the members association edge of the role node.

    """
    def put(self,
            role_id,
            partner_id):
        """
        .. :quickref: Role Members; Assign a partner to a role.

        Assign a partner to a role.

        **Example request**:

        .. sourcecode:: http

            PUT /roles/5/members/1 HTTP/1.1
            Host: example.com
            Authorization: Bearer <token>

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 204 No Content

        :param int role_id: the role the partner is assigned to
        :param int partner_id: the partner who is assigned to the role

        :reqheader Authorization: JSON Web Token to authenticate

        :status 204: Partner is assigned to role
        :status 400: Token is not well-formed
        :status 401: Token has expired
        :status 401: User is not authorized
        :status 404: Role is not found
        :status 404: Partner is not found
        :status 409: Role is not associated with partner's organization

        """
        role = RoleModel.query.get(role_id)

        if role is None:
            abort(404)

        partner = PartnerModel.query.get(partner_id)

        if partner is None:
            abort(404)

        if role.organization_id != partner.organization_id:
            abort(409, 'Cannot assign a partner to a role that is not '
                       'associated with the partner\'s organization.')

        role.members.append(partner)
        db.session.commit()

        return None, 204

    def delete(self,
               role_id,
               partner_id):
        """
        .. :quickref: Role Members; Unassign a partner from a role.

        Unassign a partner from a role.

        **Example request**:

        .. sourcecode:: http

            DELETE /roles/5/members/1 HTTP/1.1
            Host: example.com
            Authorization: Bearer <token>

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 204 No Content

        :param int role_id: the role the partner is unassigned from
        :param int partner_id: the partner who is unassigned from the role

        :reqheader Authorization: JSON Web Token to authenticate

        :status 204: Partner is unassigned from role
        :status 400: Token is not well-formed
        :status 401: Token has expired
        :status 401: User is not authorized
        :status 404: Role is not found
        :status 404: Partner is not found

        """
        role = RoleModel.query.get(role_id)

        if role is None:
            abort(404)

        partner = PartnerModel.query.get(partner_id)

        if partner is None:
            abort(404)

        role.members.remove(partner)
        db.session.commit()

        return None, 204


class RoleDomains(Resource):
    """
    Define the endpoints for the domain edge of the role node.

    """
    @auth.login_required
    def get(self, role_id):
        """
        .. :quickref: Role Domains; List domains of a role.

        List domains of a role.

        **Example request**:

        .. sourcecode:: http

            GET /roles/1/domains HTTP/1.1
            Host: example.com
            Authorization: Bearer <token>

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: application/json

            [
                {
                    'id': 1,
                    'title': 'Domain\'s title',
                    'role_id': 1
                }
            ]

        :param int role_id: the role the domains are listed for

        :reqheader Authorization: JSON Web Token to authenticate

        :resheader Content-Type: data is received as application/json

        :>jsonarr int id: the domain's unique id
        :>jsonarr string title: the domain's title
        :>jsonarr int role_id: the role the domain is related to

        :status 200: Domains are listed
        :status 400: Token is not well-formed
        :status 401: Token has expired
        :status 401: User is not authorized
        :status 404: Role is not found

        """
        role = RoleModel.query.get(role_id)

        if role is None:
            abort(404)

        data = [i.serialize for i in role.domains]

        return data, 200

    @auth.login_required
    def post(self, role_id):
        """
        .. :quickref: Role Domains; Add a domain to a role.

        Add a domain to a role.

        **Example request**:

        .. sourcecode:: http

            POST /roles/1/domains HTTP/1.1
            Host: example.com
            Authorization: Bearer <token>
            Content-Type: application/json

            {
                'title': 'Domain\'s title'
            }

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 201 Created
            Content-Type: application/json

            {
                'id': 1,
                'title': 'Domain\'s title',
                'role_id': 1
            }

        :param int role_id: the role the domain is added to

        :reqheader Authorization: JSON Web Token to authenticate
        :reqheader Content-Type: data is sent as application/json or
                                 application/x-www-form-urlencoded

        :<json string title: the domain's title

        :resheader Content-Type: data is received as application/json

        :>json int id: the domain's unique id
        :>json string title: the domain's title
        :>json int role_id: the role the domain is related to

        :status 201: Domain is added
        :status 400: Parameters are missing
        :status 400: Token is not well-formed
        :status 401: Token has expired
        :status 401: User is not authorized
        :status 404: Role is not found

        """
        role = RoleModel.query.get(role_id)

        if role is None:
            abort(404)

        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('title', required=True)
        args = parser.parse_args()

        domain = DomainModel(args['title'], role.id)

        role.domains.append(domain)
        db.session.commit()

        return domain.serialize, 200


class RoleAccountabilities(Resource):
    """
    Define the endpoints for the accountability edge of the role node.

    """
    @auth.login_required
    def get(self, role_id):
        """
        .. :quickref: Role Accountabilities; List accountabilities of a role.

        List accountabilities of a role.

        **Example request**:

        .. sourcecode:: http

            GET /roles/1/accountabilities HTTP/1.1
            Host: example.com
            Authorization: Bearer <token>

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Content-Type: application/json

            [
                {
                    'id': 1,
                    'title': 'Accountability\'s title',
                    'role_id': 1
                }
            ]

        :param int role_id: the role the accountabilities are listed for

        :reqheader Authorization: JSON Web Token to authenticate

        :resheader Content-Type: data is received as application/json

        :>jsonarr int id: the accountability's unique id
        :>jsonarr string title: the accountability's title
        :>jsonarr int role_id: the role the accountability is related to

        :status 200: Accountabilities are listed
        :status 400: Token is not well-formed
        :status 401: Token has expired
        :status 401: User is not authorized
        :status 404: Role is not found

        """
        role = RoleModel.query.get(role_id)

        if role is None:
            abort(404)

        data = [i.serialize for i in role.accountabilities]

        return data, 200

    @auth.login_required
    def post(self, role_id):
        """
        .. :quickref: Role Accountabilities; Add an accountability to a role.

        Add an accountability to a role.

        **Example request**:

        .. sourcecode:: http

            POST /roles/1/accountabilities HTTP/1.1
            Host: example.com
            Authorization: Bearer <token>
            Content-Type: application/json

            {
                'title': 'Accountability\'s title'
            }

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 201 Created
            Content-Type: application/json

            {
                'id': 1,
                'title': 'Accountability\'s title',
                'role_id': 1
            }

        :param int role_id: the role the accountability is added to

        :reqheader Authorization: JSON Web Token to authenticate
        :reqheader Content-Type: data is sent as application/json or
                                 application/x-www-form-urlencoded

        :<json string title: the accountability's title

        :resheader Content-Type: data is received as application/json

        :>json int id: the accountability's unique id
        :>json string title: the accountability's title
        :>json int role_id: the role the accountability is related to

        :status 201: Accountability is added
        :status 400: Parameters are missing
        :status 400: Token is not well-formed
        :status 401: Token has expired
        :status 401: User is not authorized
        :status 404: Role is not found

        """
        role = RoleModel.query.get(role_id)

        if role is None:
            abort(404)

        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('title', required=True)
        args = parser.parse_args()

        accountability = AccountabilityModel(args['title'], role.id)

        role.accountabilities.append(accountability)
        db.session.commit()

        return accountability.serialize, 201


class RoleCircle(Resource):
    """
    Define the endpoints for the circle edge of the role node.

    """
    @auth.login_required
    def put(self,
            role_id):
        """
        .. :quickref: Role Circle; Add circle properties to a role.

        Add circle properties to a role.

        **Example request**:

        .. sourcecode:: http

            PUT /roles/5/circle HTTP/1.1
            Host: example.com
            Authorization: Bearer <token>

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 204 No Content

        :param int role_id: the role to add circle properties to

        :reqheader Authorization: JSON Web Token to authenticate

        :status 204: Circle properties are added to role
        :status 400: Token is not well-formed
        :status 401: Token has expired
        :status 401: User is not authorized
        :status 404: Role is not found
        :status 409: Role type is other than custom

        """
        role = RoleModel.query.get(role_id)

        if role is None:
            abort(404)

        if role.type == RoleType.circle:
            pass
        elif role.type == RoleType.custom:
            try:
                role.type = RoleType.circle

                circle = CircleModel(role.id, None)
                db.session.add(circle)
                db.session.flush()

                lead_link = RoleModel(RoleType.lead_link, 'Lead Link',
                                      'Lead Link\'s Purpose', role.id,
                                      role.organization_id)
                db.session.add(lead_link)

                secretary = RoleModel(RoleType.secretary, 'Secretary',
                                      'Secretary\'s Purpose', role.id,
                                      role.organization_id)
                db.session.add(secretary)

                facilitator = RoleModel(RoleType.facilitator, 'Facilitator',
                                        'Facilitator\'s Purpose', role.id,
                                        role.organization_id)
                db.session.add(facilitator)

                db.session.commit()
            except:
                db.session.rollback()
                abort(409, 'Cannot add circle properties to this role.')
        else:
            abort(409, 'Cannot add circle properties to a role that is not a '
                       'custom role.')

        return None, 204

    @auth.login_required
    def delete(self,
               role_id):
        """
        .. :quickref: Role Circle; Remove circle properties from a role.

        Remove circle properties from a role.

        **Example request**:

        .. sourcecode:: http

            DELETE /roles/5/circle HTTP/1.1
            Host: example.com
            Authorization: Bearer <token>

        **Example response**:

        .. sourcecode:: http

            HTTP/1.1 204 No Content

        :param int role_id: the role to remove circle properties from

        :reqheader Authorization: JSON Web Token to authenticate

        :status 204: Circle properties are removed from role
        :status 400: Token is not well-formed
        :status 401: Token has expired
        :status 401: User is not authorized
        :status 404: Role is not found
        :status 409: Role is other than circle
        :status 409: Role is an anchor circle of an organization

        """
        role = RoleModel.query.get(role_id)

        if role is None:
            abort(404)

        if role.type != RoleType.circle:
            abort(409, 'Cannot remove circle properties from a role that is '
                       'not a circle.')

        if role.parent_circle is None:
            abort(409, 'Cannot remove circle properties from a role that is '
                       'an anchor circle.')

        try:
            role.type = RoleType.custom

            db.session.delete(role.derived_circle)
            db.session.commit()
        except:
            db.session.rollback()
            abort(409, 'Cannot remove circle properties from this role.')

        return None, 204
