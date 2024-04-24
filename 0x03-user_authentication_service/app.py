#!/usr/bin/env python3
"""Implement flask app"""
from flask import Flask, jsonify, request, abort, redirect, url_for
from auth import Auth


AUTH = Auth()
app = Flask(__name__)


@app.route('/')
def index() -> str:
    """
    Route decorator for the index endpoint.
    No parameters.
    Returns a JSON response containing the form data as a string.
    """
    form = {"message": "Bienvenue"}
    return jsonify(form)


@app.route('/users', methods=['POST'])
def users() -> str:
    """
    Handle POST requests to create new users.

    Retrieves email and password from the request form and attempts to
    register a new user with the provided credentials.

    Returns:
        - If successful, it returns a JSON
        response with the new user's email and a success message.
        - If the email is already registered,
        it returns a JSON response with an
        error message and status code 400.
    """
    email = request.form['email']  # retrieve email from the request form
    password = request.form['password']

    try:
        new_user = AUTH.register_user(email, password)
        return jsonify({"email": f"{email}", "message": "user created"})

    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login() -> str:
    """
    Route for logging in, takes email and password from
    form data and validates the login.
    If valid, creates a session and returns a JSON response with
    the email and a success message,
    also setting a session ID cookie. If not
    valid, aborts with a 401 status code.
    Returns a JSON response.
    """
    email = request.form['email']
    password = request.form['password']

    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)

        response = jsonify({"email": f"{email}", "message": "logged in"})

        response.set_cookie('session_id', session_id)

        return response
    else:
        abort(401)


@app.route('/sessions', methods=['DELETE'])
def logout():
    """
    Function to handle the logout process.
    This function deletes the session and redirects
    to the index page if the user is logged in,
    otherwise, it aborts with a 403 error.
    """
    session_id = request.cookies.get('session_id')

    user = AUTH.get_user_from_session_id(session_id)

    if user is not None:
        AUTH.destroy_session(user.id)
        return redirect(url_for('index'))
    else:
        abort(403)


@app.route('/profile', methods=['GET'])
def profile():
    """
    Retrieves the user's profile based on the session ID
    in the request cookies.
    Returns the user's email in JSON format with a
    status code of 200 if the user is found,
    otherwise aborts the request with a status code of 403.
    """
    session_id = request.cookies.get('session_id')

    user = AUTH.get_user_from_session_id(session_id)

    if user is not None:
        return jsonify({"email": user.email}), 200
    else:
        abort(403)


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token():
    """
    Function to handle the POST request for resetting a password.
    Takes no parameters.
    Returns a JSON response with the email and reset token if successful,
    otherwise aborts with a 403 error.
    """
    email = request.form['email']

    try:
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": token}), 200
    except ValueError:
        abort(403)


@app.route("/reset_password", methods=['PUT'])
def update_password():
    """Update password end-point"""
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    try:
        AUTH.update_password(reset_token, new_password)
        response = {"email": email, "message": "Password updated"}
        return jsonify(response), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
