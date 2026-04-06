"""
Rotas de Autenticação — Registo, Login, Refresh Token.
Blueprint: /api/v1/auth
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity
)
import bcrypt
from app import db, limiter
from app.models.utilizador import Utilizador

auth_bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')


@auth_bp.route('/register', methods=['POST'])
@limiter.limit("10/hour")
def register():
    """Registo de novo utilizador."""
    data = request.get_json()

    if not data:
        return jsonify({'status': 'error', 'error': {'code': 'BAD_REQUEST', 'message': 'Dados em falta'}}), 400

    nome = data.get('nome', '').strip()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')

    # Validações
    errors = []
    if not nome or len(nome) < 2:
        errors.append('Nome deve ter pelo menos 2 caracteres')
    if not email or '@' not in email:
        errors.append('Email inválido')
    if not password or len(password) < 8:
        errors.append('Password deve ter pelo menos 8 caracteres')

    if errors:
        return jsonify({'status': 'error', 'error': {'code': 'VALIDATION_ERROR', 'message': errors[0], 'details': errors}}), 400

    # Verificar se email já existe
    if Utilizador.query.filter_by(email=email).first():
        return jsonify({'status': 'error', 'error': {'code': 'CONFLICT', 'message': 'Email já registado'}}), 409

    # Criar utilizador
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    user = Utilizador(nome=nome, email=email, password_hash=password_hash)
    db.session.add(user)
    db.session.commit()

    return jsonify({
        'status': 'success',
        'data': user.to_dict(),
        'message': 'Conta criada com sucesso'
    }), 201


@auth_bp.route('/login', methods=['POST'])
@limiter.limit("20/hour")
def login():
    """Login com emissão de JWT token."""
    data = request.get_json()

    if not data:
        return jsonify({'status': 'error', 'error': {'code': 'BAD_REQUEST', 'message': 'Dados em falta'}}), 400

    email = data.get('email', '').strip().lower()
    password = data.get('password', '')

    if not email or not password:
        return jsonify({'status': 'error', 'error': {'code': 'VALIDATION_ERROR', 'message': 'Email e password obrigatórios'}}), 400

    user = Utilizador.query.filter_by(email=email, ativo=True).first()

    if not user or not bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
        return jsonify({'status': 'error', 'error': {'code': 'UNAUTHORIZED', 'message': 'Credenciais inválidas'}}), 401

    # Gerar tokens
    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))

    return jsonify({
        'status': 'success',
        'data': {
            'token': access_token,
            'refresh_token': refresh_token,
            'user': user.to_dict()
        }
    }), 200


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Renovação de access token."""
    user_id = get_jwt_identity()
    access_token = create_access_token(identity=str(user_id))
    return jsonify({
        'status': 'success',
        'data': {'token': access_token}
    }), 200


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    """Perfil do utilizador atual."""
    user_id = get_jwt_identity()
    user = Utilizador.query.get(user_id)
    if not user:
        return jsonify({'status': 'error', 'error': {'code': 'NOT_FOUND', 'message': 'Utilizador não encontrado'}}), 404

    return jsonify({'status': 'success', 'data': user.to_dict()}), 200
