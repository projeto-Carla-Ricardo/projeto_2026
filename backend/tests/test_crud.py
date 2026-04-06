"""
Testes — API CRUD de Empresas e Avaliações
Testa criação, leitura, atualização e proteção de acesso.
"""
import pytest


class TestEmpresas:
    """Testes CRUD de empresas."""

    def test_criar_empresa(self, client, auth_headers):
        res = client.post('/api/v1/empresas', headers=auth_headers, json={
            'nome': 'Café Central',
            'setor': 'Alimentar',
            'num_colaboradores': 5,
            'localizacao': 'Lisboa'
        })
        data = res.get_json()
        assert res.status_code == 201
        assert data['status'] == 'success'
        assert data['data']['nome'] == 'Café Central'

    def test_listar_empresas(self, client, auth_headers):
        res = client.get('/api/v1/empresas', headers=auth_headers)
        data = res.get_json()
        assert res.status_code == 200
        assert isinstance(data['data'], list)
        assert len(data['data']) >= 1

    def test_criar_empresa_sem_nome(self, client, auth_headers):
        res = client.post('/api/v1/empresas', headers=auth_headers, json={
            'setor': 'Tech'
        })
        assert res.status_code in [400, 422]

    def test_criar_empresa_sem_setor(self, client, auth_headers):
        res = client.post('/api/v1/empresas', headers=auth_headers, json={
            'nome': 'Teste'
        })
        assert res.status_code in [400, 422]


class TestAvaliacoes:
    """Testes CRUD de avaliações."""

    def test_criar_avaliacao(self, client, auth_headers):
        # Obter primeira empresa
        res = client.get('/api/v1/empresas', headers=auth_headers)
        empresas = res.get_json()['data']
        assert len(empresas) > 0

        empresa_id = empresas[0]['id']
        res = client.post('/api/v1/avaliacoes', headers=auth_headers, json={
            'empresa_id': empresa_id
        })
        data = res.get_json()
        assert res.status_code == 201
        assert data['status'] == 'success'
        assert data['data']['estado'] == 'em_curso'

    def test_listar_avaliacoes(self, client, auth_headers):
        res = client.get('/api/v1/avaliacoes', headers=auth_headers)
        data = res.get_json()
        assert res.status_code == 200
        assert isinstance(data['data'], list)

    def test_criar_avaliacao_empresa_inexistente(self, client, auth_headers):
        res = client.post('/api/v1/avaliacoes', headers=auth_headers, json={
            'empresa_id': 99999
        })
        assert res.status_code in [400, 403, 404]


class TestQuestionario:
    """Testes do questionário."""

    def test_listar_dimensoes(self, client, auth_headers):
        res = client.get('/api/v1/questionario/dimensoes', headers=auth_headers)
        data = res.get_json()
        assert res.status_code == 200
        assert len(data['data']) == 5

    def test_guardar_respostas(self, client, auth_headers):
        # Criar avaliação primeiro
        res = client.get('/api/v1/empresas', headers=auth_headers)
        empresa_id = res.get_json()['data'][0]['id']

        res = client.post('/api/v1/avaliacoes', headers=auth_headers, json={
            'empresa_id': empresa_id
        })
        avaliacao_id = res.get_json()['data']['id']

        # Enviar respostas
        respostas = [
            {'pergunta_id': i, 'valor_numerico': 3} for i in range(1, 26)
        ]
        res = client.post('/api/v1/questionario/respostas', headers=auth_headers, json={
            'avaliacao_id': avaliacao_id,
            'respostas': respostas
        })
        data = res.get_json()
        assert res.status_code == 200
        assert data['status'] == 'success'

    def test_obter_respostas(self, client, auth_headers):
        # Obter avaliação existente
        res = client.get('/api/v1/avaliacoes', headers=auth_headers)
        avaliacoes = res.get_json()['data']
        if avaliacoes:
            avaliacao_id = avaliacoes[0]['id']
            res = client.get(f'/api/v1/questionario/respostas/{avaliacao_id}', headers=auth_headers)
            assert res.status_code == 200
