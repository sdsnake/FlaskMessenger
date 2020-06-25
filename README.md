# FlaskMessenger
FSND

#Heroku url: http://messagor.herokuapp.com/

# Capstone Udacity - Full Stack API Final Project
This project is to deploy a Flask application using Heroku and PostgreSQL and enable Role Based Authentication and roles-based access control git (RBAC) with Auth0 (third-party authentication systems).

#Application: Messagor
A secure app for communicate easily. Based on administrator role to secure and manage the application.

## Getting Started

#### Pre-Requisites
Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

You need pip to for next stage
#### PIP Dependencies

Install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

##### Running the server
From within the backend directory first ensure you are working using your created virtual environment.

To run the server, execute:

```export FLASK_APP=flaskr
export FLASK_APP=app.py
flask run
```

## link for authentication: 

https://sidelo.auth0.com/authorize?audience=messagor&response_type=token&client_id=FhBQ5eiZ3itpOdPSlOF9zwR0lFdPxNOZ&redirect_uri=https://localhost:8100/callback

return the token in url.

## Models
chat rooms contain name and messages 

### Roles

User or Chatter.

get:rooms
get:messages
post:messages

All permissions as Administrator.

get:rooms
get:messages
post:messages
patch:messages
delete:messages

### ENDPOINTS

```

GET '/rooms'

return list rooms

{
    "rooms": [
        {
            "id": 1,
            "name": "main"
        }
    ],
    "success": true
}

GET '/rooms/<int:room_id>/messages'

return messages list

{
    "messages": [
        {
            "avatar": "diego",
            "content": "how are you?",
            "id": 2
        },
        {
            "avatar": "diego",
            "content": "test",
            "id": 3
        },
        {
            "avatar": "diego",
            "content": "test post3",
            "id": 4
        },
        {
            "avatar": "diego",
            "content": "test post3",
            "id": 5
        },
        {
            "avatar": "samantha",
            "content": "fine",
            "id": 6
        },
        {
            "avatar": "diego",
            "content": "good",
            "id": 7
        }
    ],
    "success": true
}

POST '/rooms/<int:room_id>/messages'

return name avatar and message posted with statut success

{
    "avatar": "diego",
    "message": "Hi!",
    "success": true
}

PATCH '/messages/<int:message_id>'

return message modified and success

{
    "message": "change ok",
    "success": true
}

DELETE '/messages/<int:message_id>'

return ID and success

{
    "deleted": 1,
    "messages": [],
    "success": true
}

```
## ERRORS
The application retourn this errors:

```
404: Resource not found
422: unprocessable
401 not authorized
```

## Testing
To run the tests go into root folder application and run in your terminal

```
python test_app.py
```
