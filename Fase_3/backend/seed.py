#!/usr/bin/env python3
"""Script para popular a base de dados com dados iniciais do AILO."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app, db
from app.models.ailo import CamadaAilo, Componente, Indicador
from app.models.ferramenta import FerramentaIA
from seeds.seed_data import CAMADAS, COMPONENTES, INDICADORES, FERRAMENTAS_IA

def seed():
    app = create_app('development')
    with app.app_context():
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
        for cam_ord, comp_ord, codigo, pergunta, n1, n3, n5, peso, ordem in INDICADORES:
            ind = Indicador(
                componente_id=comp_map[(cam_ord, comp_ord)],
                codigo=codigo, pergunta=pergunta,
                desc_nivel_1=n1, desc_nivel_3=n3, desc_nivel_5=n5,
                desc_nivel_2=None, desc_nivel_4=None,
                peso=peso, obrigatorio=True, ordem=ordem
            )
            db.session.add(ind)
        print(f"✅ {len(INDICADORES)} indicadores criados")

        # 4. Criar ferramentas IA
        for nome, desc, cam_ord, area, custo, compl, url in FERRAMENTAS_IA:
            f = FerramentaIA(nome=nome, descricao=desc, camada_id=camadas_map.get(cam_ord), area_funcional=area, custo=custo, complexidade=compl, url=url)
            db.session.add(f)
        print(f"✅ {len(FERRAMENTAS_IA)} ferramentas IA criadas")

        db.session.commit()
        print("\n🎉 Seed completo!")
        print(f"   Camadas: {CamadaAilo.query.count()}")
        print(f"   Componentes: {Componente.query.count()}")
        print(f"   Indicadores: {Indicador.query.count()}")
        print(f"   Ferramentas: {FerramentaIA.query.count()}")

if __name__ == '__main__':
    seed()
