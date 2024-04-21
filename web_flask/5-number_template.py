#!/usr/bin/python3
"""Start Flask webapplication"""


from flask import Flask as F
from flask import render_template as rt

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


@app.route("/python/<text>", strict_slashes=False)
@app.route("/python/", strict_slashes=False)
def pythontext(text="is cool"):
    """The default value of text is “is cool"""
    return f"Python {text.replace('_', ' ')}"


@app.route("/number/<int:n>", strict_slashes=False)
def number(n):
    """ display “n is a number” only if n is an integer"""
    return f"{n} is a number"


@app.route("/number_template/<int:n>", strict_slashes=False)
def number_templete(n):
    """ display a HTML page only if n is an integer"""
    return rt("5-number.html", n=n)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
