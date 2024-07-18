#!/usr/bin/env python3
"""
Auth file
"""
import bcrypt
from db import DB, User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """Create password Hash"""
    return bcrypt.hashpw(password.encode('utf-8'),
                         bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a user"""
        try:
            cur_user = self._db.find_user_by(email=email)

            if cur_user:
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            pass

        hp = _hash_password(password)
        newUser = self._db.add_user(
               email=email, hashed_password=hp.decode('utf-8'))
        return newUser

    def valid_login(self, email: str, password: str) -> bool:
        """Checks if a user's login details are valid.
        """
        try:
            user = self._db.find_user_by(email=email)
            if user and bcrypt.checkpw(password.encode("utf-8"),
                                       user.hashed_password):
                return True
        except NoResultFound:
            pass
        return False
