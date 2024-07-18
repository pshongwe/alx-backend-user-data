#!/usr/bin/env python3
"""
App file
"""
from flask import Flask, jsonify, request
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def get():
    """Get json payload"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def create_user() -> str:
    """
    Create a new user account.

    Returns:
        tuple: A JSON response and HTTP status code.
            On success: ({'email': str, 'message': str}, 201)
            On failure: ({'message': str}, 400)
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email,
                        "message": "User created successfully"}), 201
    except ValueError as e:
        return jsonify({"message": str(e)}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
