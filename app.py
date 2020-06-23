import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import json
import sys
from models import setup_db, Room, Message
from authlib.integrations.flask_client import OAuth
from auth import AuthError, requires_auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
  CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
    CORS(app, resources={r"*": {"origins": "*"}},
         supports_credentials=True)

    '''
  after_request decorator to set Access-Control-Allow
  '''
    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response

    @app.route('/', methods=['GET'])
    def get_home():
        return "hello welcome to messagor"

    @app.route('/rooms/<int:room_id>/messages/', methods=['GET'])
    @requires_auth('get:messages')
    def get_messages(jwt, room_id):
        try:

            messages = Message.query.filter(Message.room_id == room_id).all()
            if not messages:
                abort(404)
            formated_messages = [
                message.format() for message in messages]
            return jsonify({
                'success': True,
                'messages': formated_messages
            })
        except:
            print(sys.exc_info())
            abort(422)

    @app.route('/rooms/', methods=['GET'])
    @requires_auth('get:rooms')
    def get_rooms(jwt):
        try:
            rooms = Room.query.all()
            formated_rooms = [
                room.format() for room in rooms]
            if rooms == []:
                abort(404)
            print(jwt)
            return jsonify({
                'success': True,
                'rooms': formated_rooms
            })
        except:
            print(sys.exc_info())
            abort(422)

    @app.route('/rooms/<int:room_id>/messages/', methods=['POST'])
    @requires_auth('post:messages')
    def new_message(jwt, room_id):
        active_room = Room.query.get(room_id)
        print(active_room)
        print(room_id)
        try:
            body = request.get_json()
            content = body.get('content')
            avatar = body.get('avatar')
            print(content)
            new_message = Message(content=content, avatar=avatar)
            if content is None:
                abort(422)
            new_message.room = active_room
            print(new_message.room)
            new_message.insert()

            return jsonify({"success": True, "avatar": new_message.avatar, "message": new_message.content})
        except:
            print(sys.exc_info())
            abort(422)

    @app.route('/messages/<int:message_id>/', methods=['PATCH'])
    @requires_auth('patch:messages')
    def update_message(jwt, message_id):
        body = request.get_json()
        try:
            message = Message.query.filter(
                Message.id == message_id).one_or_none()

            if message is None:
                abort(404)
            message.content = body.get('content')
            message.update()
            return jsonify({
                'success': True,
                'message': message.content
            })
        except:
            abort(404)

    @app.route('/messages/<int:message_id>/', methods=['DELETE'])
    @requires_auth('delete:messages')
    def delete_message(jwt, message_id):
        try:
            message = Message.query.filter(
                Message.id == message_id).one_or_none()
            if message is None:
                abort(404)
            message.delete()
            messages = Message.query.filter(
                Message.room_id == message.room_id).all()
            print(message)
            formated_messages = [
                message.format() for message in messages]

            return jsonify({"success": True, 'deleted': message_id, "messages": formated_messages})
        except:
            print(sys.exc_info())
            abort(422)

        # Error Handling
    '''
    error handling for unprocessable entity
    '''
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    '''
        implement error handler for 404
        error handler should conform to general task above
    '''

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    '''
        error handler for AuthError
        error handler should conform to general task above
    '''

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error['description']
        }), error.status_code

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
