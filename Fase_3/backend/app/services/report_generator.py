"""Gerador de Relatórios AILO — HTML e PDF."""
import json, os
from datetime import datetime
from app import db
from app.models.avaliacao import Avaliacao
from app.models.resultado import ResultadoCamada, Interdependencia
from app.models.conversa import Relatorio
from app.models.organizacao import Organizacao

def gerar_relatorio(avaliacao_id):
    """Gera relatório completo para uma avaliação."""
    avaliacao = Avaliacao.query.get(avaliacao_id)
    if not avaliacao or avaliacao.status != 'completa':
        return None

    org = avaliacao.organizacao
    resultados = ResultadoCamada.query.filter_by(avaliacao_id=avaliacao_id).all()
    interdeps = Interdependencia.query.filter_by(avaliacao_id=avaliacao_id).all()

    conteudo = {
        'organizacao': org.to_dict(),
        'avaliacao': avaliacao.to_dict(),
        'resultados': [r.to_dict() for r in resultados],
        'interdependencias': [i.to_dict() for i in interdeps],
        'data_geracao': datetime.utcnow().isoformat()
    }

    titulo = f"Diagnóstico AILO — {org.nome}"

    # Verificar se já existe relatório
    rel = Relatorio.query.filter_by(avaliacao_id=avaliacao_id).first()
    if rel:
        rel.conteudo_json = json.dumps(conteudo, ensure_ascii=False)
        rel.titulo = titulo
    else:
        rel = Relatorio(avaliacao_id=avaliacao_id, titulo=titulo, conteudo_json=json.dumps(conteudo, ensure_ascii=False))
        db.session.add(rel)

    db.session.commit()
    return rel

def gerar_html_relatorio(avaliacao_id):
    """Gera HTML formatado do relatório."""
    avaliacao = Avaliacao.query.get(avaliacao_id)
    if not avaliacao:
        return None

    org = avaliacao.organizacao
    resultados = ResultadoCamada.query.filter_by(avaliacao_id=avaliacao_id).all()
    interdeps = Interdependencia.query.filter_by(avaliacao_id=avaliacao_id).all()

    def nivel_cor(score):
        if score >= 3.5: return '#27AE60'
        elif score >= 2.7: return '#F39C12'
        return '#E74C3C'

    # Construir HTML
    camadas_html = ""
    for r in sorted(resultados, key=lambda x: x.camada.ordem if x.camada else 0):
        pf = json.loads(r.pontos_fortes) if r.pontos_fortes else []
        lac = json.loads(r.lacunas) if r.lacunas else []
        rec = json.loads(r.recomendacoes) if r.recomendacoes else []
        cor = r.camada.cor if r.camada else '#333'

        pf_html = "".join(f"<li>✅ {p}</li>" for p in pf) or "<li>Sem pontos fortes identificados</li>"
        lac_html = "".join(f"<li>⚠️ {l}</li>" for l in lac) or "<li>Sem lacunas identificadas</li>"
        rec_html = "".join(f"<li>💡 {r_}</li>" for r_ in rec) or "<li>Sem recomendações</li>"

        camadas_html += f"""
        <div style="margin-bottom:30px;page-break-inside:avoid;">
            <h2 style="color:{cor};border-bottom:3px solid {cor};padding-bottom:8px;">
                {r.camada.nome if r.camada else 'N/A'}
            </h2>
            <div style="display:flex;align-items:center;gap:20px;margin:10px 0;">
                <span style="font-size:36px;font-weight:700;color:{nivel_cor(r.score)};">{r.score:.1f}</span>
                <span style="font-size:18px;color:#666;">{r.nivel}</span>
                <div style="flex:1;height:10px;background:#eee;border-radius:5px;">
                    <div style="width:{r.score/5*100}%;height:100%;background:{cor};border-radius:5px;"></div>
                </div>
            </div>
            <h3>Pontos Fortes</h3><ul>{pf_html}</ul>
            <h3>Lacunas</h3><ul>{lac_html}</ul>
            <h3>Recomendações</h3><ul>{rec_html}</ul>
        </div>"""

    interdeps_html = ""
    for i in interdeps:
        icon = {'fortalece':'✅','risco':'⚠️','bloqueia':'🔴','oportunidade':'💡'}.get(i.tipo_relacao, '•')
        interdeps_html += f"<tr><td>{icon} {i.camada_a.nome if i.camada_a else ''}</td><td>{i.camada_b.nome if i.camada_b else ''}</td><td>{i.tipo_relacao}</td><td>{i.descricao}</td><td>{i.impacto}</td></tr>"

    html = f"""<!DOCTYPE html>
<html lang="pt"><head><meta charset="UTF-8">
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    body {{ font-family: 'Inter', sans-serif; color: #333; max-width: 800px; margin: 0 auto; padding: 40px; }}
    h1 {{ color: #2E4057; }} h2 {{ margin-top: 30px; }} h3 {{ color: #555; }}
    table {{ width: 100%; border-collapse: collapse; margin: 15px 0; }}
    th, td {{ border: 1px solid #ddd; padding: 10px; text-align: left; font-size: 14px; }}
    th {{ background: #2E4057; color: white; }}
    .cover {{ text-align: center; padding: 80px 0; }}
    .cover h1 {{ font-size: 36px; margin-bottom: 10px; }}
    .summary {{ background: #f8f9fa; padding: 30px; border-radius: 12px; margin: 20px 0; }}
    ul {{ padding-left: 20px; }} li {{ margin: 5px 0; }}
</style></head><body>
    <div class="cover">
        <h1>DIAGNÓSTICO AILO</h1>
        <h2 style="color:#048A81;">{org.nome}</h2>
        <p style="color:#666;font-size:18px;">{datetime.utcnow().strftime('%B %Y')}</p>
        <p style="color:#999;">Artificial Intelligence in a Learning Organization</p>
    </div>
    <div class="summary">
        <h2>Resumo Executivo</h2>
        <p><strong>Índice Global AILO:</strong> <span style="font-size:28px;color:{nivel_cor(avaliacao.score_global or 0)};">{avaliacao.score_global:.1f}</span> / 5.0</p>
        <p><strong>Classificação:</strong> {avaliacao.nivel_global}</p>
        <p><strong>Setor:</strong> {org.setor} | <strong>Dimensão:</strong> {org.dimensao} | <strong>Tipo:</strong> {org.tipo}</p>
    </div>
    <h1>Diagnóstico por Camada</h1>
    {camadas_html}
    <h1>Interdependências</h1>
    <table><tr><th>Camada A</th><th>Camada B</th><th>Tipo</th><th>Descrição</th><th>Impacto</th></tr>
    {interdeps_html}</table>
    <div style="margin-top:50px;padding:20px;background:#f0f4f8;border-radius:8px;">
        <p style="text-align:center;color:#999;">Relatório gerado pela Plataforma AILO — {datetime.utcnow().strftime('%d/%m/%Y %H:%M')}</p>
    </div>
</body></html>"""
    return html
