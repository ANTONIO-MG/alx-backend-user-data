#!/usr/bin/env python3
"""
a simple flask app
"""
from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def welcome():
    """
    a simple python route that returns a Json data
    """
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
