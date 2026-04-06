# Motor de Recomendação de Ferramentas IA

## Visão Geral

O motor de recomendação sugere **ferramentas de IA** personalizadas para cada empresa, cruzando os resultados do diagnóstico com o catálogo de ferramentas IA presente na base de dados.

## Catálogo de Ferramentas

A BD contém **15 ferramentas IA** pré-catalogadas no seed (`seeds/ferramentas_ia.json`), organizadas por:

| Campo | Descrição | Exemplos |
|-------|-----------|----------|
| `nome` | Nome da ferramenta | "ChatGPT", "Canva IA" |
| `categoria` | Área funcional | dados, gestao, marketing, atendimento, operacoes, automacao |
| `custo` | Modelo de preço | Gratuito, Freemium, Pago (baixo custo), Pago |
| `complexidade` | Dificuldade de adoção | Básica, Intermédia, Avançada |
| `url` | Link oficial | https://... |
| `setores_alvo` | Setores recomendados | JSON array |

## Algoritmo de Matching

### 1. Mapeamento Dimensão → Categorias

Cada dimensão IALO está associada a categorias de ferramentas:

```python
DIMENSAO_CATEGORIAS = {
    'DADOS': ['dados', 'gestao', 'automacao'],
    'INFRA': ['operacoes', 'automacao', 'gestao'],
    'COMP':  ['marketing', 'atendimento', 'gestao'],
    'ESTR':  ['gestao', 'dados', 'operacoes'],
    'CULT':  ['atendimento', 'marketing', 'automacao'],
}
```

### 2. Score de Relevância

Para cada par (ferramenta, dimensão), é calculado um score:

| Critério | Pontos |
|----------|--------|
| Categoria corresponde à dimensão | +5 |
| Custo adequado ao perfil da empresa | +2 |
| Complexidade compatível com o nível | +1 |
| **Mínimo para recomendação** | **≥ 3** |

### 3. Ajuste por Perfil da Empresa

O custo recomendado varia com o número de colaboradores:

| Colaboradores | Custos Aceites |
|---------------|----------------|
| ≤ 5 | Gratuito, Freemium |
| 6–20 | Gratuito, Freemium, Pago (baixo custo) |
| > 20 | Todos |

A complexidade máxima varia com o nível de maturidade:

| Nível | Complexidade Máxima |
|-------|-------------------|
| 1–2 | Básica |
| 3–4 | Intermédia |
| 5 | Avançada |

### 4. Prioridade

As recomendações são priorizadas:

| Prioridade | Critério |
|------------|----------|
| 🔴 Alta | Dimensão com gap crítico |
| 🟡 Média | Dimensão com pontuação < 60% |
| 🟢 Baixa | Dimensão com pontuação ≥ 60% |

## Ações Sugeridas

Para cada dimensão e nível, existe uma **ação concreta sugerida**:

```python
'DADOS': {
    1: 'Começar por registar vendas e clientes numa folha de cálculo.',
    2: 'Organizar os dados existentes com categorias.',
    3: 'Implementar um CRM simples ou ERP leve.',
    4: 'Automatizar recolha de dados e criar dashboards.',
    5: 'Explorar analytics avançado e modelos preditivos.',
}
```

## Output

O motor retorna uma lista por dimensão, cada uma com:

```json
{
    "dimensao": "Dados",
    "codigo": "DADOS",
    "pontuacao": 45,
    "prioridade": "alta",
    "acao_sugerida": "Organizar dados com categorias...",
    "ferramentas": [
        {
            "ferramenta": { "nome": "Google Sheets", "custo": "Gratuito", ... },
            "score_relevancia": 8,
            "razao": "A dimensão 'Dados' é um gap crítico (45%)..."
        }
    ]
}
```

## Ficheiros

| Ficheiro | Descrição |
|----------|-----------|
| `backend/app/services/recommendation_engine.py` | Lógica de matching |
| `backend/app/routes/relatorios.py` | Rota `/recomendacoes` |
| `backend/app/models/ferramenta.py` | Modelo de ferramenta IA |
| `backend/seeds/ferramentas_ia.json` | Catálogo seed (15 ferramentas) |
