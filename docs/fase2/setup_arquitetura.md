# Fase 2 — Setup e Arquitetura
## Ambiente Web para Framework IALO

**Projeto**: Ambiente Web para Framework IALO  
**Fase**: 2 — Setup e Arquitetura  
**Data**: 26/03/2026  

---

## 1. Stack Tecnológica Implementada

| Camada | Tecnologia | Versão |
|--------|-----------|--------|
| **Backend** | Python + Flask | Python 3.12, Flask 3.1.3 |
| **ORM** | SQLAlchemy + Flask-Migrate | SQLAlchemy 2.0.48, Alembic 1.18.4 |
| **Base de Dados** | SQLite (dev) | Migrável para PostgreSQL via SQLAlchemy |
| **Autenticação** | flask-jwt-extended | JWT com access + refresh tokens |
| **CORS** | flask-cors | Configurado para cross-origin |
| **Rate Limiting** | flask-limiter | 200 req/hora por defeito |
| **Frontend** | HTML5 + CSS3 + JavaScript (Vanilla) | Sem frameworks, design system customizado |
| **Tipografia** | Google Fonts (Inter) | Peso 300-800 |

---

## 2. Estrutura de Pastas Criada

```
Projeto/
├── .gitignore
├── README.md
├── docs/
│   ├── fase1/                          # 6 documentos (completo)
│   └── fase2/
│       └── setup_arquitetura.md        # Este documento
│
├── backend/
│   ├── app/
│   │   ├── __init__.py                 # Factory Flask + extensões
│   │   ├── config.py                   # Dev/Test/Prod configs
│   │   ├── models/                     # 12 modelos SQLAlchemy
│   │   │   ├── utilizador.py
│   │   │   ├── empresa.py
│   │   │   ├── avaliacao.py
│   │   │   ├── dimensao.py
│   │   │   ├── indicador.py
│   │   │   ├── pergunta.py
│   │   │   ├── resposta.py
│   │   │   ├── resultado.py
│   │   │   ├── relatorio.py
│   │   │   ├── ferramenta.py
│   │   │   ├── recomendacao.py
│   │   │   └── conversa.py
│   │   ├── routes/                     # Blueprints (Fase 3)
│   │   ├── services/                   # Lógica de negócio (Fase 3)
│   │   ├── utils/                      # Utilitários
│   │   └── templates/                  # Templates PDF (Fase 4)
│   ├── migrations/                     # Alembic migrations
│   ├── seeds/                          # Dados iniciais JSON
│   │   ├── dimensoes.json              # 5 dimensões IALO
│   │   ├── indicadores.json            # 25 indicadores
│   │   ├── perguntas.json              # 25 perguntas
│   │   └── ferramentas_ia.json         # 15 ferramentas IA
│   ├── seed.py                         # Script de seed
│   ├── run.py                          # Entry point
│   ├── requirements.txt               # Dependências Python
│   ├── .env.example                    # Template de variáveis
│   └── venv/                           # Ambiente virtual
│
└── frontend/
    ├── index.html                      # Landing page
    ├── css/
    │   └── styles.css                  # Design system completo
    ├── js/
    │   ├── app.js                      # Inicialização + animações
    │   └── api.js                      # Cliente API com JWT
    └── pages/                          # (Fase 3/4)
```

---

## 3. Base de Dados — 12 Tabelas

| Tabela | Registos (seed) | Descrição |
|--------|-----------------|-----------|
| utilizadores | 0 | Utilizadores do sistema |
| empresas | 0 | Perfis de empresas |
| avaliacoes | 0 | Sessões de diagnóstico |
| dimensoes | **5** | Dimensões IALO (referência) |
| indicadores | **25** | Indicadores por dimensão |
| perguntas | **25** | Questionário IALO |
| respostas | 0 | Respostas dos utilizadores |
| resultados_dimensao | 0 | Scoring por dimensão |
| relatorios | 0 | Relatórios gerados |
| ferramentas_ia | **15** | Catálogo de ferramentas IA |
| recomendacoes | 0 | Recomendações em relatórios |
| conversas_ia | 0 | Histórico do assistente IA |

---

## 4. Como Executar

```bash
# 1. Entrar na pasta do backend
cd backend

# 2. Ativar ambiente virtual
source venv/bin/activate

# 3. Copiar variáveis de ambiente
cp .env.example .env

# 4. Aplicar migrations
flask db upgrade

# 5. Popular base de dados
python seed.py

# 6. Arrancar servidor
python run.py
# → http://localhost:5000

# 7. Testar health check
curl http://localhost:5000/api/v1/health
```

---

## 5. Próximos Passos (Fase 3)

A Fase 3 implementará a lógica funcional core:
- **3.1** Backend CRUD + Autenticação (rotas, blueprints)
- **3.2** Motor de Scoring (o "cérebro" IALO)
- **3.3** Integração com LLM (assistente IA)
- **3.4** Questionário Interativo (frontend)
