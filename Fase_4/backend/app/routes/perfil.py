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
    completas = Avaliacao.query.filter(
        Avaliacao.user_id == user.id,
        Avaliacao.status.in_(['completa', 'concluida'])
    ).count()

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


MODELOS_PERMITIDOS = [
    'gemini-3.5-flash',
    'gemini-3.1-flash-lite',
    'gemini-3-flash-preview',
]


@perfil_bp.route('/configuracoes', methods=['GET'])
@login_required
def ver_configuracoes():
    """Retorna configurações do utilizador (API key mascarada)."""
    user = request.current_user
    api_key = user.gemini_api_key or ''
    # Mascarar a chave: mostrar apenas os últimos 4 caracteres
    masked = ''
    if api_key:
        masked = '•' * max(0, len(api_key) - 4) + api_key[-4:] if len(api_key) > 4 else '•' * len(api_key)

    return jsonify({
        'gemini_api_key': api_key,
        'gemini_api_key_masked': masked,
        'has_gemini_key': bool(api_key),
        'gemini_model': user.gemini_model or 'gemini-3.5-flash',
        'modelos_disponiveis': MODELOS_PERMITIDOS
    }), 200


@perfil_bp.route('/configuracoes', methods=['PUT'])
@login_required
def guardar_configuracoes():
    """Guardar configurações do utilizador (API key e modelo)."""
    data = request.get_json()
    user = request.current_user

    if 'gemini_api_key' in data:
        user.gemini_api_key = data['gemini_api_key'].strip() if data['gemini_api_key'] else None

    if 'gemini_model' in data:
        model = data['gemini_model']
        if model in MODELOS_PERMITIDOS:
            user.gemini_model = model
        else:
            return jsonify({'error': f'Modelo inválido. Modelos permitidos: {", ".join(MODELOS_PERMITIDOS)}'}), 400

    db.session.commit()
    return jsonify({'message': 'Configurações guardadas com sucesso'}), 200

