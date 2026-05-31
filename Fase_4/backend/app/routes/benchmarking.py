"""Rotas de Benchmarking Setorial — comparação anónima entre organizações do mesmo setor."""
from flask import Blueprint, jsonify, request
from sqlalchemy import func
from app import db
from app.models.organizacao import Organizacao
from app.models.avaliacao import Avaliacao
from app.models.resultado import ResultadoCamada
from app.models.ailo import CamadaAilo
from app.utils.decorators import login_required

bench_bp = Blueprint('benchmarking', __name__)


@bench_bp.route('/setores', methods=['GET'])
@login_required
def listar_setores():
    """Lista todos os setores com avaliações concluídas."""
    setores = db.session.query(
        Organizacao.setor,
        func.count(Avaliacao.id).label('total_avaliacoes')
    ).join(Avaliacao, Avaliacao.organizacao_id == Organizacao.id)\
     .filter(Avaliacao.status == 'concluida')\
     .group_by(Organizacao.setor)\
     .having(func.count(Avaliacao.id) >= 1)\
     .all()

    return jsonify({
        'setores': [{'nome': s.setor, 'total_avaliacoes': s.total_avaliacoes} for s in setores]
    }), 200


@bench_bp.route('/<string:setor>', methods=['GET'])
@login_required
def benchmarking_setor(setor):
    """Retorna scores médios por camada para um setor, comparando com a organização do utilizador."""
    org_id = request.args.get('org_id', type=int)

    # Obter todas as avaliações concluídas de organizações do setor
    avaliacoes_setor = db.session.query(Avaliacao.id).join(
        Organizacao, Organizacao.id == Avaliacao.organizacao_id
    ).filter(
        Organizacao.setor == setor,
        Avaliacao.status == 'concluida'
    ).all()

    aval_ids = [a.id for a in avaliacoes_setor]
    if not aval_ids:
        return jsonify({'error': f'Sem avaliações concluídas no setor "{setor}"'}), 404

    # Scores médios do setor por camada
    camadas = CamadaAilo.query.order_by(CamadaAilo.ordem).all()
    medias_setor = {}
    for camada in camadas:
        avg = db.session.query(func.avg(ResultadoCamada.score)).filter(
            ResultadoCamada.avaliacao_id.in_(aval_ids),
            ResultadoCamada.camada_id == camada.id
        ).scalar()
        medias_setor[camada.id] = {
            'camada': camada.nome,
            'camada_id': camada.id,
            'score_medio': round(float(avg), 2) if avg else 0,
            'ordem': camada.ordem,
            'cor': camada.cor
        }

    # Score global médio do setor
    avg_global = db.session.query(func.avg(Avaliacao.score_global)).filter(
        Avaliacao.id.in_(aval_ids),
        Avaliacao.score_global.isnot(None)
    ).scalar()

    resultado = {
        'setor': setor,
        'total_avaliacoes': len(aval_ids),
        'score_global_medio': round(float(avg_global), 2) if avg_global else 0,
        'camadas': list(medias_setor.values()),
    }

    # Se org_id fornecido, adicionar dados da organização para comparação
    if org_id:
        ultima_aval = Avaliacao.query.filter_by(
            organizacao_id=org_id, status='concluida'
        ).order_by(Avaliacao.data_fim.desc()).first()

        if ultima_aval:
            org = Organizacao.query.get(org_id)
            org_scores = {}
            for rc in ResultadoCamada.query.filter_by(avaliacao_id=ultima_aval.id).all():
                org_scores[rc.camada_id] = round(rc.score, 2)

            resultado['organizacao'] = {
                'nome': org.nome if org else 'N/A',
                'score_global': round(ultima_aval.score_global, 2) if ultima_aval.score_global else 0,
                'camadas': org_scores,
                'percentil': _calcular_percentil(ultima_aval.score_global, aval_ids)
            }

    return jsonify(resultado), 200


def _calcular_percentil(score, aval_ids):
    """Calcula o percentil de um score dentro das avaliações do setor."""
    if not score:
        return 0
    total = len(aval_ids)
    abaixo = Avaliacao.query.filter(
        Avaliacao.id.in_(aval_ids),
        Avaliacao.score_global < score
    ).count()
    return round((abaixo / total) * 100) if total > 0 else 0
