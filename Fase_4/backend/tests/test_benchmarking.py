"""Testes de Benchmarking Setorial."""


class TestListarSetores:
    def test_listar_setores_vazio(self, client, auth_header):
        res = client.get('/api/v1/benchmarking/setores', headers=auth_header)
        assert res.status_code == 200
        assert 'setores' in res.get_json()

    def test_listar_setores_com_dados(self, client, auth_header, org_id, avaliacao_id):
        """Após finalizar avaliação, setor deve aparecer."""
        from app.models.ailo import Indicador
        with client.application.app_context():
            inds = Indicador.query.all()
            respostas = [{'indicador_id': i.id, 'score': 3} for i in inds]
            client.post(f'/api/v1/avaliacoes/{avaliacao_id}/respostas/batch',
                        json={'respostas': respostas}, headers=auth_header)
            client.post(f'/api/v1/avaliacoes/{avaliacao_id}/finalizar', headers=auth_header)

            res = client.get('/api/v1/benchmarking/setores', headers=auth_header)
            assert res.status_code == 200
            data = res.get_json()
            assert len(data['setores']) >= 1


class TestBenchmarkingSetor:
    def test_setor_inexistente(self, client, auth_header):
        res = client.get('/api/v1/benchmarking/SetorFake', headers=auth_header)
        assert res.status_code == 404

    def test_setor_com_dados(self, client, auth_header, org_id, avaliacao_id):
        from app.models.ailo import Indicador
        with client.application.app_context():
            inds = Indicador.query.all()
            respostas = [{'indicador_id': i.id, 'score': 4} for i in inds]
            client.post(f'/api/v1/avaliacoes/{avaliacao_id}/respostas/batch',
                        json={'respostas': respostas}, headers=auth_header)
            client.post(f'/api/v1/avaliacoes/{avaliacao_id}/finalizar', headers=auth_header)

            res = client.get(f'/api/v1/benchmarking/Tecnologia?org_id={org_id}', headers=auth_header)
            assert res.status_code == 200
            data = res.get_json()
            assert 'camadas' in data
            assert 'setor' in data
            assert data['total_avaliacoes'] >= 1
            assert 'organizacao' in data
