# Dashboards e Visualizações

## Visão Geral

A Fase 4 implementa visualizações ricas para apresentar os resultados do diagnóstico de forma intuitiva e visualmente apelativa, incluindo gráficos radar, barras de progresso e indicadores visuais.

## Gráfico Radar (Spider Chart)

### Implementação

O gráfico radar é implementado em **Canvas puro** (sem bibliotecas externas como Chart.js), para minimizar dependências:

```javascript
function drawRadarChart(radarData) {
    const canvas = document.getElementById('radar-chart');
    const ctx = canvas.getContext('2d');
    // ... desenho programático com Canvas 2D API
}
```

### Estrutura Visual

```
            Dados (72%)
              ╱╲
             ╱  ╲
    Cultura ╱    ╲ Infraestrutura
    (80%) ╱  ████ ╲ (45%)
          ╲  ████ ╱
           ╲    ╱
    Estratégia ╲╱ Competências
    (55%)        (68%)
```

### Componentes do Radar

1. **Grelha** — 5 níveis concêntricos (20%, 40%, 60%, 80%, 100%)
2. **Eixos** — 5 linhas radiais, uma por dimensão
3. **Polígono de dados** — Preenchido com cor semi-transparente
4. **Pontos** — Círculos nos vértices dos dados
5. **Labels** — Nome da dimensão + pontuação junto a cada eixo
6. **Escala** — Percentagens no eixo vertical

### Cores

| Elemento | Cor |
|----------|-----|
| Grelha | `rgba(99, 102, 241, 0.12)` |
| Eixos | `rgba(99, 102, 241, 0.3)` |
| Área preenchida | `rgba(99, 102, 241, 0.15)` |
| Contorno dados | `rgba(99, 102, 241, 0.8)` |
| Pontos | `#6366f1` (Indigo) |

## Barras de Progresso por Dimensão

Barras horizontais animadas com gradientes de cor:

| Pontuação | Classe | Gradiente |
|-----------|--------|-----------|
| ≥ 60% | `dim-bar-fill--high` | Verde (#22c55e → #16a34a) |
| 40–59% | `dim-bar-fill--medium` | Âmbar (#f59e0b → #d97706) |
| < 40% | `dim-bar-fill--low` | Vermelho (#ef4444 → #dc2626) |

### Animação

As barras iniciam com `width: 0%` e expandem para o valor alvo com transição CSS de 1 segundo:

```css
.dim-bar-fill { transition: width 1s ease; }
```

## Círculo de Pontuação Global

SVG animado que renderiza um arco circular proporcional à pontuação:

```svg
<circle cx="100" cy="100" r="85" 
        stroke-dasharray="534" 
        stroke-dashoffset="534→offset" />
```

A animação usa `stroke-dashoffset` com transição de 1.5 segundos.

## Badges e Indicadores

| Badge | Significado | Cor |
|-------|------------|-----|
| `GAP` | Dimensão com gap crítico | Vermelho |
| `OK` | Dimensão acima do limiar | Verde |

## Cards de Recomendação

Grid responsivo de cards com:
- Nome da ferramenta
- Custo (badge verde)
- Descrição curta
- Razão da recomendação (itálico)
- Dimensão associada (badge indigo)

Efeito hover: `border-color` + `translateY(-2px)`.

## Responsividade

| Viewport | Layout |
|----------|--------|
| Desktop (>768px) | 2 colunas para fortes/necessidades, radar completo |
| Tablet/Mobile (<768px) | 1 coluna, score hero empilhado |

## Ficheiros

| Ficheiro | Descrição |
|----------|-----------|
| `frontend/pages/resultados.html` | Página de resultados |
| `frontend/css/resultados.css` | Estilos responsivos |
| `frontend/js/resultados.js` | Radar chart, barras, animações |
