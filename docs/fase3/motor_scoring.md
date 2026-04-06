# Motor de Scoring IALO

## Visão Geral

O Motor de Scoring é o "cérebro" do sistema IALO. Calcula a maturidade digital de uma empresa com base nas respostas ao questionário, utilizando **lógica fuzzy** e ponderação por dimensão.

## Arquitetura do Motor

```
┌─────────────────┐     ┌────────────────┐     ┌──────────────────┐
│   Respostas     │────►│  Fuzzy Logic   │────►│  Scoring Engine  │
│  (texto/escala) │     │  (normalizar)  │     │  (calcular)      │
└─────────────────┘     └────────────────┘     └──────────────────┘
                                                       │
                              ┌─────────────────────────┤
                              │                         │
                    ┌─────────▼────────┐    ┌──────────▼──────────┐
                    │   Resultado por   │    │  Resultado Global   │
                    │   Dimensão (5)    │    │  + Gaps Críticos    │
                    └──────────────────┘    └─────────────────────┘
```

## As 5 Dimensões do Framework IALO

| Código | Dimensão | Peso | Descrição |
|--------|----------|------|-----------|
| `DADOS` | Dados | 25% | Recolha, organização e utilização de dados |
| `INFRA` | Infraestrutura | 20% | Equipamento, ferramentas digitais, conectividade |
| `COMP` | Competências | 20% | Literacia digital da equipa |
| `ESTR` | Estratégia | 20% | Visão e plano de digitalização |
| `CULT` | Cultura | 15% | Abertura à inovação e mudança |

## Lógica Fuzzy

O módulo `fuzzy_logic.py` converte respostas qualitativas em valores numéricos (1-5):

```python
FUZZY_RULES = {
    'papel': 1,      # Processos em papel
    'excel': 2,      # Folha de cálculo básica
    'software': 3,   # Software dedicado
    'integrado': 4,  # Sistemas integrados
    'automatico': 5, # Automação completa
}
```

### Tipos de Resposta Suportados

| Tipo | Conversão |
|------|-----------|
| `escala_1_5` | Valor direto (1 a 5) |
| `sim_nao` | Sim=5, Não=1 |
| `escolha_multipla` | Mapeamento fuzzy por opção |
| `texto_livre` | Análise semântica (futuro) |

## Algoritmo de Cálculo

### 1. Pontuação por Indicador
```
pontuacao_indicador = média(respostas do indicador) / 5 × 100
```

### 2. Pontuação por Dimensão
```
pontuacao_dimensao = média(indicadores da dimensão)
```

### 3. Pontuação Global
```
pontuacao_global = Σ (pontuacao_dimensao × peso_dimensao)
```

### 4. Nível de Maturidade

| Nível | Pontuação | Nome |
|-------|-----------|------|
| 1 | 0–20% | Inicial |
| 2 | 21–40% | Básico |
| 3 | 41–60% | Gerido |
| 4 | 61–80% | Otimizado |
| 5 | 81–100% | Inovador |

### 5. Gaps Críticos

Uma dimensão é considerada **gap crítico** quando:
- Pontuação < 40% **ou**
- Diferença > 30% em relação à média global

## Persistência

Os resultados são guardados na tabela `resultados_dimensao`:

```python
class ResultadoDimensao(db.Model):
    avaliacao_id    # FK para avaliação
    dimensao_id     # FK para dimensão
    pontuacao       # Float: 0-100
    nivel           # Int: 1-5
    gap_critico     # Boolean
```

## Ficheiros

| Ficheiro | Descrição |
|----------|-----------|
| `backend/app/services/scoring_engine.py` | Lógica principal de scoring |
| `backend/app/utils/fuzzy_logic.py` | Conversão fuzzy de respostas |
| `backend/app/routes/scoring.py` | Rota API de scoring |
| `backend/app/models/resultado.py` | Modelo de resultado por dimensão |
