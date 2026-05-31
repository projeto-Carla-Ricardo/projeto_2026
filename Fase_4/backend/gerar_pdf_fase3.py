#!/usr/bin/env python3
"""Gera o PDF 'O_que_foi_feito.pdf' documentando a Fase 3."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY

PDF_PATH = os.path.join(os.path.dirname(__file__), '..', 'O_que_foi_feito.pdf')

AILO_DARK = HexColor('#2E4057')
AILO_ACCENT = HexColor('#048A81')
WHITE = HexColor('#FFFFFF')
GRAY = HexColor('#666666')
LIGHT_BG = HexColor('#F0F4F8')

def build_pdf():
    doc = SimpleDocTemplate(PDF_PATH, pagesize=A4, topMargin=2*cm, bottomMargin=2*cm, leftMargin=2.5*cm, rightMargin=2.5*cm)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle('CustomTitle', parent=styles['Title'], fontSize=28, textColor=AILO_DARK, spaceAfter=10, alignment=TA_CENTER, fontName='Helvetica-Bold')
    subtitle_style = ParagraphStyle('Subtitle', parent=styles['Normal'], fontSize=14, textColor=AILO_ACCENT, spaceAfter=20, alignment=TA_CENTER)
    h1 = ParagraphStyle('H1', parent=styles['Heading1'], fontSize=18, textColor=AILO_DARK, spaceBefore=20, spaceAfter=10, fontName='Helvetica-Bold')
    h2 = ParagraphStyle('H2', parent=styles['Heading2'], fontSize=14, textColor=AILO_ACCENT, spaceBefore=14, spaceAfter=8, fontName='Helvetica-Bold')
    body = ParagraphStyle('Body', parent=styles['Normal'], fontSize=11, leading=16, spaceAfter=8, alignment=TA_JUSTIFY)
    bullet = ParagraphStyle('Bullet', parent=body, leftIndent=20, bulletIndent=10, spaceAfter=4)
    small = ParagraphStyle('Small', parent=styles['Normal'], fontSize=9, textColor=GRAY, alignment=TA_CENTER)

    story = []

    # === CAPA ===
    story.append(Spacer(1, 4*cm))
    story.append(Paragraph("O QUE FOI FEITO", title_style))
    story.append(Paragraph("Fase 3 — Consolidação, Testes e Funcionalidades Avançadas", subtitle_style))
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph("Artificial Intelligence in a Learning Organization", ParagraphStyle('C2', parent=body, alignment=TA_CENTER, fontSize=12, textColor=GRAY)))
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph("Projeto de Engenharia Informática — Universidade Aberta", ParagraphStyle('C3', parent=body, alignment=TA_CENTER, fontSize=11, textColor=GRAY)))
    story.append(Paragraph("Ricardo &amp; Carla", ParagraphStyle('C4', parent=body, alignment=TA_CENTER, fontSize=11, textColor=GRAY)))
    story.append(Paragraph("Baseado no framework de Santos &amp; Mamede (2026)", ParagraphStyle('C5', parent=body, alignment=TA_CENTER, fontSize=10, textColor=GRAY)))
    story.append(Spacer(1, 2*cm))
    story.append(Paragraph("Maio 2026", ParagraphStyle('Date', parent=body, alignment=TA_CENTER, fontSize=12, textColor=AILO_DARK)))
    story.append(PageBreak())

    # === ÍNDICE ===
    story.append(Paragraph("Índice", h1))
    toc = [
        "1. Enquadramento e Objetivos da Fase 3",
        "2. Evolução face à Fase 2",
        "3. Testes Automatizados (pytest)",
        "4. Exportação de Relatórios PDF (ReportLab)",
        "5. Painel de Administração",
        "6. Comparação Temporal de Avaliações",
        "7. Motor de Recomendação de Ferramentas IA",
        "8. Perfil de Utilizador",
        "9. Melhorias de Robustez e Arquitetura",
        "10. Estrutura de Ficheiros",
        "11. Instruções de Instalação e Execução",
        "12. Instruções para Deployment Real",
        "13. Resultados dos Testes",
        "14. Trabalho Futuro",
    ]
    for item in toc:
        story.append(Paragraph(item, body))
    story.append(PageBreak())

    # === 1. ENQUADRAMENTO ===
    story.append(Paragraph("1. Enquadramento e Objetivos da Fase 3", h1))
    story.append(Paragraph("A Fase 3 do projeto AILO representa a consolidação da plataforma, evoluindo o MVP funcional da Fase 2 com testes automatizados, funcionalidades avançadas e melhorias de robustez. O projeto é desenvolvido por Ricardo e Carla no âmbito do curso de Engenharia Informática da Universidade Aberta, baseado no framework teórico de Santos &amp; Mamede (2026).", body))
    story.append(Paragraph("Objetivos principais:", body))
    story.append(Paragraph("• Implementar testes automatizados com pytest (37 testes)", bullet))
    story.append(Paragraph("• Exportação de relatórios de diagnóstico em PDF profissional (ReportLab)", bullet))
    story.append(Paragraph("• Painel de administração para gestão de indicadores, ferramentas e estatísticas", bullet))
    story.append(Paragraph("• Comparação temporal entre avaliações da mesma organização", bullet))
    story.append(Paragraph("• Motor de recomendação de ferramentas IA baseado nos resultados", bullet))
    story.append(Paragraph("• Gestão de perfil de utilizador", bullet))
    story.append(Paragraph("• Melhorias de robustez: error handlers, validação, paginação", bullet))
    story.append(PageBreak())

    # === 2. EVOLUÇÃO ===
    story.append(Paragraph("2. Evolução face à Fase 2", h1))
    story.append(Paragraph("A Fase 3 partiu da base de código da Fase 2 e adicionou as seguintes evoluções:", body))
    evol = [
        ["Área", "Fase 2", "Fase 3"],
        ["Testes", "Validação manual", "37 testes automatizados (pytest)"],
        ["Relatórios PDF", "Apenas HTML", "PDF profissional com ReportLab"],
        ["Administração", "Sem painel admin", "Dashboard com estatísticas e CRUD"],
        ["Comparação", "Avaliação única", "Sobreposição temporal multi-avaliação"],
        ["Recomendações", "Sem recomendações", "Motor baseado em scores por camada"],
        ["Perfil", "Sem gestão de perfil", "Edição de nome e alteração de password"],
        ["Error handling", "Básico", "Handlers JSON para 404/500 + validação"],
        ["Config", "Dev/Prod", "Dev/Prod/Testing (in-memory SQLite)"],
        ["Rotas backend", "9 blueprints", "11 blueprints (+admin, +perfil)"],
        ["Páginas frontend", "7 páginas", "10 páginas (+admin, +comparação, +perfil)"],
    ]
    t = Table(evol, colWidths=[3*cm, 5.5*cm, 7*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), AILO_DARK), ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTSIZE', (0, 0), (-1, -1), 8), ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, GRAY), ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, LIGHT_BG]),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'), ('TOPPADDING', (0, 0), (-1, -1), 4), ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t)
    story.append(PageBreak())

    # === 3. TESTES ===
    story.append(Paragraph("3. Testes Automatizados (pytest)", h1))
    story.append(Paragraph("Foram implementados 37 testes automatizados distribuídos por 6 ficheiros, utilizando pytest com fixtures partilhados e base de dados in-memory (SQLite):", body))
    testes = [
        ["Ficheiro", "Testes", "Cobertura"],
        ["conftest.py", "—", "Fixtures: app, client, db_session, auth_header, org_id, avaliacao_id"],
        ["test_auth.py", "11", "Registo (sucesso, email duplicado, campos em falta, email inválido, password fraca), Login (sucesso, credenciais inválidas, email inexistente), Me (com/sem/token inválido)"],
        ["test_organizacoes.py", "9", "CRUD completo: criar (sucesso, sem campos, sem auth), listar (vazio, com dados), editar (sucesso, inexistente), eliminar (sucesso, inexistente)"],
        ["test_avaliacoes.py", "8", "Criar (sucesso, sem org, sem auth), listar, detalhar, respostas (individual, batch, score inválido)"],
        ["test_scoring.py", "7", "Classificação de níveis (5 níveis), scoring com avaliação inexistente, scoring com respostas completas"],
        ["test_interdependencias.py", "2", "Análise completa com dados reais (fluxo API), função direta com avaliação inexistente"],
    ]
    t2 = Table(testes, colWidths=[3.5*cm, 1.5*cm, 10.5*cm])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), AILO_DARK), ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTSIZE', (0, 0), (-1, -1), 7.5), ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, GRAY), ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, LIGHT_BG]),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'), ('TOPPADDING', (0, 0), (-1, -1), 3), ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t2)
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("<b>Configuração de testes:</b> A classe TestingConfig utiliza SQLite in-memory (sqlite:///:memory:) para isolamento total. Os fixtures com scope 'session' populam a BD uma vez com os 51 indicadores AILO; fixtures com scope 'function' garantem independência entre testes.", body))
    story.append(PageBreak())

    # === 4. PDF ===
    story.append(Paragraph("4. Exportação de Relatórios PDF (ReportLab)", h1))
    story.append(Paragraph("O serviço services/pdf_report.py gera relatórios PDF profissionais com a biblioteca ReportLab. Funcionalidades:", body))
    story.append(Paragraph("• <b>Capa personalizada</b> com nome da organização, data e score global", bullet))
    story.append(Paragraph("• <b>Resumo executivo</b> com scores por camada em tabela formatada", bullet))
    story.append(Paragraph("• <b>Detalhes por camada</b>: score, nível, pontos fortes, lacunas e recomendações", bullet))
    story.append(Paragraph("• <b>Interdependências</b>: tabela com pares críticos, tipo de relação e impacto", bullet))
    story.append(Paragraph("• <b>Endpoint REST</b>: GET /api/v1/avaliacoes/:id/relatorio/pdf — retorna o ficheiro PDF como download", bullet))
    story.append(Paragraph("• <b>Botão na UI</b>: Botão '📥 Download PDF' na página de resultados", bullet))

    # === 5. ADMIN ===
    story.append(Paragraph("5. Painel de Administração", h1))
    story.append(Paragraph("O painel de administração (routes/admin.py + pages/admin.html) fornece:", body))
    story.append(Paragraph("• <b>Dashboard de estatísticas:</b> Total de utilizadores, organizações, avaliações e score médio global", bullet))
    story.append(Paragraph("• <b>Gestão de indicadores:</b> Edição de pesos dos indicadores por camada", bullet))
    story.append(Paragraph("• <b>Gestão de ferramentas IA:</b> CRUD completo do catálogo de ferramentas (nome, descrição, área, custo, complexidade, URL)", bullet))
    story.append(Paragraph("• <b>Lista de utilizadores:</b> Visualização de todos os utilizadores registados", bullet))
    story.append(Paragraph("• <b>Proteção:</b> Todas as rotas admin requerem papel 'admin' via decorador @admin_required", bullet))
    story.append(PageBreak())

    # === 6. COMPARAÇÃO ===
    story.append(Paragraph("6. Comparação Temporal de Avaliações", h1))
    story.append(Paragraph("A funcionalidade de comparação temporal (pages/comparacao.html) permite sobrepor múltiplas avaliações da mesma organização para visualizar a evolução da maturidade ao longo do tempo.", body))
    story.append(Paragraph("<b>Backend:</b> Endpoint GET /api/v1/organizacoes/:id/comparacao que retorna todas as avaliações concluídas com os respetivos resultados por camada.", body))
    story.append(Paragraph("<b>Frontend:</b> Dois gráficos Chart.js:", body))
    story.append(Paragraph("• <b>Radar multi-dataset:</b> Sobreposição dos perfis de cada avaliação (uma cor por avaliação)", bullet))
    story.append(Paragraph("• <b>Gráfico de linhas:</b> Evolução do score global ao longo das avaliações", bullet))
    story.append(Paragraph("• <b>Tabela comparativa:</b> Scores lado a lado com setas de tendência (↑↓→)", bullet))

    # === 7. RECOMENDAÇÕES ===
    story.append(Paragraph("7. Motor de Recomendação de Ferramentas IA", h1))
    story.append(Paragraph("O serviço services/recomendacoes.py cruza os resultados do diagnóstico com o catálogo de ferramentas IA para gerar recomendações personalizadas.", body))
    story.append(Paragraph("<b>Algoritmo:</b>", body))
    story.append(Paragraph("• Para cada camada com score &lt; 3.5 (abaixo de 'Gerido'), identifica ferramentas IA relevantes", bullet))
    story.append(Paragraph("• Calcula prioridade com base no gap (5.0 - score) × peso da camada", bullet))
    story.append(Paragraph("• Ordena recomendações por prioridade descendente", bullet))
    story.append(Paragraph("• Gera justificação contextualizada para cada recomendação", bullet))
    story.append(Paragraph("<b>Endpoint:</b> GET /api/v1/avaliacoes/:id/recomendacoes", body))
    story.append(Paragraph("<b>UI:</b> Secção dedicada na página de resultados com cards de ferramentas recomendadas, organizadas por prioridade.", body))
    story.append(PageBreak())

    # === 8. PERFIL ===
    story.append(Paragraph("8. Perfil de Utilizador", h1))
    story.append(Paragraph("A página de perfil (routes/perfil.py + pages/perfil.html) permite:", body))
    story.append(Paragraph("• <b>Ver dados pessoais:</b> Nome, email e papel", bullet))
    story.append(Paragraph("• <b>Editar nome:</b> PUT /api/v1/perfil com validação", bullet))
    story.append(Paragraph("• <b>Alterar password:</b> PUT /api/v1/perfil/password com verificação da password atual", bullet))

    # === 9. ROBUSTEZ ===
    story.append(Paragraph("9. Melhorias de Robustez e Arquitetura", h1))
    story.append(Paragraph("• <b>Error handlers JSON:</b> Respostas 404 e 500 em formato JSON em vez de HTML", bullet))
    story.append(Paragraph("• <b>TestingConfig:</b> Configuração dedicada para testes com BD in-memory", bullet))
    story.append(Paragraph("• <b>Geração lazy de recomendações:</b> Se as recomendações não existem ao consultar, são geradas automaticamente", bullet))
    story.append(Paragraph("• <b>Navbar dinâmica:</b> Links para admin (visível apenas para administradores), perfil e comparação", bullet))
    story.append(Paragraph("• <b>Integração no finalizar:</b> Ao finalizar uma avaliação, o sistema executa automaticamente scoring → interdependências → recomendações → relatório", bullet))

    # === 10. ESTRUTURA ===
    story.append(Paragraph("10. Estrutura de Ficheiros", h1))
    dirs = [
        "Fase_3/backend/app/__init__.py — App factory (11 blueprints, error handlers)",
        "Fase_3/backend/app/config.py — Configurações dev/prod/testing",
        "Fase_3/backend/app/models/ — 8 modelos SQLAlchemy (12+ tabelas)",
        "Fase_3/backend/app/routes/ — 11 ficheiros de rotas (auth, org, ailo, avaliações, respostas, resultados, chat, relatórios, admin, perfil)",
        "Fase_3/backend/app/services/ — 6 serviços (scoring, interdependências, IA, relatórios, PDF, recomendações)",
        "Fase_3/backend/app/utils/ — Auth JWT, decoradores, validadores",
        "Fase_3/backend/tests/ — 6 ficheiros de testes (37 testes pytest)",
        "Fase_3/backend/seeds/ — Dados iniciais do framework AILO",
        "Fase_3/frontend/pages/ — 10 páginas HTML (+ admin, comparação, perfil)",
        "Fase_3/frontend/css/ — Design system premium dark theme",
        "Fase_3/frontend/js/ — API wrapper e app module",
    ]
    for d in dirs:
        story.append(Paragraph(f"• {d}", bullet))
    story.append(PageBreak())

    # === 11. INSTALAÇÃO ===
    story.append(Paragraph("11. Instruções de Instalação e Execução", h1))
    story.append(Paragraph("11.1 Pré-requisitos", h2))
    story.append(Paragraph("• Python 3.10+ instalado", bullet))
    story.append(Paragraph("11.2 Instalação e Execução", h2))
    cmds = [
        "cd Fase_3/backend",
        "python3 -m venv venv",
        "source venv/bin/activate  # Linux/Mac",
        "pip install -r requirements.txt",
        "cp .env.example .env  # Editar com as suas configurações",
        "python seed.py  # Popular a base de dados",
        "python run.py  # Iniciar → http://localhost:5000",
    ]
    for c in cmds:
        story.append(Paragraph(f"<font face='Courier' size='9'>$ {c}</font>", bullet))
    story.append(Paragraph("11.3 Executar Testes", h2))
    story.append(Paragraph("<font face='Courier' size='9'>$ python -m pytest tests/ -v</font>", bullet))
    story.append(Paragraph("Resultado esperado: 37 passed", body))

    # === 12. DEPLOYMENT ===
    story.append(Paragraph("12. Instruções para Deployment Real", h1))
    story.append(Paragraph("• <b>Base de Dados:</b> Migrar para PostgreSQL (alterar DATABASE_URL no .env)", bullet))
    story.append(Paragraph("• <b>Servidor WSGI:</b> gunicorn -w 4 -b 0.0.0.0:5000 'app:create_app(\"production\")'", bullet))
    story.append(Paragraph("• <b>Proxy Reverso:</b> Nginx com SSL (Let's Encrypt)", bullet))
    story.append(Paragraph("• <b>SECRET_KEY:</b> Gerar chave forte (python -c \"import secrets; print(secrets.token_hex(32))\")", bullet))
    story.append(Paragraph("• <b>GEMINI_API_KEY:</b> Obter em https://aistudio.google.com/apikey", bullet))
    story.append(Paragraph("• <b>Criar utilizador admin:</b> Inserir manualmente na BD um utilizador com papel='admin'", bullet))

    # === 13. RESULTADOS ===
    story.append(Paragraph("13. Resultados dos Testes", h1))
    story.append(Paragraph("Todos os 37 testes passam com sucesso:", body))
    story.append(Paragraph("• test_auth.py: 11 passed ✅", bullet))
    story.append(Paragraph("• test_organizacoes.py: 9 passed ✅", bullet))
    story.append(Paragraph("• test_avaliacoes.py: 8 passed ✅", bullet))
    story.append(Paragraph("• test_scoring.py: 7 passed ✅", bullet))
    story.append(Paragraph("• test_interdependencias.py: 2 passed ✅", bullet))
    story.append(Paragraph("• Servidor Flask inicia sem erros ✅", bullet))
    story.append(PageBreak())

    # === 14. FUTURO ===
    story.append(Paragraph("14. Trabalho Futuro", h1))
    story.append(Paragraph("• Integração com LMS (Moodle) via xAPI/LTI", bullet))
    story.append(Paragraph("• Benchmarking setorial (comparação entre organizações do mesmo setor)", bullet))
    story.append(Paragraph("• Aplicação mobile (PWA — Progressive Web App)", bullet))
    story.append(Paragraph("• Sistema de notificações por email", bullet))
    story.append(Paragraph("• Migração de base de dados com Alembic", bullet))
    story.append(Paragraph("• CI/CD pipeline com GitHub Actions", bullet))
    story.append(Paragraph("• Docker + docker-compose para deployment containerizado", bullet))
    story.append(Paragraph("• Expansão do catálogo de ferramentas IA com filtragem inteligente", bullet))
    story.append(Paragraph("• Dashboard analytics com métricas de utilização da plataforma", bullet))

    story.append(Spacer(1, 2*cm))
    story.append(Paragraph("—— Fim do documento ——", small))
    story.append(Paragraph("Gerado automaticamente pela plataforma AILO · Maio 2026", small))

    doc.build(story)
    print(f"✅ PDF gerado: {os.path.abspath(PDF_PATH)}")

if __name__ == '__main__':
    build_pdf()
