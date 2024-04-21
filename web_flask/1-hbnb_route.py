#!/usr/bin/python3
"""Start Flask webapplication"""


from flask import Flask as F


app = F(__name__)


@app.route("/", strict_slashes=False)
def hello():
    """print the massage"""

    return f"Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """print HBNB"""

    return f"HBNB"


if (__name__) == "__main__":
    app.run(host="0.0.0.0", port="5000")
