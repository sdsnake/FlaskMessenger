import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Room, Message


class MessagorTestCase(unittest.TestCase):
    """This class represents the messagor test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "messagor_test"
        self.database_path = "postgres://{}:{}@{}/{}".format(
            'postgres', 'password', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_create_new_message(self):
        new_message = {
            'content': 'test'
        }
        res = self.client().post('/rooms/1/messages/', json=new_message)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['messages']))

    def test_get_messages(self):
        res = self.client().get('/rooms/1/messages/')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        print(data['messages'])
        self.assertTrue(data['messages'])

    def test_get_rooms(self):
        res = self.client().get('/rooms/')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_question(self):
        res = self.client().delete('/rooms/2/messages/')
        data = json.loads(res.data)

        message = Message.query.filter(Message.id == 2).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 2)
        self.assertTrue(len(data['messages']))
        self.assertEqual(message, None)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
