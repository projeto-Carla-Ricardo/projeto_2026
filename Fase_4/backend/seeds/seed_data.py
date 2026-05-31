"""Seed data completo para o framework AILO — 6 camadas, 23 componentes, 51 indicadores."""

CAMADAS = [
    {'nome': 'Organizacional', 'nome_en': 'Organizational', 'descricao': 'Liga a aprendizagem organizacional à estratégia, processos, decisão e criação de valor.', 'peso': 1.0, 'ordem': 1, 'cor': '#2E4057', 'icone': 'building'},
    {'nome': 'Humana', 'nome_en': 'Human', 'descricao': 'Fundação da aprendizagem: pessoas, cultura, autonomia e ética.', 'peso': 1.2, 'ordem': 2, 'cor': '#048A81', 'icone': 'users'},
    {'nome': 'Aprendizagem', 'nome_en': 'Learning', 'descricao': 'Contextos, experiências e processos de aprendizagem organizacional.', 'peso': 1.0, 'ordem': 3, 'cor': '#54C6EB', 'icone': 'book-open'},
    {'nome': 'Cognitiva (IA)', 'nome_en': 'Cognitive (AI)', 'descricao': 'IA como mediador cognitivo: geração, recomendação, síntese e previsão.', 'peso': 1.0, 'ordem': 4, 'cor': '#8EE3EF', 'icone': 'cpu'},
    {'nome': 'Tecnológica', 'nome_en': 'Technological', 'descricao': 'Infraestrutura que suporta o ecossistema AILO.', 'peso': 0.8, 'ordem': 5, 'cor': '#7C77B9', 'icone': 'server'},
    {'nome': 'Avaliação', 'nome_en': 'Evaluation', 'descricao': 'Processo contínuo e formativo que fecha o ciclo de aprendizagem.', 'peso': 1.0, 'ordem': 6, 'cor': '#E8567F', 'icone': 'bar-chart'},
]

# Componentes por camada (camada_ordem, nome, nome_en, descricao, peso, ordem)
COMPONENTES = [
    # Camada 1 — Organizacional
    (1, 'Estratégia', 'Strategy', 'Alinhamento entre aprendizagem, inovação e objetivos organizacionais.', 1.0, 1),
    (1, 'Processos', 'Processes', 'Integração da aprendizagem nos fluxos de trabalho e rotinas de gestão.', 1.0, 2),
    (1, 'Decisão', 'Decision-Making', 'Utilização de evidência suportada por IA preservando julgamento humano.', 1.0, 3),
    (1, 'Valor', 'Value', 'Impacto no desempenho, inovação, resiliência e sustentabilidade.', 1.0, 4),
    # Camada 2 — Humana
    (2, 'Pessoas', 'People', 'Aprendentes, formadores, líderes, decisores.', 1.0, 1),
    (2, 'Cultura', 'Culture', 'Valores de reflexão, experimentação, aprendizagem coletiva.', 1.0, 2),
    (2, 'Autonomia', 'Autonomy', 'Capacidade de questionar e sobrepor-se a recomendações algorítmicas.', 1.0, 3),
    (2, 'Ética', 'Ethics', 'Transparência, privacidade, equidade, responsabilização.', 1.0, 4),
    # Camada 3 — Aprendizagem
    (3, 'Contextos Adaptativos', 'Adaptive Contexts', 'Ambientes personalizados a perfis e necessidades.', 1.0, 1),
    (3, 'Experiências Personalizadas', 'Personalized Experiences', 'Microlearning, simulações, conteúdos multimodais.', 1.0, 2),
    (3, 'Integração Formal-Informal', 'Formal-Informal Integration', 'Conexão entre formação e aprendizagem no trabalho.', 1.0, 3),
    # Camada 4 — Cognitiva (IA)
    (4, 'Geração', 'Generation', 'Produção de explanações, exemplos, cenários, avaliações.', 1.0, 1),
    (4, 'Recomendação', 'Recommendation', 'Sugestão de recursos, atividades, especialistas, comunidades.', 1.0, 2),
    (4, 'Síntese', 'Synthesis', 'Agregação e interpretação de grandes volumes de informação.', 1.0, 3),
    (4, 'Previsão', 'Prediction', 'Antecipação de gaps, necessidades e impactos.', 1.0, 4),
    # Camada 5 — Tecnológica
    (5, 'Plataformas', 'Platforms', 'LMS, LXP, ferramentas de colaboração, serviços de IA.', 1.0, 1),
    (5, 'Dados', 'Data', 'Recolha, governação, qualidade, linhagem, controlos de acesso.', 1.0, 2),
    (5, 'Integração', 'Integration', 'Interoperabilidade via APIs entre sistemas.', 1.0, 3),
    (5, 'Segurança e Conformidade', 'Security & Compliance', 'Privacidade, cibersegurança, alinhamento regulatório.', 1.0, 4),
    # Camada 6 — Avaliação
    (6, 'Evidência de Aprendizagem', 'Learning Evidence', 'Traces digitais, artefactos, outputs de colaboração.', 1.0, 1),
    (6, 'Avaliação Formativa Contínua', 'Continuous Formative Assessment', 'Feedback iterativo via learning analytics + facilitação humana.', 1.0, 2),
    (6, 'Avaliação de Competências', 'Competency Assessment', 'Mobilização de conhecimento em situações reais.', 1.0, 3),
    (6, 'Impacto Organizacional', 'Organizational Impact', 'Ligações entre aprendizagem, desempenho, inovação e valor.', 1.0, 4),
]

# Indicadores: (camada_ordem, comp_ordem, codigo, pergunta, n1, n3, n5, peso, ordem)
INDICADORES = [
    # === CAMADA 1: ORGANIZACIONAL ===
    # Estratégia
    (1,1,'O.E.1','Qual o nível de alinhamento entre a estratégia de aprendizagem e os objetivos da organização?','Sem ligação formal entre aprendizagem e estratégia','Plano de formação alinhado com objetivos estratégicos','Aprendizagem integrada no planeamento estratégico com KPIs',1.0,1),
    (1,1,'O.E.2','Existe uma visão estratégica para a utilização de IA na organização?','Sem visão definida para IA','Estratégia de IA documentada e comunicada','IA como pilar estratégico com roadmap ativo e revisão periódica',1.0,2, 'O.E.1 >= 3'),
    (1,1,'O.E.3','Qual o nível de investimento em aprendizagem e tecnologias de IA?','Sem orçamento dedicado','Orçamento anual definido para formação e IA','Investimento com ROI medido e otimizado continuamente',1.0,3),
    # Processos
    (1,2,'O.P.1','A aprendizagem está integrada nos fluxos de trabalho diários?','Aprendizagem separada do trabalho','Momentos de aprendizagem integrados em processos','Aprendizagem contínua embebida em todos os processos',1.0,4),
    (1,2,'O.P.2','Existem processos formais de gestão do conhecimento?','Sem processos formais de gestão do conhecimento','Repositórios e práticas documentadas','KMS integrado com IA e analytics avançados',1.0,5),
    (1,2,'O.P.3','Existem ciclos de melhoria contínua na organização?','Sem ciclos de melhoria definidos','PDCA ou equivalente implementado','Ciclos automatizados com feedback de IA e dados em tempo real',1.0,6),
    # Decisão
    (1,3,'O.D.1','Como são tomadas as decisões na organização?','Decisões baseadas principalmente em intuição','Dashboards e métricas utilizados para apoio à decisão','Decisão augmentada por IA com human-in-the-loop',1.0,7),
    (1,3,'O.D.2','Existe um framework de governação de IA?','Sem governação de IA','Políticas básicas de uso de IA definidas','Framework de governação completo com monitorização contínua',1.0,8),
    # Valor
    (1,4,'O.V.1','Como é medido o impacto da aprendizagem na organização?','Sem medição de impacto','Indicadores de satisfação e participação medidos','ROI quantificado com impacto demonstrado no desempenho',1.0,9),
    (1,4,'O.V.2','A IA contribui para a inovação na organização?','Sem ligação entre IA e inovação','IA usada em projetos piloto de inovação','IA como motor de inovação sistemática e contínua',1.0,10),
    # Extra indicator to reach 11 for Organizacional
    (1,4,'O.V.3','A organização mede o valor gerado pela integração de IA nos processos de aprendizagem?','Sem medição do valor da IA na aprendizagem','Métricas básicas de adoção de IA','Valor da IA quantificado com impacto na sustentabilidade organizacional',1.0,11),

    # === CAMADA 2: HUMANA ===
    # Pessoas
    (2,1,'H.P.1','Qual o nível de literacia digital dos colaboradores?','Competências digitais básicas ausentes em muitos colaboradores','Formação digital regular para a maioria','Competências digitais avançadas e continuamente atualizadas',1.0,1),
    (2,1,'H.P.2','Os colaboradores compreendem as capacidades e limitações da IA?','Desconhecimento generalizado sobre IA','Formação básica em IA realizada','Compreensão crítica das capacidades e limitações da IA',1.0,2),
    (2,1,'H.P.3','A liderança promove ativamente a aprendizagem contínua?','Liderança não promove aprendizagem','Líderes incentivam formação pontualmente','Liderança modela e integra aprendizagem contínua no dia-a-dia',1.0,3),
    # Cultura
    (2,2,'H.C.1','Existe uma cultura de experimentação e tolerância ao erro?','Medo de errar inibe experimentação','Experimentação permitida em contextos controlados','Cultura fail-fast com aprendizagem sistemática a partir de erros',1.0,4),
    (2,2,'H.C.2','Como é a partilha de conhecimento entre equipas?','Silos de informação entre departamentos','Práticas de partilha de conhecimento existem','Cultura aberta com comunidades de prática ativas e suportadas',1.0,5, 'H.C.1 >= 3'),
    (2,2,'H.C.3','Qual a abertura da organização à mudança?','Resistência generalizada à mudança','Mudança aceite quando bem justificada','Organização adaptativa, proativa e orientada à mudança',1.0,6),
    # Autonomia
    (2,3,'H.A.1','Os colaboradores avaliam criticamente os outputs de IA?','Aceitação cega dos outputs de IA','Questionamento ocasional de resultados de IA','Avaliação crítica sistemática de todas as recomendações de IA',1.0,7),
    (2,3,'H.A.2','Os colaboradores têm autonomia na sua aprendizagem?','Aprendizagem totalmente prescrita pela organização','Mix entre aprendizagem prescrita e autodirigida','Aprendizagem autodirigida e personalizada com suporte organizacional',1.0,8),
    # Ética
    (2,4,'H.E.1','Existe consciência ética no uso de IA?','Sem consciência ética sobre uso de IA','Princípios éticos definidos e comunicados','Framework ético ativo com monitorização e auditoria regulares',1.0,9),
    (2,4,'H.E.2','Como são tratados os dados pessoais e a privacidade?','Sem políticas de privacidade definidas','RGPD implementado com procedimentos básicos','Privacy-by-design com auditorias regulares e formação contínua',1.0,10),

    # === CAMADA 3: APRENDIZAGEM ===
    # Contextos Adaptativos
    (3,1,'A.C.1','Qual o nível de personalização dos percursos de aprendizagem?','One-size-fits-all para todos os colaboradores','Percursos diferenciados por perfil ou função','IA gera percursos adaptativos individualizados em tempo real',1.0,1),
    (3,1,'A.C.2','Que ambientes de aprendizagem estão disponíveis?','Apenas formação presencial em sala','LMS com conteúdos online disponíveis','Ecossistema multimodal e adaptativo com múltiplos canais',1.0,2),
    # Experiências Personalizadas
    (3,2,'A.E.1','Qual a diversidade de formatos de aprendizagem?','Apenas texto e slides','Vídeo, quizzes e exercícios práticos disponíveis','Microlearning, simulações, IA generativa e gamificação integrados',1.0,3),
    (3,2,'A.E.2','Os conteúdos são relevantes para o contexto real dos aprendentes?','Conteúdos genéricos sem adaptação','Conteúdos adaptados ao setor de atividade','Conteúdos personalizados ao contexto real de cada aprendente',1.0,4),
    # Integração Formal-Informal
    (3,3,'A.I.1','Existe ligação entre a formação formal e a aprendizagem no trabalho?','Formação desligada do contexto de trabalho','Projetos aplicados pós-formação implementados','Aprendizagem contínua integrada no workflow diário',1.0,5),
    (3,3,'A.I.2','Existem comunidades de prática na organização?','Comunidades inexistentes','Comunidades formais estabelecidas','Comunidades ativas com suporte de IA e analytics',1.0,6),

    # === CAMADA 4: COGNITIVA (IA) ===
    # Geração
    (4,1,'C.G.1','Como é utilizada a IA generativa na organização?','Sem utilização de IA generativa','Uso pontual de ferramentas como ChatGPT','IA generativa integrada em processos de criação de conteúdo',1.0,1),
    (4,1,'C.G.2','Qual a qualidade dos outputs gerados por IA?','N/A — sem utilização','Outputs requerem revisão significativa','Outputs fiáveis com supervisão humana mínima',1.0,2),
    # Recomendação
    (4,2,'C.R.1','Existem sistemas de recomendação de conteúdos?','Sem recomendações automatizadas','Recomendações básicas (popular/recente)','Recomendações contextuais baseadas em perfil e comportamento',1.0,3),
    (4,2,'C.R.2','Qual o nível de personalização por IA?','Sem personalização por IA','Segmentação por grupos de utilizadores','Personalização individual em tempo real com IA',1.0,4),
    # Síntese
    (4,3,'C.S.1','Como é feita a síntese de informação?','Processo manual de síntese','IA auxilia na criação de resumos e sumários','IA sintetiza informação multi-fonte automaticamente',1.0,5),
    (4,3,'C.S.2','São utilizados learning analytics?','Sem learning analytics','Métricas básicas de participação e notas','Analytics avançados com identificação de padrões e previsões',1.0,6),
    # Previsão
    (4,4,'C.P.1','A organização antecipa necessidades de formação?','Abordagem totalmente reativa','Análises retrospetivas periódicas','Modelos preditivos para gaps de competências futuros',1.0,7),
    (4,4,'C.P.2','Existe capacidade de antecipar riscos relacionados com IA?','Sem capacidade de antecipação de riscos','Alertas básicos configurados','Previsão proativa de riscos e oportunidades com IA',1.0,8),

    # === CAMADA 5: TECNOLÓGICA ===
    # Plataformas
    (5,1,'T.P.1','Que plataforma de aprendizagem é utilizada?','Sem plataforma de aprendizagem','LMS implementado e em uso','Ecossistema LMS/LXP com IA integrada',1.0,1),
    (5,1,'T.P.2','Que ferramentas de colaboração estão disponíveis?','Apenas email para comunicação','Ferramentas de colaboração ativas (Teams/Slack)','Suite integrada de colaboração com IA assistente',1.0,2),
    # Dados
    (5,2,'T.D.1','Existe governação de dados na organização?','Sem governação de dados','Políticas básicas de dados definidas','Framework de governação com lineage e qualidade monitorizada',1.0,3),
    (5,2,'T.D.2','Qual a qualidade dos dados disponíveis?','Dados fragmentados e inconsistentes','Dados centralizados e limpos','Data quality management contínuo com processos automatizados',1.0,4),
    # Integração
    (5,3,'T.I.1','Os sistemas da organização são interoperáveis?','Sistemas isolados sem integração','Integrações pontuais entre sistemas principais','APIs e standards de interoperabilidade implementados plenamente',1.0,5),
    (5,3,'T.I.2','A IA está integrada nos sistemas existentes?','IA usada como ferramenta standalone','IA integrada em alguns processos','IA integrada no stack tecnológico completo',1.0,6),
    # Segurança e Conformidade
    (5,4,'T.S.1','Qual o nível de cibersegurança da organização?','Cibersegurança básica ou inexistente','Controlos de segurança implementados','Segurança por design com monitorização contínua',1.0,7),
    (5,4,'T.S.2','A organização está em conformidade regulatória?','Sem conformidade formal','RGPD parcialmente implementado','Conformidade plena com RGPD, AI Act e ISO 42001',1.0,8),

    # === CAMADA 6: AVALIAÇÃO ===
    # Evidência de Aprendizagem
    (6,1,'V.E.1','Como é feita a recolha de evidências de aprendizagem?','Sem recolha sistemática de evidências','Registos de participação e presença','Traces digitais, artefactos e portfolios diversificados',1.0,1),
    (6,1,'V.E.2','Qual a diversidade das evidências recolhidas?','Apenas registos de presença','Testes e avaliações formais','Multi-fonte: comportamento, output, colaboração e reflexão',1.0,2),
    # Avaliação Formativa Contínua
    (6,2,'V.F.1','Como é dado feedback aos aprendentes?','Sem feedback estruturado','Feedback periódico em momentos formais','Feedback contínuo informado por analytics e facilitação humana',1.0,3),
    (6,2,'V.F.2','São utilizados learning analytics para avaliação?','Sem uso de learning analytics','Dashboards básicos disponíveis','Analytics avançados para intervenção proativa e personalizada',1.0,4),
    # Avaliação de Competências
    (6,3,'V.C.1','Como são avaliadas as competências?','Apenas testes escritos','Avaliação em projetos e contextos aplicados','Avaliação contínua em situações reais de trabalho',1.0,5),
    (6,3,'V.C.2','Existe um framework de competências atualizado?','Sem framework de competências','Competências definidas por função','Framework dinâmico atualizado com suporte de IA',1.0,6),
    # Impacto Organizacional
    (6,4,'V.I.1','O impacto da aprendizagem no desempenho é medido?','Sem medição de impacto','Métricas de satisfação recolhidas','Impacto no desempenho, inovação e valor quantificado',1.0,7),
    (6,4,'V.I.2','Existem ciclos de melhoria baseados em avaliação?','Sem ciclos de melhoria','Revisões anuais dos programas','Ciclo contínuo aprender→aplicar→transformar→reaprender',1.0,8),
]

FERRAMENTAS_IA = [
    ('Google Gemini', 'IA generativa multimodal da Google para criação de conteúdos, análise e assistência.', 4, 'aprendizagem', 'freemium', 'media', 'https://gemini.google.com'),
    ('ChatGPT', 'IA conversacional da OpenAI para geração de texto, análise e apoio à decisão.', 4, 'aprendizagem', 'freemium', 'media', 'https://chat.openai.com'),
    ('Moodle', 'LMS open-source para gestão de aprendizagem com plugins de IA.', 5, 'aprendizagem', 'gratuito', 'media', 'https://moodle.org'),
    ('Microsoft 365 Copilot', 'IA integrada na suite Microsoft para produtividade e colaboração.', 5, 'automacao', 'pago', 'baixa', 'https://copilot.microsoft.com'),
    ('Power BI', 'Plataforma de analytics e visualização de dados da Microsoft.', 6, 'analytics', 'freemium', 'media', 'https://powerbi.microsoft.com'),
    ('Notion AI', 'Workspace colaborativo com IA integrada para gestão de conhecimento.', 1, 'comunicacao', 'freemium', 'baixa', 'https://notion.so'),
    ('Coursera for Business', 'Plataforma de aprendizagem corporativa com percursos personalizados.', 3, 'aprendizagem', 'pago', 'baixa', 'https://coursera.org/business'),
    ('Synthesia', 'Criação de vídeos de formação com avatares IA.', 4, 'aprendizagem', 'pago', 'media', 'https://synthesia.io'),
    ('Degreed', 'LXP com recomendações de aprendizagem personalizadas por IA.', 3, 'aprendizagem', 'pago', 'alta', 'https://degreed.com'),
    ('Slack + IA', 'Comunicação empresarial com automações e IA integrada.', 5, 'comunicacao', 'freemium', 'baixa', 'https://slack.com'),
]
