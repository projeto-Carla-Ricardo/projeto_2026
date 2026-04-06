# Questionário Interativo

## Visão Geral

O questionário é o ponto central de interação do IALO com o utilizador. Consiste em **25 perguntas** distribuídas por **5 dimensões** (5 indicadores por dimensão, 1 pergunta por indicador), com um assistente IA integrado.

## Estrutura do Questionário

```
Framework IALO
├── DADOS (5 indicadores, 5 perguntas)
├── INFRA (5 indicadores, 5 perguntas)
├── COMP  (5 indicadores, 5 perguntas)
├── ESTR  (5 indicadores, 5 perguntas)
└── CULT  (5 indicadores, 5 perguntas)
```

## Interface

### Layout Split-Screen

O questionário utiliza um layout de ecrã dividido:

```
┌─────────────────────────────────┬──────────────────┐
│  Área do Questionário (70%)     │  Chat IA (30%)   │
│                                 │                  │
│  [Tabs de Dimensão]             │  🤖 Assistente   │
│  ┌─────────────────────────┐    │  ┌────────────┐  │
│  │  Pergunta 3 de 25       │    │  │ Mensagens  │  │
│  │                         │    │  │            │  │
│  │  "Como regista as       │    │  │            │  │
│  │   vendas da empresa?"   │    │  │            │  │
│  │                         │    │  └────────────┘  │
│  │  ○ Papel                │    │  ┌────────────┐  │
│  │  ● Excel                │    │  │ Input      │  │
│  │  ○ Software próprio     │    │  └────────────┘  │
│  └─────────────────────────┘    │                  │
│                                 │                  │
│  [Progresso: ████░░ 45%]        │                  │
│  [← Anterior] [Guardar] [→]    │                  │
└─────────────────────────────────┴──────────────────┘
```

### Tipos de Resposta

| Tipo | Componente UI | Exemplo |
|------|--------------|---------|
| `escala_1_5` | 5 botões numéricos | Avaliação 1-5 |
| `escolha_multipla` | Radio buttons | "Papel", "Excel", "Software" |
| `sim_nao` | 2 botões | "Sim" / "Não" |
| `texto_livre` | Textarea | Resposta aberta |

### Navegação

- **Tabs de Dimensão**: Saltar entre dimensões (DADOS, INFRA, COMP, ESTR, CULT)
- **Anterior/Seguinte**: Navegação sequencial entre perguntas
- **Guardar Progresso**: Persistência a qualquer momento
- **Concluir**: Disponível na última pergunta → redireciona para resultados

### Barra de Progresso

A barra de progresso atualiza automaticamente com base no número de respostas:

```
progresso = (respostas_dadas / total_perguntas) × 100%
```

As tabs de dimensão mostram um indicador ✓ quando todas as perguntas dessa dimensão estão respondidas.

## Persistência

### Guardar Respostas

As respostas são enviadas em **batch** para minimizar pedidos:

```json
POST /api/v1/questionario/respostas
{
    "avaliacao_id": 1,
    "respostas": [
        { "pergunta_id": 1, "valor_numerico": 3 },
        { "pergunta_id": 2, "valor_texto": "Excel" }
    ]
}
```

O backend calcula automaticamente o `valor_fuzzy` usando as regras de fuzzy logic.

### Retomar Questionário

O utilizador pode fechar o browser e retomar mais tarde:
1. A `avaliacao_id` é guardada no `localStorage`
2. Ao reabrir, as respostas anteriores são carregadas via API
3. O questionário posiciona-se na primeira pergunta sem resposta

## Fluxo Completo

```
Dashboard → Novo Diagnóstico → Selecionar Empresa
    → Questionário (25 perguntas, 5 dimensões)
        → Guardar progresso (a qualquer momento)
        → Concluir diagnóstico
    → Scoring automático
    → Página de Resultados (radar, barras, recomendações)
```

## Ficheiros

| Ficheiro | Descrição |
|----------|-----------|
| `frontend/pages/questionario.html` | Página do questionário |
| `frontend/css/questionario.css` | Estilos (split-screen, tabs) |
| `frontend/js/questionario.js` | Lógica de navegação, respostas, chat |
| `backend/app/routes/questionario.py` | API de dimensões e respostas |
| `backend/seeds/perguntas.json` | Seed data com 25 perguntas |
