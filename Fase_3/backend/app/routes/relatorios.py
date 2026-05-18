"""Rotas de Relatórios."""
from flask import Blueprint, request, jsonify, Response, send_file
from app.models.avaliacao import Avaliacao
from app.models.conversa import Relatorio
from app.models.resultado import ResultadoCamada, Interdependencia
from app.services.report_generator import gerar_relatorio, gerar_html_relatorio
from app.utils.decorators import login_required

relat_bp = Blueprint('relatorios', __name__)

@relat_bp.route('/avaliacoes/<int:aval_id>/relatorio', methods=['POST'])
@login_required
def gerar(aval_id):
    aval = Avaliacao.query.filter_by(id=aval_id, user_id=request.current_user.id).first()
    if not aval:
        return jsonify({'error': 'Avaliação não encontrada'}), 404
    if aval.status != 'completa':
        return jsonify({'error': 'Avaliação não finalizada'}), 400

    rel = gerar_relatorio(aval_id)
    if not rel:
        return jsonify({'error': 'Erro ao gerar relatório'}), 500
    return jsonify(rel.to_dict()), 201

@relat_bp.route('/relatorios/<int:id>', methods=['GET'])
@login_required
def obter(id):
    rel = Relatorio.query.get(id)
    if not rel:
        return jsonify({'error': 'Relatório não encontrado'}), 404
    import json
    data = rel.to_dict()
    data['conteudo'] = json.loads(rel.conteudo_json)
    return jsonify(data), 200

@relat_bp.route('/relatorios/<int:id>/html', methods=['GET'])
@login_required
def obter_html(id):
    rel = Relatorio.query.get(id)
    if not rel:
        return jsonify({'error': 'Relatório não encontrado'}), 404
    html = gerar_html_relatorio(rel.avaliacao_id)
    return Response(html, mimetype='text/html')

@relat_bp.route('/avaliacoes/<int:aval_id>/relatorio/html', methods=['GET'])
@login_required
def obter_html_por_avaliacao(aval_id):
    aval = Avaliacao.query.filter_by(id=aval_id, user_id=request.current_user.id).first()
    if not aval:
        return jsonify({'error': 'Avaliação não encontrada'}), 404
    html = gerar_html_relatorio(aval_id)
    if not html:
        return jsonify({'error': 'Relatório não disponível'}), 404
    return Response(html, mimetype='text/html')

@relat_bp.route('/avaliacoes/<int:aval_id>/relatorio/pdf', methods=['GET'])
@login_required
def download_pdf(aval_id):
    """Gera e faz download do relatório em PDF."""
    aval = Avaliacao.query.filter_by(id=aval_id, user_id=request.current_user.id).first()
    if not aval:
        return jsonify({'error': 'Avaliação não encontrada'}), 404
    if aval.status != 'completa':
        return jsonify({'error': 'Avaliação não finalizada'}), 400

    resultados = ResultadoCamada.query.filter_by(avaliacao_id=aval_id).all()
    interdeps = Interdependencia.query.filter_by(avaliacao_id=aval_id).all()

    from app.services.pdf_report import gerar_relatorio_pdf
    pdf_buffer = gerar_relatorio_pdf(aval, resultados, interdeps)
    org_nome = aval.organizacao.nome.replace(' ', '_') if aval.organizacao else 'relatorio'
    filename = f"AILO_Relatorio_{org_nome}.pdf"

    return send_file(pdf_buffer, mimetype='application/pdf', as_attachment=True, download_name=filename)

