"""Rotas de Respostas."""
from flask import Blueprint, request, jsonify
from app import db
from app.models.resposta import Resposta
from app.models.avaliacao import Avaliacao
from app.utils.decorators import login_required

resp_bp = Blueprint('respostas', __name__)

@resp_bp.route('/<int:aval_id>/respostas', methods=['POST'])
@login_required
def guardar(aval_id):
    aval = Avaliacao.query.filter_by(id=aval_id, user_id=request.current_user.id).first()
    if not aval:
        return jsonify({'error': 'Avaliação não encontrada'}), 404

    data = request.get_json()
    ind_id = data.get('indicador_id')
    score = data.get('score')
    if not ind_id or not score or score < 1 or score > 5:
        return jsonify({'error': 'indicador_id e score (1-5) são obrigatórios'}), 400

    resp = Resposta.query.filter_by(avaliacao_id=aval_id, indicador_id=ind_id).first()
    if resp:
        resp.score = score
        resp.justificacao = data.get('justificacao')
    else:
        resp = Resposta(avaliacao_id=aval_id, indicador_id=ind_id, score=score, justificacao=data.get('justificacao'))
        db.session.add(resp)

    db.session.commit()
    return jsonify(resp.to_dict()), 200

@resp_bp.route('/<int:aval_id>/respostas/batch', methods=['POST'])
@login_required
def guardar_batch(aval_id):
    aval = Avaliacao.query.filter_by(id=aval_id, user_id=request.current_user.id).first()
    if not aval:
        return jsonify({'error': 'Avaliação não encontrada'}), 404

    data = request.get_json()
    respostas = data.get('respostas', [])
    saved = 0
    for r in respostas:
        ind_id, score = r.get('indicador_id'), r.get('score')
        if not ind_id or not score or score < 1 or score > 5:
            continue
        resp = Resposta.query.filter_by(avaliacao_id=aval_id, indicador_id=ind_id).first()
        if resp:
            resp.score = score
            resp.justificacao = r.get('justificacao')
        else:
            resp = Resposta(avaliacao_id=aval_id, indicador_id=ind_id, score=score, justificacao=r.get('justificacao'))
            db.session.add(resp)
        saved += 1

    db.session.commit()
    return jsonify({'saved': saved}), 200

@resp_bp.route('/<int:aval_id>/respostas', methods=['GET'])
@login_required
def listar(aval_id):
    aval = Avaliacao.query.filter_by(id=aval_id, user_id=request.current_user.id).first()
    if not aval:
        return jsonify({'error': 'Avaliação não encontrada'}), 404

    respostas = Resposta.query.filter_by(avaliacao_id=aval_id).all()
    return jsonify({'data': [r.to_dict() for r in respostas], 'total': len(respostas)}), 200
