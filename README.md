# Projeto final de curso Engenharia Informatica

Este projeto é o meu projeto de final de curso, cujo enquadramento pode ser visto no base.md e no Relatorio inicial.pdf nesta pasta. 

Serão desenvolvidas todas as funcionalidades lá propostas, por ordem de prioridade. 

Deve ser criado um repositório git nesta pasta que vai gravando sempre tudas as alterações que forem sendo feitas. Cada commit deve ter na sua descrição a fase do projeto que está a ser desenvolvida, conforme indicação do pdf. Por exemplo, no desenvolvimento da fase 1, os commits devem ser feitos com a descrição "Fase 1 - ...".  

> **REGRA DE GESTÃO DE VERSÕES POR PASTAS DE FASES (INSTRUÇÃO PARA A IA)**
> Existem 6 pastas (`Fase 1` a `Fase 6`) na raiz do projeto. O desenvolvimento original é feito SEMPRE na raiz (`PROJETO_2026`). 
> Sempre que uma fase do "Índice de Desenvolvimento" for terminada, todo o código atual e funcional desenvolvido até esse momento deve ser **copiado** para a pasta da respetiva fase. 
> - **Exemplo:** Ao terminar a Fase 2, todo o projeto (que já engloba o que foi feito na 1 e 2) é copiado para dentro da pasta `Fase 2`. Ao terminar a Fase 4, todo o projeto (fases 1 a 4 consolidadas) entra na pasta `Fase 4`.
> - **Objetivo:** O projeto será carregado para o GitHub agrupado em fases para o professor poder avaliar a evolução do desenvolvimento. A IA deve ajudar a assegurar que as pastas têm os conteúdos corretos de cada fase.


O projeto deve ter sempre por base de fundo as diretrizes do professor que abaixo descrevo: 

"
*Titulo*: "Ambiente web para Framework IALO (Inteligência Artificial em LO)"

*Descrição*: "A integração de Inteligência Artificial em contextos organizacionais requer instrumentos que permitam avaliar maturidade, necessidades e estratégias de implementação. A formalização computacional de um framework de análise constitui uma oportunidade para articular modelação conceptual e desenvolvimento aplicacional.
O projeto consiste na conceção e desenvolvimento de um ambiente web que suporte a aplicação de um framework de avaliação e planeamento de IA em LO, permitindo recolher dados estruturados, gerar relatórios e apoiar decisões. A implementação deverá envolver desenho de modelo de dados, definição de fluxos de interação e validação da consistência dos resultados produzidos"

*Areas a incorporar*: Introdução à Inteligência Artificial; Raciocínio e Representação do Conhecimento; Modelação de Sistemas de Informação; Laboratório de Sistemas e Serviços Web; Ética e Práticas de Engenharia
"

Tendo por base estas diretrizes, e seguindo em especifico o Relatório inicial.pdf, devemos desenvolver o projeto. 

# Indice de desenvolvimento

## Fase 1 — Levantamento e Modelação
- [x] 1.1. Análise detalhada do Framework IALO (dimensões de maturidade, indicadores, níveis de prontidão)
- [x] 1.2. Levantamento de requisitos funcionais (fluxos de interação, regras de negócio do IALO)
- [x] 1.3. Levantamento de requisitos não-funcionais (usabilidade, escalabilidade, segurança de dados)
- [x] 1.4. Modelação entidade-relacionamento da base de dados (empresas, dimensões de maturidade, indicadores, respostas, relatórios, utilizadores)
- [x] 1.5. Diagramas de casos de uso
- [x] 1.6. Especificação da API (endpoints RESTful, payloads, autenticação)
- [x] 1.7. Prototipagem de UI/UX (wireframes/mockups dos ecrãs principais)
- [x] 1.8. Definição da arquitetura de software (padrão MVC / camadas: frontend, backend, BD)


## Fase 2 — Setup e Arquitetura
- [x] 2.1. Configuração do ambiente de desenvolvimento (repositório Git, ferramentas, linters)
- [x] 2.2. Definição da stack tecnológica (linguagens, frameworks, sistema de BD)
- [x] 2.3. Estruturação do projeto (pastas frontend/, backend/, database/, docs/)
- [x] 2.4. Criação do esquema relacional da base de dados (tabelas, relações, constraints, índices)
- [x] 2.5. Implementação de migrations e seed data inicial (dimensões IALO, indicadores base)
- [x] 2.6. Configuração de variáveis de ambiente e ficheiros de configuração
- [x] 2.7. Configuração de CI/CD básico ou scripts de build/deploy

## Fase 3 — Desenvolvimento Core
- [x] 3.1. **Backend — CRUD e Autenticação**
  - [x] 3.1.1. Sistema de autenticação de utilizadores (registo, login, sessões/JWT)
  - [x] 3.1.2. API CRUD de empresas (criar, ler, atualizar, eliminar perfis de empresas)
  - [x] 3.1.3. API CRUD de avaliações/diagnósticos
  - [x] 3.1.4. API CRUD de respostas ao questionário
  - [x] 3.1.5. Middleware de autorização e proteção de rotas
- [x] 3.2. **Motor de Scoring (O "Cérebro")**
  - [x] 3.2.1. Implementação das regras do Framework IALO em código
  - [x] 3.2.2. Algoritmos de cálculo de maturidade por dimensão (dados, infraestrutura, competências, estratégia, cultura)
  - [x] 3.2.3. Cálculo de índice global de maturidade digital
  - [x] 3.2.4. Identificação automática de gaps críticos e lacunas estruturais
  - [x] 3.2.5. Lógica fuzzy ou ponderada para cálculo de níveis de prontidão
  - [x] 3.2.6. Stored procedures / funções para cálculos complexos de maturidade
- [x] 3.3. **Integração com API de LLM (Assistente IA)**
  - [x] 3.3.1. Configuração da ligação à API Gemini (Google AI)
  - [x] 3.3.2. Prompt engineering para o assistente conversacional (system prompts, templates)
  - [x] 3.3.3. Lógica de contexto conversacional (manter histórico de conversa por sessão)
  - [x] 3.3.4. Capacidade de explicar conceitos técnicos do IALO em linguagem simples
  - [x] 3.3.5. Validação de consistência de respostas via IA (detetar contradições)
- [x] 3.4. **Questionário Interativo**
  - [x] 3.4.1. Estrutura do questionário (secções por dimensão do IALO)
  - [x] 3.4.2. Interface conversacional integrada no questionário
  - [x] 3.4.3. Lógica de navegação condicional (perguntas dependentes de respostas anteriores)
  - [x] 3.4.4. Persistência de progresso (guardar e retomar questionário)
  - [x] 3.4.5. Validação de respostas em tempo real (frontend + backend)

## Fase 4 — Geração de Relatórios e UI
- [x] 4.1. **Sistema de Relatórios**
  - [x] 4.1.1. Templates de relatório PDF (Roteiro de Implementação de IA)
  - [x] 4.1.2. Geração automática de conteúdo do relatório a partir dos resultados do scoring
  - [x] 4.1.3. Secção de pontos fortes da empresa
  - [x] 4.1.4. Secção de necessidades críticas e lacunas
  - [x] 4.1.5. Secção de primeiros passos e recomendações de ferramentas de IA acessíveis
  - [x] 4.1.6. Exportação de relatório em PDF
  - [x] 4.1.7. Visualização interativa do relatório na web
- [x] 4.2. **Dashboards e Visualizações**
  - [x] 4.2.1. Dashboard principal com resumo do diagnóstico
  - [x] 4.2.2. Gráficos radar/spider para maturidade por dimensão
  - [x] 4.2.3. Gráficos de barras/progresso para gaps identificados
  - [x] 4.2.4. Comparação entre avaliações (evolução temporal)
  - [x] 4.2.5. Indicadores visuais de nível de prontidão para IA
- [x] 4.3. **Refinamento da Interface Web**
  - [x] 4.3.1. Design responsivo (mobile, tablet, desktop)
  - [x] 4.3.2. Página de landing / apresentação do sistema
  - [x] 4.3.3. Painel de gestão de utilizador (perfil, histórico de avaliações)
  - [x] 4.3.4. Navegação intuitiva e acessível a utilizadores sem formação técnica
  - [x] 4.3.5. Feedback visual e micro-animações (loading states, transições)
- [x] 4.4. **Lógica de Recomendação**
  - [x] 4.4.1. Motor de recomendação baseado nos resultados (sugestões de ferramentas IA por perfil)
  - [x] 4.4.2. Base de dados de ferramentas IA com categorias, custo e complexidade
  - [x] 4.4.3. Matching entre perfil da empresa e ferramentas recomendadas

## Fase 5 — Testes e Validação
- [x] 5.1. Testes unitários da lógica de cálculo de scoring
- [x] 5.2. Testes unitários das APIs backend
- [x] 5.3. Testes de integração (fluxo completo: questionário → scoring → relatório)
- [x] 5.4. Testes de usabilidade com utilizadores representativos (dono de loja, gestor de microempresa)
- [x] 5.5. Validação da consistência dos relatórios gerados contra cenários pré-definidos
- [x] 5.6. Testes de segurança (autenticação, autorização, proteção de dados)
- [x] 5.7. Testes de desempenho e carga
- [x] 5.8. Correção de bugs identificados
- [x] 5.9. Validação do assistente IA (qualidade das explicações, deteção de contradições)

## Fase 6 — Documentação e Fecho
- [x] 6.1. Redação do relatório final de projeto
- [x] 6.2. Documentação técnica da arquitetura e modelação
- [x] 6.3. Manual de utilizador
- [x] 6.4. Documentação da API (Swagger / OpenAPI)
- [x] 6.5. Análise crítica da eficácia do assistente IA
- [x] 6.6. Preparação da defesa / apresentação
- [x] 6.7. Deployment de demonstração (ambiente de validação)

---

# Descrição Exaustiva do Desenvolvimento

## 1. Visão Geral do Projeto

O projeto **"Ambiente Web para Framework IALO"** consiste no desenvolvimento de uma plataforma web inteligente que operacionaliza o Framework IALO (Innovative Action Learning Organisation). O objetivo central é transformar um modelo conceptual de avaliação de maturidade em digitalização e implementação de IA numa **ferramenta prática de diagnóstico e planeamento estratégico**, direcionada a Micro e Pequenas Empresas (MPEs).

A plataforma integra três componentes fundamentais:
- Um **assistente conversacional** baseado em LLM (Large Language Model)
- Um **motor de análise** baseado em regras de scoring do Framework IALO
- Um **sistema de geração automática de relatórios** personalizados

### O Problema Endereçado
As MPEs enfrentam um "abismo digital" caracterizado por: ausência de departamentos de TI, orçamentos limitados para consultoria estratégica, e dificuldade em acompanhar a evolução das tecnologias de IA. Este projeto serve de ponte entre a formalização académica de frameworks de maturidade (tipicamente acessíveis apenas a grandes corporações) e a realidade operacional das pequenas organizações.

---

## 2. Descrição Detalhada por Fase

### Fase 1 — Levantamento e Modelação

**Objetivo**: Estabelecer a base conceptual e documental completa do projeto antes de qualquer implementação.

**Análise do Framework IALO**: Estudo aprofundado do framework, que define as dimensões de maturidade digital e prontidão para IA. As 5 dimensões-chave a modelar são: *Dados*, *Infraestrutura*, *Competências*, *Estratégia* e *Cultura*. Para cada dimensão, serão definidos indicadores, perguntas-guia e critérios de pontuação. Os níveis de prontidão serão escalonados (ex.: Inicial → Em Desenvolvimento → Definido → Gerido → Otimizado).

**Requisitos Funcionais**: Incluem os fluxos de interação do utilizador (registo → diagnóstico → resultados → relatório), as regras de negócio do IALO (fórmulas de scoring, pesos dimensionais, limiares de classificação) e as funcionalidades de gestão (CRUD de empresas, histórico de avaliações).

**Requisitos Não-Funcionais**: Usabilidade (interface acessível a utilizadores sem formação técnica), escalabilidade (arquitetura que permita crescimento futuro), segurança (proteção de dados empresariais potencialmente sensíveis) e desempenho (tempo de resposta do assistente IA aceitável).

**Modelação da Base de Dados**: Desenho do modelo entidade-relacionamento que inclui tabelas como: `utilizadores`, `empresas`, `avaliacoes`, `dimensoes_ialo`, `indicadores`, `respostas`, `resultados_scoring`, `relatorios`, `ferramentas_ia`, `recomendacoes`. Definição de chaves primárias, estrangeiras, restrições de integridade e índices.

**Diagramas UML**: Criação de diagramas de casos de uso que representem atores (empresário, administrador) e as suas interações com o sistema (realizar diagnóstico, consultar relatório, gerir avaliações).

**Especificação da API**: Documentação dos endpoints RESTful com verbos HTTP, payloads de request/response, códigos de estado, e mecanismos de autenticação (JWT tokens).

**Prototipagem UI/UX**: Wireframes e mockups dos ecrãs principais: página de entrada, registo/login, questionário interativo (com chat IA lateral), dashboard de resultados, visualização de relatório, e painel de gestão.

---

### Fase 2 — Setup e Arquitetura

**Objetivo**: Preparar toda a infraestrutura técnica do projeto.

**Stack Tecnológica**: Definição das tecnologias a usar. Sugestão base: Python/Flask ou Node.js para o backend; HTML/CSS/JavaScript (com possível framework como React ou Vue) para o frontend; SQLite ou PostgreSQL para a base de dados; integração com APIs de LLM (OpenAI, Claude, ou modelo open-source local como Ollama).

**Estruturação do Projeto**: Organização do repositório em pastas lógicas: `frontend/` (código do cliente), `backend/` (servidor e API), `database/` (migrations e seeds), `docs/` (documentação), `tests/` (testes automatizados).

**Implementação do Esquema de BD**: Criação das tabelas e relações definidas na Fase 1, incluindo migrations versionadas para controlo de alterações ao esquema. Inserção de dados iniciais (seed) com as dimensões do Framework IALO, indicadores de referência e tabelas de lookup.

**Configuração do Ambiente**: Ficheiros `.env` para variáveis sensíveis (chaves API, credenciais BD), ficheiros de configuração para diferentes ambientes (dev, test, prod), e scripts de setup automatizado.

---

### Fase 3 — Desenvolvimento Core

**Objetivo**: Implementar toda a lógica funcional central da aplicação.

#### 3.1. Backend — CRUD e Autenticação
Sistema completo de gestão de utilizadores com registo (email, password hashed com bcrypt/argon2), login com emissão de JWT, middleware de proteção de rotas, e gestão de sessões. APIs RESTful completas para gestão de empresas (perfil, setor, dimensão, localização), avaliações (criar nova, listar historial, ver detalhes), e respostas ao questionário (guardar, atualizar, eliminar).

#### 3.2. Motor de Scoring — O "Cérebro" do Sistema
Esta é a componente mais criticamente técnica do projeto. O motor implementa computacionalmente as regras do Framework IALO:

- **Scoring por dimensão**: Cada uma das 5 dimensões (Dados, Infraestrutura, Competências, Estratégia, Cultura) recebe uma pontuação baseada nas respostas do questionário. Os algoritmos aplicam pesos configuráveis a cada indicador.
- **Índice global de maturidade**: Agregação ponderada das pontuações dimensionais num índice global que classifica a empresa num nível de maturidade (ex.: 1-Inicial a 5-Otimizado).
- **Identificação de gaps**: Comparação da pontuação de cada dimensão contra limiares de referência para identificar lacunas críticas (ex.: "a empresa tem boa estratégia mas infraestrutura insuficiente").
- **Lógica fuzzy/ponderada**: Para lidar com a imprecisão inerente às respostas qualitativas (ex.: "usamos dados parcialmente" não é binário), o motor pode usar lógica fuzzy para gradações de maturidade.
- **Stored procedures**: Funções de BD para cálculos complexos que beneficiem de execução no servidor de dados (agregações, médias ponderadas por setor).

#### 3.3. Integração com LLM — Assistente IA
O assistente de IA é o diferencial do projeto. Implementa-se:

- **Configuração da API**: Ligação segura à API do LLM escolhido, com gestão de tokens, retry logic e fallback.
- **Prompt Engineering**: Design cuidadoso dos system prompts que definem o comportamento do assistente — deve atuar como "consultor amigável" que conhece o Framework IALO, traduz jargão técnico em linguagem do dia-a-dia, e guia o empresário pelas perguntas. Exemplo: explicar "dados estruturados" usando o exemplo do sistema de facturação da empresa.
- **Contexto conversacional**: Manutenção do histórico de conversa por sessão para que o assistente se lembre de respostas anteriores e possa fazer referências cruzadas (ex.: "Mencionou que usa WhatsApp para clientes — isso já é uma forma de canal digital!").
- **Validação de consistência**: O assistente deteta contradições nas respostas (ex.: "não temos dados digitais" vs. "usamos ERP há 5 anos") e alerta o utilizador de forma pedagógica.

#### 3.4. Questionário Interativo
Interface web onde o utilizador responde às perguntas do Framework IALO com apoio do assistente IA:

- **Estrutura por secções**: O questionário é organizado pelas 5 dimensões do IALO, com perguntas específicas por indicador.
- **Chat lateral**: Um painel de chat integrado no questionário permite ao utilizador pedir esclarecimentos ao assistente IA a qualquer momento.
- **Navegação condicional**: Perguntas que aparecem ou desaparecem conforme respostas anteriores (ex.: se a empresa não tem presença online, não faz sentido perguntar sobre analytics web).
- **Persistência de progresso**: O utilizador pode guardar o questionário a meio e retomar mais tarde sem perder dados.
- **Validação em tempo real**: Verificação imediata de respostas obrigatórias, formatos inválidos, e alertas de inconsistência.

---

### Fase 4 — Geração de Relatórios e UI

**Objetivo**: Desenvolver a camada de output do sistema e polir a interface.

#### 4.1. Sistema de Relatórios — Roteiro de Implementação de IA
O produto final que o utilizador recebe. O relatório inclui:

- **Pontos Fortes**: O que a empresa já faz bem em termos de digitalização e potencial para IA.
- **Necessidades Críticas**: Lacunas identificadas por dimensão, priorizadas por impacto.
- **Primeiros Passos**: Recomendações concretas e acionáveis com ferramentas de IA de baixo custo e alta acessibilidade (ex.: "Usar ChatGPT para automatizar respostas a clientes no WhatsApp", "Implementar Google Sheets + AppSheet para gestão de stock").
- **Exportação PDF**: Geração de documento PDF formatado profissionalmente com logótipo, gráficos e texto estruturado.
- **Visualização Web**: Versão interativa do relatório acessível no browser, com gráficos dinâmicos e possibilidade de drill-down.

#### 4.2. Dashboards e Visualizações
Painéis visuais que apresentam os resultados de forma imediata e compreensível:

- **Gráfico radar/spider**: Visualização das 5 dimensões de maturidade numa estrela, tornando imediatamente visível quais as áreas fortes e fracas.
- **Barras de progresso**: Para cada dimensão e indicador, mostrando a pontuação relativa ao máximo possível.
- **Comparação temporal**: Se a empresa repetir o diagnóstico no futuro, o dashboard permite comparar a evolução entre avaliações.
- **Indicadores semáforo**: Vermelho/amarelo/verde para comunicar de forma instantânea o nível de prontidão por área.

#### 4.3. Interface Web
Refinamento completo da experiência do utilizador:

- **Responsividade**: Layout adaptável a ecrãs de diferentes tamanhos, garantindo que empresários possam usar a aplicação no telemóvel ou tablet.
- **Landing Page**: Página de apresentação que explica o que é o Framework IALO, o que o sistema oferece, e como começar.
- **Painel de Gestão**: Área pessoal onde o utilizador vê as suas avaliações anteriores, acede a relatórios guardados e gere o perfil da empresa.
- **Acessibilidade**: Design orientado a utilizadores sem formação técnica, com linguagem clara, ícones descritivos e percursos de navegação simples.

#### 4.4. Motor de Recomendação
Sistema que cruza os resultados do diagnóstico com uma base de dados de ferramentas de IA:

- **Catálogo de ferramentas**: Base de dados com ferramentas de IA categorizadas por área (atendimento, gestão, marketing, operações), custo (gratuito, freemium, pago) e nível de complexidade técnica.
- **Matching inteligente**: Algoritmo que, com base no perfil da empresa (setor, dimensão, pontuação por dimensão), seleciona as ferramentas mais adequadas e prioriza-as.

---

### Fase 5 — Testes e Validação

**Objetivo**: Garantir que o sistema funciona corretamente, de forma consistente e segura.

- **Testes unitários**: Cobertura da lógica de scoring (verificar que as fórmulas produzem os resultados esperados para inputs conhecidos), das APIs (verificar respostas corretas para cada endpoint) e das validações.
- **Testes de integração**: Fluxo end-to-end desde o preenchimento do questionário até à geração do relatório, verificando que todos os componentes interagem corretamente.
- **Testes de usabilidade**: Sessões com utilizadores representativos (donos de pequenas lojas, gestores de microempresas) para identificar pontos de fricção na interface e na interação com o assistente IA.
- **Validação de consistência do IALO**: Criação de cenários de teste pré-definidos (empresas fictícias com perfis conhecidos) e verificação de que os relatórios gerados são coerentes e acionáveis.
- **Testes de segurança**: Verificação de autenticação, autorização, proteção contra SQL injection, XSS, e garantia de privacidade dos dados empresariais.
- **Validação do assistente IA**: Avaliação da qualidade das explicações, da capacidade de detetar contradições, e da utilidade percebida pelos utilizadores de teste.

---

### Fase 6 — Documentação e Fecho

**Objetivo**: Produzir toda a documentação necessária e preparar a entrega final.

- **Relatório Final**: Documento académico completo com introdução, estado da arte, metodologia, arquitetura, implementação, resultados, conclusões e trabalho futuro.
- **Documentação Técnica**: Descrição da arquitetura do sistema, modelação de dados (diagramas ER), documentação da API (Swagger/OpenAPI), e guia de instalação/deployment.
- **Manual de Utilizador**: Guia passo-a-passo de como usar a plataforma, com screenshots e exemplos, orientado ao público-alvo (empresários sem formação técnica).
- **Análise Crítica da IA**: Secção do relatório dedicada à avaliação da eficácia do assistente conversacional: quantas vezes foi útil, que limitações tem, comparação entre respostas com e sem assistente.
- **Defesa/Apresentação**: Preparação de slides e demonstração funcional do sistema.
- **Deployment de Demonstração**: Colocação do sistema num servidor acessível para efeitos de demonstração na defesa e avaliação.
