#!/usr/bin/python3
"""
script that starts a Flask web application:

listening on 0.0.0.0, port 5000
Routes:
/: display “Hello HBNB!”
/hbnb: display “HBNB”
/c/<text>
/python/<text>
/number/<n>
"""
from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """Display "Hello HBNB!"."""
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def display_hbnb():
    """Display "HBNB"."""
    return "HBNB!"


@app.route('/c/<text>', strict_slashes=False)
def display_c_text(text):
    """Display 'C ' followed by the value of the text variable."""
    return f"C {text.replace('_', ' ')}"


@app.route('/python/', defaults={'text': 'is cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def display_python_text(text):
    """display “Python ”, followed by the value of the text variable
    (replace underscore _ symbols with a space"""
    return f"Python {text.replace('_', ' ')}"


@app.route('/number/<int:n>', strict_slashes=False)
def display_number_n(n):
    """display “n is a number” only if n is an integer"""
    return f"{n} is a number"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
