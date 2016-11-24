import pytest

from flask import request, url_for


class TestFixtures:
    def test_client(self, client):
        assert client.get(url_for('signin')).status == '200 OK'
