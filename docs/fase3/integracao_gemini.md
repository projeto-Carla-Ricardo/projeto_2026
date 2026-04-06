# Integração com API Gemini (Assistente IA)

## Visão Geral

O IALO integra o **Google Gemini** como assistente IA conversacional durante o questionário de diagnóstico. O assistente utiliza o modelo `gemini-3.1-flash-lite-preview` e é capaz de explicar conceitos técnicos, ajudar o utilizador a responder e detetar inconsistências.

## Configuração

### SDK Utilizado

```
google-genai >= 1.0.0
```

O SDK `google-genai` (novo SDK unificado da Google) é utilizado em vez do antigo `google-generativeai`.

### Configuração de API Key

A API Key pode ser configurada de duas formas:

1. **Variável de ambiente** (`.env`):
   ```
   GEMINI_API_KEY=AIza...
   GEMINI_MODEL=gemini-3.1-flash-lite-preview
   ```

2. **Dashboard de Definições** (runtime):
   - Rota: `PUT /api/v1/settings/ai`
   - O admin pode definir a key e o modelo via interface web
   - A chave é armazenada mascarada na BD (`AIza***...***xyz`)

### Modelos Disponíveis

| Modelo | Descrição |
|--------|-----------|
| `gemini-3.1-flash-lite-preview` | **Recomendado** — Rápido e económico |
| `gemini-2.0-flash` | Alternativa mais capaz |
| `gemini-2.0-flash-lite` | Alternativa leve |
| `gemini-1.5-flash` | Modelo estável anterior |

## System Prompt

O assistente usa um system prompt especializado que define:

- **Papel**: Consultor de transformação digital para PME portuguesas
- **Contexto**: Framework IALO e as 5 dimensões de maturidade
- **Tom**: Acessível, sem jargão técnico excessivo
- **Capacidades**: Explicar conceitos, sugerir respostas, detetar contradições

## Arquitetura

```
┌──────────┐   POST /assistente/mensagem   ┌──────────┐   SDK   ┌───────────┐
│ Frontend │ ──────────────────────────►   │ Backend  │ ──────► │  Gemini   │
│ (Chat)   │   { mensagem, contexto }      │ (Flask)  │        │  API      │
└──────────┘                               └──────────┘        └───────────┘
     ▲                                          │
     └──── { resposta } ◄──────────────────────┘
```

### Gestão de Contexto

- Cada sessão de avaliação tem o seu próprio histórico de conversação
- O histórico é mantido em memória durante a sessão
- O contexto inclui a pergunta atual do questionário para respostas relevantes

## Rota API

### `POST /api/v1/assistente/mensagem`

**Body:**
```json
{
    "avaliacao_id": 1,
    "mensagem": "O que significa maturidade digital?",
    "pergunta_atual_id": 5
}
```

**Resposta:**
```json
{
    "status": "success",
    "data": {
        "resposta": "A maturidade digital refere-se ao grau de preparação..."
    }
}
```

## Teste de Conexão

### `POST /api/v1/settings/ai/test`

Testa a conexão com a API Gemini sem enviar dados sensíveis.

## Ficheiros

| Ficheiro | Descrição |
|----------|-----------|
| `backend/app/services/ai_assistant.py` | Serviço de integração com Gemini |
| `backend/app/routes/assistente.py` | Rotas do assistente IA |
| `backend/app/routes/settings.py` | Configuração de API key e modelo |
| `frontend/js/questionario.js` | Interface de chat no frontend |
