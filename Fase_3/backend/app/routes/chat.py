"""Rotas do Chat IA."""
from flask import Blueprint, request, jsonify
from app.models.avaliacao import Avaliacao
from app.models.conversa import ConversaIA
from app.services.ia_assistant import get_gemini_response
from app.utils.decorators import login_required

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/<int:aval_id>/chat', methods=['POST'])
@login_required
def enviar_mensagem(aval_id):
    aval = Avaliacao.query.filter_by(id=aval_id, user_id=request.current_user.id).first()
    if not aval:
        return jsonify({'error': 'Avaliação não encontrada'}), 404

    data = request.get_json()
    mensagem = data.get('mensagem')
    camada_id = data.get('camada_id')

    if not mensagem:
        return jsonify({'error': 'Mensagem é obrigatória'}), 400

    resposta = get_gemini_response(mensagem, aval_id, camada_id)
    return jsonify({'resposta': resposta, 'camada_contexto': camada_id}), 200

@chat_bp.route('/<int:aval_id>/chat/historico', methods=['GET'])
@login_required
def historico(aval_id):
    aval = Avaliacao.query.filter_by(id=aval_id, user_id=request.current_user.id).first()
    if not aval:
        return jsonify({'error': 'Avaliação não encontrada'}), 404

    msgs = ConversaIA.query.filter_by(avaliacao_id=aval_id).order_by(ConversaIA.created_at).all()
    return jsonify({'mensagens': [m.to_dict() for m in msgs]}), 200
