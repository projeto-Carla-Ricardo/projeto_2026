"""
Testes Unitários — Lógica Fuzzy
Testa a conversão de respostas qualitativas para valores numéricos.
"""
import pytest
from app.utils.fuzzy_logic import (
    text_to_fuzzy,
    option_index_to_fuzzy,
    calculate_fuzzy_value,
    FUZZY_MAP,
)


class TestTextToFuzzy:
    """Testes de conversão texto → valor fuzzy."""

    def test_resposta_sim(self):
        assert text_to_fuzzy('Sim') == 5.0

    def test_resposta_nao(self):
        assert text_to_fuzzy('Não') == 1.0
        assert text_to_fuzzy('nao') == 1.0

    def test_resposta_papel(self):
        assert text_to_fuzzy('papel') == 1.0

    def test_resposta_excel(self):
        assert text_to_fuzzy('Excel') == 2.5
        assert text_to_fuzzy('excel') == 2.5

    def test_resposta_software(self):
        assert text_to_fuzzy('Software dedicado') == 4.0
        assert text_to_fuzzy('software') == 4.0

    def test_resposta_erp(self):
        assert text_to_fuzzy('ERP') == 5.0
        assert text_to_fuzzy('ERP integrado') == 5.0

    def test_resposta_cloud(self):
        assert text_to_fuzzy('cloud') == 5.0
        assert text_to_fuzzy('nuvem') == 5.0

    def test_resposta_vazia(self):
        assert text_to_fuzzy('') is None
        assert text_to_fuzzy(None) is None

    def test_resposta_desconhecida(self):
        assert text_to_fuzzy('xyz_desconhecido_123') is None

    def test_resposta_parcial(self):
        """Correspondência parcial deve funcionar."""
        assert text_to_fuzzy('caderno de notas') is not None

    def test_todas_entradas_mapa(self):
        """Todas as entradas do FUZZY_MAP devem retornar valores entre 1 e 5."""
        for key, value in FUZZY_MAP.items():
            assert 1.0 <= value <= 5.0, f"Valor fora do range para '{key}': {value}"


class TestOptionIndexToFuzzy:
    """Testes de conversão índice → valor fuzzy."""

    def test_primeira_opcao(self):
        assert option_index_to_fuzzy(0, 4) == 1.0

    def test_ultima_opcao(self):
        assert option_index_to_fuzzy(3, 4) == 5.0

    def test_opcao_media(self):
        result = option_index_to_fuzzy(1, 3)
        assert 2.0 <= result <= 4.0

    def test_uma_opcao(self):
        assert option_index_to_fuzzy(0, 1) == 3.0

    def test_distribuicao_linear(self):
        """Com 5 opções, a distribuição deve ser 1, 2, 3, 4, 5."""
        results = [option_index_to_fuzzy(i, 5) for i in range(5)]
        assert results == [1.0, 2.0, 3.0, 4.0, 5.0]


class TestCalculateFuzzyValue:
    """Testes da função principal de cálculo fuzzy."""

    def test_escala_1_5(self):
        assert calculate_fuzzy_value(None, 3, 'escala_1_5') == 3.0
        assert calculate_fuzzy_value(None, 1, 'escala_1_5') == 1.0
        assert calculate_fuzzy_value(None, 5, 'escala_1_5') == 5.0

    def test_escala_sem_valor(self):
        assert calculate_fuzzy_value(None, None, 'escala_1_5') == 3.0

    def test_sim_nao_texto(self):
        assert calculate_fuzzy_value('Sim', None, 'sim_nao') == 5.0
        assert calculate_fuzzy_value('Não', None, 'sim_nao') == 1.0

    def test_sim_nao_numerico(self):
        assert calculate_fuzzy_value(None, 1, 'sim_nao') == 5.0
        assert calculate_fuzzy_value(None, 0, 'sim_nao') == 1.0

    def test_escolha_multipla(self):
        opcoes = ['Papel', 'Excel', 'Software', 'ERP']
        assert calculate_fuzzy_value('Papel', None, 'escolha_multipla', opcoes) == 1.0
        assert calculate_fuzzy_value('ERP', None, 'escolha_multipla', opcoes) == 5.0

    def test_escolha_multipla_meio(self):
        opcoes = ['Papel', 'Excel', 'Software', 'ERP']
        val = calculate_fuzzy_value('Excel', None, 'escolha_multipla', opcoes)
        assert 1.0 < val < 5.0

    def test_texto_livre(self):
        assert calculate_fuzzy_value('excel', None, 'texto_livre') == 2.5
        assert calculate_fuzzy_value('cloud', None, 'texto_livre') == 5.0

    def test_texto_livre_desconhecido(self):
        assert calculate_fuzzy_value('algo random', None, 'texto_livre') == 3.0

    def test_fallback_geral(self):
        assert calculate_fuzzy_value(None, 4, 'tipo_desconhecido') == 4
