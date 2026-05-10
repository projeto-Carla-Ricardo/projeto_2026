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
