# Especificação da API RESTful

## Base URL
```
http://localhost:5000/api/v1
```

## Autenticação
Todas as rotas (exceto login/registo) requerem JWT token no header:
```
Authorization: Bearer <token>
```

---

## 1. Autenticação

### POST /auth/register
Registar novo utilizador.
```json
// Request
{
    "nome": "Ricardo Costa",
    "email": "ricardo@exemplo.pt",
    "password": "Min8chars!"
}

// Response 201
{
    "id": 1,
    "nome": "Ricardo Costa",
    "email": "ricardo@exemplo.pt",
    "papel": "utilizador",
    "token": "eyJhbGciOiJIUzI1NiIs..."
}
```

### POST /auth/login
```json
// Request
{ "email": "ricardo@exemplo.pt", "password": "Min8chars!" }

// Response 200
{ "token": "eyJhbGciOiJIUzI1NiIs...", "user": { "id": 1, "nome": "Ricardo", "papel": "utilizador" } }
```

### GET /auth/me
Obter perfil do utilizador autenticado.
```json
// Response 200
{ "id": 1, "nome": "Ricardo Costa", "email": "ricardo@exemplo.pt", "papel": "utilizador" }
```

---

## 2. Organizações

### GET /organizacoes
Listar organizações do utilizador.
```json
// Response 200
{
    "data": [
        { "id": 1, "nome": "TechSchool", "setor": "Educação", "dimensao": "media", "tipo": "ensino_superior", "avaliacoes_count": 2 }
    ],
    "total": 1
}
```

### POST /organizacoes
```json
// Request
{
    "nome": "TechSchool",
    "setor": "Educação",
    "dimensao": "media",
    "tipo": "ensino_superior",
    "pais": "Portugal",
    "descricao": "Instituição de ensino superior com 500 alunos"
}

// Response 201
{ "id": 1, "nome": "TechSchool", ... }
```

### GET /organizacoes/:id
### PUT /organizacoes/:id
### DELETE /organizacoes/:id

---

## 3. Framework AILO (Read-only para utilizadores)

### GET /ailo/camadas
Listar as 6 camadas com componentes.
```json
// Response 200
{
    "data": [
        {
            "id": 1,
            "nome": "Organizacional",
            "nome_en": "Organizational",
            "descricao": "Liga a aprendizagem organizacional à estratégia...",
            "peso": 1.0,
            "ordem": 1,
            "cor": "#2E4057",
            "componentes": [
                {
                    "id": 1,
                    "nome": "Estratégia",
                    "indicadores_count": 3
                }
            ]
        }
    ]
}
```

### GET /ailo/camadas/:id/indicadores
Listar indicadores de uma camada (agrupados por componente).
```json
// Response 200
{
    "camada": { "id": 1, "nome": "Organizacional" },
    "componentes": [
        {
            "id": 1,
            "nome": "Estratégia",
            "indicadores": [
                {
                    "id": 1,
                    "codigo": "O.E.1",
                    "pergunta": "Qual o nível de alinhamento entre a estratégia de aprendizagem e os objetivos da organização?",
                    "desc_nivel_1": "Sem ligação formal",
                    "desc_nivel_3": "Plano de formação alinhado com objetivos",
                    "desc_nivel_5": "Aprendizagem integrada no planeamento estratégico",
                    "obrigatorio": true
                }
            ]
        }
    ]
}
```

### GET /ailo/indicadores
Listar todos os 51 indicadores (flat list para administração).

---

## 4. Avaliações

### POST /avaliacoes
Iniciar nova avaliação.
```json
// Request
{ "organizacao_id": 1 }

// Response 201
{
    "id": 1,
    "organizacao_id": 1,
    "status": "em_curso",
    "data_inicio": "2026-04-19T18:00:00Z",
    "progresso": { "total_indicadores": 51, "respondidos": 0, "percentagem": 0 }
}
```

### GET /avaliacoes
Listar avaliações do utilizador.
```json
// Response 200
{
    "data": [
        {
            "id": 1,
            "organizacao": { "id": 1, "nome": "TechSchool" },
            "status": "em_curso",
            "data_inicio": "2026-04-19T18:00:00Z",
            "progresso": { "percentagem": 45 }
        }
    ]
}
```

### GET /avaliacoes/:id
Detalhe de uma avaliação com progresso por camada.
```json
// Response 200
{
    "id": 1,
    "organizacao": { "id": 1, "nome": "TechSchool" },
    "status": "em_curso",
    "progresso_por_camada": [
        { "camada_id": 1, "nome": "Organizacional", "respondidos": 8, "total": 11, "percentagem": 73 },
        { "camada_id": 2, "nome": "Humana", "respondidos": 0, "total": 10, "percentagem": 0 }
    ]
}
```

### POST /avaliacoes/:id/finalizar
Finalizar avaliação e calcular scoring.
```json
// Response 200
{
    "id": 1,
    "status": "completa",
    "score_global": 3.2,
    "nivel_global": "Definido",
    "resultados_por_camada": [ ... ]
}
```

### DELETE /avaliacoes/:id
Cancelar avaliação em curso.

---

## 5. Respostas

### POST /avaliacoes/:id/respostas
Guardar/atualizar resposta a um indicador.
```json
// Request
{
    "indicador_id": 1,
    "score": 3,
    "justificacao": "Temos um plano anual mas falta integração com a estratégia global"
}

// Response 200
{ "id": 1, "indicador_id": 1, "score": 3, "justificacao": "..." }
```

### POST /avaliacoes/:id/respostas/batch
Guardar múltiplas respostas de uma vez (autosave).
```json
// Request
{
    "respostas": [
        { "indicador_id": 1, "score": 3 },
        { "indicador_id": 2, "score": 4 },
        { "indicador_id": 3, "score": 2 }
    ]
}

// Response 200
{ "saved": 3 }
```

### GET /avaliacoes/:id/respostas
Obter todas as respostas de uma avaliação (para retomar).
```json
// Response 200
{
    "data": [
        { "indicador_id": 1, "codigo": "O.E.1", "score": 3, "justificacao": "..." }
    ],
    "total": 15
}
```

---

## 6. Resultados e Scoring

### GET /avaliacoes/:id/resultados
Obter resultados completos (apenas para avaliações completas).
```json
// Response 200
{
    "score_global": 3.2,
    "nivel_global": "Definido",
    "camadas": [
        {
            "camada_id": 1,
            "nome": "Organizacional",
            "score": 3.5,
            "nivel": "Gerido",
            "pontos_fortes": ["Estratégia bem definida", "Processos de KM ativos"],
            "lacunas": ["Falta governação de IA formal"],
            "recomendacoes": ["Implementar framework de governação de IA"],
            "cr_relevantes": ["CR3", "CR5"]
        }
    ],
    "interdependencias": [
        {
            "camada_a": "Humana",
            "camada_b": "Avaliação",
            "tipo": "fortalece",
            "descricao": "Elevada maturidade humana e avaliativa favorece double-loop learning",
            "impacto": "alto"
        }
    ]
}
```

---

## 7. Assistente IA (Chat)

### POST /avaliacoes/:id/chat
Enviar mensagem ao assistente e receber resposta.
```json
// Request
{
    "mensagem": "O que significa mediação cognitiva no contexto do AILO?",
    "camada_id": 4
}

// Response 200
{
    "resposta": "No AILO, mediação cognitiva refere-se ao papel da IA como parceiro cognitivo...",
    "camada_contexto": "Cognitiva (IA)"
}
```

### GET /avaliacoes/:id/chat/historico
Obter histórico de conversa.
```json
// Response 200
{
    "mensagens": [
        { "papel": "user", "mensagem": "O que significa...", "camada_id": 4, "created_at": "..." },
        { "papel": "assistant", "mensagem": "No AILO, mediação...", "camada_id": 4, "created_at": "..." }
    ]
}
```

---

## 8. Relatórios

### POST /avaliacoes/:id/relatorio
Gerar relatório para avaliação completa.
```json
// Response 201
{
    "id": 1,
    "titulo": "Diagnóstico AILO — TechSchool",
    "avaliacao_id": 1,
    "created_at": "2026-04-19T19:00:00Z"
}
```

### GET /relatorios/:id
Obter dados do relatório (para visualização web).

### GET /relatorios/:id/pdf
Download do relatório em PDF.

---

## 9. Recomendações

### GET /avaliacoes/:id/recomendacoes
Obter recomendações de ferramentas IA baseadas no diagnóstico.
```json
// Response 200
{
    "data": [
        {
            "prioridade": 1,
            "ferramenta": { "nome": "Google Gemini", "custo": "freemium", "complexidade": "media" },
            "camada": "Cognitiva (IA)",
            "justificacao": "A organização tem baixa maturidade em IA generativa. O Gemini pode..."
        }
    ]
}
```

---

## Códigos de Erro

| Código | Significado |
|--------|-------------|
| 200 | Sucesso |
| 201 | Criado com sucesso |
| 400 | Dados inválidos (validação falhou) |
| 401 | Não autenticado (token ausente/inválido) |
| 403 | Não autorizado (permissão insuficiente) |
| 404 | Recurso não encontrado |
| 409 | Conflito (ex: email já existe) |
| 500 | Erro interno do servidor |

Formato de erro:
```json
{ "error": "Descrição do erro", "code": 400 }
```
