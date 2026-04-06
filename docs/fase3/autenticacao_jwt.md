# Autenticação e Autorização — JWT

## Visão Geral

O sistema de autenticação do IALO utiliza **JSON Web Tokens (JWT)** para proteger todas as rotas da API. A implementação é feita com o pacote `flask-jwt-extended`.

## Fluxo de Autenticação

```
┌──────────┐     POST /auth/register      ┌──────────┐
│  Cliente  │ ──────────────────────────►  │  Backend │
│ (Browser) │     { nome, email, pwd }     │  (Flask) │
└──────────┘                               └──────────┘
                                                │
     ◄──────── 201 Created ────────────────────┘

┌──────────┐     POST /auth/login          ┌──────────┐
│  Cliente  │ ──────────────────────────►  │  Backend │
│ (Browser) │     { email, password }      │  (Flask) │
└──────────┘                               └──────────┘
                                                │
     ◄──────── { token, refresh_token } ───────┘

┌──────────┐     GET /api/v1/empresas      ┌──────────┐
│  Cliente  │ ──────────────────────────►  │  Backend │
│ (Browser) │  Authorization: Bearer <JWT> │  (Flask) │
└──────────┘                               └──────────┘
```

## Tokens

| Token | Duração | Uso |
|-------|---------|-----|
| **Access Token** | 1 hora | Autenticação de pedidos à API |
| **Refresh Token** | 30 dias | Renovação do access token expirado |

## Roles e Permissões

| Role | Permissões |
|------|-----------|
| `empresario` | CRUD das suas próprias empresas e avaliações |
| `consultor` | Visualização de avaliações atribuídas |
| `admin` | Acesso total, incluindo configurações do sistema |

## Decoradores de Proteção

```python
@jwt_required()              # Qualquer utilizador autenticado
@admin_required              # Apenas administradores
@owner_or_admin              # Proprietário do recurso ou admin
```

## Armazenamento no Frontend

Os tokens são guardados no `localStorage` do browser:

```javascript
localStorage.setItem('ialo_token', data.token);
localStorage.setItem('ialo_refresh', data.refresh_token);
localStorage.setItem('ialo_user', JSON.stringify(data.user));
```

## Ficheiros Relevantes

| Ficheiro | Descrição |
|----------|-----------|
| `backend/app/routes/auth.py` | Rotas de registo, login, refresh |
| `backend/app/utils/auth_helpers.py` | Decoradores e utilitários |
| `backend/app/models/utilizador.py` | Modelo ORM do utilizador |
| `frontend/js/auth.js` | Lógica de login/registo no frontend |

## Segurança

- Passwords são hashed com **bcrypt** (salt automático)
- JWT identity usa string (compatibilidade com flask-jwt-extended)
- Rate limiting aplicado nas rotas de autenticação via `flask-limiter`
- Tokens incluem claims personalizados (`role`, `nome`)
