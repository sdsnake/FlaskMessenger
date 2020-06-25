# FlaskMessenger
FSND

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
