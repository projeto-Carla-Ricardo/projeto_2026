"""
Conftest — Fixtures partilhadas para testes.
Cria a app Flask em modo testing com BD SQLite in-memory.
"""
import json
import pytest
from app import create_app, db as _db
from app.models.utilizador import Utilizador
from app.models.empresa import Empresa
from app.models.avaliacao import Avaliacao
from app.models.dimensao import Dimensao
from app.models.indicador import Indicador
from app.models.pergunta import Pergunta
from app.models.resposta import Resposta
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()


@pytest.fixture(scope='session')
def app():
    """Criar a aplicação Flask de teste (uma vez por sessão)."""
    app = create_app('testing')
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.app_context():
        _db.create_all()
        _seed_test_data()
        yield app
        _db.drop_all()


@pytest.fixture(scope='function')
def db(app):
    """Garantir que cada teste tem uma sessão limpa."""
    with app.app_context():
        yield _db
        _db.session.rollback()


@pytest.fixture(scope='session')
def client(app):
    """Cliente de teste HTTP."""
    return app.test_client()


@pytest.fixture(scope='session')
def auth_headers(client):
    """Headers de autenticação com JWT (utilizador normal)."""
    res = client.post('/api/v1/auth/login', json={
        'email': 'teste@ialo.pt',
        'password': 'password123'
    })
    data = res.get_json()
    token = data['data']['token']
    return {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}


@pytest.fixture(scope='session')
def admin_headers(client):
    """Headers de autenticação com JWT (admin)."""
    res = client.post('/api/v1/auth/login', json={
        'email': 'admin@ialo.pt',
        'password': 'admin12345'
    })
    data = res.get_json()
    token = data['data']['token']
    return {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}


def _seed_test_data():
    """Povoar BD de teste com dados mínimos."""
    # Utilizador normal
    user = Utilizador(
        nome='Teste IALO',
        email='teste@ialo.pt',
        password_hash=bcrypt.generate_password_hash('password123').decode('utf-8'),
        role='empresario'
    )
    _db.session.add(user)

    # Admin
    admin = Utilizador(
        nome='Admin IALO',
        email='admin@ialo.pt',
        password_hash=bcrypt.generate_password_hash('admin12345').decode('utf-8'),
        role='admin'
    )
    _db.session.add(admin)
    _db.session.flush()

    # Empresa
    empresa = Empresa(
        nome='Padaria Teste',
        setor='Alimentar',
        num_colaboradores=3,
        localizacao='Porto',
        utilizador_id=user.id
    )
    _db.session.add(empresa)
    _db.session.flush()

    # 5 Dimensões com 5 indicadores e 5 perguntas cada
    dimensoes_data = [
        {'codigo': 'DADOS', 'nome': 'Dados', 'peso': 0.25, 'ordem': 1},
        {'codigo': 'INFRA', 'nome': 'Infraestrutura', 'peso': 0.20, 'ordem': 2},
        {'codigo': 'COMP', 'nome': 'Competências', 'peso': 0.20, 'ordem': 3},
        {'codigo': 'ESTR', 'nome': 'Estratégia', 'peso': 0.20, 'ordem': 4},
        {'codigo': 'CULT', 'nome': 'Cultura', 'peso': 0.15, 'ordem': 5},
    ]

    pergunta_id_counter = 1
    for d in dimensoes_data:
        dim = Dimensao(codigo=d['codigo'], nome=d['nome'], peso=d['peso'], ordem=d['ordem'])
        _db.session.add(dim)
        _db.session.flush()

        for j in range(1, 6):
            ind = Indicador(
                codigo=f"{d['codigo']}{j}",
                nome=f"Indicador {j} de {d['nome']}",
                dimensao_id=dim.id,
                ordem=j
            )
            _db.session.add(ind)
            _db.session.flush()

            pergunta = Pergunta(
                texto=f"Pergunta {pergunta_id_counter} ({d['nome']})",
                tipo_resposta='escala_1_5',
                indicador_id=ind.id,
                ordem=1
            )
            _db.session.add(pergunta)
            pergunta_id_counter += 1

    _db.session.commit()
