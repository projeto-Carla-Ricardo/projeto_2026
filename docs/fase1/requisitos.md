# Requisitos do Sistema
## Ambiente Web para Framework IALO

**Projeto**: Ambiente Web para Framework IALO  
**Fase**: 1 — Levantamento e Modelação  
**Data**: 25/03/2026  

---

## 1. Requisitos Funcionais

### 1.1. Autenticação e Gestão de Utilizadores

| ID | Requisito | Prioridade | Descrição |
|----|-----------|------------|-----------|
| RF01 | Registo de utilizador | Must | O sistema deve permitir o registo com email, nome e password. Password armazenada com hash seguro (bcrypt/argon2). |
| RF02 | Login / Logout | Must | Autenticação via email + password com emissão de token JWT. Sessão com expiração configurável. |
| RF03 | Recuperação de password | Should | O utilizador pode solicitar reset de password via email. |
| RF04 | Perfil de utilizador | Must | O utilizador pode ver e editar os seus dados pessoais. |
| RF05 | Papéis de utilizador | Should | Distinção entre Empresário (utilizador normal) e Administrador (gestão do sistema). |

### 1.2. Gestão de Empresas

| ID | Requisito | Prioridade | Descrição |
|----|-----------|------------|-----------|
| RF06 | Criar perfil de empresa | Must | O utilizador pode criar um perfil com: nome, setor de atividade, nº de colaboradores, localização, ano de fundação. |
| RF07 | Editar perfil de empresa | Must | Atualizar dados da empresa a qualquer momento. |
| RF08 | Listar empresas | Must | Administrador pode listar todas as empresas. Empresário vê apenas as suas. |
| RF09 | Eliminar empresa | Should | Eliminação lógica (soft delete) com confirmação. |

### 1.3. Questionário Interativo (Diagnóstico IALO)

| ID | Requisito | Prioridade | Descrição |
|----|-----------|------------|-----------|
| RF10 | Iniciar diagnóstico | Must | O utilizador pode iniciar uma nova avaliação IALO para uma empresa. |
| RF11 | Questionário por dimensão | Must | Perguntas organizadas pelas 5 dimensões do IALO (Dados, Infraestrutura, Competências, Estratégia, Cultura). |
| RF12 | Navegação entre secções | Must | Navegação livre entre dimensões (avançar, recuar, saltar). |
| RF13 | Guardar progresso | Must | O questionário pode ser guardado a meio e retomado mais tarde. |
| RF14 | Navegação condicional | Could | Perguntas que aparecem/desaparecem conforme respostas anteriores. |
| RF15 | Validação de respostas | Must | Validação em tempo real (campos obrigatórios, formatos). |
| RF16 | Barra de progresso | Should | Indicação visual do progresso do questionário. |

### 1.4. Assistente IA (Agente Conversacional)

| ID | Requisito | Prioridade | Descrição |
|----|-----------|------------|-----------|
| RF17 | Chat integrado no questionário | Must | Painel de chat lateral onde o utilizador pode interagir com o assistente IA durante o preenchimento. |
| RF18 | Explicação de conceitos | Must | O assistente explica termos técnicos do IALO em linguagem simples, com exemplos contextualizados ao setor da empresa. |
| RF19 | Validação de consistência | Should | O assistente deteta contradições entre respostas e alerta o utilizador. |
| RF20 | Contexto conversacional | Must | O assistente mantém histórico da conversa na sessão, recordando respostas anteriores. |
| RF21 | Sugestão de resposta | Could | O assistente pode sugerir como responder a uma pergunta com base no contexto. |

### 1.5. Motor de Scoring

| ID | Requisito | Prioridade | Descrição |
|----|-----------|------------|-----------|
| RF22 | Cálculo por dimensão | Must | Calcular a pontuação de cada dimensão (0-100%) com base nos indicadores. |
| RF23 | Índice global de maturidade | Must | Calcular o índice global ponderado (pesos por dimensão). |
| RF24 | Classificação por nível | Must | Atribuir nível de maturidade (1-Inicial a 5-Otimizado) por dimensão e global. |
| RF25 | Identificação de gaps | Must | Identificar dimensões com pontuação ≤ 40% como gaps críticos. |
| RF26 | Lógica fuzzy | Should | Converter respostas qualitativas em valores numéricos via regras fuzzy. |

### 1.6. Geração de Relatórios e Recomendações

| ID | Requisito | Prioridade | Descrição |
|----|-----------|------------|-----------|
| RF27 | Relatório automático | Must | Gerar relatório com pontos fortes, necessidades, gaps e recomendações. |
| RF28 | Recomendação de ferramentas | Must | Sugerir ferramentas de IA acessíveis com base no perfil e gaps da empresa. |
| RF29 | Exportação PDF | Must | Exportar relatório completo em formato PDF. |
| RF30 | Relatório interativo web | Should | Versão web do relatório com gráficos dinâmicos e drill-down. |

### 1.7. Dashboard e Visualizações

| ID | Requisito | Prioridade | Descrição |
|----|-----------|------------|-----------|
| RF31 | Dashboard de resultados | Must | Painel com resumo visual do diagnóstico após conclusão. |
| RF32 | Gráfico radar | Must | Gráfico radar/spider das 5 dimensões de maturidade. |
| RF33 | Gráficos de progresso | Should | Barras de progresso por dimensão e indicador. |
| RF34 | Histórico de avaliações | Should | Listar avaliações anteriores com possibilidade de comparação temporal. |
| RF35 | Indicadores semáforo | Should | Verde/amarelo/vermelho para comunicação imediata do estado por dimensão. |

### 1.8. Administração

| ID | Requisito | Prioridade | Descrição |
|----|-----------|------------|-----------|
| RF36 | Gestão de utilizadores | Could | Administrador pode listar, ativar/desativar utilizadores. |
| RF37 | Gestão de ferramentas IA | Could | CRUD do catálogo de ferramentas de IA recomendáveis. |
| RF38 | Estatísticas globais | Could | Dashboard com métricas agregadas (nº avaliações, maturidade média por setor). |

---

## 2. Requisitos Não-Funcionais

| ID | Requisito | Categoria | Descrição |
|----|-----------|-----------|-----------|
| RNF01 | Interface intuitiva | Usabilidade | A interface deve ser compreensível por utilizadores sem formação técnica. Linguagem clara, ícones descritivos, percursos simples. |
| RNF02 | Design responsivo | Usabilidade | A aplicação deve adaptar-se a desktop, tablet e smartphone (min. 320px). |
| RNF03 | Tempo de resposta | Desempenho | Páginas devem carregar em < 2 segundos. Respostas da API em < 500ms (exceto IA). |
| RNF04 | Resposta do assistente IA | Desempenho | Resposta do assistente em < 10 segundos com indicador de loading. |
| RNF05 | Armazenamento seguro de passwords | Segurança | Passwords hash com bcrypt ou argon2. Nunca armazenadas em texto plano. |
| RNF06 | Autenticação JWT | Segurança | Tokens com expiração, refresh tokens, e proteção contra CSRF/XSS. |
| RNF07 | Proteção de dados | Segurança | Dados empresariais protegidos. Acesso restrito ao proprietário e admin. RGPD. |
| RNF08 | Arquitetura modular | Escalabilidade | Separação clara frontend/backend/BD. Possibilidade de substituir componentes. |
| RNF09 | Base de dados relacional | Manutenibilidade | Esquema normalizado, migrations versionadas, documentação do modelo. |
| RNF10 | Compatibilidade browser | Compatibilidade | Chrome, Firefox, Safari, Edge (últimas 2 versões). |
| RNF11 | Acessibilidade WCAG 2.1 AA | Acessibilidade | Contraste suficiente, navegação por teclado, texto alternativo em imagens. |
| RNF12 | Disponibilidade | Fiabilidade | Sistema disponível 99% do tempo em ambiente de produção. |

---

## 3. Matriz de Prioridade (MoSCoW)

### Must Have (Obrigatório)
- Registo, login, gestão de perfil
- Perfil de empresa
- Questionário completo (5 dimensões)
- Assistente IA no questionário (chat lateral com explicações)
- Motor de scoring (cálculo de maturidade e gaps)
- Geração de relatório com recomendações
- Dashboard com gráfico radar
- Exportação PDF

### Should Have (Importante)
- Recuperação de password
- Papéis (Empresário / Admin)
- Guardar progresso do questionário
- Validação de consistência via IA
- Navegação condicional no questionário
- Indicadores semáforo
- Histórico de avaliações
- Relatório interativo web

### Could Have (Desejável)
- Sugestão de resposta pelo assistente IA
- Gestão administrativa de utilizadores
- Catálogo editável de ferramentas IA
- Estatísticas globais por setor
- Comparação temporal de avaliações

### Won't Have (Fora de âmbito)
- Motor de recomendação baseado em ML complexo
- Integração com sistemas ERP externos
- App mobile nativa
- Suporte multi-idioma (apenas português inicialmente)
- Governança de IA para grandes empresas
