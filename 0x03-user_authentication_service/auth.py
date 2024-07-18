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

    def get_user_from_session_id(self, session_id: str) -> User:
        """ get user from session_id"""
        if session_id is None:
            return None
        user = None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """Destroy user session"""
        if user_id is None:
            return None
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """Generate password reset token for user"""
        user = None
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            pass
        if user is None:
            raise ValueError()
        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """Update user password using reset token"""
        user = None
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            pass
        if user is None:
            raise ValueError()
        new_password_hash = _hash_password(password)
        self._db.update_user(
            user.id,
            hashed_password=new_password_hash,
            reset_token=None,
        )
