from flask import Flask
from flask_restful import Api
from swarm_intelligence_app.models.models import db
from swarm_intelligence_app.resources import user
from swarm_intelligence_app.common import errors
from swarm_intelligence_app.common import handlers


def load_config(app):
	app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost:3306/swarm_intelligence_test'

def register_error_handlers(app):
    app.register_error_handler(errors.EntityNotFoundError, handlers.handle_entity_not_found)

def create_app():
    app = Flask(__name__)
    load_config(app)
    api = Api(app)
    api.add_resource(user.UserList, '/users')
    api.add_resource(user.User, '/users/<user_id>')
    db.init_app(app)
    register_error_handlers(app)
    return app

app = create_app()

'''
# Setup Database Tables
@app.route("/setup")
def setup():
    db.create_all()
    return "Setup Database Tables"

# Populate Database Tables
@app.route("/populate")
def populate():
    db.session.add(User('Felix', 'Borst', 'f.borst@student.fontys.nl'))
    db.session.add(User('Tobias', 'Wählen', 'tobias.waehlen@googlemail.com'))
    db.session.add(User('Andreas', 'Fischer', 'andreas.fischer@student.fontys.nl'))
    db.session.add(User('Moha', 'Messri', 'm.messri@student.fontys.nl'))
    db.session.add(User('Marvin', 'Rüsenberg', 'm.ruesenberg@student.fontys.nl'))
    db.session.commit()
    return "Populate Database Tables"
'''

if __name__ == "__main__":
    app.run(debug=True)