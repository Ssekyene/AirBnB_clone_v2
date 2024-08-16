#!/usr/bin/python3
"""
a script that starts a Flask web application
/hbnb_filters displays a HTML page like 6-index.html, which was 
done during the project 0x01. AirBnB clone - Web static

Get data:
curl -o 10-dump.sql "https://s3.amazonaws.com/intranet-projects-files/\
holbertonschool-higher-level_programming+/290/10-hbnb_filters.sql"

Load the database:
cat 10-dump.sql | sudo mysql -uroot -p

Run: cd ~/AirBnB_clone_v2 && HBNB_MYSQL_USER=hbnb_dev \
HBNB_MYSQL_PWD=hbnb_dev_pwd HBNB_MYSQL_HOST=localhost \
HBNB_MYSQL_DB=hbnb_dev_db HBNB_TYPE_STORAGE=db \
python3 -m web_flask.10-hbnb_filters
"""

from models import storage
from models.state import State
from models.amenity import Amenity
from flask import Flask, render_template
app = Flask(__name__)


@app.route('/hbnb_filters')
def hbnb_filters():
    """Render template with states
    """
    state_objs = [state for state in storage.all(State).values()]
    amenity_objs = [amenity for amenity in storage.all(Amenity).values()]
    return render_template('10-hbnb_filters.html',
                           state_objs=state_objs, amenity_objs=amenity_objs)


@app.teardown_appcontext
def app_teardown(arg=None):
    """Clean-up session
    """
    storage.close()


if __name__ == '__main__':
    app.url_map.strict_slashes = False
    app.run(host='0.0.0.0', port=5000, debug=True)
