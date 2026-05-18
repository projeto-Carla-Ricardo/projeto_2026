"""Rotas de autenticação."""
from flask import Blueprint, request, jsonify
from app import db
from app.models.utilizador import Utilizador
from app.utils.auth import hash_password, check_password, generate_token
from app.utils.decorators import login_required
from app.utils.validators import validate_email, validate_password, validate_required_fields

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    ok, msg = validate_required_fields(data, ['nome', 'email', 'password'])
    if not ok:
        return jsonify({'error': msg}), 400

    if not validate_email(data['email']):
        return jsonify({'error': 'Formato de email inválido'}), 400

    ok, msg = validate_password(data['password'])
    if not ok:
        return jsonify({'error': msg}), 400

    if Utilizador.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email já registado'}), 409

    user = Utilizador(nome=data['nome'], email=data['email'], password_hash=hash_password(data['password']))
    db.session.add(user)
    db.session.commit()

    token = generate_token(user.id)
    result = user.to_dict()
    result['token'] = token
    return jsonify(result), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    ok, msg = validate_required_fields(data, ['email', 'password'])
    if not ok:
        return jsonify({'error': msg}), 400

    user = Utilizador.query.filter_by(email=data['email']).first()
    if not user or not check_password(data['password'], user.password_hash):
        return jsonify({'error': 'Credenciais inválidas'}), 401

    token = generate_token(user.id)
    return jsonify({'token': token, 'user': user.to_dict()}), 200

@auth_bp.route('/me', methods=['GET'])
@login_required
def me():
    return jsonify(request.current_user.to_dict()), 200
