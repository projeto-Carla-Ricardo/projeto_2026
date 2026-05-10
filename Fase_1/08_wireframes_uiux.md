# Wireframes e Prototipagem UI/UX

## 1. Mapa de Navegação

```
                            ┌──────────────┐
                            │ Landing Page │
                            └──────┬───────┘
                                   │
                          ┌────────┴────────┐
                          ▼                 ▼
                   ┌──────────┐      ┌──────────┐
                   │  Login   │      │ Registo  │
                   └────┬─────┘      └────┬─────┘
                        │                 │
                        └────────┬────────┘
                                 ▼
                        ┌────────────────┐
                        │   Dashboard    │
                        │   Principal    │
                        └───────┬────────┘
                                │
              ┌─────────┬───────┼───────┬──────────┐
              ▼         ▼       ▼       ▼          ▼
        ┌──────────┐ ┌─────┐ ┌──────┐ ┌─────┐ ┌──────┐
        │Organizaç.│ │Nova │ │Histór│ │Perfil│ │Admin │
        │ Lista    │ │Aval.│ │ico   │ │      │ │Panel │
        └────┬─────┘ └──┬──┘ └──┬───┘ └──────┘ └──────┘
             │          │       │
             │          ▼       │
             │   ┌─────────────────────────────────┐
             │   │       QUESTIONÁRIO AILO          │
             │   │                                  │
             │   │  Tab 1: Organizacional           │
             │   │  Tab 2: Humana                   │
             │   │  Tab 3: Aprendizagem             │
             │   │  Tab 4: Cognitiva (IA)           │
             │   │  Tab 5: Tecnológica              │
             │   │  Tab 6: Avaliação                │
             │   │                   ┌────────────┐ │
             │   │                   │  Chat IA   │ │
             │   │                   │  Lateral   │ │
             │   │                   └────────────┘ │
             │   └────────────┬────────────────────┘
             │                │
             │                ▼
             │   ┌─────────────────────────────────┐
             │   │       RESULTADOS                 │
             │   │                                  │
             │   │  ┌──────────┐ ┌──────────────┐  │
             │   │  │Dashboard │ │ Relatório    │  │
             │   │  │Hexagonal │ │ Detalhado    │  │
             │   │  └──────────┘ └──────────────┘  │
             │   │  ┌──────────┐ ┌──────────────┐  │
             │   │  │Interdep. │ │ Recomendações│  │
             │   │  └──────────┘ └──────────────┘  │
             │   │              ┌──────────────┐   │
             │   │              │  PDF Export   │   │
             │   │              └──────────────┘   │
             │   └─────────────────────────────────┘
             │
             └──────▶ Comparação temporal
```

---

## 2. Wireframes Detalhados

### 2.1. Landing Page

```
┌────────────────────────────────────────────────────────────────────────┐
│  🔷 AILO Platform                                  [Login] [Registar] │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│              Avalie a maturidade da sua organização                    │
│              com o Framework AILO                                      │
│                                                                        │
│     A IA como mediador cognitivo nas Organizações Aprendentes         │
│                                                                        │
│                    [ Começar Avaliação →  ]                            │
│                                                                        │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│   ┌────────────┐    ┌────────────┐    ┌────────────┐                  │
│   │ 🏢         │    │ 🤖         │    │ 📊         │                  │
│   │ 6 Camadas  │    │ Assistente │    │ Relatórios │                  │
│   │ AILO       │    │ IA         │    │ Detalhados │                  │
│   │            │    │            │    │            │                  │
│   │ Avaliação  │    │ Ajuda-o a  │    │ Diagnóstico│                  │
│   │ integrada  │    │ compreender│    │ por camada │                  │
│   │ de todas   │    │ cada       │    │ com        │                  │
│   │ as camadas │    │ conceito   │    │ recomend.  │                  │
│   └────────────┘    └────────────┘    └────────────┘                  │
│                                                                        │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│              [Figura 1 — Hexágono AILO]                               │
│                                                                        │
│        O framework AILO organiza-se em 6 camadas:                     │
│                                                                        │
│        • Organizacional — Estratégia e governação                     │
│        • Humana — Pessoas, cultura e ética                            │
│        • Aprendizagem — Contextos e experiências                      │
│        • Cognitiva (IA) — Geração, recomendação, síntese, previsão   │
│        • Tecnológica — Infraestrutura e dados                         │
│        • Avaliação — Ciclo de melhoria contínua                       │
│                                                                        │
├────────────────────────────────────────────────────────────────────────┤
│  © 2026 Projeto AILO — Engenharia Informática — UAb                  │
└────────────────────────────────────────────────────────────────────────┘
```

### 2.2. Dashboard Principal (após login)

```
┌────────────────────────────────────────────────────────────────────────┐
│  🔷 AILO    [Organizações] [Avaliações] [Perfil]        Ricardo ▾    │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  Bem-vindo, Ricardo                                                    │
│                                                                        │
│  ┌───────────────────────────┐  ┌───────────────────────────┐         │
│  │  📋 Minhas Organizações   │  │  📊 Últimas Avaliações    │         │
│  │                           │  │                           │         │
│  │  TechSchool    [Avaliar]  │  │  TechSchool  3.2/5  ██▓░ │         │
│  │  MicroRetail   [Avaliar]  │  │  19/04/2026  Definido    │         │
│  │                           │  │                           │         │
│  │  [+ Nova Organização]     │  │  MicroRetail  Em curso... │         │
│  └───────────────────────────┘  └───────────────────────────┘         │
│                                                                        │
│  ┌──────────────────────────────────────────────────────────┐         │
│  │  Avaliação mais recente: TechSchool                      │         │
│  │                                                          │         │
│  │          ┌─────────────┐                                 │         │
│  │          │ Organiz.    │                                 │         │
│  │          │   3.5       │                                 │         │
│  │     ┌────┤             ├────┐                            │         │
│  │     │Hum.│             │Apr.│                            │         │
│  │     │3.8 │  AILO 3.2   │2.9 │   ← Hexágono/Radar       │         │
│  │     └────┤             ├────┘                            │         │
│  │          │             │                                 │         │
│  │     ┌────┤             ├────┐                            │         │
│  │     │Aval│             │Cog.│                            │         │
│  │     │3.1 │             │2.7 │                            │         │
│  │     └────┤             ├────┘                            │         │
│  │          │ Tecnol.     │                                 │         │
│  │          │   3.3       │                                 │         │
│  │          └─────────────┘                                 │         │
│  │                                                          │         │
│  │  [Ver Detalhes]  [Gerar PDF]  [Ver Recomendações]       │         │
│  └──────────────────────────────────────────────────────────┘         │
└────────────────────────────────────────────────────────────────────────┘
```

### 2.3. Questionário AILO

```
┌────────────────────────────────────────────────────────────────────────┐
│  🔷 AILO    Avaliação: TechSchool           Progresso: ████░░ 67%    │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  ┌─ CAMADAS ──────────────────────────────────────────────────────┐   │
│  │ ✅ Organiz. │ ✅ Humana │ 🔵 Aprendiz. │ ○ Cogn. │ ○ Tecn. │ ○ Aval │
│  └────────────────────────────────────────────────────────────────┘   │
│                                                                        │
│  ┌──────────────────────────────────────────┐ ┌──────────────────────┐│
│  │                                          │ │  💬 Assistente AILO  ││
│  │  Camada de Aprendizagem                  │ │                      ││
│  │  ━━━━━━━━━━━━━━━━━━━━━━                  │ │  Olá! Estamos na     ││
│  │                                          │ │  Camada de           ││
│  │  📌 Contextos Adaptativos                │ │  Aprendizagem.       ││
│  │                                          │ │  Esta camada avalia  ││
│  │  A.C.1 — Personalização de percursos     │ │  como a organização  ││
│  │  ┌─────────────────────────────────────┐ │ │  cria ambientes de   ││
│  │  │ Qual o nível de personalização dos  │ │ │  aprendizagem        ││
│  │  │ percursos de aprendizagem?          │ │ │  adaptativos.        ││
│  │  │                                     │ │ │                      ││
│  │  │  ○ 1 - One-size-fits-all            │ │ │  Pergunte-me         ││
│  │  │  ○ 2 - Alguma diferenciação         │ │ │  qualquer dúvida!    ││
│  │  │  ● 3 - Percursos por perfil/função  │ │ │                      ││
│  │  │  ○ 4 - Adaptação parcial por IA     │ │ │ ┌──────────────────┐ ││
│  │  │  ○ 5 - IA gera percursos adaptativ. │ │ │ │ O que são       │ ││
│  │  │                                     │ │ │ │ contextos       │ ││
│  │  │  Justificação (opcional):           │ │ │ │ adaptativos?    │ ││
│  │  │  ┌────────────────────────────────┐ │ │ │ └────────┬─────────┘ ││
│  │  │  │ Temos percursos por função... │ │ │ │          │           ││
│  │  │  └────────────────────────────────┘ │ │ │ Contextos adaptativos││
│  │  │                           [?] Ajuda │ │ │ são ambientes de     ││
│  │  └─────────────────────────────────────┘ │ │ aprendizagem que se  ││
│  │                                          │ │ ajustam ao perfil,   ││
│  │  A.C.2 — Ambientes de aprendizagem       │ │ função e necessidades││
│  │  ┌─────────────────────────────────────┐ │ │ de cada aprendente.  ││
│  │  │ ...                                 │ │ │ Na sua escola, isto  ││
│  │  └─────────────────────────────────────┘ │ │ poderia significar...││
│  │                                          │ │                      ││
│  │  📌 Experiências Personalizadas          │ │ ┌──────────────────┐ ││
│  │  ...                                     │ │ │ Escreva aqui...  │ ││
│  │                                          │ │ └────────┬─────────┘ ││
│  │  [← Camada Anterior]  [Próxima Camada →] │ │          [Enviar]    ││
│  └──────────────────────────────────────────┘ └──────────────────────┘│
│                                                                        │
│  Auto-save ativo ✓                          Última gravação: 18:45   │
└────────────────────────────────────────────────────────────────────────┘
```

### 2.4. Dashboard de Resultados

```
┌────────────────────────────────────────────────────────────────────────┐
│  🔷 AILO    Resultados: TechSchool          [Gerar PDF] [Partilhar]  │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  ┌───────────────────────────────────────────────────────────────────┐│
│  │  Índice Global AILO: 3.2 / 5.0                                   ││
│  │  Classificação: ██████████████████████░░░░░░░░  DEFINIDO          ││
│  │                                                                   ││
│  │  A organização tem processos formais estabelecidos com             ││
│  │  implementação consistente, mas com margem para otimização.       ││
│  └───────────────────────────────────────────────────────────────────┘│
│                                                                        │
│  ┌────────────────────────────┐  ┌───────────────────────────────────┐│
│  │                            │  │  Scores por Camada               ││
│  │    [Gráfico Hexagonal]     │  │                                   ││
│  │                            │  │  🟢 Humana         3.8  ████████░ ││
│  │     Organiz. 3.5           │  │  🟢 Organizacional 3.5  ███████░░ ││
│  │      /      \              │  │  🟡 Tecnológica    3.3  ██████░░░ ││
│  │  Hum 3.8    Apr 2.9       │  │  🟡 Avaliação      3.1  ██████░░░ ││
│  │     |  AILO  |            │  │  🟡 Aprendizagem   2.9  █████░░░░ ││
│  │  Ava 3.1    Cog 2.7       │  │  🔴 Cognitiva(IA)  2.7  █████░░░░ ││
│  │      \      /              │  │                                   ││
│  │     Tecnol. 3.3            │  │                                   ││
│  │                            │  └───────────────────────────────────┘│
│  └────────────────────────────┘                                       │
│                                                                        │
│  ┌───────────────────────────────────────────────────────────────────┐│
│  │  Interdependências Chave                                          ││
│  │                                                                   ││
│  │  ✅ Humana × Organizacional (fortalece)                           ││
│  │     Boa maturidade humana suporta a estratégia organizacional     ││
│  │                                                                   ││
│  │  ⚠️ Cognitiva × Tecnológica (risco)                               ││
│  │     Ambição cognitiva limitada por infraestrutura tecnológica     ││
│  │                                                                   ││
│  │  ⚠️ Avaliação × Cognitiva (risco) — CR5                           ││
│  │     Avaliação insuficiente pode permitir bypass de conhecimento   ││
│  └───────────────────────────────────────────────────────────────────┘│
│                                                                        │
│  ┌───────────────────────────────────────────────────────────────────┐│
│  │  Top Recomendações                                                ││
│  │                                                                   ││
│  │  1. 🔴 Cognitiva: Implementar IA generativa para criação de      ││
│  │     conteúdos de aprendizagem (ex: Google Gemini) — Custo: Free   ││
│  │                                                                   ││
│  │  2. 🟡 Aprendizagem: Criar percursos adaptativos por função      ││
│  │     utilizando LXP com recomendação — Custo: Freemium             ││
│  │                                                                   ││
│  │  3. 🟡 Avaliação: Implementar learning analytics para feedback   ││
│  │     contínuo — Custo: Integrado no LMS                            ││
│  │                                                                   ││
│  │  [Ver todas as recomendações →]                                   ││
│  └───────────────────────────────────────────────────────────────────┘│
└────────────────────────────────────────────────────────────────────────┘
```

### 2.5. Relatório PDF — Estrutura

```
┌─────────────────────────────────┐
│                                 │
│     DIAGNÓSTICO AILO            │
│     ─────────────────           │
│     TechSchool                  │
│                                 │
│     Abril 2026                  │
│                                 │
│     [Logo AILO hexágono]        │
│                                 │
├─────────────────────────────────┤  Página 1 — Capa
│                                 │
│  RESUMO EXECUTIVO               │
│                                 │
│  Índice Global: 3.2 (Definido)  │
│  [Gráfico hexagonal]            │
│                                 │
│  Pontos fortes: Camada Humana,  │
│  Organizacional                 │
│                                 │
│  Áreas prioritárias: Cognitiva, │
│  Aprendizagem                   │
│                                 │
├─────────────────────────────────┤  Página 2 — Resumo
│                                 │
│  1. CAMADA ORGANIZACIONAL       │
│     Score: 3.5 — Gerido         │
│     [Barra de progresso]        │
│                                 │
│     Pontos fortes:              │
│     • Estratégia alinhada       │
│     • Processos de KM ativos    │
│                                 │
│     Lacunas:                    │
│     • Governação IA formal      │
│                                 │
│     Recomendações:              │
│     • Implementar framework     │
│       de governação             │
│                                 │
├─────────────────────────────────┤  Páginas 3-8 — Uma por camada
│  ...                            │
│  (repete para cada camada)      │
│                                 │
├─────────────────────────────────┤
│                                 │
│  INTERDEPENDÊNCIAS              │
│  [Tabela/Grafo de relações]     │
│                                 │
├─────────────────────────────────┤  Página 9
│                                 │
│  ROTEIRO DE IMPLEMENTAÇÃO       │
│                                 │
│  Prioridade 1 (imediato):       │
│  • ...                          │
│                                 │
│  Prioridade 2 (curto prazo):    │
│  • ...                          │
│                                 │
│  Prioridade 3 (médio prazo):    │
│  • ...                          │
│                                 │
└─────────────────────────────────┘  Página 10 — Roteiro
```

---

## 3. Design System

### 3.1. Paleta de Cores (alinhada com AILO)

| Elemento | Cor | Hex | Uso |
|----------|-----|-----|-----|
| Primary | Azul escuro | `#2E4057` | Headers, botões primários |
| Organizacional | Azul escuro | `#2E4057` | Camada organizacional |
| Humana | Verde teal | `#048A81` | Camada humana |
| Aprendizagem | Azul claro | `#54C6EB` | Camada aprendizagem |
| Cognitiva (IA) | Ciano | `#8EE3EF` | Camada cognitiva |
| Tecnológica | Púrpura | `#7C77B9` | Camada tecnológica |
| Avaliação | Rosa | `#E8567F` | Camada avaliação |
| Background | Cinza claro | `#F5F7FA` | Fundo geral |
| Surface | Branco | `#FFFFFF` | Cards e painéis |
| Text | Cinza escuro | `#333333` | Texto principal |
| Success | Verde | `#27AE60` | Nível bom (≥3.5) |
| Warning | Amarelo | `#F39C12` | Nível médio (2.7-3.4) |
| Danger | Vermelho | `#E74C3C` | Nível baixo (<2.7) |

### 3.2. Tipografia

| Elemento | Font | Peso | Tamanho |
|----------|------|------|---------|
| H1 | Inter | 700 | 28px |
| H2 | Inter | 600 | 22px |
| H3 | Inter | 600 | 18px |
| Body | Inter | 400 | 15px |
| Small | Inter | 400 | 13px |
| Labels | Inter | 500 | 12px |

### 3.3. Componentes Base

- **Cards**: `border-radius: 12px`, `box-shadow: 0 2px 8px rgba(0,0,0,0.08)`, `padding: 24px`
- **Botões**: `border-radius: 8px`, `padding: 10px 20px`, hover com `transform: translateY(-1px)`
- **Inputs**: `border: 1px solid #E0E0E0`, `border-radius: 6px`, focus com `border-color: #2E4057`
- **Chat bubble**: `border-radius: 16px 16px 16px 0`, fundo `#F0F4F8`
- **Progress bars**: `height: 8px`, `border-radius: 4px`, cor da camada correspondente

### 3.4. Responsividade

| Breakpoint | Largura | Layout |
|-----------|---------|--------|
| Mobile | < 768px | Stack vertical, chat em fullscreen overlay |
| Tablet | 768-1024px | Questionário e chat side-by-side (60/40) |
| Desktop | > 1024px | Layout completo com sidebar (70/30) |
