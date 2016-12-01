"""
Define the main entry point for the tests.

"""
import pytest
from swarm_intelligence_app import app as api


@pytest.fixture
def app():
    """
    Initialize the api for the test package.

    :return: Flask Object
    """
    app = api.create_app()
    return app
