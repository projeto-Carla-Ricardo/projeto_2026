"""Rotas de Perfil de Utilizador."""
from flask import Blueprint, request, jsonify
from app import db
from app.models.utilizador import Utilizador
from app.utils.auth import hash_password, check_password
from app.utils.decorators import login_required

perfil_bp = Blueprint('perfil', __name__)


@perfil_bp.route('', methods=['GET'])
@login_required
def ver_perfil():
    """Retorna dados do perfil do utilizador."""
    user = request.current_user
    from app.models.avaliacao import Avaliacao
    total_aval = Avaliacao.query.filter_by(user_id=user.id).count()
    completas = Avaliacao.query.filter_by(user_id=user.id, status='completa').count()

    result = user.to_dict()
    result['total_avaliacoes'] = total_aval
    result['avaliacoes_completas'] = completas
    return jsonify(result), 200


@perfil_bp.route('', methods=['PUT'])
@login_required
def editar_perfil():
    """Editar nome do utilizador."""
    data = request.get_json()
    user = request.current_user

    if 'nome' in data:
        user.nome = data['nome']

    db.session.commit()
    return jsonify(user.to_dict()), 200


@perfil_bp.route('/password', methods=['PUT'])
@login_required
def alterar_password():
    """Alterar password do utilizador."""
    data = request.get_json()
    user = request.current_user

    if 'password_atual' not in data or 'nova_password' not in data:
        return jsonify({'error': 'Campos password_atual e nova_password são obrigatórios'}), 400

    if not check_password(data['password_atual'], user.password_hash):
        return jsonify({'error': 'Password atual incorreta'}), 401

    from app.utils.validators import validate_password
    ok, msg = validate_password(data['nova_password'])
    if not ok:
        return jsonify({'error': msg}), 400

    user.password_hash = hash_password(data['nova_password'])
    db.session.commit()
    return jsonify({'message': 'Password alterada com sucesso'}), 200
