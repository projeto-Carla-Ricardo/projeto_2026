# Wireframes e Prototipagem UI/UX

## 1. Mapa de Navegação

```mermaid
flowchart TB

LP["Landing Page"]

LOGIN["Login"]
REG["Registo"]

DP["Dashboard Principal"]

ORG["Organizações<br/>Lista"]
NOVA["Nova<br/>Avaliação"]
HIST["Histórico"]
PERFIL["Perfil"]
ADMIN["Admin Panel"]

Q["QUESTIONÁRIO AILO<br/><br/>Tab 1: Organizacional<br/>Tab 2: Humana<br/>Tab 3: Aprendizagem<br/>Tab 4: Cognitiva (IA)<br/>Tab 5: Tecnológica<br/>Tab 6: Avaliação<br/><br/>+ Chat IA Lateral"]

R["RESULTADOS<br/><br/>Dashboard Hexagonal<br/>Relatório Detalhado<br/>Interdependências<br/>Recomendações<br/>PDF Export"]

COMP["Comparação temporal"]

LP --> LOGIN
LP --> REG

LOGIN --> DP
REG --> DP

DP --> ORG
DP --> NOVA
DP --> HIST
DP --> PERFIL
DP --> ADMIN

NOVA --> Q

Q --> R

ORG --> COMP
```

---

## 2. Wireframes Detalhados

### 2.1. Landing Page

```mermaid
flowchart TB

TOP["🔷 AILO Platform<br/><br/>[ Login ]  [ Registar ]"]

TITLE["Avalie a maturidade da sua organização<br/>com o Framework AILO"]

SUB["A IA como mediador cognitivo nas Organizações Aprendentes"]

BTN["▶ Começar Avaliação"]

subgraph FEATURES["Funcionalidades"]

F1["🏢<br/><b>6 Camadas AILO</b><br/><br/>Avaliação integrada<br/>de todas as camadas"]

F2["🤖<br/><b>Assistente IA</b><br/><br/>Ajuda a compreender<br/>cada conceito"]

F3["📊<br/><b>Relatórios Detalhados</b><br/><br/>Diagnóstico por camada<br/>com recomendações"]

end

HEX["Figura 1 — Hexágono AILO"]

LAYERS["• Organizacional — Estratégia e governação<br/>• Humana — Pessoas, cultura e ética<br/>• Aprendizagem — Contextos e experiências<br/>• Cognitiva (IA) — Geração, recomendação, síntese e previsão<br/>• Tecnológica — Infraestrutura e dados<br/>• Avaliação — Ciclo de melhoria contínua"]

FOOT["© 2026 Projeto AILO — Engenharia Informática — UAb"]

TOP --> TITLE
TITLE --> SUB
SUB --> BTN

BTN --> FEATURES

FEATURES --> HEX

HEX --> LAYERS

LAYERS --> FOOT
```

### 2.2. Dashboard Principal (após login)

```mermaid
flowchart TB

TOP["🔷 AILO<br/>[Organizações] [Avaliações] [Perfil]<br/>Ricardo ▾"]

WELCOME["Bem-vindo, Ricardo"]

subgraph INFO["Painel Principal"]

ORG["📋 Minhas Organizações<br/><br/>TechSchool [Avaliar]<br/>MicroRetail [Avaliar]<br/><br/>+ Nova Organização"]

AV["📊 Últimas Avaliações<br/><br/>TechSchool — 3.2/5 — Definido<br/>19/04/2026<br/><br/>MicroRetail — Em curso..."]

end

subgraph DASH["Avaliação mais recente: TechSchool"]

HEX["Hexágono/Radar AILO<br/><br/>Organizacional: 3.5<br/>Humana: 3.8<br/>Aprendizagem: 2.9<br/>Cognitiva: 2.7<br/>Tecnológica: 3.3<br/>Avaliação: 3.1<br/><br/>AILO Global: 3.2"]

BTN["[ Ver Detalhes ]<br/>[ Gerar PDF ]<br/>[ Ver Recomendações ]"]

end

TOP --> WELCOME

WELCOME --> INFO

INFO --> DASH

HEX --> BTN
```

### 2.3. Questionário AILO

```mermaid
flowchart TB

TOP["🔷 AILO<br/>Avaliação: TechSchool<br/>Progresso: 67%"]

LAYERS["✅ Organizacional | ✅ Humana | 🔵 Aprendizagem | ○ Cognitiva | ○ Tecnológica | ○ Avaliação"]

subgraph MAIN["QUESTIONÁRIO AILO"]

subgraph LEFT["Questionário"]

TITLE["Camada de Aprendizagem"]

COMP["📌 Contextos Adaptativos"]

Q1["A.C.1 — Personalização de percursos<br/><br/>Qual o nível de personalização dos percursos de aprendizagem?<br/><br/>○ 1 — One-size-fits-all<br/>○ 2 — Alguma diferenciação<br/>● 3 — Percursos por perfil/função<br/>○ 4 — Adaptação parcial por IA<br/>○ 5 — IA gera percursos adaptativos"]

JUST["Justificação:<br/>Temos percursos por função..."]

Q2["A.C.2 — Ambientes de aprendizagem<br/>..."]

COMP2["📌 Experiências Personalizadas"]

NAV["[← Camada Anterior]  [Próxima Camada →]"]

end

subgraph RIGHT["💬 Assistente AILO"]

HELP["Olá! Estamos na Camada de Aprendizagem.<br/><br/>Esta camada avalia como a organização cria ambientes de aprendizagem adaptativos."]

USER["O que são contextos adaptativos?"]

BOT["Contextos adaptativos são ambientes de aprendizagem que se ajustam ao perfil, função e necessidades de cada aprendente."]

INPUT["Escreva aqui..."]

SEND["[Enviar]"]

end

end

BOTTOM["Auto-save ativo ✓<br/>Última gravação: 18:45"]

TOP --> LAYERS
LAYERS --> MAIN
MAIN --> BOTTOM

TITLE --> COMP
COMP --> Q1
Q1 --> JUST
JUST --> Q2
Q2 --> COMP2
COMP2 --> NAV

HELP --> USER
USER --> BOT
BOT --> INPUT
INPUT --> SEND
```

### 2.4. Dashboard de Resultados

```mermaid
flowchart TB

TOP["🔷 AILO<br/>Resultados: TechSchool<br/>[Gerar PDF] [Partilhar]"]

GLOBAL["Índice Global AILO: 3.2 / 5.0<br/><br/>Classificação: DEFINIDO<br/><br/>A organização tem processos formais estabelecidos com implementação consistente, mas com margem para otimização."]

subgraph MAIN["Resultados"]

HEX["📊 Gráfico Hexagonal<br/><br/>Organizacional: 3.5<br/>Humana: 3.8<br/>Aprendizagem: 2.9<br/>Cognitiva (IA): 2.7<br/>Tecnológica: 3.3<br/>Avaliação: 3.1"]

SCORES["📈 Scores por Camada<br/><br/>🟢 Humana — 3.8<br/>🟢 Organizacional — 3.5<br/>🟡 Tecnológica — 3.3<br/>🟡 Avaliação — 3.1<br/>🟡 Aprendizagem — 2.9<br/>🔴 Cognitiva (IA) — 2.7"]

end

subgraph INTER["🔗 Interdependências Chave"]

I1["✅ Humana × Organizacional<br/>Boa maturidade humana suporta a estratégia organizacional"]

I2["⚠️ Cognitiva × Tecnológica<br/>Ambição cognitiva limitada pela infraestrutura tecnológica"]

I3["⚠️ Avaliação × Cognitiva (CR5)<br/>Avaliação insuficiente pode permitir bypass de conhecimento"]

end

subgraph REC["💡 Top Recomendações"]

R1["🔴 Cognitiva<br/>Implementar IA generativa para criação de conteúdos"]

R2["🟡 Aprendizagem<br/>Criar percursos adaptativos por função"]

R3["🟡 Avaliação<br/>Implementar learning analytics para feedback contínuo"]

BTN["[Ver todas as recomendações →]"]

end

TOP --> GLOBAL

GLOBAL --> MAIN

MAIN --> INTER

INTER --> REC

R1 --> BTN
R2 --> BTN
R3 --> BTN
```

### 2.5. Relatório PDF — Estrutura

```mermaid
flowchart TB

CAPA["📘 Página 1 — Capa<br/><br/>DIAGNÓSTICO AILO<br/>TechSchool<br/>Abril 2026<br/><br/>[Logo AILO Hexágono]"]

RESUMO["📄 Página 2 — Resumo Executivo<br/><br/>Índice Global: 3.2 (Definido)<br/>[Gráfico Hexagonal]<br/><br/>Pontos fortes:<br/>• Camada Humana<br/>• Organizacional<br/><br/>Áreas prioritárias:<br/>• Cognitiva<br/>• Aprendizagem"]

CAMADA["📊 Páginas 3-8 — Diagnóstico por Camada<br/><br/>1. Camada Organizacional<br/>Score: 3.5 — Gerido<br/>[Barra de progresso]<br/><br/>Pontos fortes<br/>Lacunas<br/>Recomendações<br/><br/>↺ Repetido para as 6 camadas"]

INTER["🔗 Página 9 — Interdependências<br/><br/>[Tabela/Grafo de relações]"]

ROTEIRO["🛣️ Página 10 — Roteiro de Implementação<br/><br/>Prioridade 1 — Imediato<br/>Prioridade 2 — Curto prazo<br/>Prioridade 3 — Médio prazo"]

CAPA --> RESUMO

RESUMO --> CAMADA

CAMADA --> INTER

INTER --> ROTEIRO
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
