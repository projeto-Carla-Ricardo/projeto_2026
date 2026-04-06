"""
Rotas do Scoring — Resultados de diagnóstico.
Blueprint: /api/v1/scoring
"""
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from app.models.avaliacao import Avaliacao
from app.models.empresa import Empresa
from app.services.scoring_engine import calcular_scoring_completo, NIVEL_NOMES
from app.utils.auth_helpers import get_current_user

scoring_bp = Blueprint('scoring', __name__, url_prefix='/api/v1/scoring')


@scoring_bp.route('/<int:avaliacao_id>', methods=['GET'])
@jwt_required()
def obter_scoring(avaliacao_id):
    """Obter resultados de scoring de uma avaliação concluída."""
    user = get_current_user()
    avaliacao = Avaliacao.query.get_or_404(avaliacao_id)
    empresa = Empresa.query.get(avaliacao.empresa_id)

    if empresa.utilizador_id != user.id and user.role != 'admin':
        return jsonify({'status': 'error', 'error': {'code': 'FORBIDDEN', 'message': 'Sem permissão'}}), 403

    if avaliacao.estado != 'concluida':
        return jsonify({'status': 'error', 'error': {'code': 'BAD_REQUEST', 'message': 'Avaliação ainda não concluída'}}), 400

    # Recalcular ou usar cache
    resultados = calcular_scoring_completo(avaliacao_id)

    return jsonify({'status': 'success', 'data': resultados}), 200
