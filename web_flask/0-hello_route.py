#!/usr/bin/python3
"""Start Flask webapplication"""


from flask import Flask as F


app = F(__name__)


@app.route("/")
def hello():
    """print the massage"""

    return f"Hello HBNB!"


# if (__name__) == (__main__):
app.run(host="0.0.0.0", port="5000")
