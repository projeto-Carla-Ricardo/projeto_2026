"""
Rotas do Questionário — Dimensões, perguntas, respostas e progresso.
Blueprint: /api/v1/questionario
"""
import json
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.dimensao import Dimensao
from app.models.indicador import Indicador
from app.models.pergunta import Pergunta
from app.models.resposta import Resposta
from app.models.avaliacao import Avaliacao
from app.models.empresa import Empresa
from app.utils.auth_helpers import get_current_user
from app.utils.fuzzy_logic import calculate_fuzzy_value

questionario_bp = Blueprint('questionario', __name__, url_prefix='/api/v1/questionario')


@questionario_bp.route('/dimensoes', methods=['GET'])
@jwt_required()
def listar_dimensoes():
    """Lista dimensões com indicadores e perguntas (estrutura completa do questionário)."""
    dimensoes = Dimensao.query.order_by(Dimensao.ordem).all()
    result = []

    for dim in dimensoes:
        dim_data = dim.to_dict()
        dim_data['indicadores'] = []

        for ind in dim.indicadores.order_by(Indicador.ordem).all():
            ind_data = ind.to_dict()
            ind_data['perguntas'] = [p.to_dict() for p in ind.perguntas.order_by(Pergunta.ordem).all()]
            dim_data['indicadores'].append(ind_data)

        result.append(dim_data)

    return jsonify({'status': 'success', 'data': result}), 200


@questionario_bp.route('/respostas', methods=['POST'])
@jwt_required()
def guardar_respostas():
    """Guardar respostas em batch (permite guardar progresso parcial)."""
    data = request.get_json()
    user = get_current_user()

    avaliacao_id = data.get('avaliacao_id')
    respostas_data = data.get('respostas', [])

    if not avaliacao_id or not respostas_data:
        return jsonify({'status': 'error', 'error': {'code': 'VALIDATION_ERROR', 'message': 'avaliacao_id e respostas obrigatórios'}}), 400

    # Verificar permissão
    avaliacao = Avaliacao.query.get(avaliacao_id)
    if not avaliacao:
        return jsonify({'status': 'error', 'error': {'code': 'NOT_FOUND', 'message': 'Avaliação não encontrada'}}), 404

    empresa = Empresa.query.get(avaliacao.empresa_id)
    if empresa.utilizador_id != user.id and user.role != 'admin':
        return jsonify({'status': 'error', 'error': {'code': 'FORBIDDEN', 'message': 'Sem permissão'}}), 403

    if avaliacao.estado != 'em_curso':
        return jsonify({'status': 'error', 'error': {'code': 'BAD_REQUEST', 'message': 'Avaliação não está em curso'}}), 400

    guardadas = 0
    for resp_data in respostas_data:
        pergunta_id = resp_data.get('pergunta_id')
        if not pergunta_id:
            continue

        pergunta = Pergunta.query.get(pergunta_id)
        if not pergunta:
            continue

        # Calcular valor fuzzy
        opcoes = None
        if pergunta.opcoes_json:
            try:
                opcoes = json.loads(pergunta.opcoes_json)
            except (json.JSONDecodeError, TypeError):
                opcoes = None

        valor_texto = resp_data.get('valor_texto')
        valor_numerico = resp_data.get('valor_numerico')
        valor_fuzzy = calculate_fuzzy_value(valor_texto, valor_numerico, pergunta.tipo_resposta, opcoes)

        # Upsert: atualizar se já existe, inserir se não
        resposta = Resposta.query.filter_by(
            avaliacao_id=avaliacao_id,
            pergunta_id=pergunta_id
        ).first()

        if resposta:
            resposta.valor_texto = valor_texto
            resposta.valor_numerico = valor_numerico
            resposta.valor_fuzzy = valor_fuzzy
        else:
            resposta = Resposta(
                avaliacao_id=avaliacao_id,
                pergunta_id=pergunta_id,
                valor_texto=valor_texto,
                valor_numerico=valor_numerico,
                valor_fuzzy=valor_fuzzy
            )
            db.session.add(resposta)

        guardadas += 1

    db.session.commit()

    # Calcular progresso
    total_perguntas = Pergunta.query.count()
    respondidas = Resposta.query.filter_by(avaliacao_id=avaliacao_id).count()
    percentagem = round((respondidas / total_perguntas) * 100) if total_perguntas > 0 else 0

    return jsonify({
        'status': 'success',
        'data': {
            'guardadas': guardadas,
            'progresso': {
                'total_perguntas': total_perguntas,
                'respondidas': respondidas,
                'percentagem': percentagem
            }
        }
    }), 200


@questionario_bp.route('/respostas/<int:avaliacao_id>', methods=['GET'])
@jwt_required()
def obter_respostas(avaliacao_id):
    """Obter respostas guardadas de uma avaliação."""
    user = get_current_user()
    avaliacao = Avaliacao.query.get_or_404(avaliacao_id)
    empresa = Empresa.query.get(avaliacao.empresa_id)

    if empresa.utilizador_id != user.id and user.role != 'admin':
        return jsonify({'status': 'error', 'error': {'code': 'FORBIDDEN', 'message': 'Sem permissão'}}), 403

    respostas = Resposta.query.filter_by(avaliacao_id=avaliacao_id).all()
    return jsonify({'status': 'success', 'data': [r.to_dict() for r in respostas]}), 200


@questionario_bp.route('/progresso/<int:avaliacao_id>', methods=['GET'])
@jwt_required()
def ver_progresso(avaliacao_id):
    """Ver progresso do questionário."""
    user = get_current_user()
    avaliacao = Avaliacao.query.get_or_404(avaliacao_id)
    empresa = Empresa.query.get(avaliacao.empresa_id)

    if empresa.utilizador_id != user.id and user.role != 'admin':
        return jsonify({'status': 'error', 'error': {'code': 'FORBIDDEN', 'message': 'Sem permissão'}}), 403

    total_perguntas = Pergunta.query.count()
    respondidas = Resposta.query.filter_by(avaliacao_id=avaliacao_id).count()

    # Progresso por dimensão
    dimensoes = Dimensao.query.order_by(Dimensao.ordem).all()
    progresso_dimensoes = []
    for dim in dimensoes:
        perguntas_dim = Pergunta.query.join(Indicador).filter(Indicador.dimensao_id == dim.id).count()
        respondidas_dim = (
            Resposta.query
            .filter_by(avaliacao_id=avaliacao_id)
            .join(Pergunta)
            .join(Indicador)
            .filter(Indicador.dimensao_id == dim.id)
            .count()
        )
        progresso_dimensoes.append({
            'codigo': dim.codigo,
            'nome': dim.nome,
            'total': perguntas_dim,
            'respondidas': respondidas_dim,
            'completa': respondidas_dim >= perguntas_dim
        })

    return jsonify({
        'status': 'success',
        'data': {
            'total_perguntas': total_perguntas,
            'respondidas': respondidas,
            'percentagem': round((respondidas / total_perguntas) * 100) if total_perguntas > 0 else 0,
            'dimensoes': progresso_dimensoes
        }
    }), 200
