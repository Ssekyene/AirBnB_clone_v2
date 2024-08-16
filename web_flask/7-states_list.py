#!/usr/bin/python3
"""
Script that starts a Flask web application
Web application must be listening on 0.0.0.0, port 5000
After each request you must remove the current SQLAlchemy Session:
Declare a method to handle @app.teardown_appcontext
Call in this method storage.close()
Routes:
        /states_list: display a HTML page: (inside the tag BODY)
            H1 tag: “States”
            UL tag: with the list of all State objects present
            in DBStorage sorted by name (A->Z) tip
            LI tag: description of one State: <state.id>: <B><state.name></B>
Must use the option strict_slashes=False in your route definition

To get some data use: curl -o 7-dump.sql "https://s3.amazonaws.com/\
intranet-projects-files/holbertonschool-higher-level_programming+/290/7-states_list.sql"

Then: cat 7-dump.sql | sudo mysql -uroot -p

Run: cd ~/AirBnB_Clone_v2 && HBNB_MYSQL_USER=hbnb_dev \
HBNB_MYSQL_PWD=hbnb_dev_pwd HBNB_MYSQL_HOST=localhost \
HBNB_MYSQL_DB=hbnb_dev_db HBNB_TYPE_STORAGE=db \
python3 -m web_flask.7-states_list
"""
from models import storage
from models import State
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/states_list')
def fecth_states():
    """
    display html page
    fecth sorted states to insert into html UL tag
    """
    states = storage.all(State)
    sorted_states = sorted(states.values(), key=lambda state: state.name)
    return render_template("7-states_list.html",
                           sorted_states=sorted_states)


@app.teardown_appcontext
def tear_down(arg=None):
    """
    remove the current SQLAlchemy Session
    """
    storage.close()


if __name__ == "__main__":
    app.url_map.strict_slashes = False
    app.run(host="0.0.0.0", port=5000, debug=True)
