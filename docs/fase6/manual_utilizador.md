# Manual de Utilizador — IALO

## 1. Introdução

O **IALO** (Innovative Action Learning Organisation) é uma plataforma web de diagnóstico de maturidade digital para Micro e Pequenas Empresas (MPEs). Através de um questionário interativo assistido por IA, o sistema analisa 5 dimensões de prontidão digital e gera um relatório personalizado com recomendações práticas.

### Para quem é o IALO?

- Donos de pequenas empresas (padarias, cafés, lojas, oficinas)
- Gestores de microempresas em processo de digitalização
- Consultores de transformação digital
- Investigadores na área de maturidade digital

---

## 2. Primeiros Passos

### 2.1 Criar Conta

1. Abra o IALO no browser
2. Clique em **"Começar Diagnóstico Gratuito"** ou **"Entrar"**
3. Na página de registo, preencha:
   - **Nome completo**
   - **Email**
   - **Password** (mínimo 8 caracteres)
4. Clique em **"Criar Conta"**
5. Será automaticamente redirecionado para o Dashboard

### 2.2 Entrar (Login)

1. Aceda à página de login
2. Introduza o email e password da conta criada
3. Clique em **"Entrar"**

---

## 3. Dashboard

### 3.1 Visão Geral

O Dashboard mostra um resumo da atividade:

| Card | Informação |
|------|-----------|
| 🏢 **Empresas** | Número total de empresas registadas |
| 📊 **Diagnósticos** | Total de avaliações realizadas |
| ✅ **Concluídos** | Diagnósticos finalizados |
| 🎯 **Média** | Pontuação média das avaliações concluídas |

### 3.2 Criar Empresa

1. Clique em **"+ Nova Empresa"**
2. Preencha o formulário:
   - **Nome da empresa** (obrigatório)
   - **Setor de atividade** (obrigatório): Alimentar, Comércio, Serviços, etc.
   - **Nº de colaboradores** (opcional)
   - **Localização** (opcional)
   - **Descrição** (opcional)
3. Clique em **"Criar"**

### 3.3 Iniciar Diagnóstico

1. Na secção **Empresas**, localize a empresa desejada
2. Clique em **"🔍 Novo Diagnóstico"**
3. Será redirecionado para o questionário

---

## 4. Questionário

### 4.1 Estrutura

O questionário contém **25 perguntas** organizadas em **5 dimensões**:

| Dimensão | Sigla | O que avalia |
|----------|-------|-------------|
| Dados | DADOS | Como a empresa recolhe e usa dados |
| Infraestrutura | INFRA | Equipamento e ferramentas digitais |
| Competências | COMP | Capacidades digitais da equipa |
| Estratégia | ESTR | Plano e visão de digitalização |
| Cultura | CULT | Abertura à mudança e inovação |

### 4.2 Como Responder

- Use os **botões de escala** (1-5) para avaliar cada área
- Ou selecione a **opção** que melhor descreve a sua situação
- Pode navegar entre dimensões clicando nas **tabs** no topo

### 4.3 Assistente IA

No painel lateral, tem acesso ao **Assistente IALO** que pode:
- Explicar o significado de cada pergunta
- Ajudar a decidir qual opção escolher
- Dar exemplos concretos do seu setor

**Para usar:** Escreva a sua dúvida no campo de texto e carregue Enter.

### 4.4 Guardar Progresso

- Clique em **"💾 Guardar Progresso"** a qualquer momento
- Pode fechar o browser e continuar mais tarde
- O progresso é guardado automaticamente

### 4.5 Concluir

- Após responder a todas as perguntas, clique em **"Concluir Diagnóstico"**
- O sistema calcula automaticamente a pontuação
- Será redirecionado para a página de resultados

---

## 5. Resultados

### 5.1 Pontuação Global

A pontuação global (0-100%) indica o nível de maturidade digital:

| Nível | Pontuação | Significado |
|-------|-----------|------------|
| 1 — Inicial | 0-20% | Primeiros passos na digitalização |
| 2 — Em Desenvolvimento | 21-40% | Algumas práticas, mas inconsistentes |
| 3 — Definido | 41-60% | Práticas definidas em várias áreas |
| 4 — Gerido | 61-80% | Bom nível de maturidade digital |
| 5 — Otimizado | 81-100% | Excelência digital |

### 5.2 Gráfico Radar

O gráfico radar mostra a pontuação em cada uma das 5 dimensões, permitindo identificar visualmente os pontos fortes e fracos.

### 5.3 Pontos Fortes e Necessidades

- **✅ Pontos Fortes**: Dimensões com pontuação ≥ 60%
- **⚠️ Necessidades**: Dimensões com pontuação < 60% (com ações sugeridas)
- **🔴 Gap Crítico**: Dimensões com pontuação ≤ 40% (prioridade alta)

### 5.4 Primeiros Passos

Os 3 passos mais importantes para melhorar, com sugestão de ferramenta IA concreta.

### 5.5 Ferramentas IA Recomendadas

Cards com ferramentas sugeridas, incluindo:
- Nome e descrição
- Custo (Gratuito, Freemium, Pago)
- Razão da recomendação

### 5.6 Descarregar PDF

Clique em **"📄 Descarregar PDF"** para gerar e descarregar o relatório completo.

---

## 6. Definições (Administrador)

### 6.1 Configuração IA

Na secção **⚙️ Definições** do Dashboard:

1. **API Key Gemini**: Cole a chave da API Google Gemini
2. **Modelo**: Selecione o modelo (recomendado: `gemini-3.1-flash-lite-preview`)
3. **Testar**: Clique em "Testar Conexão" para verificar
4. **Guardar**: Clique em "Guardar Configuração"

> **Nota:** Apenas utilizadores com role `admin` podem aceder às definições.

---

## 7. Perguntas Frequentes

**P: Posso alterar as respostas depois de submeter?**
R: Sim, desde que não tenha concluído o diagnóstico. Basta voltar ao questionário e modificar as respostas.

**P: Os meus dados são seguros?**
R: Sim. Os dados são guardados com encriptação, as passwords com bcrypt, e o acesso é protegido por JWT.

**P: Preciso de formação técnica para usar o IALO?**
R: Não. O sistema foi desenhado para ser intuitivo e o assistente IA ajuda a esclarecer qualquer dúvida.

**P: Posso fazer vários diagnósticos à mesma empresa?**
R: Sim. Isso permite acompanhar a evolução da maturidade digital ao longo do tempo.

**P: O assistente IA precisa de ligação à internet?**
R: Sim, o assistente utiliza a API Google Gemini que requer ligação à internet.
