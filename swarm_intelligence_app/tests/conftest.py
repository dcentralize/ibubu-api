import pytest
from swarm_intelligence_app.app import create_app
from flask import Flask, jsonify


@pytest.fixture
def app():
    application = create_app()
    return application


@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '42'

    @app.route('/')
    def index():
        return app.response_class('OK')

    @app.route('/ping')
    def ping():
        return jsonify(ping='pong')

    return app