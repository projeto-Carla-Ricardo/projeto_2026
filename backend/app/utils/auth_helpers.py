"""
Utilitários de autenticação — decorators e helpers JWT.
"""
from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from app.models.utilizador import Utilizador


def get_current_user():
    """Retorna o utilizador atual a partir do JWT."""
    user_id = get_jwt_identity()
    return Utilizador.query.get(int(user_id))


def admin_required(fn):
    """Decorator que requer role 'admin'."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user = get_current_user()
        if not user or user.role != 'admin':
            return jsonify({
                'status': 'error',
                'error': {'code': 'FORBIDDEN', 'message': 'Acesso restrito a administradores'}
            }), 403
        return fn(*args, **kwargs)
    return wrapper


def owner_or_admin(model_class, id_param='id', user_field='utilizador_id'):
    """
    Decorator factory que verifica se o utilizador é proprietário do recurso ou admin.
    Usa-se: @owner_or_admin(Empresa)
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            user = get_current_user()
            if not user:
                return jsonify({
                    'status': 'error',
                    'error': {'code': 'UNAUTHORIZED', 'message': 'Utilizador não encontrado'}
                }), 401

            if user.role == 'admin':
                return fn(*args, **kwargs)

            resource_id = kwargs.get(id_param)
            if resource_id:
                resource = model_class.query.get(resource_id)
                if not resource:
                    return jsonify({
                        'status': 'error',
                        'error': {'code': 'NOT_FOUND', 'message': 'Recurso não encontrado'}
                    }), 404
                if getattr(resource, user_field) != user.id:
                    return jsonify({
                        'status': 'error',
                        'error': {'code': 'FORBIDDEN', 'message': 'Sem permissão para este recurso'}
                    }), 403

            return fn(*args, **kwargs)
        return wrapper
    return decorator
