"""Testes de Exportação RGPD."""


class TestExportarDados:
    def test_exportar_sem_auth(self, client):
        res = client.get('/api/v1/export/meus-dados')
        assert res.status_code == 401

    def test_exportar_com_auth(self, client, auth_header):
        res = client.get('/api/v1/export/meus-dados', headers=auth_header)
        assert res.status_code == 200
        data = res.get_json()
        assert 'utilizador' in data
        assert 'organizacoes' in data
        assert 'nota_rgpd' in data

    def test_exportar_com_dados(self, client, auth_header, org_id):
        res = client.get('/api/v1/export/meus-dados', headers=auth_header)
        assert res.status_code == 200
        data = res.get_json()
        assert len(data['organizacoes']) >= 1


class TestEliminarConta:
    def test_eliminar_sem_confirmacao(self, client, auth_header):
        res = client.delete('/api/v1/export/eliminar-conta', json={}, headers=auth_header)
        assert res.status_code == 400

    def test_eliminar_com_confirmacao(self, client, auth_header):
        res = client.delete('/api/v1/export/eliminar-conta',
                            json={'confirmacao': 'ELIMINAR'}, headers=auth_header)
        assert res.status_code == 200
        assert 'RGPD' in res.get_json()['message']
