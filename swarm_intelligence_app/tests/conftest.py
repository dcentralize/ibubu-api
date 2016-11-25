"""
Define the main entry point for the tests.

"""
import pytest
from swarm_intelligence_app import app as API


@pytest.fixture
def app():
    app = API.create_app()
    return app
