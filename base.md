
# Proposta inicial ao professor
Enquadrado na proposta **nº9** da lista sugerida, sob o tema “Ambiente web para Framework IALO (Inteligência Artificial em LO)”. Professor: **Arnaldo Santos**.

Pretende-se desenvolver uma aplicação web para apoiar diagnóstico e planeamento de adoção de digitalização e IA em contexto organizacional (LO). A solução inclui recolha estruturada de dados, aplicação de regras de scoring, geração de relatórios e visualização de resultados para suporte à decisão. O projeto será construído com foco em arquitetura modular (frontend, backend, base de dados), garantindo clareza no modelo de dados, consistência nos cálculos e possibilidade de evolução futura.
No plano técnico, serão usadas práticas típicas de projeto: definição de requisitos, modelação de entidades, implementação incremental, testes de funcionalidade,documentação e validação com casos de uso reais/simulados.

# O que está no excel do professor 
*Titulo*: "Ambiente web para Framework IALO (Inteligência Artificial em LO)"

*Descrição*: "A integração de Inteligência Artificial em contextos organizacionais requer instrumentos que permitam avaliar maturidade, necessidades e estratégias de implementação. A formalização computacional de um framework de análise constitui uma oportunidade para articular modelação conceptual e desenvolvimento aplicacional.
O projeto consiste na conceção e desenvolvimento de um ambiente web que suporte a aplicação de um framework de avaliação e planeamento de IA em LO, permitindo recolher dados estruturados, gerar relatórios e apoiar decisões. A implementação deverá envolver desenho de modelo de dados, definição de fluxos de interação e validação da consistência dos resultados produzidos"

*Areas*: Introdução à Inteligência Artificial; Raciocínio e Representação do Conhecimento; Modelação de Sistemas de Informação; Laboratório de Sistemas e Serviços Web; Ética e Práticas de Engenharia

# Minha descrição do projeto
Como funciona o projeto (na prática):
Podemos dividir o que temos de fazer em três partes principais:

-> O Questionário Inteligente: Vais criar um ambiente onde as pessoas da organização inserem dados. Em vez de um papel ou Excel desorganizado, usam a aplicação para responder a perguntas sobre a situação atual deles. Uma IA interativa estará presente para guiar o utilizador ao longo do questionário se necessário. 

-> O "Cérebro" (O Framework IALO): A aplicação vai usar as regras desse "Framework IALO" para processar as respostas. Ele vai analisar se a empresa tem maturidade (conhecimento e recursos) e o que lhe falta. IA auxilia na análise e interpretação dos dados e ajusta á realidade individual da empresa.

-> O Resultado Final: A aplicação gera relatórios automáticos. Basicamente, a aplicação diz à empresa: "Estão aqui, precisam disto e o vosso plano de ação deve ser este".

O que vou ter de desenvolver:
Base de Dados: Vou ter de desenhar como a informação será guardada de forma organizada.

Interface (Design): Vou ter de criar os ecrãs por onde o utilizador vai navegar.

Lógica de Programação: Vou ter de garantir que os cálculos e os relatórios batem certo com o que o framework define.



*Projeto IA-IALO: Democratizando a Inteligência Artificial para MPEs*

- 1. **O Problema**: O "Abismo Digital"As micro e pequenas empresas enfrentam dois grandes obstáculos na adoção de novas tecnologias:
    - *Falta de Estrutura*: Não têm departamentos de TI ou especialistas em estratégia.
    - *Velocidade da Evolução*: A IA avança tão rápido que os pequenos empresários sentem-se perdidos e acabam por não adotar nada por medo ou desconhecimento.

- 2. **A Solução**: Framework IALO + Assistente Inteligente. O objetivo deste projeto é transformar um framework técnico e conceptual (o IALO) num guia prático e conversacional. Não será apenas um site com formulários; será um ambiente onde um Agente de IA acompanha o empresário.
    - O que o sistema faz:
        - *Diagnóstico Humanizado*: Em vez de perguntas técnicas complexas, o sistema utiliza um chatbot de IA para "conversar" com o empresário e entender o seu negócio, seguindo uma estrutura pré definida na framework IALO. 
        - *Avaliação de Maturidade*: O "cérebro" do sistema (Framework IALO) analisa as respostas para perceber se a empresa está pronta para a IA.
        - *Plano de Ação Traduzido*: Gera um relatório que explica, em termos simples, que evolução necessita em termos de digitalização e onde a IA pode ajudar (ex: "Usar IA para responder a clientes no WhatsApp").

- 3. *Como funciona (Traços Gerais)* 
-> O projeto assenta em três camadas principais:
    - *Camada 1*: Interface web - *Descrição*: Um painel simples e intuitivo onde o utilizador interage com o sistema.
    - *Camada 2*: Interação com IA - *Descrição*: Um assistente (LLM) que serve de tradutor. Ele explica os conceitos do framework e ajuda o utilizador a responder às questões.
    - *Camada 3*: Motor de Análise - *Descrição*: A lógica do Framework IALO que processa os dados e gera o nível de maturidade e recomendações.

- 4. *Diferencial*: A IA ao serviço do utilizador
A grande inovação aqui é que a própria ferramenta exemplifica o benefício da IA enquanto avalia a empresa.
    - *Interatividade*: Se o empresário não entende o que é "recolha de dados estruturados", o assistente de IA explica com um exemplo do dia-a-dia daquela loja ou oficina específica.
    - *Validação*: A IA verifica se as respostas do utilizador são consistentes, evitando diagnósticos errados por falta de compreensão das perguntas

- 5. *Resultado Esperado*
No final da utilização, o dono da pequena empresa recebe um Roteiro de Implementação de IA. Este documento dirá:
    - O que a empresa já tem (Pontos Fortes).
    - O que precisa de melhorar (Necessidades).
    - Primeiros Passos: Sugestões de ferramentas de IA acessíveis e de baixo custo para o seu caso específico.

*Integrações* - API de IA