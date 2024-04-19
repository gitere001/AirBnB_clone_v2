#!/usr/bin/python3
"""
script that starts a Flask web application:

listening on 0.0.0.0, port 5000
Routes:
/: display “Hello HBNB!”
/hbnb: display “HBNB”
"""
from flask import Flask
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """display “Hello HBNB!”"""
    return "hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def display_hbnb():
    """route /hbnb"""
    return "HBNB!"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
