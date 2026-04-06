# Sistema de Relatórios

## Visão Geral

O sistema de relatórios do IALO gera documentos de diagnóstico completos, tanto para visualização interativa na web como para exportação em PDF. Cada relatório é gerado automaticamente a partir dos resultados do scoring.

## Estrutura do Relatório

Um relatório completo contém:

1. **Dados da Empresa** — Nome, setor, colaboradores, localização
2. **Resultado Global** — Pontuação (0-100%) e nível de maturidade (1-5)
3. **Resultados por Dimensão** — Pontuação e nível em cada uma das 5 dimensões
4. **Pontos Fortes** — Dimensões com pontuação ≥ 60%
5. **Necessidades Críticas** — Dimensões com pontuação < 60%
6. **Primeiros Passos** — Top 3 ações prioritárias concretas
7. **Recomendações** — Ferramentas IA sugeridas por dimensão

## Pipeline de Geração

```
┌──────────┐     ┌──────────────┐     ┌────────────────┐     ┌──────────┐
│ Respostas│────►│ Scoring      │────►│ Report         │────►│ Relatório│
│ (batch)  │     │ Engine       │     │ Generator      │     │ (JSON)   │
└──────────┘     └──────────────┘     └────────────────┘     └──────────┘
                                             │                      │
                                    ┌────────▼────────┐    ┌───────▼───────┐
                                    │ Recommendation  │    │  PDF (HTML    │
                                    │ Engine          │    │  → WeasyPrint)│
                                    └─────────────────┘    └───────────────┘
```

## API de Relatórios

| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/api/v1/relatorios/:avaliacao_id` | Relatório completo (JSON) |
| `GET` | `/api/v1/relatorios/:avaliacao_id/recomendacoes` | Recomendações IA |
| `GET` | `/api/v1/relatorios/:avaliacao_id/pdf` | Download PDF |

### Resposta JSON

```json
{
    "titulo": "Diagnóstico de Maturidade Digital — Café Central",
    "resumo": {
        "pontuacao_global": 62,
        "nivel_global": 4,
        "nivel_descricao": "Otimizado",
        "gaps_criticos": 1
    },
    "dimensoes": [...],
    "pontos_fortes": [...],
    "necessidades": [...],
    "primeiros_passos": [...],
    "recomendacoes": [...],
    "radar_data": {
        "labels": ["Dados", "Infraestrutura", "Competências", "Estratégia", "Cultura"],
        "values": [72, 45, 68, 55, 80]
    }
}
```

## Geração de PDF

O PDF é gerado usando **WeasyPrint**, convertendo HTML formatado em PDF:

1. O `report_generator.py` gera os dados estruturados
2. A rota `/pdf` chama `_render_pdf_html(data)` para criar HTML com CSS inline
3. O WeasyPrint converte o HTML em PDF

### Template PDF

O template inclui:
- Cabeçalho com logo e nome da empresa
- Secção de resultado global (pontuação grande)
- Barras de progresso por dimensão
- Listagens de pontos fortes e necessidades
- Passos recomendados numerados
- Rodapé institucional (Framework IALO, Universidade Aberta)

## Persistência

Os relatórios gerados são guardados na tabela `relatorios`:

```python
class Relatorio(db.Model):
    avaliacao_id    # FK (unique)
    conteudo_json   # JSON do relatório completo
    pontos_fortes   # Texto resumo
    necessidades    # Texto resumo
    gerado_em       # Data de geração
```

## Ficheiros

| Ficheiro | Descrição |
|----------|-----------|
| `backend/app/services/report_generator.py` | Geração de dados estruturados |
| `backend/app/routes/relatorios.py` | Rotas API (JSON + PDF) |
| `backend/app/models/relatorio.py` | Modelo ORM |
| `frontend/pages/resultados.html` | Página de visualização |
| `frontend/js/resultados.js` | Renderização web com radar chart |
