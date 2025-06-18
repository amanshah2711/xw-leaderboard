
from cryptography.fernet import Fernet
import os
from itsdangerous import SignatureExpired, BadSignature, URLSafeTimedSerializer 

timed_serializer = URLSafeTimedSerializer(os.getenv('FLASK_SECRET_KEY', 'default-secret-key'))

fernet = Fernet(os.getenv('NYT_COOKIE_ENCRYPTION_KEY', "sdfsdfdsfsdfs"))

def encrypt_cookie(cookie):
    return fernet.encrypt(cookie.encode()).decode()

def decrypt_cookie(encrypted_cookie):
    return fernet.decrypt(encrypted_cookie.encode()).decode()


def generate_token(email, salt):
    return timed_serializer.dumps(email, salt)

def verify_token(token, salt, expiration = 3600):
    try:
        data = timed_serializer.loads(token, salt=salt, max_age=expiration)
        return data 
    except SignatureExpired:
        return None  # Token expired
    except BadSignature:
        return None  # Token tampered

