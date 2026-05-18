"""Rotas de Avaliações."""
from flask import Blueprint, request, jsonify
from datetime import datetime
from app import db
from app.models.avaliacao import Avaliacao
from app.models.organizacao import Organizacao
from app.models.resposta import Resposta
from app.models.ailo import Indicador
from app.services.scoring import calcular_scoring
from app.services.interdependencias import analisar_interdependencias
from app.services.report_generator import gerar_relatorio
from app.services.recomendacoes import gerar_recomendacoes
from app.utils.decorators import login_required

aval_bp = Blueprint('avaliacoes', __name__)

@aval_bp.route('', methods=['POST'])
@login_required
def criar():
    data = request.get_json()
    org_id = data.get('organizacao_id')
    org = Organizacao.query.filter_by(id=org_id, user_id=request.current_user.id).first()
    if not org:
        return jsonify({'error': 'Organização não encontrada'}), 404

    aval = Avaliacao(organizacao_id=org_id, user_id=request.current_user.id)
    db.session.add(aval)
    db.session.commit()

    total = Indicador.query.count()
    result = aval.to_dict()
    result['progresso'] = {'total_indicadores': total, 'respondidos': 0, 'percentagem': 0}
    return jsonify(result), 201

@aval_bp.route('', methods=['GET'])
@login_required
def listar():
    avals = Avaliacao.query.filter_by(user_id=request.current_user.id).order_by(Avaliacao.created_at.desc()).all()
    result = []
    for a in avals:
        d = a.to_dict()
        respondidos = Resposta.query.filter_by(avaliacao_id=a.id).count()
        total = Indicador.query.count()
        d['progresso'] = {'total_indicadores': total, 'respondidos': respondidos, 'percentagem': int(respondidos/total*100) if total > 0 else 0}
        result.append(d)
    return jsonify({'data': result}), 200

@aval_bp.route('/<int:id>', methods=['GET'])
@login_required
def detalhar(id):
    aval = Avaliacao.query.filter_by(id=id, user_id=request.current_user.id).first()
    if not aval:
        return jsonify({'error': 'Avaliação não encontrada'}), 404

    from app.models.ailo import CamadaAilo, Componente
    d = aval.to_dict()
    camadas = CamadaAilo.query.order_by(CamadaAilo.ordem).all()
    progresso_camada = []
    for cam in camadas:
        ind_ids = [i.id for c in cam.componentes for i in c.indicadores]
        respondidos = Resposta.query.filter(Resposta.avaliacao_id==id, Resposta.indicador_id.in_(ind_ids)).count() if ind_ids else 0
        total = len(ind_ids)
        progresso_camada.append({
            'camada_id': cam.id, 'nome': cam.nome, 'cor': cam.cor,
            'respondidos': respondidos, 'total': total,
            'percentagem': int(respondidos/total*100) if total > 0 else 0
        })
    d['progresso_por_camada'] = progresso_camada
    return jsonify(d), 200

@aval_bp.route('/<int:id>/finalizar', methods=['POST'])
@login_required
def finalizar(id):
    aval = Avaliacao.query.filter_by(id=id, user_id=request.current_user.id).first()
    if not aval:
        return jsonify({'error': 'Avaliação não encontrada'}), 404
    if aval.status == 'completa':
        return jsonify({'error': 'Avaliação já foi finalizada'}), 400

    aval.status = 'completa'
    aval.data_fim = datetime.utcnow()
    db.session.commit()

    resultado = calcular_scoring(id)
    analisar_interdependencias(id)
    gerar_recomendacoes(id)
    gerar_relatorio(id)

    d = aval.to_dict()
    d['resultados_por_camada'] = [r.to_dict() for r in aval.resultados_camada]
    return jsonify(d), 200
