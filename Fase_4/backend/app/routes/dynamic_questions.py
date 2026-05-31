"""Rotas do Questionário Dinâmico — Perguntas personalizadas via IA."""
from flask import Blueprint, request, jsonify
from app.models.avaliacao import Avaliacao
from app.services.dynamic_questionnaire import generate_dynamic_layer, generate_ai_commentary
from app.utils.decorators import login_required

dynamic_bp = Blueprint('dynamic_questions', __name__)


@dynamic_bp.route('/<int:aval_id>/dynamic-layer/<int:camada_id>', methods=['GET'])
@login_required
def get_dynamic_layer(aval_id, camada_id):
    """Retorna perguntas personalizadas pela IA para uma camada específica."""
    aval = Avaliacao.query.filter_by(id=aval_id, user_id=request.current_user.id).first()
    if not aval:
        return jsonify({'error': 'Avaliação não encontrada'}), 404
    
    try:
        result = generate_dynamic_layer(aval_id, camada_id, user=request.current_user)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Erro ao gerar perguntas dinâmicas: {str(e)[:200]}'}), 500


@dynamic_bp.route('/<int:aval_id>/ai-commentary', methods=['POST'])
@login_required
def get_ai_commentary(aval_id):
    """Retorna comentário da IA sobre as respostas dadas até ao momento."""
    aval = Avaliacao.query.filter_by(id=aval_id, user_id=request.current_user.id).first()
    if not aval:
        return jsonify({'error': 'Avaliação não encontrada'}), 404
    
    data = request.get_json() or {}
    current_camada_idx = data.get('current_camada_idx', 0)
    
    try:
        result = generate_ai_commentary(aval_id, current_camada_idx, user=request.current_user)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Erro ao gerar comentário: {str(e)[:200]}'}), 500
