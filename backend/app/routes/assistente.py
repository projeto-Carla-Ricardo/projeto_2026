"""
Rotas do Assistente IA — Chat com Gemini.
Blueprint: /api/v1/assistente
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models.avaliacao import Avaliacao
from app.models.empresa import Empresa
from app.services.ai_assistant import enviar_mensagem, get_historico
from app.utils.auth_helpers import get_current_user
from app import limiter

assistente_bp = Blueprint('assistente', __name__, url_prefix='/api/v1/assistente')


@assistente_bp.route('/mensagem', methods=['POST'])
@jwt_required()
@limiter.limit("60/hour")
def enviar():
    """Enviar mensagem ao assistente IA."""
    data = request.get_json()
    user = get_current_user()

    avaliacao_id = data.get('avaliacao_id')
    mensagem = data.get('mensagem', '').strip()
    pergunta_atual_id = data.get('pergunta_atual_id')

    if not avaliacao_id or not mensagem:
        return jsonify({'status': 'error', 'error': {'code': 'VALIDATION_ERROR', 'message': 'avaliacao_id e mensagem obrigatórios'}}), 400

    # Verificar permissão
    avaliacao = Avaliacao.query.get(avaliacao_id)
    if not avaliacao:
        return jsonify({'status': 'error', 'error': {'code': 'NOT_FOUND', 'message': 'Avaliação não encontrada'}}), 404

    empresa = Empresa.query.get(avaliacao.empresa_id)
    if empresa.utilizador_id != user.id and user.role != 'admin':
        return jsonify({'status': 'error', 'error': {'code': 'FORBIDDEN', 'message': 'Sem permissão'}}), 403

    resultado = enviar_mensagem(avaliacao_id, mensagem, pergunta_atual_id)

    return jsonify({'status': 'success', 'data': resultado}), 200


@assistente_bp.route('/historico/<int:avaliacao_id>', methods=['GET'])
@jwt_required()
def historico(avaliacao_id):
    """Histórico de conversa com o assistente."""
    user = get_current_user()
    avaliacao = Avaliacao.query.get_or_404(avaliacao_id)
    empresa = Empresa.query.get(avaliacao.empresa_id)

    if empresa.utilizador_id != user.id and user.role != 'admin':
        return jsonify({'status': 'error', 'error': {'code': 'FORBIDDEN', 'message': 'Sem permissão'}}), 403

    mensagens = get_historico(avaliacao_id)
    return jsonify({'status': 'success', 'data': mensagens}), 200
