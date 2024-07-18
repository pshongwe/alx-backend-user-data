#!/usr/bin/env python3
"""E2E Test file main.py"""
import requests


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
URL = "http://0.0.0.0:5000"


def register_user(email: str, password: str) -> None:
    """Test registering a user"""
    u = "{}/users".format(BASE_URL)
    body = {
        'email': email,
        'password': password,
    }
    res = requests.post(u, data=body)
    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "user created"}
    res = requests.post(url, data=body)
    assert res.status_code == 400
    assert res.json() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    """Test logging in with wrong password."""
    u = "{}/sessions".format(BASE_URL)
    body = {
        'email': email,
        'password': password,
    }
    res = requests.post(u, data=body)
    assert res.status_code == 401


def log_in(email: str, password: str) -> str:
    """Test logging in"""
    u = "{}/sessions".format(BASE_URL)
    body = {
        'email': email,
        'password': password,
    }
    res = requests.post(u, data=body)
    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "logged in"}
    return res.cookies.get('session_id')


def profile_unlogged() -> None:
    """Test retrieving profile
    information whilst logged out"""
    u = "{}/profile".format(BASE_URL)
    res = requests.get(u)
    assert res.status_code == 403


def profile_logged(session_id: str) -> None:
    """Test retrieving profile
    information whilst logged on"""
    u = "{}/profile".format(BASE_URL)
    req_cookies = {
        'session_id': session_id,
    }
    res = requests.get(u, cookies=req_cookies)
    assert res.status_code == 200
    assert "email" in res.json()


def log_out(session_id: str) -> None:
    """Test logging out of a session"""
    u = "{}/sessions".format(BASE_URL)
    req_cookies = {
        'session_id': session_id,
    }
    res = requests.delete(u, cookies=req_cookies)
    assert res.status_code == 200
    assert res.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    """Test password reset request"""
    u = "{}/reset_password".format(BASE_URL)
    body = {'email': email}
    res = requests.post(u, data=body)
    assert res.status_code == 200
    assert "email" in res.json()
    assert res.json()["email"] == email
    assert "reset_token" in res.json()
    return res.json().get('reset_token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Test user password update"""
    u = "{}/reset_password".format(BASE_URL)
    body = {
        'email': email,
        'reset_token': reset_token,
        'new_password': new_password,
    }
    res = requests.put(u, data=body)
    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "Password updated"}


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
