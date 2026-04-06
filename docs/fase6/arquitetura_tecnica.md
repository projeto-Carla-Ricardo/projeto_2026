# Documentação Técnica — Arquitetura e Modelação

## 1. Visão Geral da Arquitetura

O IALO segue uma arquitetura **cliente-servidor** com separação clara entre frontend e backend.

```
┌──────────────────────────────────────────────────────────────┐
│                     FRONTEND (Browser)                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐│
│  │ Landing  │  │ Auth     │  │Dashboard │  │ Questionário ││
│  │ Page     │  │ (Login/  │  │ (CRUD,   │  │ (Perguntas,  ││
│  │          │  │ Register)│  │ Settings)│  │  Chat IA)    ││
│  └──────────┘  └──────────┘  └──────────┘  └──────────────┘│
│                        │ fetch() + JWT                       │
└────────────────────────┼─────────────────────────────────────┘
                         │
                    HTTP REST API
                         │
┌────────────────────────┼─────────────────────────────────────┐
│                     BACKEND (Flask)                           │
│  ┌─────────────────────┼─────────────────────────────────┐   │
│  │              8 Blueprints API                         │   │
│  │  auth │ empresas │ avaliacoes │ questionario          │   │
│  │  scoring │ assistente │ settings │ relatorios         │   │
│  └─────────────────────┼─────────────────────────────────┘   │
│  ┌─────────────────────┼─────────────────────────────────┐   │
│  │           Serviços (Business Logic)                   │   │
│  │  scoring_engine │ ai_assistant │ recommendation_engine│   │
│  │  report_generator │ fuzzy_logic                       │   │
│  └─────────────────────┼─────────────────────────────────┘   │
│  ┌─────────────────────┼─────────────────────────────────┐   │
│  │            12 Modelos SQLAlchemy                       │   │
│  │  Utilizador │ Empresa │ Avaliacao │ Dimensao          │   │
│  │  Indicador │ Pergunta │ Resposta │ ResultadoDimensao   │   │
│  │  Relatorio │ Recomendacao │ FerramentaIA │ Conversa    │   │
│  └─────────────────────┼─────────────────────────────────┘   │
│                        │                                     │
│                   SQLAlchemy ORM                              │
│                        │                                     │
│                ┌───────▼───────┐                             │
│                │   SQLite DB   │                             │
│                └───────────────┘                             │
│                                                              │
│  ┌───────────────────────────────────────────────────────┐   │
│  │              Serviços Externos                        │   │
│  │              Google Gemini API                        │   │
│  └───────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────┘
```

## 2. Stack Tecnológica

### Backend
| Componente | Tecnologia | Versão |
|------------|-----------|--------|
| Framework Web | Flask | 3.x |
| ORM | SQLAlchemy | 2.x |
| Migrações | Flask-Migrate (Alembic) | 4.x |
| Autenticação | Flask-JWT-Extended | 4.x |
| Hashing | Flask-Bcrypt | 1.x |
| Rate Limiting | Flask-Limiter | 3.x |
| IA | Google GenAI SDK | 1.x |
| PDF | WeasyPrint | 62.x |
| Base de Dados | SQLite | Built-in |

### Frontend
| Componente | Tecnologia |
|------------|-----------|
| Estrutura | HTML5 Semântico |
| Estilos | CSS3 (Custom Properties, Grid, Flexbox) |
| Lógica | JavaScript (Vanilla ES6+) |
| Tipografia | Inter (Google Fonts) |
| Gráficos | Canvas API (sem dependências) |

### Testes
| Componente | Tecnologia |
|------------|-----------|
| Framework | pytest |
| Cobertura | pytest-cov |
| BD de teste | SQLite in-memory |

## 3. Modelo de Dados

### Diagrama Entidade-Relação

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Utilizador  │1───N│   Empresa    │1───N│  Avaliação   │
│──────────────│     │──────────────│     │──────────────│
│ id           │     │ id           │     │ id           │
│ nome         │     │ nome         │     │ empresa_id   │
│ email        │     │ setor        │     │ estado       │
│ password_hash│     │ num_colab    │     │ pontuacao    │
│ role         │     │ localizacao  │     │ nivel        │
│ ativo        │     │ utilizador_id│     │ iniciado_em  │
└──────────────┘     └──────────────┘     └──────┬───────┘
                                                  │1
                                                  │
                              ┌────────────────────┤
                              │                    │N
                    ┌─────────▼────────┐  ┌───────▼────────┐
                    │ResultadoDimensao │  │   Resposta     │
                    │──────────────────│  │────────────────│
                    │ avaliacao_id     │  │ avaliacao_id   │
                    │ dimensao_id      │  │ pergunta_id    │
                    │ pontuacao        │  │ valor_texto    │
                    │ nivel            │  │ valor_numerico │
                    │ gap_critico      │  │ valor_fuzzy    │
                    └──────────────────┘  └────────────────┘

┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Dimensão   │1───N│  Indicador   │1───N│   Pergunta   │
│──────────────│     │──────────────│     │──────────────│
│ id           │     │ id           │     │ id           │
│ codigo       │     │ codigo       │     │ texto        │
│ nome         │     │ nome         │     │ tipo_resposta│
│ peso         │     │ dimensao_id  │     │ indicador_id │
│ ordem        │     │ ordem        │     │ opcoes_json  │
└──────────────┘     └──────────────┘     └──────────────┘

┌──────────────┐     ┌──────────────┐
│  Relatório   │     │FerramentaIA  │
│──────────────│     │──────────────│
│ avaliacao_id │     │ id           │
│ conteudo_json│     │ nome         │
│ gerado_em    │     │ categoria    │
└──────────────┘     │ custo        │
                     │ complexidade │
                     └──────────────┘
```

## 4. Padrões de Design

| Padrão | Onde | Descrição |
|--------|------|-----------|
| Factory | `create_app()` | Criação da app com config injetada |
| Blueprint | `routes/` | Organização modular de rotas |
| Repository | `models/` | ORM como camada de acesso a dados |
| Service Layer | `services/` | Lógica de negócio isolada das rotas |
| Strategy | `fuzzy_logic.py` | Diferentes estratégias de conversão |
| Decorator | `auth_helpers.py` | `@jwt_required`, `@admin_required` |

## 5. Fluxo de Dados

```
1. Utilizador responde pergunta
   → Frontend envia POST /questionario/respostas
   → Backend guarda na tabela 'respostas'
   → fuzzy_logic calcula valor fuzzy

2. Utilizador conclui diagnóstico
   → Frontend envia POST /avaliacoes/:id/concluir
   → scoring_engine calcula pontuações por dimensão
   → scoring_engine calcula índice global ponderado
   → scoring_engine identifica gaps críticos
   → Resultados guardados em 'resultados_dimensao'

3. Utilizador visualiza resultados
   → Frontend pede GET /relatorios/:id
   → report_generator agrega scoring + empresa
   → recommendation_engine sugere ferramentas
   → JSON completo devolvido ao frontend
   → Canvas API desenha radar chart
```

## 6. Segurança

| Camada | Implementação |
|--------|--------------|
| Autenticação | JWT (access + refresh tokens) |
| Hashing | bcrypt com salt automático |
| Autorização | Decoradores `@owner_or_admin` |
| Rate Limiting | Flask-Limiter (200 req/hora) |
| Input Validation | Validação server-side em todas as rotas |
| CORS | Flask-CORS configurado |
| API Keys | Mascaramento na BD e resposta |
