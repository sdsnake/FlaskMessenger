import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from sqlalchemy.sql.expression import func
import random
import json

from models import setup_db, Room, Message


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
        return "hello home"
    return app
