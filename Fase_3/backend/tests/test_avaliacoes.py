"""Testes de Avaliações — criar, listar, detalhar, finalizar."""


class TestCriarAvaliacao:
    def test_criar_sucesso(self, client, auth_header, org_id):
        res = client.post('/api/v1/avaliacoes', json={
            'organizacao_id': org_id
        }, headers=auth_header)
        assert res.status_code == 201
        data = res.get_json()
        assert data['status'] == 'em_curso'
        assert data['organizacao_id'] == org_id

    def test_criar_sem_org(self, client, auth_header):
        res = client.post('/api/v1/avaliacoes', json={}, headers=auth_header)
        assert res.status_code in [400, 404]

    def test_criar_sem_auth(self, client):
        res = client.post('/api/v1/avaliacoes', json={'organizacao_id': 1})
        assert res.status_code == 401


class TestListarAvaliacoes:
    def test_listar(self, client, auth_header, avaliacao_id):
        res = client.get('/api/v1/avaliacoes', headers=auth_header)
        assert res.status_code == 200
        assert 'data' in res.get_json()

    def test_detalhar(self, client, auth_header, avaliacao_id):
        res = client.get(f'/api/v1/avaliacoes/{avaliacao_id}', headers=auth_header)
        assert res.status_code == 200
        data = res.get_json()
        assert data['id'] == avaliacao_id


class TestResponderQuestionario:
    def test_guardar_resposta(self, client, auth_header, avaliacao_id):
        from app.models.ailo import Indicador
        with client.application.app_context():
            ind = Indicador.query.first()
            res = client.post(f'/api/v1/avaliacoes/{avaliacao_id}/respostas', json={
                'indicador_id': ind.id,
                'score': 4,
                'justificacao': 'Teste'
            }, headers=auth_header)
            assert res.status_code in [200, 201]

    def test_guardar_batch(self, client, auth_header, avaliacao_id):
        from app.models.ailo import Indicador
        with client.application.app_context():
            inds = Indicador.query.limit(5).all()
            respostas = [{'indicador_id': i.id, 'score': 3} for i in inds]
            res = client.post(f'/api/v1/avaliacoes/{avaliacao_id}/respostas/batch',
                              json={'respostas': respostas}, headers=auth_header)
            assert res.status_code == 200

    def test_score_invalido(self, client, auth_header, avaliacao_id):
        from app.models.ailo import Indicador
        with client.application.app_context():
            ind = Indicador.query.first()
            res = client.post(f'/api/v1/avaliacoes/{avaliacao_id}/respostas', json={
                'indicador_id': ind.id,
                'score': 99
            }, headers=auth_header)
            assert res.status_code == 400
