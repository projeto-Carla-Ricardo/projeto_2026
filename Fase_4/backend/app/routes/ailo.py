"""Rotas do Framework AILO (read-only)."""
from flask import Blueprint, jsonify
from app.models.ailo import CamadaAilo, Indicador
from app.utils.decorators import login_required

ailo_bp = Blueprint('ailo', __name__)

@ailo_bp.route('/camadas', methods=['GET'])
@login_required
def listar_camadas():
    camadas = CamadaAilo.query.order_by(CamadaAilo.ordem).all()
    return jsonify({'data': [c.to_dict(include_componentes=True) for c in camadas]}), 200

@ailo_bp.route('/camadas/<int:id>/indicadores', methods=['GET'])
@login_required
def indicadores_camada(id):
    camada = CamadaAilo.query.get(id)
    if not camada:
        return jsonify({'error': 'Camada não encontrada'}), 404
    return jsonify({
        'camada': {'id': camada.id, 'nome': camada.nome, 'cor': camada.cor},
        'componentes': [c.to_dict(include_indicadores=True) for c in camada.componentes]
    }), 200

@ailo_bp.route('/indicadores', methods=['GET'])
@login_required
def listar_indicadores():
    indicadores = Indicador.query.order_by(Indicador.id).all()
    return jsonify({'data': [i.to_dict() for i in indicadores], 'total': len(indicadores)}), 200
