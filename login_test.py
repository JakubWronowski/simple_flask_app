from urllib.parse import urlparse
from flask_testing import TestCase
from main import app, db, User

class MyTest(TestCase):

    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
        return app

    def setUp(self):
        db.create_all()
        test_user = User(id='testuser')
        test_user.set_password('testpassword')
        db.session.add(test_user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_login_page(self):
        response = self.client.get('/login')
        self.assert200(response)

    def test_main_page(self):
        response = self.client.get('/')
        self.assertEqual(urlparse(response.location).path, '/login')

