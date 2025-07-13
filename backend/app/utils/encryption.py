
from cryptography.fernet import Fernet
import os
from itsdangerous import SignatureExpired, BadSignature, URLSafeTimedSerializer 

timed_serializer = URLSafeTimedSerializer(os.getenv('FLASK_SECRET_KEY', 'default-secret-key'))
 
password_reset_salt = os.getenv('PASSWORD_RESET_SALT', 'password-reset-salt')
email_verify_salt = os.getenv('EMAIL_VERIFY_SALT', 'email-verify-salt')

fernet = Fernet(os.getenv('NYT_COOKIE_ENCRYPTION_KEY', Fernet.generate_key()))

def encrypt_cookie(cookie):
    return fernet.encrypt(cookie.encode()).decode()

def decrypt_cookie(encrypted_cookie):
    return fernet.decrypt(encrypted_cookie.encode()).decode()

def generate_token(data, salt):
    return timed_serializer.dumps(data, salt)

def verify_token(token, salt, expiration = 3600):
    try:
        data = timed_serializer.loads(token, salt=salt, max_age=expiration)
        return data 
    except SignatureExpired:
        return None  # Token expired
    except BadSignature:
        return None  # Token tampered

