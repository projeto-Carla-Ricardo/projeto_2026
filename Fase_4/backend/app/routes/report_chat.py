"""Rotas do Chat do Relatório — Interação com IA sobre resultados."""
from flask import Blueprint, request, jsonify
from app.models.avaliacao import Avaliacao
from app.models.conversa import ConversaIA
from app.services.ia_assistant import get_report_chat_response
from app.services.immediate_suggestions import generate_immediate_suggestions
from app.utils.decorators import login_required

report_chat_bp = Blueprint('report_chat', __name__)


@report_chat_bp.route('/avaliacoes/<int:aval_id>/report-chat', methods=['POST'])
@login_required
def enviar_mensagem_relatorio(aval_id):
    """Enviar mensagem ao chat do relatório."""
    aval = Avaliacao.query.filter_by(id=aval_id, user_id=request.current_user.id).first()
    if not aval:
        return jsonify({'error': 'Avaliação não encontrada'}), 404
    if aval.status not in ('completa', 'concluida'):
        return jsonify({'error': 'Avaliação ainda não foi finalizada'}), 400
    
    data = request.get_json()
    mensagem = data.get('mensagem')
    if not mensagem:
        return jsonify({'error': 'Mensagem é obrigatória'}), 400
    
    try:
        resposta = get_report_chat_response(mensagem, aval_id, user=request.current_user)
        return jsonify({'resposta': resposta}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Erro no chat: {str(e)[:200]}'}), 500


@report_chat_bp.route('/avaliacoes/<int:aval_id>/report-chat/historico', methods=['GET'])
@login_required
def historico_relatorio(aval_id):
    """Retorna histórico do chat do relatório."""
    aval = Avaliacao.query.filter_by(id=aval_id, user_id=request.current_user.id).first()
    if not aval:
        return jsonify({'error': 'Avaliação não encontrada'}), 404
    
    # Report chat messages have camada_id = None (to distinguish from questionnaire chat)
    msgs = ConversaIA.query.filter_by(
        avaliacao_id=aval_id
    ).filter(
        ConversaIA.camada_id.is_(None)
    ).order_by(ConversaIA.created_at).all()
    
    return jsonify({'mensagens': [m.to_dict() for m in msgs]}), 200


@report_chat_bp.route('/avaliacoes/<int:aval_id>/suggestions', methods=['GET'])
@login_required
def get_suggestions(aval_id):
    """Retorna sugestões imediatas, pontos críticos e nível de maturidade."""
    aval = Avaliacao.query.filter_by(id=aval_id, user_id=request.current_user.id).first()
    if not aval:
        return jsonify({'error': 'Avaliação não encontrada'}), 404
    if aval.status not in ('completa', 'concluida'):
        return jsonify({'error': 'Avaliação ainda não foi finalizada'}), 400
    
    try:
        result = generate_immediate_suggestions(aval_id, user=request.current_user)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Erro ao gerar sugestões: {str(e)[:200]}'}), 500
