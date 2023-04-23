#!/usr/bin/python3
"""script to display HBNB"""
from flask import Flask
app = Flask(__name__)


@app.route("/", strict_slashes=False)
def index():
    "function to return hello HBNB"
    return 'Hello HBNB'


if "__name == __main__":
    app.run(host="0.0.0.0", port=5000)
