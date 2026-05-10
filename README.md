# AILO — Artificial Intelligence in a Learning Organization

Plataforma de diagnóstico de maturidade organizacional para integração de IA.

## 🚀 Como Instalar e Executar (Fase 2)

### Pré-requisitos
- **Python 3.10+** ([download](https://www.python.org/downloads/))
- **pip** (incluído com Python)
- **Git** (para clonar o repositório)

### Passo a passo

```bash
# 1. Clonar o repositório
git clone <URL_DO_REPOSITÓRIO>
cd projeto_2026

# 2. Entrar na pasta do backend
cd Fase_2/backend

# 3. Criar ambiente virtual Python
python3 -m venv venv

# 4. Ativar o ambiente virtual
source venv/bin/activate        # Linux / Mac
# venv\Scripts\activate          # Windows

# 5. Instalar dependências
pip install -r requirements.txt

# 6. Configurar variáveis de ambiente (opcional)
cp .env.example .env
# Editar .env se quiser ativar o assistente IA (GEMINI_API_KEY)

# 7. Popular a base de dados com os dados AILO
python seed.py

# 8. Iniciar o servidor
python run.py
```

### Aceder à aplicação
Abrir no browser: **http://localhost:5000**

### Fluxo de utilização
1. **Registar** uma conta na plataforma
2. **Criar** uma organização (nome, setor, dimensão, tipo)
3. **Iniciar** uma avaliação
4. **Responder** ao questionário AILO (6 camadas, 51 indicadores)
5. **Finalizar** a avaliação para ver os resultados
6. **Consultar** o dashboard com gráfico radar e recomendações

## 📁 Estrutura do Projeto

```
Fase_1/          → Documentação conceptual e técnica
Fase_2/
├── backend/     → Servidor Python/Flask
│   ├── app/     → Aplicação (models, routes, services, utils)
│   ├── seeds/   → Dados iniciais do framework AILO
│   ├── seed.py  → Script para popular a BD
│   └── run.py   → Ponto de entrada
├── frontend/    → Interface web (HTML, CSS, JS)
└── O_que_foi_feito.pdf → Relatório da Fase 2
```

## ⚙️ Configuração Opcional

Para ativar o **Assistente IA** (chat), editar o ficheiro `.env`:
```
GEMINI_API_KEY=a-sua-chave-da-google-ai
```
Obter chave em: https://aistudio.google.com/apikey

Sem esta chave, a aplicação funciona normalmente — apenas o chat responde em modo offline.

## 👥 Autores
Ricardo & Carla — Engenharia Informática — Universidade Aberta

Framework teórico: Santos & Mamede (2026) — *Artificial Intelligence in a Learning Organization*
