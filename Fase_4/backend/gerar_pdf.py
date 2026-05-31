#!/usr/bin/env python3
"""Gera o PDF 'O_que_foi_feito.pdf' documentando a Fase 2."""
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
AILO_LIGHT = HexColor('#54C6EB')
WHITE = HexColor('#FFFFFF')
GRAY = HexColor('#666666')
LIGHT_BG = HexColor('#F0F4F8')

def build_pdf():
    doc = SimpleDocTemplate(PDF_PATH, pagesize=A4, topMargin=2*cm, bottomMargin=2*cm, leftMargin=2.5*cm, rightMargin=2.5*cm)
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle('CustomTitle', parent=styles['Title'], fontSize=28, textColor=AILO_DARK, spaceAfter=10, alignment=TA_CENTER, fontName='Helvetica-Bold')
    subtitle_style = ParagraphStyle('Subtitle', parent=styles['Normal'], fontSize=14, textColor=AILO_ACCENT, spaceAfter=20, alignment=TA_CENTER)
    h1 = ParagraphStyle('H1', parent=styles['Heading1'], fontSize=18, textColor=AILO_DARK, spaceBefore=20, spaceAfter=10, fontName='Helvetica-Bold')
    h2 = ParagraphStyle('H2', parent=styles['Heading2'], fontSize=14, textColor=AILO_ACCENT, spaceBefore=14, spaceAfter=8, fontName='Helvetica-Bold')
    body = ParagraphStyle('Body', parent=styles['Normal'], fontSize=11, leading=16, spaceAfter=8, alignment=TA_JUSTIFY)
    bullet = ParagraphStyle('Bullet', parent=body, leftIndent=20, bulletIndent=10, spaceAfter=4)
    small = ParagraphStyle('Small', parent=styles['Normal'], fontSize=9, textColor=GRAY, alignment=TA_CENTER)

    story = []

    # COVER
    story.append(Spacer(1, 4*cm))
    story.append(Paragraph("O QUE FOI FEITO", title_style))
    story.append(Paragraph("Fase 2 — Implementação da Plataforma AILO", subtitle_style))
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph("Artificial Intelligence in a Learning Organization", ParagraphStyle('Cover2', parent=body, alignment=TA_CENTER, fontSize=12, textColor=GRAY)))
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph("Projeto de Engenharia Informática — Universidade Aberta", ParagraphStyle('Cover3', parent=body, alignment=TA_CENTER, fontSize=11, textColor=GRAY)))
    story.append(Paragraph("Ricardo & Carla", ParagraphStyle('Cover4', parent=body, alignment=TA_CENTER, fontSize=11, textColor=GRAY)))
    story.append(Paragraph("Baseado no framework de Santos & Mamede (2026)", ParagraphStyle('Cover5', parent=body, alignment=TA_CENTER, fontSize=10, textColor=GRAY)))
    story.append(Spacer(1, 2*cm))
    story.append(Paragraph("Maio 2026", ParagraphStyle('Date', parent=body, alignment=TA_CENTER, fontSize=12, textColor=AILO_DARK)))
    story.append(PageBreak())

    # TABLE OF CONTENTS
    story.append(Paragraph("Índice", h1))
    toc_items = [
        "1. Enquadramento e Objetivos",
        "2. Arquitetura Implementada",
        "3. Backend — Modelos de Dados",
        "4. Backend — API RESTful",
        "5. Backend — Motor de Scoring",
        "6. Backend — Assistente IA (Gemini)",
        "7. Frontend — Interface de Utilizador",
        "8. Base de Dados — Seed Data",
        "9. Segurança e Autenticação",
        "10. Testes e Validação",
        "11. Instruções de Instalação e Execução",
        "12. Instruções para Deployment Real",
        "13. Trabalho Futuro",
    ]
    for item in toc_items:
        story.append(Paragraph(item, body))
    story.append(PageBreak())

    # 1. ENQUADRAMENTO
    story.append(Paragraph("1. Enquadramento e Objetivos", h1))
    story.append(Paragraph("A Fase 2 do projeto AILO teve como objetivo transformar toda a documentação conceptual e técnica produzida na Fase 1 numa plataforma web funcional (MVP — Minimum Viable Product). O AILO é uma plataforma de diagnóstico de maturidade organizacional para integração de Inteligência Artificial nas Organizações Aprendentes, baseada no framework teórico de Santos & Mamede (2026). O projeto é desenvolvido por Ricardo e Carla no âmbito do curso de Engenharia Informática.", body))
    story.append(Paragraph("O framework AILO organiza-se em 6 camadas interdependentes:", body))
    camadas = [
        ("Organizacional", "Estratégia, processos, decisão e criação de valor"),
        ("Humana", "Pessoas, cultura, autonomia e ética"),
        ("Aprendizagem", "Contextos adaptativos, experiências personalizadas"),
        ("Cognitiva (IA)", "Geração, recomendação, síntese e previsão"),
        ("Tecnológica", "Plataformas, dados, integração, segurança"),
        ("Avaliação", "Evidências, avaliação formativa, competências, impacto"),
    ]
    for nome, desc in camadas:
        story.append(Paragraph(f"<b>• {nome}</b> — {desc}", bullet))
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph("A plataforma implementa 51 indicadores de maturidade distribuídos por 23 componentes nestas 6 camadas, cada um avaliado numa escala de 1 (Inicial) a 5 (Otimizado).", body))
    story.append(PageBreak())

    # 2. ARQUITETURA
    story.append(Paragraph("2. Arquitetura Implementada", h1))
    story.append(Paragraph("A arquitetura segue o modelo de 3 camadas definido na Fase 1:", body))
    story.append(Paragraph("<b>Frontend:</b> HTML5, CSS3 (design system premium dark theme), JavaScript Vanilla, Chart.js para gráficos radar e barras.", bullet))
    story.append(Paragraph("<b>Backend:</b> Python 3 com Flask (app factory pattern), Flask-SQLAlchemy para ORM, Flask-CORS para CORS, PyJWT para autenticação JWT, bcrypt para hashing de passwords.", bullet))
    story.append(Paragraph("<b>Base de Dados:</b> SQLite (desenvolvimento), com modelo preparado para PostgreSQL em produção.", bullet))
    story.append(Paragraph("<b>IA:</b> Integração com Google Gemini API para assistente conversacional contextualizado.", bullet))

    story.append(Paragraph("2.1 Estrutura de Pastas", h2))
    dirs = [
        "Fase_2/backend/app/__init__.py — Flask app factory",
        "Fase_2/backend/app/config.py — Configurações dev/prod",
        "Fase_2/backend/app/models/ — 8 ficheiros de modelos SQLAlchemy",
        "Fase_2/backend/app/routes/ — 8 ficheiros de rotas API REST",
        "Fase_2/backend/app/services/ — Scoring, interdependências, IA, relatórios",
        "Fase_2/backend/app/utils/ — Auth JWT, decoradores, validadores",
        "Fase_2/backend/seeds/ — Dados iniciais (6 camadas, 23 componentes, 51 indicadores)",
        "Fase_2/frontend/ — HTML pages, CSS design system, JS modules",
    ]
    for d in dirs:
        story.append(Paragraph(f"• {d}", bullet))
    story.append(PageBreak())

    # 3. MODELOS
    story.append(Paragraph("3. Backend — Modelos de Dados", h1))
    story.append(Paragraph("Foram implementados os seguintes modelos SQLAlchemy, correspondentes às 12 tabelas definidas no modelo relacional da Fase 1:", body))

    tabela_data = [
        ["Tabela", "Descrição", "Campos Principais"],
        ["utilizadores", "Utilizadores da plataforma", "nome, email, password_hash, papel"],
        ["organizacoes", "Organizações a avaliar", "nome, setor, dimensao, tipo, pais"],
        ["camadas_ailo", "6 camadas do framework", "nome, descricao, peso, ordem, cor"],
        ["componentes", "23 componentes por camada", "nome, camada_id, peso, ordem"],
        ["indicadores", "51 indicadores de maturidade", "codigo, pergunta, desc_nivel_1/3/5, peso"],
        ["avaliacoes", "Instâncias de avaliação", "organizacao_id, status, score_global, nivel"],
        ["respostas", "Respostas aos indicadores", "avaliacao_id, indicador_id, score, justificacao"],
        ["resultados_camada", "Scores por camada", "score, nivel, pontos_fortes, lacunas, recomendacoes"],
        ["interdependencias", "Relações entre camadas", "camada_a/b, tipo_relacao, impacto"],
        ["ferramentas_ia", "Catálogo de ferramentas IA", "nome, area_funcional, custo, complexidade"],
        ["recomendacoes", "Ferramentas recomendadas", "ferramenta_id, prioridade, justificacao"],
        ["conversas_ia", "Histórico do chat IA", "papel, mensagem, camada_id"],
        ["relatorios", "Relatórios gerados", "titulo, conteudo_json, pdf_path"],
    ]
    t = Table(tabela_data, colWidths=[3.5*cm, 5*cm, 7*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), AILO_DARK), ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTSIZE', (0, 0), (-1, -1), 8), ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, GRAY), ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, LIGHT_BG]),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'), ('TOPPADDING', (0, 0), (-1, -1), 4), ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t)
    story.append(PageBreak())

    # 4. API
    story.append(Paragraph("4. Backend — API RESTful", h1))
    story.append(Paragraph("A API segue a especificação definida na Fase 1, com base URL /api/v1. Todos os endpoints (exceto auth) requerem token JWT no header Authorization.", body))

    endpoints = [
        ["Módulo", "Método", "Endpoint", "Descrição"],
        ["Auth", "POST", "/auth/register", "Registo de utilizador"],
        ["Auth", "POST", "/auth/login", "Login com JWT"],
        ["Auth", "GET", "/auth/me", "Perfil do utilizador autenticado"],
        ["Organizações", "GET/POST", "/organizacoes", "Listar/Criar organizações"],
        ["Organizações", "GET/PUT/DEL", "/organizacoes/:id", "Detalhar/Atualizar/Eliminar"],
        ["AILO", "GET", "/ailo/camadas", "Listar camadas com componentes e indicadores"],
        ["AILO", "GET", "/ailo/camadas/:id/indicadores", "Indicadores de uma camada"],
        ["Avaliações", "POST/GET", "/avaliacoes", "Criar/Listar avaliações"],
        ["Avaliações", "GET", "/avaliacoes/:id", "Detalhar com progresso por camada"],
        ["Avaliações", "POST", "/avaliacoes/:id/finalizar", "Finalizar e calcular scoring"],
        ["Respostas", "POST", "/avaliacoes/:id/respostas", "Guardar resposta individual"],
        ["Respostas", "POST", "/avaliacoes/:id/respostas/batch", "Guardar múltiplas respostas"],
        ["Resultados", "GET", "/avaliacoes/:id/resultados", "Obter scores e interdependências"],
        ["Chat IA", "POST", "/avaliacoes/:id/chat", "Enviar mensagem ao assistente"],
        ["Relatórios", "POST", "/avaliacoes/:id/relatorio", "Gerar relatório"],
    ]
    t2 = Table(endpoints, colWidths=[2.5*cm, 2.5*cm, 5.5*cm, 5*cm])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), AILO_DARK), ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTSIZE', (0, 0), (-1, -1), 8), ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, GRAY), ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, LIGHT_BG]),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'), ('TOPPADDING', (0, 0), (-1, -1), 3), ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t2)
    story.append(PageBreak())

    # 5. SCORING
    story.append(Paragraph("5. Backend — Motor de Scoring", h1))
    story.append(Paragraph("O motor de scoring é o componente central da plataforma, implementado em services/scoring.py. Calcula a maturidade organizacional seguindo a hierarquia:", body))
    story.append(Paragraph("<b>1. Score por Indicador:</b> Valor de 1-5 atribuído pelo avaliador, multiplicado pelo peso do indicador.", bullet))
    story.append(Paragraph("<b>2. Score por Componente:</b> Média ponderada dos scores dos indicadores do componente.", bullet))
    story.append(Paragraph("<b>3. Score por Camada:</b> Média ponderada dos scores dos componentes da camada.", bullet))
    story.append(Paragraph("<b>4. Score Global:</b> Média ponderada dos scores das 6 camadas (pesos: Humana=1.2, Tecnológica=0.8, restantes=1.0).", bullet))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("Classificação de Níveis de Maturidade:", h2))
    niveis = [["Score", "Nível"], ["1.0 - 1.8", "Inicial"], ["1.9 - 2.6", "Em Desenvolvimento"], ["2.7 - 3.4", "Definido"], ["3.5 - 4.2", "Gerido"], ["4.3 - 5.0", "Otimizado"]]
    t3 = Table(niveis, colWidths=[4*cm, 6*cm])
    t3.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), AILO_ACCENT), ('TEXTCOLOR', (0, 0), (-1, 0), WHITE), ('FONTSIZE', (0, 0), (-1, -1), 10), ('GRID', (0, 0), (-1, -1), 0.5, GRAY), ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold')]))
    story.append(t3)
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("Adicionalmente, o serviço interdependencias.py analisa 4 pares críticos de camadas (ex: Humana×Avaliação, Cognitiva×Tecnológica), classificando a relação como fortalece, risco, bloqueia ou oportunidade, com mapeamento aos critérios CR1-CR6.", body))
    story.append(PageBreak())

    # 6. IA
    story.append(Paragraph("6. Backend — Assistente IA (Google Gemini)", h1))
    story.append(Paragraph("O assistente IA está implementado em services/ia_assistant.py e utiliza a API do Google Gemini (modelo gemini-2.0-flash por defeito). Funcionalidades:", body))
    story.append(Paragraph("<b>System prompt AILO:</b> Instruções que contextualizam o modelo como especialista em aprendizagem organizacional e IA.", bullet))
    story.append(Paragraph("<b>Contextualização dinâmica:</b> O prompt inclui informações da organização (setor, dimensão, tipo) e da camada atual do questionário.", bullet))
    story.append(Paragraph("<b>Histórico de conversa:</b> As últimas 10 mensagens são incluídas para manter coerência conversacional.", bullet))
    story.append(Paragraph("<b>Modo offline:</b> Quando não há chave API configurada, o assistente responde com mensagem informativa em vez de erro.", bullet))
    story.append(Paragraph("<b>Persistência:</b> Todas as mensagens são guardadas na tabela conversas_ia para referência futura.", bullet))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("<b>Nota importante:</b> Para ativar o assistente IA completo, é necessário configurar a variável GEMINI_API_KEY no ficheiro .env com uma chave válida da Google AI Platform.", body))
    story.append(PageBreak())

    # 7. FRONTEND
    story.append(Paragraph("7. Frontend — Interface de Utilizador", h1))
    story.append(Paragraph("O frontend foi desenvolvido em HTML5, CSS3 e JavaScript Vanilla, seguindo os wireframes definidos na Fase 1. Utiliza um design system premium com tema escuro.", body))
    story.append(Paragraph("7.1 Design System (main.css)", h2))
    story.append(Paragraph("• Paleta de cores AILO (6 cores por camada + tons escuros premium)", bullet))
    story.append(Paragraph("• Tipografia Inter (Google Fonts) com pesos 300-800", bullet))
    story.append(Paragraph("• Componentes: cards, botões, formulários, tabelas, modais, toasts", bullet))
    story.append(Paragraph("• Glassmorphism na navbar (backdrop-filter blur)", bullet))
    story.append(Paragraph("• Micro-animações (fadeIn, slideIn, pulse, spin)", bullet))
    story.append(Paragraph("• Layout responsivo com breakpoint mobile (768px)", bullet))

    story.append(Paragraph("7.2 Páginas Implementadas", h2))
    pages = [
        ("index.html", "Landing page com hero, features e hexágono AILO"),
        ("login.html", "Formulário de autenticação com validação"),
        ("register.html", "Registo de novos utilizadores"),
        ("dashboard.html", "Painel principal com organizações, avaliações e gráfico radar (Chart.js)"),
        ("organizacoes.html", "CRUD de organizações com modal de criação/edição"),
        ("questionario.html", "Questionário AILO com tabs por camada, seleção 1-5, auto-save, barra de progresso e chat IA lateral"),
        ("resultados.html", "Dashboard de resultados com radar hexagonal, barras por camada, pontos fortes/lacunas/recomendações e tabela de interdependências"),
    ]
    for nome, desc in pages:
        story.append(Paragraph(f"<b>• {nome}</b> — {desc}", bullet))
    story.append(PageBreak())

    # 8. SEED
    story.append(Paragraph("8. Base de Dados — Seed Data", h1))
    story.append(Paragraph("O ficheiro seeds/seed_data.py contém todos os dados iniciais do framework AILO, totalizando:", body))
    story.append(Paragraph("<b>• 6 camadas</b> com nomes em PT/EN, descrições, pesos e cores", bullet))
    story.append(Paragraph("<b>• 23 componentes</b> distribuídos pelas camadas", bullet))
    story.append(Paragraph("<b>• 51 indicadores</b> com código único, pergunta em português, descrições de nível 1/3/5 e pesos", bullet))
    story.append(Paragraph("<b>• 10 ferramentas IA</b> no catálogo inicial (Gemini, ChatGPT, Moodle, etc.)", bullet))
    story.append(Paragraph("O script seed.py popula a base de dados com estes dados. Pode ser executado múltiplas vezes (limpa e re-popula automaticamente).", body))

    # 9. SEGURANÇA
    story.append(Paragraph("9. Segurança e Autenticação", h1))
    story.append(Paragraph("<b>• JWT (JSON Web Tokens):</b> Tokens com expiração de 24 horas, gerados via PyJWT.", bullet))
    story.append(Paragraph("<b>• Bcrypt:</b> Hashing de passwords com 12 rounds de salt.", bullet))
    story.append(Paragraph("<b>• Decoradores:</b> @login_required e @admin_required protegem todas as rotas da API.", bullet))
    story.append(Paragraph("<b>• Validação:</b> Campos obrigatórios, formato de email e sanitização de HTML.", bullet))
    story.append(Paragraph("<b>• CORS:</b> Configurado para aceitar pedidos da origem do frontend.", bullet))
    story.append(Paragraph("<b>• .env:</b> Chaves API e segredos armazenados em variáveis de ambiente, nunca no código.", bullet))

    # 10. TESTES
    story.append(Paragraph("10. Testes e Validação", h1))
    story.append(Paragraph("A validação da Fase 2 incluiu:", body))
    story.append(Paragraph("• Execução do seed.py — 6 camadas, 23 componentes, 51 indicadores criados com sucesso", bullet))
    story.append(Paragraph("• Servidor Flask inicia sem erros em http://localhost:5000", bullet))
    story.append(Paragraph("• Landing page renderiza corretamente com design premium", bullet))
    story.append(Paragraph("• Fluxo de registo e login funcional com persistência JWT", bullet))
    story.append(Paragraph("• CRUD de organizações operacional", bullet))
    story.append(Paragraph("• API RESTful responde corretamente a todos os endpoints", bullet))
    story.append(PageBreak())

    # 11. INSTALAÇÃO
    story.append(Paragraph("11. Instruções de Instalação e Execução", h1))
    story.append(Paragraph("11.1 Pré-requisitos", h2))
    story.append(Paragraph("• Python 3.10+ instalado", bullet))
    story.append(Paragraph("• pip (gestor de pacotes Python)", bullet))
    story.append(Paragraph("11.2 Instalação", h2))
    cmds = [
        "cd Fase_2/backend",
        "python3 -m venv venv",
        "source venv/bin/activate  # Linux/Mac",
        "pip install -r requirements.txt",
        "cp .env.example .env  # Editar com as suas configurações",
        "python seed.py  # Popular a base de dados",
        "python run.py  # Iniciar o servidor",
    ]
    for c in cmds:
        story.append(Paragraph(f"<font face='Courier' size='9'>$ {c}</font>", bullet))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("Após iniciar, aceder a http://localhost:5000 no browser.", body))

    # 12. DEPLOYMENT
    story.append(Paragraph("12. Instruções para Deployment Real", h1))
    story.append(Paragraph("Para colocar a plataforma em produção, são necessárias as seguintes alterações:", body))
    story.append(Paragraph("<b>12.1 Base de Dados — Migrar para PostgreSQL:</b>", h2))
    story.append(Paragraph("• Instalar PostgreSQL e criar base de dados", bullet))
    story.append(Paragraph("• Alterar DATABASE_URL no .env para: postgresql://user:pass@host:5432/ailo_db", bullet))
    story.append(Paragraph("• pip install psycopg2-binary", bullet))
    story.append(Paragraph("<b>12.2 Servidor WSGI — Gunicorn:</b>", h2))
    story.append(Paragraph("• Substituir python run.py por: gunicorn -w 4 -b 0.0.0.0:5000 'app:create_app(\"production\")'", bullet))
    story.append(Paragraph("<b>12.3 Proxy Reverso — Nginx:</b>", h2))
    story.append(Paragraph("• Configurar Nginx para servir ficheiros estáticos (frontend) e proxy para Gunicorn", bullet))
    story.append(Paragraph("• Configurar certificado SSL (Let's Encrypt)", bullet))
    story.append(Paragraph("<b>12.4 Variáveis de Ambiente:</b>", h2))
    story.append(Paragraph("• SECRET_KEY: Gerar chave aleatória forte (ex: python -c \"import secrets; print(secrets.token_hex(32))\")", bullet))
    story.append(Paragraph("• GEMINI_API_KEY: Obter chave em https://aistudio.google.com/apikey", bullet))
    story.append(Paragraph("<b>12.5 Docker (opcional):</b>", h2))
    story.append(Paragraph("• Criar Dockerfile e docker-compose.yml para deployment containerizado", bullet))

    # 13. FUTURO
    story.append(Paragraph("13. Trabalho Futuro", h1))
    story.append(Paragraph("Funcionalidades planeadas para fases seguintes:", body))
    story.append(Paragraph("• Testes unitários e de integração automatizados (pytest)", bullet))
    story.append(Paragraph("• Exportação de relatórios para PDF (WeasyPrint)", bullet))
    story.append(Paragraph("• Dashboard administrativo para gestão de utilizadores", bullet))
    story.append(Paragraph("• Comparação entre avaliações da mesma organização (evolução temporal)", bullet))
    story.append(Paragraph("• Integração com LMS (Moodle) via xAPI/LTI", bullet))
    story.append(Paragraph("• Catálogo expandido de ferramentas IA com filtragem inteligente", bullet))
    story.append(Paragraph("• Benchmarking setorial (comparação entre organizações do mesmo setor)", bullet))
    story.append(Paragraph("• Aplicação mobile (PWA)", bullet))

    story.append(Spacer(1, 2*cm))
    story.append(Paragraph("—— Fim do documento ——", small))
    story.append(Paragraph("Gerado automaticamente pela plataforma AILO · Maio 2026", small))

    doc.build(story)
    print(f"✅ PDF gerado: {os.path.abspath(PDF_PATH)}")

if __name__ == '__main__':
    build_pdf()
