#!/usr/bin/python3
"""
a script that starts a Flask web application
/hbnb: display a HTML page like 8-index.html,
done during the 0x01. AirBnB clone - Web static project

Get data: curl -o 100-dump.sql \
"https://s3.amazonaws.com/intranet-projects-files/\
holbertonschool-higher-level_programming+/290/100-hbnb.sql"

Load the database:
cat 100-dump.sql | sudo mysql -uroot -p

Run: cd ~/AirBnB_clone_v2 && HBNB_MYSQL_USER=hbnb_dev \
HBNB_MYSQL_PWD=hbnb_dev_pwd HBNB_MYSQL_HOST=localhost \
HBNB_MYSQL_DB=hbnb_dev_db HBNB_TYPE_STORAGE=db \
python3 -m web_flask.10-hbnb
"""

from models import storage
from models.state import State
from models.amenity import Amenity
from models.place import Place
from models.user import User
from flask import Flask, render_template
app = Flask(__name__)


@app.route('/hbnb')
def html_all_filters():
    """display html page w/ working city/state filters & amenities/properties
       runs with web static css files
    """
    state_objs = [state for state in storage.all(State).values()]
    amenity_objs = [amenity for amenity in storage.all(Amenity).values()]
    place_objs = [place for place in storage.all(Place).values()]
    user_objs = [user for user in storage.all(User).values()]
    place_owner_objs = []
    for place in place_objs:
        for user in user_objs:
            if place.user_id == user.id:
                place_owner_objs.append(["{} {}".format(
                    user.first_name, user.last_name), place])
    place_owner_objs.sort(key=lambda p: p[1].name)
    return render_template('100-hbnb.html',
                           state_objs=state_objs,
                           amenity_objs=amenity_objs,
                           place_owner_objs=place_owner_objs)



if __name__ == '__main__':
    app.url_map.strict_slashes = False
    app.run(host='0.0.0.0', port=5000, debug=True)
