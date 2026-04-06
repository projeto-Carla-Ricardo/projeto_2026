"""
Rotas de Relatórios — Geração e download de relatórios.
Blueprint: /api/v1/relatorios
"""
from flask import Blueprint, jsonify, make_response
from flask_jwt_extended import jwt_required
from app.models.avaliacao import Avaliacao
from app.models.empresa import Empresa
from app.services.report_generator import gerar_relatorio
from app.services.recommendation_engine import gerar_recomendacoes
from app.utils.auth_helpers import get_current_user

relatorios_bp = Blueprint('relatorios', __name__, url_prefix='/api/v1/relatorios')


@relatorios_bp.route('/<int:avaliacao_id>', methods=['GET'])
@jwt_required()
def obter_relatorio(avaliacao_id):
    """Gerar e obter relatório completo de uma avaliação."""
    user = get_current_user()
    avaliacao = Avaliacao.query.get_or_404(avaliacao_id)
    empresa = Empresa.query.get(avaliacao.empresa_id)

    if empresa.utilizador_id != user.id and user.role != 'admin':
        return jsonify({'status': 'error', 'error': {'code': 'FORBIDDEN', 'message': 'Sem permissão'}}), 403

    if avaliacao.estado != 'concluida':
        return jsonify({'status': 'error', 'error': {'code': 'BAD_REQUEST', 'message': 'Avaliação não concluída'}}), 400

    relatorio = gerar_relatorio(avaliacao_id)
    if not relatorio:
        return jsonify({'status': 'error', 'error': {'code': 'SERVER_ERROR', 'message': 'Erro ao gerar relatório'}}), 500

    return jsonify({'status': 'success', 'data': relatorio}), 200


@relatorios_bp.route('/<int:avaliacao_id>/recomendacoes', methods=['GET'])
@jwt_required()
def obter_recomendacoes(avaliacao_id):
    """Obter recomendações de ferramentas IA para uma avaliação."""
    user = get_current_user()
    avaliacao = Avaliacao.query.get_or_404(avaliacao_id)
    empresa = Empresa.query.get(avaliacao.empresa_id)

    if empresa.utilizador_id != user.id and user.role != 'admin':
        return jsonify({'status': 'error', 'error': {'code': 'FORBIDDEN', 'message': 'Sem permissão'}}), 403

    recomendacoes = gerar_recomendacoes(avaliacao_id, empresa)
    return jsonify({'status': 'success', 'data': recomendacoes}), 200


@relatorios_bp.route('/<int:avaliacao_id>/pdf', methods=['GET'])
@jwt_required()
def download_pdf(avaliacao_id):
    """Gerar e descarregar relatório PDF."""
    user = get_current_user()
    avaliacao = Avaliacao.query.get_or_404(avaliacao_id)
    empresa = Empresa.query.get(avaliacao.empresa_id)

    if empresa.utilizador_id != user.id and user.role != 'admin':
        return jsonify({'status': 'error', 'error': {'code': 'FORBIDDEN', 'message': 'Sem permissão'}}), 403

    if avaliacao.estado != 'concluida':
        return jsonify({'status': 'error', 'error': {'code': 'BAD_REQUEST', 'message': 'Avaliação não concluída'}}), 400

    relatorio = gerar_relatorio(avaliacao_id)
    if not relatorio:
        return jsonify({'status': 'error', 'error': {'code': 'SERVER_ERROR', 'message': 'Erro ao gerar relatório'}}), 500

    # Gerar HTML para PDF
    html = _render_pdf_html(relatorio)

    try:
        from weasyprint import HTML
        pdf_bytes = HTML(string=html).write_pdf()
        response = make_response(pdf_bytes)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename=IALO_Diagnostico_{empresa.nome.replace(" ", "_")}.pdf'
        return response
    except Exception as e:
        return jsonify({'status': 'error', 'error': {'code': 'PDF_ERROR', 'message': f'Erro ao gerar PDF: {str(e)}'}}), 500


def _render_pdf_html(data):
    """Gera HTML formatado para conversão em PDF."""
    dims_html = ''
    for d in data['dimensoes']:
        bar_color = '#ff6b6b' if d['gap_critico'] else '#6366f1'
        dims_html += f'''
        <div class="dim-row">
            <div class="dim-info">
                <strong>{d['codigo']}</strong> — {d['nome']}
                <span class="dim-badge" style="background:{bar_color}20;color:{bar_color}">
                    Nível {d['nivel']} — {d['nivel_nome']}
                </span>
            </div>
            <div class="bar-container">
                <div class="bar-fill" style="width:{d['pontuacao']}%;background:{bar_color}"></div>
            </div>
            <span class="dim-score">{d['pontuacao']}%</span>
        </div>'''

    fortes_html = ''
    for p in data.get('pontos_fortes', []):
        fortes_html += f'<li><strong>{p["dimensao"]}</strong> ({p["pontuacao"]}%) — {p["destaque"]}</li>'

    necessidades_html = ''
    for n in data.get('necessidades', []):
        icon = '🔴' if n['gap_critico'] else '🟡'
        necessidades_html += f'<li>{icon} <strong>{n["dimensao"]}</strong> ({n["pontuacao"]}%) — {n["acao"]}</li>'

    passos_html = ''
    for i, p in enumerate(data.get('primeiros_passos', []), 1):
        ferramenta = f' → Sugestão: <em>{p["ferramenta"]}</em>' if p.get('ferramenta') else ''
        passos_html += f'<li><strong>Passo {i} ({p["dimensao"]}):</strong> {p["acao"]}{ferramenta}</li>'

    return f'''<!DOCTYPE html>
<html lang="pt-PT">
<head>
    <meta charset="UTF-8">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Helvetica', 'Arial', sans-serif; color: #1a1a2e; font-size: 11pt; line-height: 1.6; }}
        .page {{ padding: 40px; max-width: 800px; margin: 0 auto; }}
        .header {{ text-align: center; margin-bottom: 30px; padding-bottom: 20px; border-bottom: 3px solid #6366f1; }}
        .header h1 {{ font-size: 22pt; color: #6366f1; margin-bottom: 5px; }}
        .header h2 {{ font-size: 14pt; color: #444; font-weight: 400; }}
        .header .date {{ font-size: 9pt; color: #888; margin-top: 5px; }}
        .section {{ margin: 25px 0; }}
        .section h3 {{ font-size: 14pt; color: #6366f1; margin-bottom: 12px; padding-bottom: 6px; border-bottom: 1px solid #e0e0e0; }}
        .score-big {{ text-align: center; font-size: 48pt; font-weight: 800; color: #6366f1; margin: 15px 0 5px; }}
        .nivel-big {{ text-align: center; font-size: 14pt; color: #444; margin-bottom: 20px; }}
        .empresa-info {{ display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-bottom: 20px; }}
        .empresa-info span {{ font-size: 10pt; color: #666; }}
        .empresa-info strong {{ color: #333; }}
        .dim-row {{ display: flex; align-items: center; gap: 10px; margin-bottom: 10px; }}
        .dim-info {{ min-width: 200px; font-size: 10pt; }}
        .dim-badge {{ font-size: 8pt; padding: 2px 8px; border-radius: 10px; margin-left: 5px; }}
        .bar-container {{ flex: 1; height: 14px; background: #f0f0f0; border-radius: 7px; overflow: hidden; }}
        .bar-fill {{ height: 100%; border-radius: 7px; transition: width 0.3s; }}
        .dim-score {{ min-width: 40px; text-align: right; font-weight: 700; font-size: 11pt; }}
        ul {{ padding-left: 20px; }}
        li {{ margin-bottom: 8px; font-size: 10pt; }}
        .footer {{ margin-top: 40px; padding-top: 20px; border-top: 1px solid #e0e0e0; text-align: center; font-size: 8pt; color: #999; }}
    </style>
</head>
<body>
    <div class="page">
        <div class="header">
            <h1>🧠 IALO — Diagnóstico de Maturidade Digital</h1>
            <h2>{data['empresa']['nome']}</h2>
            <div class="date">Gerado em {data['data_geracao'][:10]}</div>
        </div>

        <div class="section">
            <h3>📋 Dados da Empresa</h3>
            <div class="empresa-info">
                <span><strong>Setor:</strong> {data['empresa']['setor']}</span>
                <span><strong>Colaboradores:</strong> {data['empresa'].get('num_colaboradores') or 'N/A'}</span>
                <span><strong>Localização:</strong> {data['empresa'].get('localizacao') or 'N/A'}</span>
            </div>
        </div>

        <div class="section">
            <h3>🎯 Resultado Global</h3>
            <div class="score-big">{data['resumo']['pontuacao_global']}%</div>
            <div class="nivel-big">Nível {data['resumo']['nivel_global']} — {data['resumo']['nivel_descricao']}</div>
        </div>

        <div class="section">
            <h3>📊 Resultados por Dimensão</h3>
            {dims_html}
        </div>

        <div class="section">
            <h3>✅ Pontos Fortes</h3>
            <ul>{fortes_html if fortes_html else '<li>Nenhum ponto forte identificado acima de 60%.</li>'}</ul>
        </div>

        <div class="section">
            <h3>⚠️ Necessidades Críticas</h3>
            <ul>{necessidades_html if necessidades_html else '<li>Nenhuma necessidade crítica identificada.</li>'}</ul>
        </div>

        <div class="section">
            <h3>🚀 Primeiros Passos Recomendados</h3>
            <ol>{passos_html if passos_html else '<li>Mantenha as boas práticas atuais e explore novas oportunidades.</li>'}</ol>
        </div>

        <div class="footer">
            Framework IALO — Inteligência Artificial para Learning Organisations<br>
            Projeto Final · Engenharia Informática · Universidade Aberta · 2025/2026
        </div>
    </div>
</body>
</html>'''
