"""
Rotas de Definições — Configuração da API Key Gemini e modelo.
Blueprint: /api/v1/settings
"""
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required
from app.services.ai_assistant import testar_conexao
from app.utils.auth_helpers import get_current_user

settings_bp = Blueprint('settings', __name__, url_prefix='/api/v1/settings')


@settings_bp.route('/ai', methods=['GET'])
@jwt_required()
def obter_config_ai():
    """Obter configuração atual da IA (sem expor a key completa)."""
    user = get_current_user()

    api_key = current_app.config.get('GEMINI_API_KEY', '')
    model = current_app.config.get('GEMINI_MODEL', 'gemini-3.1-flash-lite-preview')
    available = current_app.config.get('GEMINI_AVAILABLE_MODELS', [])

    # Mascarar a key (mostrar só últimos 6 caracteres)
    masked_key = ''
    if api_key:
        masked_key = '•' * max(0, len(api_key) - 6) + api_key[-6:]

    return jsonify({
        'status': 'success',
        'data': {
            'api_key_masked': masked_key,
            'api_key_set': bool(api_key),
            'model': model,
            'available_models': available
        }
    }), 200


@settings_bp.route('/ai', methods=['PUT'])
@jwt_required()
def atualizar_config_ai():
    """Atualizar configuração da IA (API key e/ou modelo). Persiste em runtime."""
    user = get_current_user()

    data = request.get_json()
    updated = []

    if 'api_key' in data and data['api_key']:
        current_app.config['GEMINI_API_KEY'] = data['api_key']
        updated.append('api_key')

    if 'model' in data and data['model']:
        current_app.config['GEMINI_MODEL'] = data['model']
        updated.append('model')

    if not updated:
        return jsonify({'status': 'error', 'error': {'code': 'VALIDATION_ERROR', 'message': 'Nenhum campo para atualizar'}}), 400

    return jsonify({
        'status': 'success',
        'message': f'Configuração atualizada: {", ".join(updated)}',
        'data': {
            'model': current_app.config.get('GEMINI_MODEL'),
            'api_key_set': bool(current_app.config.get('GEMINI_API_KEY'))
        }
    }), 200


@settings_bp.route('/ai', methods=['DELETE'])
@jwt_required()
def apagar_config_ai():
    """Apagar a API key guardada."""
    get_current_user()
    current_app.config['GEMINI_API_KEY'] = ''
    return jsonify({
        'status': 'success',
        'message': 'API Key removida com sucesso',
        'data': {'api_key_set': False}
    }), 200


@settings_bp.route('/ai/test', methods=['POST'])
@jwt_required()
def testar_ai():
    """Testar ligação à API Gemini."""
    user = get_current_user()

    data = request.get_json() or {}
    api_key = data.get('api_key') or current_app.config.get('GEMINI_API_KEY')
    model = data.get('model') or current_app.config.get('GEMINI_MODEL')

    success, message = testar_conexao(api_key, model)

    return jsonify({
        'status': 'success' if success else 'error',
        'data': {
            'connected': success,
            'message': message,
            'model': model
        }
    }), 200
