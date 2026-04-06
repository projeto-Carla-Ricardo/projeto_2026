# Interface Web — Design e Componentes

## Visão Geral

A interface web do IALO segue um **dark theme premium** com a fonte Inter (Google Fonts). O design system está centralizado em `frontend/css/styles.css` com variáveis CSS.

## Design System

### Paleta de Cores

```css
--color-bg:              #0a0a1a;     /* Fundo principal */
--color-surface:         #12122a;     /* Cards e superfícies */
--color-surface-hover:   #1a1a3e;     /* Hover em superfícies */
--color-border:          #1e1e3f;     /* Borders */
--color-primary-400:     #818cf8;     /* Primary suave */
--color-primary-500:     #6366f1;     /* Primary (Indigo) */
--color-primary-600:     #4f46e5;     /* Primary escuro */
--color-text:            #e2e2f0;     /* Texto principal */
--color-text-secondary:  #a0a0b8;     /* Texto secundário */
--color-text-muted:      #6b6b8a;     /* Texto subtil */
```

### Tipografia

| Elemento | Font | Size | Weight |
|----------|------|------|--------|
| H1 | Inter | 2.5rem | 800 |
| H2 | Inter | 1.5rem | 700 |
| H3 | Inter | 1.1rem | 600 |
| Body | Inter | 1rem | 400 |
| Small | Inter | 0.85rem | 400 |

### Componentes

| Componente | Classe | Variantes |
|-----------|--------|-----------|
| Botão | `.btn` | `--primary`, `--ghost`, `--sm` |
| Card | `.card` | Com `card__title`, `card__meta`, `card__actions` |
| Form Input | `.form-input` | `.form-textarea`, `.form-select` |
| Badge | `.card__badge` | `--done`, `--pending`, `--active` |

## Páginas

### 1. Landing Page (`index.html`)
- Hero section com gradiente
- CTA "Começar Diagnóstico Gratuito"
- Secções: Features, Dimensões, FAQ

### 2. Login (`pages/login.html`)
- Formulário centrado com erro inline
- Link para registo
- Loading state no botão

### 3. Registo (`pages/register.html`)
- Validação de password match
- Auto-login após registo

### 4. Dashboard (`pages/dashboard.html`)
- Sidebar com navegação
- Overview com stats (empresas, avaliações, concluídas, média)
- Secção Empresas (CRUD)
- Secção Avaliações (listar, continuar)
- Secção Definições (API key Gemini, modelo)

### 5. Questionário (`pages/questionario.html`)
- Layout split-screen (pergunta + chat IA)
- Tabs de dimensão com indicador de progresso
- Barra de progresso global
- Navegação anterior/seguinte

### 6. Resultados (`pages/resultados.html`)
- Círculo de pontuação animado (SVG)
- Gráfico radar (Canvas)
- Barras de dimensão animadas
- Pontos fortes vs necessidades (2 colunas)
- Primeiros passos numerados
- Grid de ferramentas recomendadas
- Download PDF

## Responsividade

Todos os layouts utilizam **CSS Grid** e **Flexbox** com media queries:

```css
@media (max-width: 768px) {
    .two-cols { grid-template-columns: 1fr; }
    .score-hero { flex-direction: column; }
}
```

## Acessibilidade

- Labels em todos os inputs
- Contraste AAA no tema escuro
- IDs únicos em elementos interativos
- Estrutura semântica HTML5 (header, nav, main, section)
- Aria labels nos botões de ação

## Ficheiros CSS

| Ficheiro | Escopo |
|----------|--------|
| `css/styles.css` | Design system global (variáveis, reset, componentes base) |
| `css/auth.css` | Login e registo |
| `css/dashboard.css` | Dashboard, sidebar, modals |
| `css/questionario.css` | Questionário, chat, tabs |
| `css/resultados.css` | Resultados, radar, barras, cards |

## Ficheiros JS

| Ficheiro | Escopo |
|----------|--------|
| `js/api.js` | Cliente HTTP base com auth headers |
| `js/app.js` | Landing page interactions |
| `js/auth.js` | Login, registo, JWT storage |
| `js/dashboard.js` | Sidebar, CRUD, settings |
| `js/questionario.js` | Navegação, respostas, chat IA |
| `js/resultados.js` | Radar chart, barras, PDF download |
