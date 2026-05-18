"""Testes de CRUD de organizações."""


class TestCriarOrganizacao:
    def test_criar_sucesso(self, client, auth_header):
        res = client.post('/api/v1/organizacoes', json={
            'nome': 'Empresa ABC',
            'setor': 'Educação',
            'dimensao': 'media',
            'tipo': 'ensino_superior',
            'pais': 'Portugal'
        }, headers=auth_header)
        assert res.status_code == 201
        assert res.get_json()['nome'] == 'Empresa ABC'

    def test_criar_sem_campos(self, client, auth_header):
        res = client.post('/api/v1/organizacoes', json={}, headers=auth_header)
        assert res.status_code == 400

    def test_criar_sem_auth(self, client):
        res = client.post('/api/v1/organizacoes', json={'nome': 'X', 'setor': 'Y', 'dimensao': 'Z', 'tipo': 'W'})
        assert res.status_code == 401


class TestListarOrganizacoes:
    def test_listar_vazio(self, client, auth_header):
        res = client.get('/api/v1/organizacoes', headers=auth_header)
        assert res.status_code == 200
        assert 'data' in res.get_json()

    def test_listar_com_dados(self, client, auth_header, org_id):
        res = client.get('/api/v1/organizacoes', headers=auth_header)
        assert res.status_code == 200
        assert len(res.get_json()['data']) >= 1


class TestEditarOrganizacao:
    def test_editar_sucesso(self, client, auth_header, org_id):
        res = client.put(f'/api/v1/organizacoes/{org_id}', json={
            'nome': 'Org Atualizada'
        }, headers=auth_header)
        assert res.status_code == 200
        assert res.get_json()['nome'] == 'Org Atualizada'

    def test_editar_inexistente(self, client, auth_header):
        res = client.put('/api/v1/organizacoes/999', json={'nome': 'X'}, headers=auth_header)
        assert res.status_code == 404


class TestEliminarOrganizacao:
    def test_eliminar_sucesso(self, client, auth_header, org_id):
        res = client.delete(f'/api/v1/organizacoes/{org_id}', headers=auth_header)
        assert res.status_code == 200

    def test_eliminar_inexistente(self, client, auth_header):
        res = client.delete('/api/v1/organizacoes/999', headers=auth_header)
        assert res.status_code == 404
