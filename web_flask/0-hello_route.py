#!/usr/bin/python3
"""
script that starts a Flask web application
Your web application must be listening on 0.0.0.0, port 5000
Routes:/: display “Hello HBNB!”
You must use the option strict_slashes=False in your route definition
Example usage: AirBnB_clone_v2$ python3 -m web_flask.0-hello_route
"""

from flask import Flask
app = Flask(__name__)


@app.route('/', strict_slashes=False)
@app.route('/airbnb-onepage/', strict_slashes=False)
def hello_hbnb():
    """ display message"""
    return "Hello HBNB!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
