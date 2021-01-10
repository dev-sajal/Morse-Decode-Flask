from . import app, db
from flask import Flask
import pytest


class TestCases():
    client = app.test_client()

    @pytest.fixture(scope='module')
    def setUp(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testing.db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        db.init_app(app)
        db.create_all()
        yield app

    def test_register_success(self):
        url = '/register'
        payload = '{"username": "test01", "password": "test"}'
        header = {"cache-control": "no-cache", "content-type": "application/json"}
        response = self.client.post(url, data=payload, headers=header)

        assert response.status_code == 201
    
    def test_register_fail(self):
        url = '/register'
        payload = '{"username": "test01", "password": "test"}'
        header = {"cache-control": "no-cache", "content-type": "application/json"}
        response = self.client.post(url, data=payload, headers=header)

        assert response.status_code == 400

    def test_login_user(self):
        url = '/login'
        payload = '{"username": "test01", "password": "test"}'
        header = {"cache-control": "no-cache", "content-type": "application/json"}
        response = self.client.post(url, data=payload, headers=header)

        assert response.status_code == 200

    def test_logout_user(self):
        url = '/logout'
        header = {"cache-control": "no-cache", "content-type": "application/json"}
        response = self.client.post(url, headers=header)

        assert response.status_code == 200

    def test_logout_fail(self):
        url = '/logout'
        header = {"cache-control": "no-cache", "content-type": "application/json"}
        response = self.client.post(url, headers=header)

        assert response.status_code == 400

    def test_decrypt(self):
        url = '/decrypt'
        payload = '{"message": "Hello"}'
        header = {"cache-control": "no-cache", "content-type": "application/json"}
        response = self.client.post(url, data=payload, headers=header)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
    