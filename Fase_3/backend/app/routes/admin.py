"""Rotas de Administração — gestão de indicadores, ferramentas e estatísticas."""
from flask import Blueprint, request, jsonify
from app import db
from app.models.utilizador import Utilizador
from app.models.organizacao import Organizacao
from app.models.avaliacao import Avaliacao
from app.models.ailo import CamadaAilo, Componente, Indicador
from app.models.ferramenta import FerramentaIA
from app.utils.decorators import admin_required

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/stats', methods=['GET'])
@admin_required
def estatisticas_globais():
    """Estatísticas globais da plataforma."""
    total_utilizadores = Utilizador.query.count()
    total_organizacoes = Organizacao.query.count()
    total_avaliacoes = Avaliacao.query.count()
    avaliacoes_completas = Avaliacao.query.filter_by(status='completa').count()

    # Score médio global
    from sqlalchemy import func
    score_medio = db.session.query(func.avg(Avaliacao.score_global)).filter(
        Avaliacao.score_global.isnot(None)
    ).scalar() or 0

    # Distribuição por nível
    niveis = db.session.query(
        Avaliacao.nivel_global, func.count(Avaliacao.id)
    ).filter(Avaliacao.nivel_global.isnot(None)).group_by(Avaliacao.nivel_global).all()

    return jsonify({
        'total_utilizadores': total_utilizadores,
        'total_organizacoes': total_organizacoes,
        'total_avaliacoes': total_avaliacoes,
        'avaliacoes_completas': avaliacoes_completas,
        'score_medio_global': round(score_medio, 2),
        'distribuicao_niveis': {n: c for n, c in niveis},
        'total_camadas': CamadaAilo.query.count(),
        'total_componentes': Componente.query.count(),
        'total_indicadores': Indicador.query.count(),
        'total_ferramentas': FerramentaIA.query.count(),
    }), 200


@admin_bp.route('/indicadores', methods=['GET'])
@admin_required
def listar_indicadores():
    """Lista todos os indicadores com detalhes de camada e componente."""
    indicadores = Indicador.query.all()
    result = []
    for ind in indicadores:
        d = ind.to_dict()
        d['componente_nome'] = ind.componente.nome if ind.componente else None
        d['camada_nome'] = ind.componente.camada.nome if ind.componente and ind.componente.camada else None
        result.append(d)
    return jsonify({'data': result}), 200


@admin_bp.route('/indicadores/<int:ind_id>', methods=['PUT'])
@admin_required
def editar_indicador(ind_id):
    """Editar peso ou texto de um indicador."""
    ind = Indicador.query.get(ind_id)
    if not ind:
        return jsonify({'error': 'Indicador não encontrado'}), 404

    data = request.get_json()
    if 'peso' in data:
        ind.peso = float(data['peso'])
    if 'pergunta' in data:
        ind.pergunta = data['pergunta']
    if 'desc_nivel_1' in data:
        ind.desc_nivel_1 = data['desc_nivel_1']
    if 'desc_nivel_3' in data:
        ind.desc_nivel_3 = data['desc_nivel_3']
    if 'desc_nivel_5' in data:
        ind.desc_nivel_5 = data['desc_nivel_5']

    db.session.commit()
    return jsonify(ind.to_dict()), 200


@admin_bp.route('/ferramentas', methods=['GET'])
@admin_required
def listar_ferramentas():
    """Lista todas as ferramentas IA."""
    ferramentas = FerramentaIA.query.all()
    return jsonify({'data': [f.to_dict() for f in ferramentas]}), 200


@admin_bp.route('/ferramentas', methods=['POST'])
@admin_required
def criar_ferramenta():
    """Cria nova ferramenta IA no catálogo."""
    data = request.get_json()
    required = ['nome', 'descricao', 'area_funcional', 'custo', 'complexidade']
    for field in required:
        if field not in data:
            return jsonify({'error': f'Campo obrigatório: {field}'}), 400

    ferramenta = FerramentaIA(
        nome=data['nome'], descricao=data['descricao'],
        camada_id=data.get('camada_id'), area_funcional=data['area_funcional'],
        custo=data['custo'], complexidade=data['complexidade'],
        url=data.get('url')
    )
    db.session.add(ferramenta)
    db.session.commit()
    return jsonify(ferramenta.to_dict()), 201


@admin_bp.route('/ferramentas/<int:fid>', methods=['PUT'])
@admin_required
def editar_ferramenta(fid):
    """Edita ferramenta IA."""
    ferramenta = FerramentaIA.query.get(fid)
    if not ferramenta:
        return jsonify({'error': 'Ferramenta não encontrada'}), 404

    data = request.get_json()
    for key in ['nome', 'descricao', 'area_funcional', 'custo', 'complexidade', 'url', 'camada_id']:
        if key in data:
            setattr(ferramenta, key, data[key])

    db.session.commit()
    return jsonify(ferramenta.to_dict()), 200


@admin_bp.route('/ferramentas/<int:fid>', methods=['DELETE'])
@admin_required
def eliminar_ferramenta(fid):
    """Desativa ferramenta IA (soft delete)."""
    ferramenta = FerramentaIA.query.get(fid)
    if not ferramenta:
        return jsonify({'error': 'Ferramenta não encontrada'}), 404

    ferramenta.ativo = False
    db.session.commit()
    return jsonify({'message': 'Ferramenta desativada com sucesso'}), 200


@admin_bp.route('/utilizadores', methods=['GET'])
@admin_required
def listar_utilizadores():
    """Lista todos os utilizadores."""
    users = Utilizador.query.all()
    return jsonify({'data': [u.to_dict() for u in users]}), 200
