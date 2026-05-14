# Modelo de Dados — Esquema Relacional AILO

## 1. Diagrama Entidade-Relacionamento (Textual)

```mermaid
flowchart TB

U["UTILIZADORES<br/>id (PK)<br/>nome<br/>email<br/>password_hash<br/>papel<br/>created_at<br/>updated_at"]

O["ORGANIZACOES<br/>id (PK)<br/>user_id (FK)<br/>nome<br/>setor<br/>dimensao<br/>tipo<br/>pais<br/>descricao"]

A["AVALIACOES<br/>id (PK)<br/>organizacao_id (FK)<br/>user_id (FK)<br/>data_inicio<br/>data_fim<br/>status<br/>score_global<br/>nivel_global"]

R["RESPOSTAS<br/>id (PK)<br/>avaliacao_id (FK)<br/>indicador_id (FK)<br/>score<br/>justificacao"]

RC["RESULTADOS_CAMADA<br/>id (PK)<br/>avaliacao_id (FK)<br/>camada_id (FK)<br/>score<br/>nivel"]

CI["CONVERSAS_IA<br/>id (PK)<br/>avaliacao_id (FK)<br/>mensagem<br/>papel<br/>camada_id (FK)"]

I["INDICADORES<br/>id<br/>componente_id (FK)<br/>codigo<br/>pergunta<br/>peso"]

C["COMPONENTES<br/>id<br/>camada_id (FK)<br/>nome<br/>peso"]

CA["CAMADAS_AILO<br/>id<br/>nome<br/>peso"]

U -->|"1:N"| O
O -->|"1:N"| A

A -->|"1:N"| R
A -->|"1:N"| RC
A -->|"1:N"| CI

I -->|"1:N"| R

CA -->|"1:N"| C
C -->|"1:N"| I
```

---

## 2. Esquema SQL (SQLite/PostgreSQL)

```mermaid
flowchart TB

subgraph UI["🎨 Frontend"]
    F1["Interface Web"]
    F2["Questionário AILO"]
    F3["Dashboard"]
    F4["Chat IA"]
end

subgraph API["⚙️ Backend API"]
    B1["Autenticação JWT"]
    B2["Gestão de Utilizadores"]
    B3["Motor de Scoring"]
    B4["Geração de Relatórios"]
    B5["Lógica AILO"]
end

subgraph DB["🗄️ Base de Dados"]
    D1["Utilizadores"]
    D2["Organizações"]
    D3["Avaliações"]
    D4["Respostas"]
    D5["Resultados"]
end

subgraph AI["🤖 Serviço IA"]
    A1["Explicações"]
    A2["Sugestões"]
    A3["Validação"]
    A4["Análise Contextual"]
end

subgraph EXT["🌐 Serviços Externos"]
    E1["Email SMTP"]
    E2["Exportação PDF"]
end

F1 --> B1
F2 --> B3
F3 --> B4
F4 --> A1

B1 --> D1
B2 --> D2
B3 --> D3
B3 --> D4
B4 --> D5

B5 --> AI

B4 --> E2
B1 --> E1
```

---

## 3. Dados Iniciais (Seed Data)

### 3.1. Camadas AILO

```mermaid
flowchart TB

O["🏢 Camada Organizacional<br/>Estratégia<br/>Processos<br/>Decisão<br/>Valor"]

H["👥 Camada Humana<br/>Pessoas<br/>Cultura<br/>Autonomia<br/>Ética"]

A["📚 Camada de Aprendizagem<br/>Contextos Adaptativos<br/>Experiências Personalizadas<br/>Integração Formal-Informal"]

C["🤖 Camada Cognitiva (IA)<br/>Geração<br/>Recomendação<br/>Síntese<br/>Previsão"]

T["💻 Camada Tecnológica<br/>Plataformas<br/>Dados<br/>Integração<br/>Segurança"]

V["📈 Camada de Avaliação<br/>Evidência<br/>Feedback<br/>Competências<br/>Impacto Organizacional"]

CORE["🧠 AILO CORE<br/>Conhecimento Organizacional"]

O --> CORE
H --> CORE
A --> CORE
C --> CORE
T --> CORE
V --> CORE

T --> C
H --> A
O --> V
C --> V
```

### 3.2. Componentes (exemplo — Camada Organizacional)

```mermaid
flowchart TB

O["🏢 Organizacional"]

OE["Estratégia"]
OP["Processos"]
OD["Decisão"]
OV["Valor"]

H["👥 Humana"]

HP["Pessoas"]
HC["Cultura"]
HA["Autonomia"]
HE["Ética"]

A["📚 Aprendizagem"]

AC["Contextos Adaptativos"]
AE["Experiências Personalizadas"]
AI["Integração Formal-Informal"]

C["🤖 Cognitiva (IA)"]

CG["Geração"]
CR["Recomendação"]
CS["Síntese"]
CP["Previsão"]

T["💻 Tecnológica"]

TP["Plataformas"]
TD["Dados"]
TI["Integração"]
TS["Segurança"]

V["📈 Avaliação"]

VE["Evidência"]
VF["Avaliação Formativa"]
VC["Competências"]
VI["Impacto Organizacional"]

O --> OE
O --> OP
O --> OD
O --> OV

H --> HP
H --> HC
H --> HA
H --> HE

A --> AC
A --> AE
A --> AI

C --> CG
C --> CR
C --> CS
C --> CP

T --> TP
T --> TD
T --> TI
T --> TS

V --> VE
V --> VF
V --> VC
V --> VI
```

> Os seeds completos para todas as 6 camadas, 23 componentes e 51 indicadores estão definidos no ficheiro `02_indicadores_por_camada.md` e serão implementados na Fase 2.

---

## 4. Relações e Cardinalidades

| Relação | Cardinalidade | Descrição |
|---------|---------------|-----------|
| utilizadores → organizacoes | 1:N | Um utilizador pode ter múltiplas organizações |
| organizacoes → avaliacoes | 1:N | Uma organização pode ter múltiplas avaliações |
| avaliacoes → respostas | 1:N | Uma avaliação tem múltiplas respostas (1 por indicador) |
| camadas_ailo → componentes | 1:N | Cada camada tem múltiplos componentes |
| componentes → indicadores | 1:N | Cada componente tem múltiplos indicadores |
| avaliacoes → resultados_camada | 1:N | Uma avaliação tem 6 resultados (1 por camada) |
| avaliacoes → interdependencias | 1:N | Uma avaliação tem múltiplas análises de interdependência |
| avaliacoes → conversas_ia | 1:N | Uma avaliação tem múltiplas mensagens de chat |
| avaliacoes → recomendacoes | 1:N | Uma avaliação gera múltiplas recomendações |
| avaliacoes → relatorios | 1:1 | Uma avaliação gera um relatório |
