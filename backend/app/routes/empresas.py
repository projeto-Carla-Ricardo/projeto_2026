"""
Rotas de Empresas — CRUD completo.
Blueprint: /api/v1/empresas
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.empresa import Empresa
from app.utils.auth_helpers import get_current_user

empresas_bp = Blueprint('empresas', __name__, url_prefix='/api/v1/empresas')


@empresas_bp.route('', methods=['POST'])
@jwt_required()
def criar_empresa():
    """Criar nova empresa."""
    data = request.get_json()
    user_id = get_jwt_identity()

    if not data or not data.get('nome') or not data.get('setor'):
        return jsonify({'status': 'error', 'error': {'code': 'VALIDATION_ERROR', 'message': 'Nome e setor são obrigatórios'}}), 400

    empresa = Empresa(
        utilizador_id=user_id,
        nome=data['nome'].strip(),
        setor=data['setor'].strip(),
        num_colaboradores=data.get('num_colaboradores'),
        localizacao=data.get('localizacao', '').strip() if data.get('localizacao') else None,
        ano_fundacao=data.get('ano_fundacao'),
        descricao=data.get('descricao', '').strip() if data.get('descricao') else None,
    )
    db.session.add(empresa)
    db.session.commit()

    return jsonify({'status': 'success', 'data': empresa.to_dict(), 'message': 'Empresa criada'}), 201


@empresas_bp.route('', methods=['GET'])
@jwt_required()
def listar_empresas():
    """Listar empresas do utilizador (ou todas se admin)."""
    user = get_current_user()
    if user.role == 'admin':
        empresas = Empresa.query.filter_by(ativo=True).all()
    else:
        empresas = Empresa.query.filter_by(utilizador_id=user.id, ativo=True).all()

    return jsonify({'status': 'success', 'data': [e.to_dict() for e in empresas]}), 200


@empresas_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def obter_empresa(id):
    """Detalhes de uma empresa."""
    user = get_current_user()
    empresa = Empresa.query.get_or_404(id)

    if user.role != 'admin' and empresa.utilizador_id != user.id:
        return jsonify({'status': 'error', 'error': {'code': 'FORBIDDEN', 'message': 'Sem permissão'}}), 403

    return jsonify({'status': 'success', 'data': empresa.to_dict()}), 200


@empresas_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def atualizar_empresa(id):
    """Atualizar empresa."""
    user = get_current_user()
    empresa = Empresa.query.get_or_404(id)

    if empresa.utilizador_id != user.id and user.role != 'admin':
        return jsonify({'status': 'error', 'error': {'code': 'FORBIDDEN', 'message': 'Sem permissão'}}), 403

    data = request.get_json()
    if data.get('nome'):
        empresa.nome = data['nome'].strip()
    if data.get('setor'):
        empresa.setor = data['setor'].strip()
    if 'num_colaboradores' in data:
        empresa.num_colaboradores = data['num_colaboradores']
    if 'localizacao' in data:
        empresa.localizacao = data['localizacao']
    if 'ano_fundacao' in data:
        empresa.ano_fundacao = data['ano_fundacao']
    if 'descricao' in data:
        empresa.descricao = data['descricao']

    db.session.commit()
    return jsonify({'status': 'success', 'data': empresa.to_dict(), 'message': 'Empresa atualizada'}), 200


@empresas_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def eliminar_empresa(id):
    """Soft delete de empresa."""
    user = get_current_user()
    empresa = Empresa.query.get_or_404(id)

    if empresa.utilizador_id != user.id and user.role != 'admin':
        return jsonify({'status': 'error', 'error': {'code': 'FORBIDDEN', 'message': 'Sem permissão'}}), 403

    empresa.ativo = False
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Empresa eliminada'}), 200
