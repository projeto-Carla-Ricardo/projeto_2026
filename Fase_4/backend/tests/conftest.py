"""Fixtures partilhados para todos os testes."""
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import create_app, db as _db
from app.models.utilizador import Utilizador
from app.models.organizacao import Organizacao
from app.models.avaliacao import Avaliacao
from app.utils.auth import hash_password, generate_token


@pytest.fixture(scope='session')
def app():
    """Cria instância da app para testes."""
    app = create_app('testing')
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SECRET_KEY': 'test-secret-key-ailo-2026',
        'JWT_EXPIRATION_HOURS': 24,
    })
    with app.app_context():
        _db.create_all()
        # Seed mínimo para testes
        from seeds.seed_data import CAMADAS, COMPONENTES, INDICADORES
        from app.models.ailo import CamadaAilo, Componente, Indicador
        camadas_map = {}
        for c_data in CAMADAS:
            c = CamadaAilo(**c_data)
            _db.session.add(c)
            _db.session.flush()
            camadas_map[c_data['ordem']] = c.id
        _db.session.commit()
        comp_map = {}
        for cam_ord, nome, nome_en, desc, peso, ordem in COMPONENTES:
            comp = Componente(camada_id=camadas_map[cam_ord], nome=nome, nome_en=nome_en, descricao=desc, peso=peso, ordem=ordem)
            _db.session.add(comp)
            _db.session.flush()
            comp_map[(cam_ord, ordem)] = comp.id
        _db.session.commit()
        for ind_data in INDICADORES:
            cam_ord, comp_ord, codigo, pergunta, n1, n3, n5, peso, ordem = ind_data[:9]
            condicao = ind_data[9] if len(ind_data) > 9 else None
            ind = Indicador(
                componente_id=comp_map[(cam_ord, comp_ord)],
                codigo=codigo, pergunta=pergunta,
                desc_nivel_1=n1, desc_nivel_3=n3, desc_nivel_5=n5,
                desc_nivel_2=None, desc_nivel_4=None,
                peso=peso, obrigatorio=True, ordem=ordem,
                condicao=condicao
            )
            _db.session.add(ind)
        _db.session.commit()
        yield app
        _db.drop_all()


@pytest.fixture(scope='function')
def client(app):
    """Cliente HTTP para testes."""
    return app.test_client()


@pytest.fixture(scope='function')
def db_session(app):
    """Sessão de BD para cada teste."""
    with app.app_context():
        yield _db
        _db.session.rollback()


@pytest.fixture(scope='function')
def user_data():
    """Dados de teste para utilizador."""
    return {
        'nome': 'Teste AILO',
        'email': f'teste_{os.urandom(4).hex()}@ailo.pt',
        'password': 'Teste123!'
    }


@pytest.fixture(scope='function')
def auth_header(client, user_data):
    """Regista utilizador e retorna header de autenticação."""
    res = client.post('/api/v1/auth/register', json=user_data)
    token = res.get_json().get('token')
    return {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}


@pytest.fixture(scope='function')
def org_id(client, auth_header):
    """Cria organização de teste e retorna o ID."""
    res = client.post('/api/v1/organizacoes', json={
        'nome': 'Org Teste',
        'setor': 'Tecnologia',
        'dimensao': 'pequena',
        'tipo': 'pme',
        'pais': 'Portugal'
    }, headers=auth_header)
    return res.get_json()['id']


@pytest.fixture(scope='function')
def avaliacao_id(client, auth_header, org_id):
    """Cria avaliação de teste e retorna o ID."""
    res = client.post('/api/v1/avaliacoes', json={
        'organizacao_id': org_id
    }, headers=auth_header)
    return res.get_json()['id']
