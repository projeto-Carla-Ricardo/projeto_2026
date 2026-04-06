"""
Testes de Integração — Fluxo completo
Testa o pipeline: Registo → Empresa → Avaliação → Respostas → Scoring → Relatório
"""
import pytest


class TestFluxoCompleto:
    """Teste de integração do fluxo completo de diagnóstico."""

    def test_pipeline_diagnostico(self, client):
        """Testa o pipeline completo de ponta a ponta."""

        # 1. REGISTO
        res = client.post('/api/v1/auth/register', json={
            'nome': 'Maria Silva',
            'email': 'maria@padaria.pt',
            'password': 'padaria2026'
        })
        assert res.status_code == 201, f"Registo falhou: {res.get_json()}"

        # 2. LOGIN
        res = client.post('/api/v1/auth/login', json={
            'email': 'maria@padaria.pt',
            'password': 'padaria2026'
        })
        assert res.status_code == 200
        token = res.get_json()['data']['token']
        headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}

        # 3. CRIAR EMPRESA
        res = client.post('/api/v1/empresas', headers=headers, json={
            'nome': 'Padaria da Maria',
            'setor': 'Alimentar',
            'num_colaboradores': 4,
            'localizacao': 'Braga'
        })
        assert res.status_code == 201
        empresa_id = res.get_json()['data']['id']

        # 4. CRIAR AVALIAÇÃO
        res = client.post('/api/v1/avaliacoes', headers=headers, json={
            'empresa_id': empresa_id
        })
        assert res.status_code == 201
        avaliacao_id = res.get_json()['data']['id']
        assert res.get_json()['data']['estado'] == 'em_curso'

        # 5. VERIFICAR DIMENSÕES
        res = client.get('/api/v1/questionario/dimensoes', headers=headers)
        assert res.status_code == 200
        dimensoes = res.get_json()['data']
        assert len(dimensoes) == 5

        # 6. SUBMETER RESPOSTAS (cenário realista: padaria pequena)
        respostas = []
        valores = {
            'DADOS': 2,   # Usa papel e excel
            'INFRA': 3,   # Tem computador e internet
            'COMP': 2,    # Pouca formação digital
            'ESTR': 1,    # Sem estratégia digital
            'CULT': 3,    # Aberta a mudança
        }

        pergunta_id = 1
        for dim in dimensoes:
            dim_cod = dim['codigo']
            for _ in dim.get('indicadores', [{}]):
                respostas.append({
                    'pergunta_id': pergunta_id,
                    'valor_numerico': valores.get(dim_cod, 3)
                })
                pergunta_id += 1

        res = client.post('/api/v1/questionario/respostas', headers=headers, json={
            'avaliacao_id': avaliacao_id,
            'respostas': respostas
        })
        assert res.status_code == 200, f"Guardar respostas falhou: {res.get_json()}"

        # 7. CONCLUIR DIAGNÓSTICO (trigger scoring)
        res = client.post(f'/api/v1/avaliacoes/{avaliacao_id}/concluir', headers=headers)
        assert res.status_code == 200
        scoring = res.get_json()['data']
        assert 'pontuacao_global' in scoring
        assert 'nivel_global' in scoring
        assert 'dimensoes' in scoring
        assert len(scoring['dimensoes']) == 5

        # 8. VERIFICAR SCORING
        # ESTR (valor=1) deve ter gap crítico (20%)
        estr = next(d for d in scoring['dimensoes'] if d['codigo'] == 'ESTR')
        assert estr['gap_critico'] is True
        assert estr['pontuacao'] <= 40.0

        # INFRA (valor=3) deve estar ~60%
        infra = next(d for d in scoring['dimensoes'] if d['codigo'] == 'INFRA')
        assert 40.0 <= infra['pontuacao'] <= 80.0

        # 9. GERAR RELATÓRIO
        res = client.get(f'/api/v1/relatorios/{avaliacao_id}', headers=headers)
        assert res.status_code == 200
        relatorio = res.get_json()['data']

        assert relatorio['empresa']['nome'] == 'Padaria da Maria'
        assert 'pontos_fortes' in relatorio
        assert 'necessidades' in relatorio
        assert 'primeiros_passos' in relatorio
        assert 'recomendacoes' in relatorio
        assert 'radar_data' in relatorio
        assert len(relatorio['radar_data']['labels']) == 5

        # 10. VERIFICAR RECOMENDAÇÕES
        res = client.get(f'/api/v1/relatorios/{avaliacao_id}/recomendacoes', headers=headers)
        assert res.status_code == 200
        recs = res.get_json()['data']
        assert isinstance(recs, list)

        # As dimensões com gap devem ter recomendações priorizadas
        estr_rec = next((r for r in recs if r['codigo'] == 'ESTR'), None)
        if estr_rec:
            assert estr_rec['prioridade'] == 'alta'

        print(f"\n✅ Pipeline completo OK!")
        print(f"   Pontuação: {scoring['pontuacao_global']}%")
        print(f"   Nível: {scoring['nivel_descricao']}")
        print(f"   Gaps: {len(scoring['gaps_criticos'])}")
        print(f"   Recomendações: {len(recs)} dimensões")


class TestConsistenciaRelatorios:
    """Testes de validação de consistência dos relatórios."""

    def test_relatorio_avaliacao_nao_concluida(self, client, auth_headers):
        """Relatório não deve ser gerado para avaliação em curso."""
        # Criar avaliação sem concluir
        res = client.get('/api/v1/empresas', headers=auth_headers)
        empresa_id = res.get_json()['data'][0]['id']

        res = client.post('/api/v1/avaliacoes', headers=auth_headers, json={
            'empresa_id': empresa_id
        })
        avaliacao_id = res.get_json()['data']['id']

        res = client.get(f'/api/v1/relatorios/{avaliacao_id}', headers=auth_headers)
        assert res.status_code == 400

    def test_relatorio_avaliacao_inexistente(self, client, auth_headers):
        """Relatório para avaliação inexistente deve retornar 404."""
        res = client.get('/api/v1/relatorios/99999', headers=auth_headers)
        assert res.status_code == 404


class TestSegurancaAcesso:
    """Testes de segurança de acesso entre utilizadores."""

    def test_utilizador_nao_acede_empresa_alheia(self, client):
        """Um utilizador não deve aceder a empresas de outro."""
        # Criar segundo utilizador
        client.post('/api/v1/auth/register', json={
            'nome': 'Intruso',
            'email': 'intruso@ialo.pt',
            'password': 'intruso123'
        })
        res = client.post('/api/v1/auth/login', json={
            'email': 'intruso@ialo.pt',
            'password': 'intruso123'
        })
        token2 = res.get_json()['data']['token']
        headers2 = {'Authorization': f'Bearer {token2}', 'Content-Type': 'application/json'}

        # Tentar aceder empresa do primeiro utilizador (id=1)
        res = client.get('/api/v1/empresas/1', headers=headers2)
        assert res.status_code in [403, 404]
