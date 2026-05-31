"""Testes de Interdependências entre camadas."""
from app.services.interdependencias import analisar_interdependencias


class TestInterdependencias:
    def test_analise_com_dados(self, client, auth_header, avaliacao_id):
        """Testa análise de interdependências após scoring."""
        from app.models.ailo import Indicador

        with client.application.app_context():
            # Responder a todos os indicadores
            indicadores = Indicador.query.all()
            respostas = [{'indicador_id': ind.id, 'score': 3} for ind in indicadores]
            client.post(f'/api/v1/avaliacoes/{avaliacao_id}/respostas/batch',
                         json={'respostas': respostas}, headers=auth_header)

            # Finalizar (dispara scoring + interdependências)
            res = client.post(f'/api/v1/avaliacoes/{avaliacao_id}/finalizar', headers=auth_header)
            assert res.status_code == 200

            # Verificar resultados incluem interdependências
            res = client.get(f'/api/v1/avaliacoes/{avaliacao_id}/resultados', headers=auth_header)
            assert res.status_code == 200
            data = res.get_json()
            assert 'interdependencias' in data
            assert isinstance(data['interdependencias'], list)

    def test_funcao_direta(self, app):
        """Testa função de análise diretamente com avaliação inexistente."""
        with app.app_context():
            # Sem resultados na BD para avaliação 999, retorna lista vazia
            result = analisar_interdependencias(999)
            assert isinstance(result, list)
            assert len(result) == 0
