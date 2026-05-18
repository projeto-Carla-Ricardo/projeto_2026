"""Rotas de organizações."""
from flask import Blueprint, request, jsonify
from app import db
from app.models.organizacao import Organizacao
from app.utils.decorators import login_required
from app.utils.validators import validate_required_fields

org_bp = Blueprint('organizacoes', __name__)

@org_bp.route('', methods=['GET'])
@login_required
def listar():
    orgs = Organizacao.query.filter_by(user_id=request.current_user.id).all()
    return jsonify({'data': [o.to_dict() for o in orgs], 'total': len(orgs)}), 200

@org_bp.route('', methods=['POST'])
@login_required
def criar():
    data = request.get_json()
    ok, msg = validate_required_fields(data, ['nome', 'setor', 'dimensao', 'tipo'])
    if not ok:
        return jsonify({'error': msg}), 400

    org = Organizacao(
        user_id=request.current_user.id, nome=data['nome'], setor=data['setor'],
        dimensao=data['dimensao'], tipo=data['tipo'],
        pais=data.get('pais', 'Portugal'), descricao=data.get('descricao')
    )
    db.session.add(org)
    db.session.commit()
    return jsonify(org.to_dict()), 201

@org_bp.route('/<int:id>', methods=['GET'])
@login_required
def detalhar(id):
    org = Organizacao.query.filter_by(id=id, user_id=request.current_user.id).first()
    if not org:
        return jsonify({'error': 'Organização não encontrada'}), 404
    return jsonify(org.to_dict()), 200

@org_bp.route('/<int:id>', methods=['PUT'])
@login_required
def atualizar(id):
    org = Organizacao.query.filter_by(id=id, user_id=request.current_user.id).first()
    if not org:
        return jsonify({'error': 'Organização não encontrada'}), 404

    data = request.get_json()
    for field in ['nome', 'setor', 'dimensao', 'tipo', 'pais', 'descricao']:
        if field in data:
            setattr(org, field, data[field])
    db.session.commit()
    return jsonify(org.to_dict()), 200

@org_bp.route('/<int:id>', methods=['DELETE'])
@login_required
def eliminar(id):
    org = Organizacao.query.filter_by(id=id, user_id=request.current_user.id).first()
    if not org:
        return jsonify({'error': 'Organização não encontrada'}), 404
    db.session.delete(org)
    db.session.commit()
    return jsonify({'message': 'Organização eliminada'}), 200


@org_bp.route('/<int:id>/comparacao', methods=['GET'])
@login_required
def comparacao_temporal(id):
    """Compara múltiplas avaliações da mesma organização ao longo do tempo."""
    org = Organizacao.query.filter_by(id=id, user_id=request.current_user.id).first()
    if not org:
        return jsonify({'error': 'Organização não encontrada'}), 404

    from app.models.avaliacao import Avaliacao
    from app.models.resultado import ResultadoCamada
    avaliacoes = Avaliacao.query.filter_by(
        organizacao_id=id, user_id=request.current_user.id, status='completa'
    ).order_by(Avaliacao.data_fim.asc()).all()

    if len(avaliacoes) < 1:
        return jsonify({'error': 'Nenhuma avaliação completa encontrada'}), 404

    comparacao = []
    for aval in avaliacoes:
        resultados = ResultadoCamada.query.filter_by(avaliacao_id=aval.id).all()
        camadas = {}
        for r in resultados:
            nome = r.camada.nome if r.camada else f'Camada {r.camada_id}'
            camadas[nome] = {'score': round(r.score, 2), 'nivel': r.nivel}

        comparacao.append({
            'avaliacao_id': aval.id,
            'data': aval.data_fim.isoformat() if aval.data_fim else aval.data_inicio.isoformat(),
            'score_global': aval.score_global,
            'nivel_global': aval.nivel_global,
            'camadas': camadas
        })

    return jsonify({
        'organizacao': org.to_dict(),
        'total_avaliacoes': len(comparacao),
        'avaliacoes': comparacao
    }), 200

