"""Rotas de Analytics — estatísticas avançadas para o painel admin."""
from flask import Blueprint, jsonify
from sqlalchemy import func, extract
from datetime import datetime, timedelta
from app import db
from app.models.utilizador import Utilizador
from app.models.organizacao import Organizacao
from app.models.avaliacao import Avaliacao
from app.models.resultado import ResultadoCamada
from app.models.ailo import CamadaAilo
from app.utils.decorators import admin_required

analytics_bp = Blueprint('analytics', __name__)


@analytics_bp.route('/overview', methods=['GET'])
@admin_required
def overview():
    """Estatísticas gerais da plataforma."""
    total_users = Utilizador.query.count()
    total_orgs = Organizacao.query.count()
    total_avals = Avaliacao.query.count()
    avals_concluidas = Avaliacao.query.filter_by(status='concluida').count()
    avals_em_curso = Avaliacao.query.filter_by(status='em_curso').count()

    avg_global = db.session.query(func.avg(Avaliacao.score_global)).filter(
        Avaliacao.status == 'concluida',
        Avaliacao.score_global.isnot(None)
    ).scalar()

    taxa_conclusao = round((avals_concluidas / total_avals * 100), 1) if total_avals > 0 else 0

    return jsonify({
        'utilizadores': total_users,
        'organizacoes': total_orgs,
        'avaliacoes_total': total_avals,
        'avaliacoes_concluidas': avals_concluidas,
        'avaliacoes_em_curso': avals_em_curso,
        'score_global_medio': round(float(avg_global), 2) if avg_global else 0,
        'taxa_conclusao': taxa_conclusao
    }), 200


@analytics_bp.route('/scores-por-camada', methods=['GET'])
@admin_required
def scores_por_camada():
    """Score médio por camada em todas as avaliações concluídas."""
    camadas = CamadaAilo.query.order_by(CamadaAilo.ordem).all()
    resultado = []
    for camada in camadas:
        avg = db.session.query(func.avg(ResultadoCamada.score)).filter(
            ResultadoCamada.camada_id == camada.id
        ).scalar()
        resultado.append({
            'camada': camada.nome,
            'score_medio': round(float(avg), 2) if avg else 0,
            'cor': camada.cor,
            'ordem': camada.ordem
        })
    return jsonify({'camadas': resultado}), 200


@analytics_bp.route('/distribuicao-scores', methods=['GET'])
@admin_required
def distribuicao_scores():
    """Distribuição dos scores globais em faixas."""
    faixas = [
        ('Inicial (1.0-1.8)', 1.0, 1.8),
        ('Em Desenvolvimento (1.9-2.6)', 1.9, 2.6),
        ('Definido (2.7-3.4)', 2.7, 3.4),
        ('Gerido (3.5-4.2)', 3.5, 4.2),
        ('Otimizado (4.3-5.0)', 4.3, 5.0),
    ]
    resultado = []
    for nome, min_s, max_s in faixas:
        count = Avaliacao.query.filter(
            Avaliacao.status == 'concluida',
            Avaliacao.score_global >= min_s,
            Avaliacao.score_global <= max_s
        ).count()
        resultado.append({'faixa': nome, 'count': count})
    return jsonify({'distribuicao': resultado}), 200


@analytics_bp.route('/avaliacoes-por-mes', methods=['GET'])
@admin_required
def avaliacoes_por_mes():
    """Avaliações criadas nos últimos 12 meses."""
    agora = datetime.utcnow()
    inicio = agora - timedelta(days=365)
    resultado = []
    for i in range(12):
        mes_inicio = inicio + timedelta(days=30 * i)
        mes_fim = mes_inicio + timedelta(days=30)
        count = Avaliacao.query.filter(
            Avaliacao.data_inicio >= mes_inicio,
            Avaliacao.data_inicio < mes_fim
        ).count()
        resultado.append({
            'mes': mes_inicio.strftime('%Y-%m'),
            'count': count
        })
    return jsonify({'meses': resultado}), 200


@analytics_bp.route('/setores', methods=['GET'])
@admin_required
def avaliacoes_por_setor():
    """Distribuição de avaliações por setor."""
    setores = db.session.query(
        Organizacao.setor,
        func.count(Avaliacao.id).label('total')
    ).join(Avaliacao, Avaliacao.organizacao_id == Organizacao.id)\
     .group_by(Organizacao.setor)\
     .order_by(func.count(Avaliacao.id).desc())\
     .all()
    return jsonify({
        'setores': [{'nome': s.setor, 'total': s.total} for s in setores]
    }), 200
