#!/usr/bin/env python3
"""
Auth file
"""
import bcrypt
from db import DB, User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """Create password Hash"""
    return bcrypt.hashpw(password.encode('utf-8'),
                         bcrypt.gensalt())


def _generate_uuid() -> str:
    """Generate a uuid"""
    return str(uuid4())


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
            hp = user.hashed_password.encode("utf-8")
            if user and bcrypt.checkpw(password.encode("utf-8"),
                                       hp):
                return True
        except NoResultFound:
            return False
        return False

    def create_session(self, email: str) -> str:
        """Create a session"""
        try:
            cur_user = self._db.find_user_by(email=email)

            if not cur_user:
                return None
            session_id = _generate_uuid()
            self._db.update_user(cur_user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(session_id: str) -> User:
        """ get user from session_id"""
        if not session_id:
            return None
        user = None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user
