import bcrypt
import database
from flask import session


def get_hashed_password(plain_text_password):
    # Hash a password for the first time
    #   (Using bcrypt, the salt is saved into the hash itself)
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode("utf-8")


def check_password(plain_text_password, hashed_text_password):
    hashed_bytes_password = hashed_text_password.encode("utf-8")
    # Check hashed password. Using bcrypt, the salt is saved into the hash itself
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)


def authenticate(username, password):
    user = database.get_user_by_name(username)
    if user:
        valid_password = check_password(password, user['password'])
        if valid_password:
            session['username'] = username
            session['user_id'] = user['id']
            return True
        if not valid_password:
            return False
    if not user:
        return False
