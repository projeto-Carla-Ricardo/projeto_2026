# Requisitos Funcionais e Não Funcionais

## 1. Requisitos Funcionais

### 1.1. Autenticação e Gestão de Utilizadores

| ID | Requisito | Prioridade | Descrição |
|----|-----------|------------|-----------|
| RF01 | Registo de utilizador | Alta | Formulário com nome, email, password. Validação de email único. Hash da password (bcrypt). |
| RF02 | Login | Alta | Autenticação por email/password. Emissão de JWT token com expiração de 24h. |
| RF03 | Logout | Alta | Invalidação do token de sessão. |
| RF04 | Perfil de utilizador | Média | Visualizar e editar dados do perfil. Ver histórico de avaliações. |
| RF05 | Recuperação de password | Média | Envio de email com link de reset. Token temporário com expiração. |
| RF06 | Papéis de utilizador | Alta | Dois papéis: Utilizador (realiza avaliações) e Administrador (gere sistema). |

### 1.2. Gestão de Organizações

| ID | Requisito | Prioridade | Descrição |
|----|-----------|------------|-----------|
| RF07 | Criar organização | Alta | Formulário com: nome, setor de atividade, dimensão (nº colaboradores), tipo (MPE, PME, Grande, Educação), país, descrição. |
| RF08 | Listar organizações | Alta | Lista paginada das organizações do utilizador. |
| RF09 | Editar organização | Média | Atualizar dados de uma organização existente. |
| RF10 | Eliminar organização | Baixa | Soft-delete com confirmação. Mantém histórico de avaliações. |

### 1.3. Questionário AILO

| ID | Requisito | Prioridade | Descrição |
|----|-----------|------------|-----------|
| RF11 | Iniciar avaliação | Alta | Criar nova instância de avaliação para uma organização. Regista data de início. |
| RF12 | Questionário por camada | Alta | Apresentação de perguntas organizadas pelas 6 camadas AILO. Cada camada como secção/passo. |
| RF13 | Perguntas por componente | Alta | Dentro de cada camada, perguntas agrupadas por componente (ex: Camada Humana → Pessoas, Cultura, Autonomia, Ética). |
| RF14 | Escala de resposta | Alta | Cada indicador responde numa escala de 1-5 com descrições contextuais dos níveis. |
| RF15 | Navegação condicional | Média | Perguntas que aparecem/desaparecem conforme tipo de organização e respostas anteriores. |
| RF16 | Persistência de progresso | Alta | Guardar respostas automaticamente. Permitir sair e retomar mais tarde sem perder dados. |
| RF17 | Barra de progresso | Média | Indicador visual de progresso geral e por camada. |
| RF18 | Validação em tempo real | Média | Alertar para perguntas obrigatórias não respondidas. Destacar inconsistências entre respostas. |

### 1.4. Assistente IA Conversacional

| ID | Requisito | Prioridade | Descrição |
|----|-----------|------------|-----------|
| RF19 | Chat lateral no questionário | Alta | Painel de chat integrado ao lado do questionário. Visível em todas as secções. |
| RF20 | Contextualização por camada | Alta | O assistente sabe em que camada/componente o utilizador está e adapta as respostas. |
| RF21 | Explicação de conceitos | Alta | O assistente explica conceitos do AILO em linguagem simples quando solicitado (ex: "O que é mediação cognitiva?"). |
| RF22 | Exemplos contextuais | Média | O assistente dá exemplos adaptados ao setor e tipo de organização (ex: para uma escola, para uma PME). |
| RF23 | Sugestão de resposta | Média | O assistente pode sugerir qual nível de maturidade se aplica com base na descrição do utilizador. |
| RF24 | Validação de consistência | Alta | Deteção de contradições entre respostas (ex: "temos IA integrada" mas "sem dados estruturados"). |
| RF25 | Histórico de conversa | Alta | Manutenção do contexto conversacional durante toda a avaliação. |

### 1.5. Motor de Scoring

| ID | Requisito | Prioridade | Descrição |
|----|-----------|------------|-----------|
| RF26 | Cálculo por indicador | Alta | Score 1-5 para cada um dos 51 indicadores. |
| RF27 | Cálculo por componente | Alta | Média ponderada dos indicadores de cada componente. |
| RF28 | Cálculo por camada | Alta | Média ponderada dos componentes de cada camada (6 scores de camada). |
| RF29 | Índice global AILO | Alta | Média ponderada das 6 camadas. Pesos configuráveis. |
| RF30 | Classificação de maturidade | Alta | Mapeamento do score para nível (Inicial/Em Desenvolvimento/Definido/Gerido/Otimizado). |
| RF31 | Identificação de gaps | Alta | Comparação de scores por camada vs. limiares para identificar lacunas críticas. |
| RF32 | Análise de interdependências | Média | Avaliação de pares de camadas (Humana×Avaliação, Cognitiva×Tecnológica, etc.). |
| RF33 | Mapeamento CR1-CR6 | Média | Cada resultado é mapeado para os 6 Conceptual Results da revisão sistemática. |

### 1.6. Relatórios e Visualizações

| ID | Requisito | Prioridade | Descrição |
|----|-----------|------------|-----------|
| RF34 | Gerar relatório | Alta | Relatório automático após conclusão da avaliação. |
| RF35 | Diagnóstico por camada | Alta | Secção do relatório para cada camada: score, pontos fortes, lacunas, recomendações. |
| RF36 | Análise integrada | Alta | Visão global das 6 camadas, interdependências e classificação AILO. |
| RF37 | Recomendações acionáveis | Alta | Sugestões concretas por camada com priorização. |
| RF38 | Exportação PDF | Alta | Download do relatório em formato PDF formatado. |
| RF39 | Visualização web | Alta | Relatório interativo no browser com gráficos dinâmicos. |
| RF40 | Dashboard hexagonal | Média | Gráfico radar/hexagonal inspirado na Figura 1 do AILO. |
| RF41 | Gráficos por camada | Média | Barras, indicadores semáforo e barras de progresso por componente. |
| RF42 | Comparação temporal | Baixa | Sobreposição de resultados de avaliações diferentes da mesma organização. |

### 1.7. Motor de Recomendação

| ID | Requisito | Prioridade | Descrição |
|----|-----------|------------|-----------|
| RF43 | Catálogo de ferramentas IA | Média | BD com ferramentas de IA categorizadas por: camada AILO, área funcional, custo, complexidade. |
| RF44 | Matching por perfil | Média | Algoritmo que cruza resultados do diagnóstico com ferramentas adequadas ao perfil. |
| RF45 | Priorização de recomendações | Média | Ordenação por impacto esperado e facilidade de implementação. |

### 1.8. Administração

| ID | Requisito | Prioridade | Descrição |
|----|-----------|------------|-----------|
| RF46 | Gestão de indicadores | Baixa | Admin pode adicionar/editar/remover indicadores e ajustar pesos. |
| RF47 | Gestão de ferramentas IA | Baixa | Admin pode gerir o catálogo de ferramentas. |
| RF48 | Estatísticas globais | Baixa | Dashboard admin com estatísticas de uso da plataforma. |

---

## 2. Requisitos Não Funcionais

### 2.1. Usabilidade

| ID | Requisito | Critério de Aceitação |
|----|-----------|----------------------|
| RNF01 | Interface intuitiva | Utilizador sem formação técnica consegue completar avaliação sem ajuda externa |
| RNF02 | Linguagem acessível | Todo o texto da interface em linguagem clara, sem jargão técnico não explicado |
| RNF03 | Feedback visual | Loading states, transições suaves, confirmações de ações |
| RNF04 | Responsividade | Funcional em desktop (≥1024px), tablet (≥768px) e mobile (≥375px) |
| RNF05 | Acessibilidade | Contraste WCAG AA, navegação por teclado, labels em formulários |

### 2.2. Desempenho

| ID | Requisito | Critério de Aceitação |
|----|-----------|----------------------|
| RNF06 | Tempo de carregamento | Páginas carregam em < 2 segundos |
| RNF07 | Resposta do assistente IA | Resposta do LLM em < 5 segundos |
| RNF08 | Geração de relatório | Relatório PDF gerado em < 10 segundos |
| RNF09 | Scoring | Cálculo completo das 6 camadas em < 1 segundo |

### 2.3. Segurança

| ID | Requisito | Critério de Aceitação |
|----|-----------|----------------------|
| RNF10 | Autenticação segura | Passwords hashed com bcrypt (≥12 rounds). JWT com expiração. |
| RNF11 | Proteção de rotas | Todas as rotas protegidas por autenticação JWT. Autorização por papel. |
| RNF12 | Input sanitization | Proteção contra SQL injection e XSS em todos os inputs. |
| RNF13 | HTTPS | Todas as comunicações cifradas em produção. |
| RNF14 | Chaves API protegidas | Chaves de API (Gemini) nunca expostas no frontend. Apenas no backend. |

### 2.4. Privacidade e Conformidade

| ID | Requisito | Critério de Aceitação |
|----|-----------|----------------------|
| RNF15 | Conformidade RGPD | Consentimento informado, direito ao esquecimento, portabilidade de dados. |
| RNF16 | Anonimização | Dados de demonstração/teste anonimizados. |
| RNF17 | Dados organizacionais | Dados de avaliação acessíveis apenas ao proprietário. |

### 2.5. Escalabilidade e Manutenibilidade

| ID | Requisito | Critério de Aceitação |
|----|-----------|----------------------|
| RNF18 | Arquitetura modular | Separação clara frontend/backend/BD. Componentes desacoplados. |
| RNF19 | Código documentado | Docstrings em funções públicas. README com instruções de setup. |
| RNF20 | Versionamento | Git com commits descritivos por fase. |
| RNF21 | Extensibilidade | Novas camadas/indicadores adicionáveis sem reescrever o motor de scoring. |

### 2.6. Disponibilidade

| ID | Requisito | Critério de Aceitação |
|----|-----------|----------------------|
| RNF22 | Acesso via web | Acessível via browser sem instalação local. |
| RNF23 | Compatibilidade | Chrome, Firefox, Safari, Edge (versões atuais). |
