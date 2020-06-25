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
        self.token_admin = os.environ['ADMIN_TOKEN']
        self.token_user = os.environ['USER_TOKEN']

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
            "content": "test post",
            "avatar": "diego"
        }
        res = self.client().post(
            '/rooms/1/messages/',
            headers={
                "Authorization": "Bearer {}".format(
                    self.token_admin)},
            json=new_message)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['message']))

    def test_cannot_create_null_message(self):
        new_message = {
            'contnt': None
        }
        res = self.client().post(
            '/rooms/1/messages/',
            headers={
                "Authorization": "Bearer {}".format(
                    self.token_admin)},
            json=new_message)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_get_messages(self):
        res = self.client().get('/rooms/1/messages/', headers={
            "Authorization": "Bearer {}".format(self.token_admin)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        print(data['messages'])
        self.assertTrue(data['messages'])

    def test_error_get_messages(self):
        res = self.client().get('/rooms/677/messages/', headers={
            "Authorization": "Bearer {}".format(self.token_admin)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_get_rooms(self):
        res = self.client().get('/rooms/', headers={
            "Authorization": "Bearer {}".format(self.token_admin)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_not_authorized_get_rooms(self):
        res = self.client().get('/rooms/')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_delete_message(self):
        res = self.client().delete('/messages/3/', headers={
            "Authorization": "Bearer {}".format(self.token_admin)})
        data = json.loads(res.data)

        message = Message.query.filter(Message.id == 3).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 3)
        self.assertTrue(len(data['messages']))
        self.assertEqual(message, None)

    def test_error_delete_message(self):
        res = self.client().delete('/messages/999/', headers={
            "Authorization": "Bearer {}".format(self.token_admin)})
        data = json.loads(res.data)

        message = Message.query.filter(Message.id == 99).one_or_none()

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_non_authorized_delete_message(self):
        res = self.client().delete('/messages/2/', headers={
            "Authorization": "Bearer {}".format(self.token_user)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_update_message(self):
        res = self.client().patch(
            '/messages/47/',
            headers={
                "Authorization": "Bearer {}".format(
                    self.token_admin)},
            json={
                'content': 'test change'})
        data = json.loads(res.data)
        message = Message.query.filter(Message.id == 47).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(message.format()['content'], 'test change')

    def test_error_update_message(self):
        res = self.client().patch(
            '/messages/755/',
            headers={
                "Authorization": "Bearer {}".format(
                    self.token_admin)},
            json={
                'content': 'test error change'})
        data = json.loads(res.data)
        message = Message.query.filter(Message.id == 5).one_or_none()

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_non_aurthorized_update_message(self):
        res = self.client().patch(
            '/messages/1/',
            headers={
                "Authorization": "Bearer {}".format(
                    self.token_user)},
            json={
                'content': 'test error change'})
        data = json.loads(res.data)
        message = Message.query.filter(Message.id == 5).one_or_none()

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
