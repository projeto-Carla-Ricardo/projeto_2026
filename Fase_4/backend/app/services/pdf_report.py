"""Serviço de geração de relatórios PDF com ReportLab."""
import io
import json
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY

AILO_DARK = HexColor('#2E4057')
AILO_ACCENT = HexColor('#048A81')
WHITE = HexColor('#FFFFFF')
GRAY = HexColor('#666666')
LIGHT_BG = HexColor('#F0F4F8')


def gerar_relatorio_pdf(avaliacao, resultados, interdependencias):
    """Gera PDF do relatório de diagnóstico AILO.
    
    Args:
        avaliacao: Objeto Avaliacao com organizacao
        resultados: Lista de ResultadoCamada
        interdependencias: Lista de Interdependencia
    
    Returns:
        BytesIO com o PDF gerado
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=2*cm, bottomMargin=2*cm,
                            leftMargin=2.5*cm, rightMargin=2.5*cm)
    styles = getSampleStyleSheet()

    title = ParagraphStyle('Title2', parent=styles['Title'], fontSize=24, textColor=AILO_DARK,
                           spaceAfter=10, alignment=TA_CENTER, fontName='Helvetica-Bold')
    subtitle = ParagraphStyle('Sub', parent=styles['Normal'], fontSize=14, textColor=AILO_ACCENT,
                              spaceAfter=20, alignment=TA_CENTER)
    h1 = ParagraphStyle('H1', parent=styles['Heading1'], fontSize=16, textColor=AILO_DARK,
                        spaceBefore=16, spaceAfter=8, fontName='Helvetica-Bold')
    h2 = ParagraphStyle('H2', parent=styles['Heading2'], fontSize=13, textColor=AILO_ACCENT,
                        spaceBefore=10, spaceAfter=6, fontName='Helvetica-Bold')
    body = ParagraphStyle('Body', parent=styles['Normal'], fontSize=10, leading=14,
                          spaceAfter=6, alignment=TA_JUSTIFY)
    bullet = ParagraphStyle('Bullet', parent=body, leftIndent=16, bulletIndent=8, spaceAfter=3)
    small = ParagraphStyle('Small', parent=styles['Normal'], fontSize=9, textColor=GRAY, alignment=TA_CENTER)

    story = []
    org = avaliacao.organizacao

    # --- CAPA ---
    story.append(Spacer(1, 3*cm))
    story.append(Paragraph("Relatório de Diagnóstico AILO", title))
    story.append(Paragraph(f"{org.nome}", subtitle))
    story.append(Spacer(1, 1*cm))

    info = [
        ["Setor", org.setor or '—'],
        ["Dimensão", org.dimensao or '—'],
        ["Tipo", org.tipo or '—'],
        ["País", org.pais or 'Portugal'],
        ["Data da Avaliação", avaliacao.data_fim.strftime('%d/%m/%Y') if avaliacao.data_fim else '—'],
    ]
    t = Table(info, colWidths=[4*cm, 8*cm])
    t.setStyle(TableStyle([
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (0, 0), (0, -1), AILO_DARK),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t)
    story.append(Spacer(1, 2*cm))
    story.append(Paragraph(f"Score Global: <b>{avaliacao.score_global or 0:.2f}</b> — {avaliacao.nivel_global or 'N/A'}", subtitle))
    story.append(PageBreak())

    # --- RESUMO EXECUTIVO ---
    story.append(Paragraph("1. Resumo Executivo", h1))
    story.append(Paragraph(
        f"A organização <b>{org.nome}</b> obteve um índice global de maturidade AILO de "
        f"<b>{avaliacao.score_global or 0:.2f}</b>, classificado como <b>{avaliacao.nivel_global or 'N/A'}</b>. "
        f"Esta avaliação abrangeu as 6 camadas interdependentes do framework AILO, analisando "
        f"{len(resultados)} dimensões com base em 51 indicadores de maturidade.", body))

    # Tabela resumo das camadas
    table_data = [["Camada", "Score", "Nível"]]
    for r in sorted(resultados, key=lambda x: x.camada.ordem if x.camada else 0):
        table_data.append([r.camada.nome if r.camada else '?', f"{r.score:.2f}", r.nivel])

    t2 = Table(table_data, colWidths=[6*cm, 3*cm, 5*cm])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), AILO_DARK), ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTSIZE', (0, 0), (-1, -1), 10), ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, GRAY),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, LIGHT_BG]),
        ('TOPPADDING', (0, 0), (-1, -1), 4), ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(Spacer(1, 0.5*cm))
    story.append(t2)

    # --- NÍVEL DE MATURIDADE ---
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph("Nível de Maturidade AILO", h2))
    
    niveis_desc = {
        'Inicial': 'A organização está nos estágios iniciais de adoção de IA e práticas de aprendizagem organizacional.',
        'Em Desenvolvimento': 'Existem iniciativas isoladas mas falta integração sistémica entre as camadas.',
        'Definido': 'A organização tem processos definidos mas a implementação é inconsistente.',
        'Gerido': 'A organização gere ativamente a integração de IA e aprendizagem organizacional.',
        'Otimizado': 'A organização está num nível de excelência com melhoria contínua integrada.'
    }
    desc = niveis_desc.get(avaliacao.nivel_global, '')
    story.append(Paragraph(f"<b>{avaliacao.nivel_global}</b> — {desc}", body))
    story.append(PageBreak())

    # --- DIAGNÓSTICO POR CAMADA ---
    story.append(Paragraph("2. Diagnóstico por Camada", h1))
    for r in sorted(resultados, key=lambda x: x.camada.ordem if x.camada else 0):
        nome_camada = r.camada.nome if r.camada else '?'
        story.append(Paragraph(f"2.{r.camada.ordem if r.camada else 0}. {nome_camada}", h2))
        story.append(Paragraph(f"<b>Score:</b> {r.score:.2f} — <b>Nível:</b> {r.nivel}", body))

        pf = json.loads(r.pontos_fortes) if r.pontos_fortes else []
        lac = json.loads(r.lacunas) if r.lacunas else []
        rec = json.loads(r.recomendacoes) if r.recomendacoes else []

        if pf:
            story.append(Paragraph("<b>Pontos Fortes:</b>", body))
            for p in pf[:3]:
                story.append(Paragraph(f"✓ {p}", bullet))
        if lac:
            story.append(Paragraph("<b>Lacunas Identificadas:</b>", body))
            for l in lac[:3]:
                story.append(Paragraph(f"✗ {l}", bullet))
        if rec:
            story.append(Paragraph("<b>Recomendações:</b>", body))
            for rr in rec[:3]:
                story.append(Paragraph(f"→ {rr}", bullet))
        story.append(Spacer(1, 0.3*cm))

    # --- PONTOS CRÍTICOS ---
    from app.models.resposta import Resposta as RespModel
    respostas_all = RespModel.query.filter_by(avaliacao_id=avaliacao.id).all()
    criticos = [(r.indicador.codigo, r.indicador.pergunta[:80], r.score, 
                 r.indicador.componente.camada.nome if r.indicador and r.indicador.componente else '?') 
                for r in respostas_all if r.score <= 2 and r.indicador]
    criticos.sort(key=lambda x: x[2])
    
    if criticos:
        story.append(Paragraph("2.5. Pontos Críticos", h1))
        crit_data = [["Indicador", "Pergunta", "Score", "Camada"]]
        for cod, perg, score, cam in criticos[:8]:
            crit_data.append([cod, perg, f"{score}/5", cam])
        tc = Table(crit_data, colWidths=[2.5*cm, 6.5*cm, 2*cm, 3*cm])
        tc.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#E74C3C')), ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
            ('FONTSIZE', (0, 0), (-1, -1), 9), ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 0.5, GRAY),
            ('TOPPADDING', (0, 0), (-1, -1), 3), ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ]))
        story.append(tc)
    story.append(PageBreak())

    # --- INTERDEPENDÊNCIAS ---
    story.append(Paragraph("3. Análise de Interdependências", h1))
    if interdependencias:
        int_data = [["Par de Camadas", "Relação", "Impacto"]]
        for i in interdependencias:
            ca = i.camada_a.nome if i.camada_a else '?'
            cb = i.camada_b.nome if i.camada_b else '?'
            int_data.append([f"{ca} × {cb}", i.tipo_relacao, i.impacto])
        t3 = Table(int_data, colWidths=[5.5*cm, 4*cm, 4.5*cm])
        t3.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), AILO_ACCENT), ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
            ('FONTSIZE', (0, 0), (-1, -1), 9), ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 0.5, GRAY),
            ('TOPPADDING', (0, 0), (-1, -1), 3), ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ]))
        story.append(t3)
    else:
        story.append(Paragraph("Sem interdependências significativas identificadas.", body))

    # --- RODAPÉ ---
    story.append(Spacer(1, 2*cm))
    story.append(Paragraph("—— Relatório gerado pela plataforma AILO ——", small))
    story.append(Paragraph("Ricardo & Carla — Universidade Aberta — 2026", small))

    doc.build(story)
    buffer.seek(0)
    return buffer
