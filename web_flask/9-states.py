#!/usr/bin/python3
"""
Routes:
    /states: display a HTML page: (inside the tag BODY)
    H1 tag: “States”
    UL tag: with the list of all State objects present
    in DBStorage sorted by name (A->Z) tip
    LI tag: description of one State: <state.id>: <B><state.name></B>
    /states/<id>: display a HTML page: (inside the tag BODY)
    If a State object is found with this id:
    H1 tag: “State: ”
    H3 tag: “Cities:”
    UL tag: with the list of City objects linked to
    the State sorted by name (A->Z)
    LI tag: description of one City: <city.id>: <B><city.name></B>
    Otherwise:
    H1 tag: “Not found!”
You must use the option strict_slashes=False in your route definition

To get some data use: curl -o 7-dump.sql "https://s3.amazonaws.com/\
intranet-projects-files/holbertonschool-higher-level_programming+/290/7-states_list.sql"

Then: cat 7-dump.sql | sudo mysql -uroot -p

Run: cd ~/AirBnB_Clone_v2 && HBNB_MYSQL_USER=hbnb_dev \
HBNB_MYSQL_PWD=hbnb_dev_pwd HBNB_MYSQL_HOST=localhost \
HBNB_MYSQL_DB=hbnb_dev_db HBNB_TYPE_STORAGE=db python3 -m web_flask.9-states
"""

from models import storage
from models.state import State
from flask import Flask, render_template
app = Flask(__name__)


@app.route('/states')
@app.route('/states/<id>')
def states_list(id=None):
    """Render template with states
    """
    path = '9-states.html'
    states = storage.all(State)
    return render_template(path, states=states, id=id)


@app.teardown_appcontext
def app_teardown(arg=None):
    """Clean-up session
    """
    storage.close()


if __name__ == '__main__':
    app.url_map.strict_slashes = False
    app.run(host='0.0.0.0', port=5000, debug=True)
