"""
Testes Unitários — Motor de Scoring
Testa o cálculo de pontuação, níveis e gaps.
"""
import pytest
from app.services.scoring_engine import pontuacao_para_nivel, identificar_gap_critico, NIVEL_NOMES


class TestPontuacaoParaNivel:
    """Testes de conversão pontuação → nível."""

    def test_nivel_1_limites(self):
        assert pontuacao_para_nivel(0) == 1
        assert pontuacao_para_nivel(10) == 1
        assert pontuacao_para_nivel(20) == 1

    def test_nivel_2_limites(self):
        assert pontuacao_para_nivel(21) == 2
        assert pontuacao_para_nivel(30) == 2
        assert pontuacao_para_nivel(40) == 2

    def test_nivel_3_limites(self):
        assert pontuacao_para_nivel(41) == 3
        assert pontuacao_para_nivel(50) == 3
        assert pontuacao_para_nivel(60) == 3

    def test_nivel_4_limites(self):
        assert pontuacao_para_nivel(61) == 4
        assert pontuacao_para_nivel(70) == 4
        assert pontuacao_para_nivel(80) == 4

    def test_nivel_5_limites(self):
        assert pontuacao_para_nivel(81) == 5
        assert pontuacao_para_nivel(90) == 5
        assert pontuacao_para_nivel(100) == 5

    def test_valores_extremos(self):
        assert pontuacao_para_nivel(0) == 1
        assert pontuacao_para_nivel(100) == 5

    def test_todos_niveis_mapeados(self):
        """Todos os 5 níveis devem ser alcançáveis."""
        niveis = set()
        for p in range(0, 101, 5):
            niveis.add(pontuacao_para_nivel(p))
        assert niveis == {1, 2, 3, 4, 5}


class TestIdentificarGapCritico:
    """Testes de identificação de gaps críticos."""

    def test_gap_quando_abaixo_40(self):
        assert identificar_gap_critico(20.0) is True
        assert identificar_gap_critico(30.0) is True
        assert identificar_gap_critico(40.0) is True

    def test_nao_gap_quando_acima_40(self):
        assert identificar_gap_critico(41.0) is False
        assert identificar_gap_critico(60.0) is False
        assert identificar_gap_critico(100.0) is False

    def test_gap_limite(self):
        assert identificar_gap_critico(40.0) is True
        assert identificar_gap_critico(40.1) is False


class TestNivelNomes:
    """Testes dos nomes de nível."""

    def test_todos_niveis_tem_nome(self):
        for nivel in range(1, 6):
            assert nivel in NIVEL_NOMES
            assert isinstance(NIVEL_NOMES[nivel], str)
            assert len(NIVEL_NOMES[nivel]) > 0

    def test_5_niveis_existem(self):
        assert len(NIVEL_NOMES) == 5


class TestScoringCompleto:
    """Testes do scoring completo (com BD)."""

    def test_scoring_com_respostas_altas(self, app, db):
        """Respostas todas 5 devem resultar em ~100%."""
        from app.models.avaliacao import Avaliacao
        from app.models.empresa import Empresa
        from app.models.resposta import Resposta
        from app.models.pergunta import Pergunta
        from app.services.scoring_engine import calcular_scoring_completo

        empresa = Empresa.query.first()
        avaliacao = Avaliacao(empresa_id=empresa.id, estado='em_curso')
        db.session.add(avaliacao)
        db.session.flush()

        perguntas = Pergunta.query.all()
        for p in perguntas:
            r = Resposta(avaliacao_id=avaliacao.id, pergunta_id=p.id,
                         valor_numerico=5, valor_fuzzy=5.0)
            db.session.add(r)
        db.session.commit()

        resultado = calcular_scoring_completo(avaliacao.id)

        assert resultado['pontuacao_global'] == 100.0
        assert resultado['nivel_global'] == 5
        assert resultado['nivel_descricao'] == 'Otimizado'
        assert len(resultado['gaps_criticos']) == 0
        assert len(resultado['dimensoes']) == 5

    def test_scoring_com_respostas_baixas(self, app, db):
        """Respostas todas 1 devem resultar em 20%."""
        from app.models.avaliacao import Avaliacao
        from app.models.empresa import Empresa
        from app.models.resposta import Resposta
        from app.models.pergunta import Pergunta
        from app.services.scoring_engine import calcular_scoring_completo

        empresa = Empresa.query.first()
        avaliacao = Avaliacao(empresa_id=empresa.id, estado='em_curso')
        db.session.add(avaliacao)
        db.session.flush()

        perguntas = Pergunta.query.all()
        for p in perguntas:
            r = Resposta(avaliacao_id=avaliacao.id, pergunta_id=p.id,
                         valor_numerico=1, valor_fuzzy=1.0)
            db.session.add(r)
        db.session.commit()

        resultado = calcular_scoring_completo(avaliacao.id)

        assert resultado['pontuacao_global'] == 20.0
        assert resultado['nivel_global'] == 1
        assert len(resultado['gaps_criticos']) > 0

    def test_scoring_com_gap_em_dimensao(self, app, db):
        """Respostas mistas devem gerar gap na dimensão fraca."""
        from app.models.avaliacao import Avaliacao
        from app.models.empresa import Empresa
        from app.models.resposta import Resposta
        from app.models.pergunta import Pergunta
        from app.models.dimensao import Dimensao
        from app.services.scoring_engine import calcular_scoring_completo

        empresa = Empresa.query.first()
        avaliacao = Avaliacao(empresa_id=empresa.id, estado='em_curso')
        db.session.add(avaliacao)
        db.session.flush()

        dimensoes = Dimensao.query.order_by(Dimensao.ordem).all()

        for dim in dimensoes:
            from app.models.indicador import Indicador
            indicadores = Indicador.query.filter_by(dimensao_id=dim.id).all()
            for ind in indicadores:
                perguntas = Pergunta.query.filter_by(indicador_id=ind.id).all()
                for p in perguntas:
                    # DADOS = 1 (gap), resto = 5
                    val = 1 if dim.codigo == 'DADOS' else 5
                    r = Resposta(avaliacao_id=avaliacao.id, pergunta_id=p.id,
                                 valor_numerico=val, valor_fuzzy=float(val))
                    db.session.add(r)
        db.session.commit()

        resultado = calcular_scoring_completo(avaliacao.id)

        # DADOS deve ser gap crítico
        dados_dim = next(d for d in resultado['dimensoes'] if d['codigo'] == 'DADOS')
        assert dados_dim['gap_critico'] is True
        assert dados_dim['pontuacao'] <= 40.0

        # Restantes não devem ser gap
        for d in resultado['dimensoes']:
            if d['codigo'] != 'DADOS':
                assert d['gap_critico'] is False
