#!/usr/bin/env python3
"""
Auth file
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """Create password Hash"""
    return bcrypt.hashpw(password.encode('utf-8'),
                         bcrypt.gensalt())
