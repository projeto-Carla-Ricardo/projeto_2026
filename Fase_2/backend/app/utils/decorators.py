"""Decoradores para proteção de rotas."""
from functools import wraps
from flask import request, jsonify
from app.utils.auth import decode_token
from app.models.utilizador import Utilizador


def login_required(f):
    """Decorator que exige autenticação JWT."""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')

        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]

        if not token:
            return jsonify({'error': 'Token de autenticação não fornecido'}), 401

        user_id = decode_token(token)
        if user_id is None:
            return jsonify({'error': 'Token inválido ou expirado'}), 401

        user = Utilizador.query.get(user_id)
        if not user or not user.ativo:
            return jsonify({'error': 'Utilizador não encontrado ou inativo'}), 401

        request.current_user = user
        return f(*args, **kwargs)

    return decorated


def admin_required(f):
    """Decorator que exige papel de administrador."""
    @wraps(f)
    @login_required
    def decorated(*args, **kwargs):
        if request.current_user.papel != 'admin':
            return jsonify({'error': 'Permissão insuficiente. Requer papel de administrador.'}), 403
        return f(*args, **kwargs)

    return decorated
