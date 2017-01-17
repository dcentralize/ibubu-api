*****************
Extending the API
*****************

Project Structure
=================

The main building blocks of the Swarm Intelligence App are resources and models. The following project structure shows the separation of different modules. Any resources are located in the *resources/* folder; any models in the *models/* folder. Helpers used accross the application are located in the *common/* folder. The app is configured in *config.py* and initialized in *app.py*, which is the main entry point of the application. ::

    swarm_intelligence_app/         # application root directory
        common/                     # any helpers and utils
            __init.py__
            authentication.py
        docs/                       # any documentation source files
        models/                     # any models
            __init__.py
            accountability.py
            circle.py
            domain.py
            invitation.py
            organization.py
            partner.py
            policy.py
            role.py
            role_member.py
            user.py
        resources/                  # any resources
            __init__.py
            accountability.py
            circle.py
            domain.py
            invitation.py
            organization.py
            partner.py
            policy.py
            role.py
            user.py
        tests/                      # any tests
        __init__.py
        app.py                      # application entry point
        config.py                   # application configuration

Adding a Resource
=================

Resources are implemented with `Flask-RESTful <http://flask-restful-cn.readthedocs.io/en/0.3.5/>`_, an extension for `Flask <http://flask.pocoo.org>`_ that adds support for building RESTful APIs. A basic CRUD resource can be defined in *resources/myresource.py* and looks like this: ::

    from flask_restful import Resource

    class MyResource(Resource):
        def post(self):             # create a new resource
            ...                     # insert data
            return 201, {}          # return status 201 and JSON data

        def get(self, id):          # read a resource
            ...                     # query data
            return 200, {}          # return status 200 and JSON data

        def put(self, id):          # update a resource
            ...                     # update data
            return 200, {}          # return status 200 and JSON data

        def delete(self, id):       # delete a resource
            ...                     # delete data
            return 204, None        # return status 204

In *app.py* import your resource class ::

    from swarm_intelligence_app.resources.myresource import MyResource

and add it to the API object ::

    def create_app():
        ...
        api.add_resource(MyResource, '/myresource')
        ...

Adding a Model
==============

The Swarm Intelligence App uses `Flask-SQLAlchemy <http://flask-sqlalchemy.pocoo.org/2.1/>`_, an extension that provides support for `SQLAlchemy <http://www.sqlalchemy.org/>`_. SQLAlchemy is an SQL toolkit and Object Relational Mapper for Python. A simple model can be defined in *models/mymodel.py* and looks like this: ::

    from swarm_intelligence_app.models import db

    class MyModel(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        firstname = db.Column(db.String(100), nullable=False)
        lastname = db.Column(db.String(100), nullable=False)

        def __init__(self, firstname):
            self.firstname = firstname
            self.lastname = lastname

        def __repr__(self):
            return '<MyModel %r>' % self.id

        @property
        def serialize(self):
            return {
                'firstname': self.firstname,
                'lastname': self.lastname
            }

Import the SQLAlchemy object and your model class and use your model as follows: ::

    from swarm_intelligence_app.models import db
    from swarm_intelligence_app.models.mymodel import MyModel

    try:
        # insert data
        mymodel = MyModel('John', 'Doe')
        db.session.add(mymodel)
        db.session.flush()

        # query data
        mymodel = MyModel.query.get(mymodel.id)

        # update data
        mymodel.lastname = 'Smith'

        # delete data
        db.session.delete(mymodel)

        # persist data
        db.session.commit()
    except:
        db.session.rollback()
