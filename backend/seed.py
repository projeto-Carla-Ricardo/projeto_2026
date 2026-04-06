"""
Script de seed — Popula a base de dados com dados iniciais do Framework IALO.
Uso: python seed.py
"""
import json
import os
import sys

# Adicionar o diretório pai ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

from app import create_app, db
from app.models.dimensao import Dimensao
from app.models.indicador import Indicador
from app.models.pergunta import Pergunta
from app.models.ferramenta import FerramentaIA


SEEDS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'seeds')


def load_json(filename):
    """Carrega um ficheiro JSON da pasta seeds."""
    filepath = os.path.join(SEEDS_DIR, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def seed_dimensoes():
    """Seed das 5 dimensões do Framework IALO."""
    data = load_json('dimensoes.json')
    count = 0
    for item in data:
        existing = Dimensao.query.filter_by(codigo=item['codigo']).first()
        if not existing:
            dim = Dimensao(
                codigo=item['codigo'],
                nome=item['nome'],
                descricao=item['descricao'],
                peso=item['peso'],
                ordem=item['ordem']
            )
            db.session.add(dim)
            count += 1
    db.session.commit()
    print(f'  ✓ {count} dimensões inseridas (total: {Dimensao.query.count()})')


def seed_indicadores():
    """Seed dos 25 indicadores (5 por dimensão)."""
    data = load_json('indicadores.json')
    count = 0
    for item in data:
        existing = Indicador.query.filter_by(codigo=item['codigo']).first()
        if not existing:
            dimensao = Dimensao.query.filter_by(codigo=item['dimensao_codigo']).first()
            if dimensao:
                ind = Indicador(
                    dimensao_id=dimensao.id,
                    codigo=item['codigo'],
                    nome=item['nome'],
                    descricao=item['descricao'],
                    ordem=item['ordem']
                )
                db.session.add(ind)
                count += 1
            else:
                print(f'  ⚠ Dimensão {item["dimensao_codigo"]} não encontrada para indicador {item["codigo"]}')
    db.session.commit()
    print(f'  ✓ {count} indicadores inseridos (total: {Indicador.query.count()})')


def seed_perguntas():
    """Seed das 25 perguntas do questionário IALO."""
    data = load_json('perguntas.json')
    count = 0
    for item in data:
        indicador = Indicador.query.filter_by(codigo=item['indicador_codigo']).first()
        if indicador:
            # Verificar se já existe uma pergunta para este indicador
            existing = Pergunta.query.filter_by(indicador_id=indicador.id, ordem=item['ordem']).first()
            if not existing:
                opcoes_json = json.dumps(item['opcoes'], ensure_ascii=False) if item['opcoes'] else None
                perg = Pergunta(
                    indicador_id=indicador.id,
                    texto=item['texto'],
                    tipo_resposta=item['tipo_resposta'],
                    opcoes_json=opcoes_json,
                    ordem=item['ordem'],
                    obrigatoria=item['obrigatoria'],
                    ajuda_contextual=item.get('ajuda_contextual')
                )
                db.session.add(perg)
                count += 1
        else:
            print(f'  ⚠ Indicador {item["indicador_codigo"]} não encontrado para pergunta')
    db.session.commit()
    print(f'  ✓ {count} perguntas inseridas (total: {Pergunta.query.count()})')


def seed_ferramentas():
    """Seed do catálogo de ferramentas IA."""
    data = load_json('ferramentas_ia.json')
    count = 0
    for item in data:
        existing = FerramentaIA.query.filter_by(nome=item['nome']).first()
        if not existing:
            ferr = FerramentaIA(
                nome=item['nome'],
                descricao=item['descricao'],
                categoria=item['categoria'],
                custo=item['custo'],
                complexidade=item['complexidade'],
                url=item.get('url'),
                setores_alvo=json.dumps(item.get('setores_alvo', []), ensure_ascii=False),
                ativo=True
            )
            db.session.add(ferr)
            count += 1
    db.session.commit()
    print(f'  ✓ {count} ferramentas IA inseridas (total: {FerramentaIA.query.count()})')


def run_seed():
    """Executa todas as seeds por ordem."""
    print('\n🌱 A popular base de dados IALO...\n')

    print('1/4 Dimensões do Framework IALO')
    seed_dimensoes()

    print('2/4 Indicadores (5 por dimensão)')
    seed_indicadores()

    print('3/4 Perguntas do Questionário')
    seed_perguntas()

    print('4/4 Catálogo de Ferramentas IA')
    seed_ferramentas()

    print('\n✅ Seed concluído com sucesso!\n')


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        run_seed()
