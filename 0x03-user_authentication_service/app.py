#!/usr/bin/env python3
"""
Basic flask app setup
"""
from flask import Flask, jsonify, request
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route('/')
def index() -> str:
    """
    return a simple message
    """
    form = {"message": "Bienvenue"}
    return jsonify(form)


@app.route('/users', methods=["POST"])
def create_new_user():
    """
    If the user does not exist, the end-point should
    register it and respond with the following JSON payload
    """
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        new_user = AUTH.register_user(email, password)
        return jsonify({"email": new_user.email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
