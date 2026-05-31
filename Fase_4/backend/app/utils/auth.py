"""Utilitários de autenticação JWT."""
import jwt
import bcrypt
from datetime import datetime, timedelta, timezone
from flask import current_app


def hash_password(password):
    """Gera hash bcrypt para password."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=12)).decode('utf-8')


def check_password(password, password_hash):
    """Verifica password contra hash."""
    return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))


def generate_token(user_id):
    """Gera JWT token para utilizador."""
    payload = {
        'user_id': user_id,
        'exp': datetime.now(timezone.utc) + timedelta(hours=current_app.config.get('JWT_EXPIRATION_HOURS', 24)),
        'iat': datetime.now(timezone.utc)
    }
    return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')


def decode_token(token):
    """Descodifica e valida JWT token."""
    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
