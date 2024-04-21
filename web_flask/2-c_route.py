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


@app.route("/c/<text>", strict_slashes=False)
def text_c(text):
    """display “C ”  of the text(replace  _ symbols with a space"""
    return f"C {text.replace('_', ' ')}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
