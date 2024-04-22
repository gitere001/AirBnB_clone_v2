#!/usr/bin/python3
"""Starts a Flask web application.

The application listens on 0.0.0.0, port 5000.
Routes:
    /states: HTML page with a list of all State objects.
    /states/<id>: HTML page displaying the given state with <id>.
"""
from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City

app = Flask(__name__)


@app.route('/states', strict_slashes=False)
def display_states():
    """Display a HTML page with a list of all State objects"""
    states = storage.all(State).values()
    sorted_states = sorted(states, key=lambda state: state.name)
    return render_template('7-states_list.html', states=sorted_states)


@app.route('/states/<id>', strict_slashes=False)
def display_state_cities(id):
    """Display a HTML page with the list of cities for a given State"""
    state = storage.get(State, id)
    if state:
        try:
            if storage.__class__.__name__ == 'DBStorage':
                cities = state.cities
            else:
                cities = state.cities()
            sorted_cities = sorted(cities, key=lambda city: city.name)
            return render_template('9-states.html', state=state, cities=sorted_cities)
        except Exception as e:
            return render_template('error.html', error_message=str(e))
    else:
        return render_template('9-states.html', not_found=True)


@app.teardown_appcontext
def teardown_db(exception):
    """Closes the current SQLAlchemy session"""
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
