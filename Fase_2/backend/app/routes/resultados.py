"""Rotas de Resultados."""
from flask import Blueprint, jsonify
from app.models.avaliacao import Avaliacao
from app.models.resultado import ResultadoCamada, Interdependencia
from app.utils.decorators import login_required

result_bp = Blueprint('resultados', __name__)

@result_bp.route('/<int:aval_id>/resultados', methods=['GET'])
@login_required
def obter_resultados(aval_id):
    from flask import request
    aval = Avaliacao.query.filter_by(id=aval_id, user_id=request.current_user.id).first()
    if not aval:
        return jsonify({'error': 'Avaliação não encontrada'}), 404
    if aval.status != 'completa':
        return jsonify({'error': 'Avaliação ainda não foi finalizada'}), 400

    resultados = ResultadoCamada.query.filter_by(avaliacao_id=aval_id).all()
    interdeps = Interdependencia.query.filter_by(avaliacao_id=aval_id).all()

    return jsonify({
        'score_global': aval.score_global,
        'nivel_global': aval.nivel_global,
        'camadas': [r.to_dict() for r in sorted(resultados, key=lambda x: x.camada.ordem if x.camada else 0)],
        'interdependencias': [i.to_dict() for i in interdeps]
    }), 200
