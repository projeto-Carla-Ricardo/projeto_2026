# Testes e Validação — Fase 5

## Visão Geral

A suite de testes do IALO utiliza **pytest** com BD SQLite in-memory. Inclui testes unitários, de API, de integração e de segurança.

## Execução

```bash
cd backend
source venv/bin/activate
python -m pytest tests/ -v
```

### Com cobertura:
```bash
python -m pytest tests/ --cov=app --cov-report=term-missing
```

## Resultados

```
64 testes PASSED — 0 falhas

tests/test_fuzzy_logic.py  — 25 testes  (Lógica fuzzy)
tests/test_scoring.py      — 14 testes  (Motor de scoring)
tests/test_auth.py         — 10 testes  (Autenticação JWT)
tests/test_crud.py         — 10 testes  (CRUD empresas/avaliações)
tests/test_integracao.py   —  5 testes  (Pipeline completo + segurança)
```

## Ficheiros de Teste

### `tests/conftest.py` — Fixtures
- App Flask com `TestingConfig` (SQLite `:memory:`)
- Seed de dados: 2 utilizadores, 1 empresa, 5 dimensões, 25 indicadores, 25 perguntas
- Fixtures: `app`, `db`, `client`, `auth_headers`, `admin_headers`

### `tests/test_fuzzy_logic.py` — Lógica Fuzzy (25 testes)
- Conversão texto → fuzzy (sim, não, papel, excel, software, ERP, cloud)
- Correspondência parcial
- Mapa completo (todos os valores entre 1.0 e 5.0)
- Conversão por índice de opção
- Função `calculate_fuzzy_value` para todos os tipos de resposta

### `tests/test_scoring.py` — Motor de Scoring (14 testes)
- Conversão pontuação → nível (limites de cada nível)
- Identificação de gaps críticos (≤40%)
- Nomes de nível completos
- Scoring completo com respostas altas (→100%, nível 5)
- Scoring completo com respostas baixas (→20%, nível 1, gaps)
- Scoring com gap numa dimensão específica

### `tests/test_auth.py` — Autenticação (10 testes)
- Registo: sucesso, email duplicado, campos em falta, password curta
- Login: sucesso, password errada, email inexistente
- Segurança: rota sem token, token inválido, token válido

### `tests/test_crud.py` — CRUD APIs (10 testes)
- Empresas: criar, listar, validação (sem nome, sem setor)
- Avaliações: criar, listar, empresa inexistente
- Questionário: listar dimensões (5), guardar respostas, obter respostas

### `tests/test_integracao.py` — Integração (5 testes)
- **Pipeline completo**: Registo → Login → Empresa → Avaliação → Respostas → Scoring → Relatório → Recomendações
- Validação de cenário realista (padaria com scores mistos)
- Relatório para avaliação não concluída (400)
- Relatório para avaliação inexistente (404)
- Segurança: utilizador não acede empresa de outro utilizador (403)

## Cenários de Teste Cobertes

| Área | Cenários | Status |
|------|----------|--------|
| Fuzzy Logic | Todas as conversões, edge cases, fallbacks | ✅ |
| Scoring | Níveis 1-5, gaps, ponderação, persistência BD | ✅ |
| Auth | JWT, bcrypt, roles, rate limiting | ✅ |
| CRUD | Create, Read, validação, ownership | ✅ |
| Integração | Pipeline E2E, consistência, segurança | ✅ |
| Relatórios | Geração, validação estado, acesso | ✅ |
