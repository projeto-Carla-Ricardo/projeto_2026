"""Testes de autenticação — registo, login, token inválido, me()."""


class TestRegisto:
    def test_registo_sucesso(self, client, user_data):
        res = client.post('/api/v1/auth/register', json=user_data)
        assert res.status_code == 201
        data = res.get_json()
        assert 'token' in data
        assert data['nome'] == user_data['nome']
        assert data['email'] == user_data['email']

    def test_registo_email_duplicado(self, client, user_data):
        client.post('/api/v1/auth/register', json=user_data)
        res = client.post('/api/v1/auth/register', json=user_data)
        assert res.status_code == 409
        assert 'já registado' in res.get_json()['error']

    def test_registo_sem_campos(self, client):
        res = client.post('/api/v1/auth/register', json={})
        assert res.status_code == 400

    def test_registo_email_invalido(self, client, user_data):
        user_data['email'] = 'email-invalido'
        res = client.post('/api/v1/auth/register', json=user_data)
        assert res.status_code == 400

    def test_registo_password_fraca(self, client, user_data):
        user_data['password'] = '12'
        res = client.post('/api/v1/auth/register', json=user_data)
        assert res.status_code == 400


class TestLogin:
    def test_login_sucesso(self, client, user_data):
        client.post('/api/v1/auth/register', json=user_data)
        res = client.post('/api/v1/auth/login', json={
            'email': user_data['email'],
            'password': user_data['password']
        })
        assert res.status_code == 200
        data = res.get_json()
        assert 'token' in data
        assert 'user' in data

    def test_login_credenciais_invalidas(self, client, user_data):
        client.post('/api/v1/auth/register', json=user_data)
        res = client.post('/api/v1/auth/login', json={
            'email': user_data['email'],
            'password': 'password-errada!'
        })
        assert res.status_code == 401

    def test_login_email_inexistente(self, client):
        res = client.post('/api/v1/auth/login', json={
            'email': 'naoexiste@ailo.pt',
            'password': 'Qualquer1!'
        })
        assert res.status_code == 401


class TestMe:
    def test_me_com_token(self, client, auth_header):
        res = client.get('/api/v1/auth/me', headers=auth_header)
        assert res.status_code == 200
        assert 'nome' in res.get_json()

    def test_me_sem_token(self, client):
        res = client.get('/api/v1/auth/me')
        assert res.status_code == 401

    def test_me_token_invalido(self, client):
        res = client.get('/api/v1/auth/me', headers={
            'Authorization': 'Bearer token-invalido'
        })
        assert res.status_code == 401
