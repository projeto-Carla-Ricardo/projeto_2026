"""Rotas de Exportação e RGPD — portabilidade de dados e direito ao esquecimento."""
from flask import Blueprint, jsonify, request
from app import db
from app.models.utilizador import Utilizador
from app.models.organizacao import Organizacao
from app.models.avaliacao import Avaliacao
from app.models.resposta import Resposta
from app.models.resultado import ResultadoCamada, Interdependencia
from app.models.conversa import ConversaIA, Relatorio
from app.models.ferramenta import Recomendacao
from app.utils.decorators import login_required

export_bp = Blueprint('export', __name__)


@export_bp.route('/meus-dados', methods=['GET'])
@login_required
def exportar_dados():
    """Exporta todos os dados do utilizador em formato JSON (RGPD Art. 20)."""
    user = request.current_user

    # Organizações
    orgs = Organizacao.query.filter_by(user_id=user.id).all()
    orgs_data = []
    for org in orgs:
        org_dict = org.to_dict()
        # Avaliações de cada organização
        avals = Avaliacao.query.filter_by(organizacao_id=org.id).all()
        avals_data = []
        for aval in avals:
            aval_dict = aval.to_dict()
            # Respostas
            resps = Resposta.query.filter_by(avaliacao_id=aval.id).all()
            aval_dict['respostas'] = [r.to_dict() for r in resps]
            # Resultados por camada
            rcs = ResultadoCamada.query.filter_by(avaliacao_id=aval.id).all()
            aval_dict['resultados_camada'] = [rc.to_dict() for rc in rcs]
            # Interdependências
            interdeps = Interdependencia.query.filter_by(avaliacao_id=aval.id).all()
            aval_dict['interdependencias'] = [i.to_dict() for i in interdeps]
            # Conversas IA
            convs = ConversaIA.query.filter_by(avaliacao_id=aval.id).all()
            aval_dict['conversas_ia'] = [c.to_dict() for c in convs]
            # Recomendações
            recs = Recomendacao.query.filter_by(avaliacao_id=aval.id).all()
            aval_dict['recomendacoes'] = [rec.to_dict() for rec in recs]
            avals_data.append(aval_dict)
        org_dict['avaliacoes'] = avals_data
        orgs_data.append(org_dict)

    dados = {
        'utilizador': {
            'id': user.id,
            'nome': user.nome,
            'email': user.email,
            'papel': user.papel,
            'criado_em': user.created_at.isoformat() if user.created_at else None
        },
        'organizacoes': orgs_data,
        'nota_rgpd': 'Exportação ao abrigo do RGPD Art. 20 — Direito à portabilidade dos dados'
    }

    return jsonify(dados), 200


@export_bp.route('/eliminar-conta', methods=['DELETE'])
@login_required
def eliminar_conta():
    """Elimina a conta e anonimiza dados (RGPD Art. 17 — Direito ao esquecimento)."""
    user = request.current_user
    confirmacao = request.json.get('confirmacao', '') if request.json else ''

    if confirmacao != 'ELIMINAR':
        return jsonify({'error': 'Envie {"confirmacao": "ELIMINAR"} para confirmar'}), 400

    # Anonimizar dados pessoais (manter dados estatísticos)
    user.nome = f'Utilizador Removido #{user.id}'
    user.email = f'removed_{user.id}@anonimo.ailo'
    user.password_hash = 'CONTA_ELIMINADA'
    user.ativo = False if hasattr(user, 'ativo') else None

    # Anonimizar organizações mas manter avaliações para benchmarking
    orgs = Organizacao.query.filter_by(user_id=user.id).all()
    for org in orgs:
        org.nome = f'Organização Anonimizada #{org.id}'
        org.descricao = None

    # Eliminar conversas IA (dados pessoais)
    for org in orgs:
        avals = Avaliacao.query.filter_by(organizacao_id=org.id).all()
        for aval in avals:
            ConversaIA.query.filter_by(avaliacao_id=aval.id).delete()

    db.session.commit()

    return jsonify({
        'message': 'Conta anonimizada com sucesso ao abrigo do RGPD Art. 17',
        'nota': 'Dados estatísticos foram preservados de forma anónima para benchmarking'
    }), 200
