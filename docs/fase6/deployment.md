# Guia de Deployment — IALO

## 1. Requisitos do Sistema

- Python 3.12+
- pip
- Git
- Navegador moderno (Chrome, Firefox, Safari)

## 2. Instalação Local (Desenvolvimento)

### 2.1 Clonar repositório
```bash
git clone <repo_url>
cd PROJETO_2026
```

### 2.2 Configurar backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate    # Linux/Mac
# venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### 2.3 Configurar variáveis de ambiente
```bash
cp .env.example .env
# Editar .env com as suas configurações:
# SECRET_KEY=<chave-secreta-forte>
# JWT_SECRET_KEY=<chave-jwt-forte>
# GEMINI_API_KEY=<sua-api-key-gemini>
# GEMINI_MODEL=gemini-3.1-flash-lite-preview
```

### 2.4 Inicializar base de dados
```bash
flask db upgrade
python seed.py
```

### 2.5 Executar servidor
```bash
python run.py
# Servidor em http://localhost:5000
```

### 2.6 Abrir frontend
Abrir no browser:
```
file:///caminho/para/PROJETO_2026/frontend/index.html
```

Ou servir com um servidor estático:
```bash
cd ../frontend
python3 -m http.server 8080
# Abrir http://localhost:8080
```

## 3. Executar Testes

```bash
cd backend
source venv/bin/activate
python -m pytest tests/ -v
```

## 4. Deployment de Produção

### 4.1 Com Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app('production')"
```

### 4.2 Com Nginx (proxy reverso)
```nginx
server {
    listen 80;
    server_name ialo.example.com;

    location /api/ {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location / {
        root /var/www/ialo/frontend;
        try_files $uri $uri/ /index.html;
    }
}
```

## 5. Estrutura do Projeto

```
PROJETO_2026/
├── backend/
│   ├── app/
│   │   ├── __init__.py          # Factory pattern
│   │   ├── config.py            # Configs por ambiente
│   │   ├── models/              # 12 modelos SQLAlchemy
│   │   ├── routes/              # 8 blueprints API
│   │   ├── services/            # Lógica de negócio
│   │   └── utils/               # Helpers e fuzzy logic
│   ├── migrations/              # Alembic migrations
│   ├── seeds/                   # JSON seed data
│   ├── tests/                   # 64 testes pytest
│   ├── requirements.txt
│   ├── run.py
│   └── seed.py
├── frontend/
│   ├── css/                     # 5 ficheiros CSS
│   ├── js/                      # 6 ficheiros JS
│   ├── pages/                   # 5 páginas HTML
│   └── index.html               # Landing page
├── docs/                        # 17 documentos técnicos
│   ├── fase1/ → fase6/
├── Fase 1/ → Fase 6/            # Snapshots por fase
└── README.md                    # Roadmap do projeto
```
