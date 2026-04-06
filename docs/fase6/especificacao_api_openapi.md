# Especificação OpenAPI — API IALO v1

## Visão Geral

A API do IALO segue o padrão REST com autenticação JWT. Todos os endpoints estão sob `/api/v1/`.

## Base URL

```
http://localhost:5000/api/v1
```

## Autenticação

Todas as rotas (exceto `/auth/*`) requerem o header:

```
Authorization: Bearer <access_token>
```

---

## Endpoints

### Saúde

#### `GET /health`
Verifica se a API está operacional.

**Resposta 200:**
```json
{ "status": "ok", "message": "IALO API operacional" }
```

---

### Autenticação (`/auth`)

#### `POST /auth/register`
Criar nova conta.

**Body:**
```json
{
    "nome": "string (required)",
    "email": "string (required, unique)",
    "password": "string (required, min 8 chars)"
}
```

**201:** `{ "status": "success", "data": { "id", "nome", "email", "role" } }`
**400:** Email duplicado ou campos em falta

#### `POST /auth/login`
Autenticação.

**Body:**
```json
{
    "email": "string (required)",
    "password": "string (required)"
}
```

**200:** `{ "status": "success", "data": { "token", "refresh_token", "user" } }`
**401:** Credenciais inválidas

#### `POST /auth/refresh`
Renovar access token.

**Headers:** `Authorization: Bearer <refresh_token>`
**200:** `{ "data": { "token": "novo_access_token" } }`

---

### Empresas (`/empresas`)

#### `GET /empresas`
Listar empresas do utilizador autenticado.

**200:** `{ "status": "success", "data": [{ "id", "nome", "setor", ... }] }`

#### `POST /empresas`
Criar empresa.

**Body:**
```json
{
    "nome": "string (required)",
    "setor": "string (required)",
    "num_colaboradores": "integer (optional)",
    "localizacao": "string (optional)",
    "descricao": "string (optional)"
}
```

**201:** `{ "status": "success", "data": { empresa } }`

#### `GET /empresas/:id`
Detalhes de uma empresa. Requer ownership.

#### `PUT /empresas/:id`
Atualizar empresa. Requer ownership.

#### `DELETE /empresas/:id`
Eliminar empresa (soft delete). Requer ownership.

---

### Avaliações (`/avaliacoes`)

#### `GET /avaliacoes`
Listar avaliações do utilizador.

#### `POST /avaliacoes`
Criar nova avaliação.

**Body:**
```json
{ "empresa_id": "integer (required)" }
```

**201:** `{ "data": { "id", "empresa_id", "estado": "em_curso" } }`

#### `GET /avaliacoes/:id`
Detalhes de uma avaliação.

#### `POST /avaliacoes/:id/concluir`
Concluir avaliação e calcular scoring.

**200:** `{ "data": { "pontuacao_global", "nivel_global", "dimensoes", ... } }`

---

### Questionário (`/questionario`)

#### `GET /questionario/dimensoes`
Listar dimensões com indicadores e perguntas.

**200:**
```json
{
    "data": [
        {
            "id": 1, "codigo": "DADOS", "nome": "Dados",
            "indicadores": [
                {
                    "id": 1, "codigo": "DADOS1",
                    "perguntas": [
                        { "id": 1, "texto": "...", "tipo_resposta": "escala_1_5" }
                    ]
                }
            ]
        }
    ]
}
```

#### `GET /questionario/respostas/:avaliacao_id`
Obter respostas existentes de uma avaliação.

#### `POST /questionario/respostas`
Guardar/atualizar respostas em batch.

**Body:**
```json
{
    "avaliacao_id": 1,
    "respostas": [
        { "pergunta_id": 1, "valor_numerico": 3 },
        { "pergunta_id": 2, "valor_texto": "Excel" }
    ]
}
```

---

### Scoring (`/scoring`)

#### `GET /scoring/:avaliacao_id`
Calcular e obter scoring de uma avaliação.

---

### Relatórios (`/relatorios`)

#### `GET /relatorios/:avaliacao_id`
Gerar e obter relatório completo.

**200:**
```json
{
    "data": {
        "titulo": "string",
        "empresa": { ... },
        "resumo": { "pontuacao_global", "nivel_global", "nivel_descricao" },
        "dimensoes": [ ... ],
        "pontos_fortes": [ ... ],
        "necessidades": [ ... ],
        "primeiros_passos": [ ... ],
        "recomendacoes": [ ... ],
        "radar_data": { "labels": [], "values": [] }
    }
}
```

#### `GET /relatorios/:avaliacao_id/recomendacoes`
Obter recomendações de ferramentas IA.

#### `GET /relatorios/:avaliacao_id/pdf`
Descarregar relatório em PDF.

**200:** Content-Type: `application/pdf`

---

### Assistente IA (`/assistente`)

#### `POST /assistente/mensagem`
Enviar mensagem ao assistente.

**Body:**
```json
{
    "avaliacao_id": 1,
    "mensagem": "O que significa maturidade digital?",
    "pergunta_atual_id": 5
}
```

**200:** `{ "data": { "resposta": "string" } }`

---

### Definições (`/settings`)

#### `GET /settings/ai`
Obter configuração IA atual. **Requer role admin.**

#### `PUT /settings/ai`
Atualizar configuração IA.

**Body:**
```json
{
    "api_key": "string (optional)",
    "model": "string (optional)"
}
```

#### `POST /settings/ai/test`
Testar conexão com API Gemini.

---

## Códigos de Erro

| Código | Significado |
|--------|-----------|
| 200 | Sucesso |
| 201 | Criado |
| 400 | Pedido inválido |
| 401 | Não autenticado |
| 403 | Sem permissão |
| 404 | Não encontrado |
| 422 | Erro de validação |
| 429 | Rate limit excedido |
| 500 | Erro interno |
