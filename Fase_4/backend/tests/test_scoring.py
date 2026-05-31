"""Testes do Motor de Scoring AILO."""
from app.services.scoring import classificar_nivel, calcular_scoring


class TestClassificarNivel:
    def test_nivel_inicial(self):
        assert classificar_nivel(1.0) == 'Inicial'
        assert classificar_nivel(1.5) == 'Inicial'
        assert classificar_nivel(1.8) == 'Inicial'

    def test_nivel_desenvolvimento(self):
        assert classificar_nivel(1.9) == 'Em Desenvolvimento'
        assert classificar_nivel(2.6) == 'Em Desenvolvimento'

    def test_nivel_definido(self):
        assert classificar_nivel(2.7) == 'Definido'
        assert classificar_nivel(3.4) == 'Definido'

    def test_nivel_gerido(self):
        assert classificar_nivel(3.5) == 'Gerido'
        assert classificar_nivel(4.2) == 'Gerido'

    def test_nivel_otimizado(self):
        assert classificar_nivel(4.3) == 'Otimizado'
        assert classificar_nivel(5.0) == 'Otimizado'


class TestCalcularScoring:
    def test_avaliacao_inexistente(self, app):
        with app.app_context():
            result = calcular_scoring(999)
            assert result is None

    def test_scoring_com_respostas(self, client, auth_header, avaliacao_id):
        """Testa scoring completo com respostas para todos os indicadores."""
        from app.models.ailo import Indicador
        from app import db as _db

        with client.application.app_context():
            indicadores = Indicador.query.all()
            respostas = [{'indicador_id': ind.id, 'score': 3} for ind in indicadores]
            # Guardar respostas via batch
            res = client.post(f'/api/v1/avaliacoes/{avaliacao_id}/respostas/batch',
                              json={'respostas': respostas}, headers=auth_header)
            assert res.status_code == 200

            # Finalizar
            res = client.post(f'/api/v1/avaliacoes/{avaliacao_id}/finalizar', headers=auth_header)
            assert res.status_code == 200
            data = res.get_json()
            assert 'score_global' in data
            assert 1.0 <= data['score_global'] <= 5.0
            assert data['nivel_global'] in ['Inicial', 'Em Desenvolvimento', 'Definido', 'Gerido', 'Otimizado']
