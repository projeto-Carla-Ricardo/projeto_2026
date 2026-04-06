"""
Rotas de Avaliações — CRUD + Conclusão de diagnóstico.
Blueprint: /api/v1/avaliacoes
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.avaliacao import Avaliacao
from app.models.empresa import Empresa
from app.services.scoring_engine import calcular_scoring_completo
from app.utils.auth_helpers import get_current_user

avaliacoes_bp = Blueprint('avaliacoes', __name__, url_prefix='/api/v1/avaliacoes')


@avaliacoes_bp.route('', methods=['POST'])
@jwt_required()
def criar_avaliacao():
    """Iniciar nova avaliação/diagnóstico para uma empresa."""
    data = request.get_json()
    user = get_current_user()
    empresa_id = data.get('empresa_id')

    if not empresa_id:
        return jsonify({'status': 'error', 'error': {'code': 'VALIDATION_ERROR', 'message': 'empresa_id obrigatório'}}), 400

    empresa = Empresa.query.get(empresa_id)
    if not empresa or (empresa.utilizador_id != user.id and user.role != 'admin'):
        return jsonify({'status': 'error', 'error': {'code': 'FORBIDDEN', 'message': 'Empresa não encontrada ou sem permissão'}}), 403

    avaliacao = Avaliacao(empresa_id=empresa_id)
    db.session.add(avaliacao)
    db.session.commit()

    return jsonify({'status': 'success', 'data': avaliacao.to_dict(), 'message': 'Diagnóstico iniciado'}), 201


@avaliacoes_bp.route('', methods=['GET'])
@jwt_required()
def listar_avaliacoes():
    """Listar avaliações (filtrável por empresa_id e estado)."""
    user = get_current_user()
    empresa_id = request.args.get('empresa_id', type=int)
    estado = request.args.get('estado')

    query = Avaliacao.query

    if empresa_id:
        empresa = Empresa.query.get(empresa_id)
        if not empresa or (empresa.utilizador_id != user.id and user.role != 'admin'):
            return jsonify({'status': 'error', 'error': {'code': 'FORBIDDEN', 'message': 'Sem permissão'}}), 403
        query = query.filter_by(empresa_id=empresa_id)
    elif user.role != 'admin':
        empresa_ids = [e.id for e in Empresa.query.filter_by(utilizador_id=user.id).all()]
        query = query.filter(Avaliacao.empresa_id.in_(empresa_ids))

    if estado:
        query = query.filter_by(estado=estado)

    avaliacoes = query.order_by(Avaliacao.criado_em.desc()).all()
    return jsonify({'status': 'success', 'data': [a.to_dict() for a in avaliacoes]}), 200


@avaliacoes_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def obter_avaliacao(id):
    """Detalhes de uma avaliação com resultados."""
    user = get_current_user()
    avaliacao = Avaliacao.query.get_or_404(id)
    empresa = Empresa.query.get(avaliacao.empresa_id)

    if empresa.utilizador_id != user.id and user.role != 'admin':
        return jsonify({'status': 'error', 'error': {'code': 'FORBIDDEN', 'message': 'Sem permissão'}}), 403

    result = avaliacao.to_dict()

    # Incluir resultados por dimensão se existirem
    if avaliacao.resultados.count() > 0:
        result['resultados_dimensao'] = [r.to_dict() for r in avaliacao.resultados.all()]

    return jsonify({'status': 'success', 'data': result}), 200


@avaliacoes_bp.route('/<int:id>/concluir', methods=['POST'])
@jwt_required()
def concluir_avaliacao(id):
    """Finalizar avaliação e calcular scoring."""
    user = get_current_user()
    avaliacao = Avaliacao.query.get_or_404(id)
    empresa = Empresa.query.get(avaliacao.empresa_id)

    if empresa.utilizador_id != user.id and user.role != 'admin':
        return jsonify({'status': 'error', 'error': {'code': 'FORBIDDEN', 'message': 'Sem permissão'}}), 403

    if avaliacao.estado != 'em_curso':
        return jsonify({'status': 'error', 'error': {'code': 'BAD_REQUEST', 'message': 'Avaliação não está em curso'}}), 400

    # Calcular scoring completo
    resultados = calcular_scoring_completo(id)

    return jsonify({
        'status': 'success',
        'data': resultados,
        'message': 'Diagnóstico concluído com sucesso'
    }), 200


@avaliacoes_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def cancelar_avaliacao(id):
    """Cancelar avaliação em curso."""
    user = get_current_user()
    avaliacao = Avaliacao.query.get_or_404(id)
    empresa = Empresa.query.get(avaliacao.empresa_id)

    if empresa.utilizador_id != user.id and user.role != 'admin':
        return jsonify({'status': 'error', 'error': {'code': 'FORBIDDEN', 'message': 'Sem permissão'}}), 403

    avaliacao.estado = 'cancelada'
    db.session.commit()

    return jsonify({'status': 'success', 'message': 'Avaliação cancelada'}), 200
