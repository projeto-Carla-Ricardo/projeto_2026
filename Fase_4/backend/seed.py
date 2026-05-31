#!/usr/bin/env python3
"""Script para popular a base de dados com dados iniciais do AILO."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app, db
from app.models.ailo import CamadaAilo, Componente, Indicador
from app.models.ferramenta import FerramentaIA
from app.models.utilizador import Utilizador
from app.utils.auth import hash_password
from seeds.seed_data import CAMADAS, COMPONENTES, INDICADORES, FERRAMENTAS_IA

def seed():
    app = create_app('development')
    with app.app_context():
        # Migração: adicionar colunas novas a tabelas existentes (SQLite)
        try:
            db.session.execute(db.text("ALTER TABLE utilizadores ADD COLUMN gemini_api_key VARCHAR(255)"))
            db.session.commit()
            print("✅ Coluna gemini_api_key adicionada")
        except Exception:
            db.session.rollback()
        try:
            db.session.execute(db.text("ALTER TABLE utilizadores ADD COLUMN gemini_model VARCHAR(50) DEFAULT 'gemini-3.5-flash'"))
            db.session.commit()
            print("✅ Coluna gemini_model adicionada")
        except Exception:
            db.session.rollback()
        try:
            db.session.execute(db.text("ALTER TABLE utilizadores ADD COLUMN memoria_ia TEXT"))
            db.session.commit()
            print("✅ Coluna memoria_ia adicionada")
        except Exception:
            db.session.rollback()

        # Verificar se já existe seed
        if CamadaAilo.query.count() > 0:
            print("⚠️  Base de dados já contém dados. A limpar e re-popular...")
            Indicador.query.delete()
            Componente.query.delete()
            CamadaAilo.query.delete()
            FerramentaIA.query.delete()
            db.session.commit()

        # 1. Criar camadas
        camadas_map = {}
        for c in CAMADAS:
            camada = CamadaAilo(**c)
            db.session.add(camada)
            db.session.flush()
            camadas_map[c['ordem']] = camada.id
        print(f"✅ {len(CAMADAS)} camadas criadas")

        # 2. Criar componentes
        comp_map = {}
        for cam_ord, nome, nome_en, desc, peso, ordem in COMPONENTES:
            comp = Componente(camada_id=camadas_map[cam_ord], nome=nome, nome_en=nome_en, descricao=desc, peso=peso, ordem=ordem)
            db.session.add(comp)
            db.session.flush()
            comp_map[(cam_ord, ordem)] = comp.id
        print(f"✅ {len(COMPONENTES)} componentes criados")

        # 3. Criar indicadores
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
            db.session.add(ind)
        print(f"✅ {len(INDICADORES)} indicadores criados")

        # 4. Criar ferramentas IA
        for nome, desc, cam_ord, area, custo, compl, url in FERRAMENTAS_IA:
            f = FerramentaIA(nome=nome, descricao=desc, camada_id=camadas_map.get(cam_ord), area_funcional=area, custo=custo, complexidade=compl, url=url)
            db.session.add(f)
        print(f"✅ {len(FERRAMENTAS_IA)} ferramentas IA criadas")

        # 5. Criar utilizador administrador
        admin = Utilizador.query.filter_by(email='admin@ailo.pt').first()
        if not admin:
            admin = Utilizador(
                nome='Administrador AILO',
                email='admin@ailo.pt',
                password_hash=hash_password('Admin2026!'),
                papel='admin',
                ativo=True
            )
            db.session.add(admin)
            print("✅ Utilizador administrador criado (admin@ailo.pt / Admin2026!)")
        else:
            print("ℹ️  Utilizador administrador já existe")

        # 6. Criar utilizador demo (opcional)
        demo = Utilizador.query.filter_by(email='demo@ailo.pt').first()
        if not demo:
            demo = Utilizador(
                nome='Utilizador Demo',
                email='demo@ailo.pt',
                password_hash=hash_password('Demo2026!'),
                papel='utilizador',
                ativo=True
            )
            db.session.add(demo)
            print("✅ Utilizador demo criado (demo@ailo.pt / Demo2026!)")
        else:
            print("ℹ️  Utilizador demo já existe")

        db.session.commit()
        print("\n🎉 Seed completo!")
        print(f"   Camadas: {CamadaAilo.query.count()}")
        print(f"   Componentes: {Componente.query.count()}")
        print(f"   Indicadores: {Indicador.query.count()}")
        print(f"   Ferramentas: {FerramentaIA.query.count()}")
        print(f"   Utilizadores: {Utilizador.query.count()}")
        print(f"\n📋 Credenciais de Acesso:")
        print(f"   Admin: admin@ailo.pt / Admin2026!")
        print(f"   Demo:  demo@ailo.pt / Demo2026!")

if __name__ == '__main__':
    seed()
