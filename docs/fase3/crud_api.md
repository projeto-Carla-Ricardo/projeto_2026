# API CRUD — Empresas, Avaliações e Respostas

## Visão Geral

A API REST do IALO segue o padrão RESTful com autenticação JWT. Todas as rotas estão versionadas sob `/api/v1/`.

## Blueprints Registados (Fase 3)

| Blueprint | Prefixo | Descrição |
|-----------|---------|-----------|
| `auth_bp` | `/api/v1/auth` | Registo, login, refresh |
| `empresas_bp` | `/api/v1/empresas` | CRUD de empresas |
| `avaliacoes_bp` | `/api/v1/avaliacoes` | CRUD de avaliações/diagnósticos |
| `questionario_bp` | `/api/v1/questionario` | Dimensões, perguntas, respostas |
| `scoring_bp` | `/api/v1/scoring` | Cálculo de scoring |
| `assistente_bp` | `/api/v1/assistente` | Chat IA (Gemini) |
| `settings_bp` | `/api/v1/settings` | Configurações do sistema |

## Rotas de Empresas

| Método | Rota | Descrição | Auth |
|--------|------|-----------|------|
| `GET` | `/api/v1/empresas` | Listar empresas do utilizador | JWT |
| `POST` | `/api/v1/empresas` | Criar nova empresa | JWT |
| `GET` | `/api/v1/empresas/:id` | Detalhes de uma empresa | JWT + Owner |
| `PUT` | `/api/v1/empresas/:id` | Atualizar empresa | JWT + Owner |
| `DELETE` | `/api/v1/empresas/:id` | Eliminar empresa (soft delete) | JWT + Owner |

### Campos de Empresa

```json
{
    "nome": "Café Central",
    "setor": "Alimentar",
    "num_colaboradores": 5,
    "localizacao": "Porto",
    "descricao": "Café tradicional com 20 anos"
}
```

## Rotas de Avaliações

| Método | Rota | Descrição | Auth |
|--------|------|-----------|------|
| `GET` | `/api/v1/avaliacoes` | Listar avaliações | JWT |
| `POST` | `/api/v1/avaliacoes` | Criar nova avaliação | JWT |
| `GET` | `/api/v1/avaliacoes/:id` | Detalhes de uma avaliação | JWT + Owner |
| `POST` | `/api/v1/avaliacoes/:id/concluir` | Concluir e calcular scoring | JWT + Owner |

### Estados de Avaliação

```
pendente → em_curso → concluida
```

## Rotas do Questionário

| Método | Rota | Descrição | Auth |
|--------|------|-----------|------|
| `GET` | `/api/v1/questionario/dimensoes` | Listar dimensões com indicadores e perguntas | JWT |
| `GET` | `/api/v1/questionario/respostas/:avaliacao_id` | Obter respostas existentes | JWT |
| `POST` | `/api/v1/questionario/respostas` | Guardar/atualizar respostas em batch | JWT |

### Estrutura de Resposta

```json
{
    "avaliacao_id": 1,
    "respostas": [
        { "pergunta_id": 1, "valor_numerico": 3 },
        { "pergunta_id": 2, "valor_texto": "Excel", "valor_numerico": 2 }
    ]
}
```

## Padrão de Resposta da API

### Sucesso
```json
{
    "status": "success",
    "data": { ... },
    "message": "Operação concluída"
}
```

### Erro
```json
{
    "status": "error",
    "error": {
        "code": "NOT_FOUND",
        "message": "Recurso não encontrado"
    }
}
```

## Ficheiros Relevantes

| Ficheiro | Descrição |
|----------|-----------|
| `backend/app/routes/empresas.py` | CRUD de empresas |
| `backend/app/routes/avaliacoes.py` | CRUD de avaliações |
| `backend/app/routes/questionario.py` | Gestão de respostas |
| `backend/app/routes/__init__.py` | Registo de blueprints |
