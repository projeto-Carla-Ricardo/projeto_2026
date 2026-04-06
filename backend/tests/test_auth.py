"""
Testes — API de Autenticação
Testa registo, login, erros e segurança.
"""
import pytest


class TestRegistro:
    """Testes de registo de utilizador."""

    def test_registo_sucesso(self, client):
        res = client.post('/api/v1/auth/register', json={
            'nome': 'Novo User',
            'email': 'novo@ialo.pt',
            'password': 'seguro12345'
        })
        data = res.get_json()
        assert res.status_code == 201
        assert data['status'] == 'success'
        assert data['data']['email'] == 'novo@ialo.pt'

    def test_registo_email_duplicado(self, client):
        res = client.post('/api/v1/auth/register', json={
            'nome': 'Duplicado',
            'email': 'teste@ialo.pt',  # já existe no seed
            'password': 'password123'
        })
        assert res.status_code in [400, 409]

    def test_registo_sem_campos(self, client):
        res = client.post('/api/v1/auth/register', json={})
        assert res.status_code in [400, 422]

    def test_registo_password_curta(self, client):
        res = client.post('/api/v1/auth/register', json={
            'nome': 'Teste',
            'email': 'curta@ialo.pt',
            'password': '123'
        })
        assert res.status_code in [400, 422]


class TestLogin:
    """Testes de login."""

    def test_login_sucesso(self, client):
        res = client.post('/api/v1/auth/login', json={
            'email': 'teste@ialo.pt',
            'password': 'password123'
        })
        data = res.get_json()
        assert res.status_code == 200
        assert data['status'] == 'success'
        assert 'token' in data['data']
        assert 'refresh_token' in data['data']

    def test_login_password_errada(self, client):
        res = client.post('/api/v1/auth/login', json={
            'email': 'teste@ialo.pt',
            'password': 'errada'
        })
        assert res.status_code == 401

    def test_login_email_inexistente(self, client):
        res = client.post('/api/v1/auth/login', json={
            'email': 'naoexiste@ialo.pt',
            'password': 'qualquer'
        })
        assert res.status_code == 401


class TestSeguranca:
    """Testes de segurança e protecção de rotas."""

    def test_rota_protegida_sem_token(self, client):
        res = client.get('/api/v1/empresas')
        assert res.status_code in [401, 422]

    def test_rota_protegida_token_invalido(self, client):
        res = client.get('/api/v1/empresas', headers={
            'Authorization': 'Bearer token_falso_12345'
        })
        assert res.status_code == 422

    def test_rota_protegida_com_token_valido(self, client, auth_headers):
        res = client.get('/api/v1/empresas', headers=auth_headers)
        assert res.status_code == 200
