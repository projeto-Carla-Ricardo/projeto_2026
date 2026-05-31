# WALKTHROUGH — Plataforma AILO (Fase 4)

> **Artificial Intelligence in a Learning Organization**
> Projeto de Fim de Curso — Engenharia Informática — Universidade Aberta
> Ricardo & Carla · Maio 2026

---

## 🚀 Como Iniciar a Aplicação

### Método Rápido (Recomendado)
```bash
cd Fase_4
./iniciar.sh
```
O script configura automaticamente o ambiente virtual, instala dependências, popula a base de dados e abre o browser.

### Método Manual
```bash
cd Fase_4/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # Editar com as suas configurações
python seed.py                 # Popular base de dados
python run.py                  # Iniciar servidor
```
Aceder a: **http://localhost:5000**

---

## 🔐 Credenciais de Acesso

| Perfil | Email | Password | Acesso |
|--------|-------|----------|--------|
| **Administrador** | `admin@ailo.pt` | `Admin2026!` | Dashboard Admin completa com gestão de utilizadores, analytics, indicadores e ferramentas |
| **Utilizador Demo** | `demo@ailo.pt` | `Demo2026!` | Dashboard de utilizador normal com questionário, resultados e benchmarking |

> **Nota:** As credenciais são criadas automaticamente pelo script `seed.py`. Se desejar credenciais diferentes, edite o ficheiro `backend/seed.py` antes de executar o seed.

---

## 📊 Dashboard de Administração

Após entrar com as credenciais de administrador, o sistema redireciona automaticamente para a **Dashboard Admin** (`/pages/admin_dashboard.html`). Esta página centraliza toda a gestão e análise da plataforma.

### KPIs em Tempo Real
- **Total de Utilizadores** registados na plataforma
- **Total de Organizações** criadas por todos os utilizadores
- **Avaliações** (concluídas / total)
- **Score Médio Global** de maturidade organizacional
- **Taxa de Conclusão** (percentagem de avaliações finalizadas)
- **Mensagens Chat IA** (total de interações com o assistente)

### Gráficos de Análise
| Gráfico | Tipo | Dados |
|---------|------|-------|
| Distribuição de Níveis de Maturidade | Donut | Quantas organizações estão em cada nível (Inicial → Otimizado) |
| Avaliações por Mês | Linha | Tendência dos últimos 12 meses |
| Avaliações por Setor | Barras Horizontais | Distribuição por setor de atividade |
| Score Médio por Camada AILO | Radar (Hexágono) | Visualização do desempenho agregado nas 6 camadas |

### Gestão (Tabs Navegáveis)

#### Tab: Avaliações
- Lista completa de todas as avaliações da plataforma
- Informações: ID, Organização, Utilizador, Status, Score, Nível, Data
- Badges coloridos para status (em curso, completa, cancelada)

#### Tab: Organizações
- Lista de todas as organizações registadas
- Colunas: Nome, Setor, Dimensão, Tipo, País, Nº Avaliações, Último Score

#### Tab: Utilizadores
- Lista de todos os utilizadores com ações de gestão
- **Ativar/Desativar**: Bloqueia o acesso de um utilizador sem o eliminar
- **Promover/Despromover**: Alterna o papel entre `utilizador` e `admin`
- Proteção: Não é possível desativar ou alterar o próprio perfil

#### Tab: Indicadores
- Listagem dos 51 indicadores do Framework AILO
- Estrutura: Camada → Componente → Código → Pergunta
- **Edição de pesos** inline (alterar e gravar automaticamente)

#### Tab: Ferramentas IA
- Catálogo de ferramentas de IA disponíveis para recomendação
- **Criar** novas ferramentas (nome, descrição, área, custo, complexidade)
- **Desativar** ferramentas (soft delete — mantém dados históricos)

---

## 👤 Funcionalidades do Utilizador Normal

### 1. Registo e Autenticação
- Criar conta com nome, email e password segura
- Login com token JWT (sessão válida por 24 horas)

### 2. Gestão de Organizações
- Criar múltiplas organizações associadas à conta
- Campos: Nome, Setor, Dimensão, Tipo, País, Descrição
- Editar e eliminar organizações

### 3. Questionário AILO (Diagnóstico de Maturidade)
- Iniciar uma avaliação para uma organização
- Questionário dividido em **6 camadas** com navegação livre:
  1. 🏢 **Organizacional** — Estratégia, processos, decisão
  2. 👥 **Humana** — Pessoas, cultura, ética, autonomia
  3. 📚 **Aprendizagem** — Contextos adaptativos, experiências
  4. 🧠 **Cognitiva (IA)** — Geração, recomendação, síntese
  5. 💻 **Tecnológica** — Infraestrutura, dados, integração
  6. 📏 **Avaliação** — Evidências, melhoria contínua
- **51 indicadores** avaliados numa escala de 1 (Inicial) a 5 (Otimizado)
- Tooltips com descrições dos níveis 1, 3 e 5
- **Auto-save** automático das respostas
- Barra de progresso em tempo real

### 4. Assistente IA Contextual
- Chat integrado no painel lateral do questionário
- Respostas personalizadas ao setor e tipo da organização
- Explicações concetuais do framework AILO
- Sugestões de nível de maturidade adequado
- Alertas de inconsistência entre respostas
- Funciona via **Google Gemini API** (modelo `gemini-3.5-flash` por defeito, com suporte a outros modelos configuráveis)
- Possui um **menu de configurações** acessível na janela inicial do painel onde cada utilizador/administrador pode definir a sua chave de API do Gemini e o modelo pretendido
- **Base de Conhecimento**: Carregada automaticamente ao iniciar a aplicação para que o assistente IA conheça perfeitamente a estrutura e interdependências do Framework AILO
- **Memória de Interações**: Histórico resumido persistido na base de dados para cada utilizador, permitindo que a IA tenha contexto particular em cada diálogo
- Modo offline ativo quando a chave API não está configurada

### 5. Resultados e Diagnóstico
- **Gráfico Radar Hexagonal** (6 eixos — camadas AILO)
- Score por camada com barras de progresso coloridas
- **Pontos Fortes** (indicadores com score ≥ 4)
- **Lacunas Críticas** (indicadores com score ≤ 2)
- **Análise de Interdependências** entre pares de camadas críticas
- **Recomendações de Ferramentas IA** priorizadas por gravidade/custo

### 6. Relatórios e Exportação
- Geração de relatórios em formato PDF
- Exportação de dados em CSV
- Comparação entre avaliações

### 7. Benchmarking Setorial
- Comparação anónima com organizações do mesmo setor
- Scores médios agregados por camada
- Cálculo do percentil da organização

---

## ⚙️ Informações Técnicas

### Stack Tecnológica
| Componente | Tecnologia |
|-----------|------------|
| Backend | Python 3.11+ · Flask 3.1 · SQLAlchemy 2.0 |
| Frontend | HTML5 · CSS3 (Dark Theme) · JavaScript Vanilla · Chart.js 4 |
| Base de Dados | SQLite (dev) · PostgreSQL 16 (prod) |
| Assistente IA | Google Gemini API (gemini-2.0-flash) |
| Relatórios PDF | WeasyPrint 63 · ReportLab 4.4 |
| Autenticação | JWT (PyJWT) · bcrypt |
| Deploy | Docker · Docker-Compose · Nginx · Gunicorn |

### Variáveis de Ambiente (.env)
```bash
SECRET_KEY=your-secret-key-here        # Chave JWT (gerar com: python -c "import secrets; print(secrets.token_hex(32))")
DATABASE_URL=sqlite:///ailo.db         # URI da base de dados
GEMINI_API_KEY=your-api-key            # Chave da Google AI (obter em https://aistudio.google.com/apikey)
GEMINI_MODEL=gemini-2.0-flash          # Modelo do assistente IA
```

### Estrutura do Framework AILO
- **6 Camadas** interdependentes articuladas em torno do Conhecimento Organizacional
- **23 Componentes** distribuídos pelas camadas
- **51 Indicadores** de maturidade (escala 1-5)
- **5 Níveis de Maturidade**: Inicial → Em Desenvolvimento → Definido → Gerido → Otimizado
- **6 Resultados Conceptuais** (CR1-CR6) mapeados nas interdependências

### API RESTful
Base URL: `http://localhost:5000/api/v1`

| Módulo | Endpoints Principais |
|--------|---------------------|
| Auth | `POST /auth/register`, `POST /auth/login`, `GET /auth/me` |
| Organizações | `GET/POST /organizacoes`, `GET/PUT/DELETE /organizacoes/:id` |
| Questionário | `GET /ailo/camadas`, `POST /avaliacoes`, `POST /avaliacoes/:id/respostas` |
| Resultados | `POST /avaliacoes/:id/finalizar`, `GET /avaliacoes/:id/resultados` |
| Chat IA | `POST /avaliacoes/:id/chat` |
| Admin | `GET /admin/dashboard`, `GET /admin/avaliacoes`, `PUT /admin/utilizadores/:id/toggle` |
| Analytics | `GET /analytics/overview`, `GET /analytics/distribuicao-scores` |
| Benchmarking | `GET /benchmarking/:setor` |

---

## 🐳 Deployment com Docker (Produção)

```bash
cp backend/.env.production.example backend/.env
# Editar .env com credenciais reais de PostgreSQL e Gemini API
docker-compose up --build -d
```

O ambiente de produção inclui:
- **PostgreSQL 16** (base de dados persistente)
- **Gunicorn** (4 workers WSGI)
- **Nginx** (proxy reverso com compressão gzip e headers de segurança)

