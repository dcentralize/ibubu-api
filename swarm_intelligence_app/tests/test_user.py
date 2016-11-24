from flask import url_for


class TestFixtures:

    def test_config_access(self, config):
        assert config['SECRET_KEY'] == '42'

    def test_client(self, client):
        assert client.get(url_for('ping')).status == '200 OK'
