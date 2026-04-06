"""
Serviço de Geração de Relatórios — Gera dados estruturados para relatório PDF e web.
"""
from datetime import datetime, timezone
from app import db
from app.models.avaliacao import Avaliacao
from app.models.empresa import Empresa
from app.models.relatorio import Relatorio
from app.services.scoring_engine import calcular_scoring_completo, NIVEL_NOMES
from app.services.recommendation_engine import gerar_recomendacoes


def gerar_relatorio(avaliacao_id):
    """
    Gera o relatório completo de diagnóstico IALO.
    Retorna dict com toda a informação para renderização web e PDF.
    """
    avaliacao = Avaliacao.query.get(avaliacao_id)
    if not avaliacao:
        return None

    empresa = Empresa.query.get(avaliacao.empresa_id)
    if not empresa:
        return None

    # Garantir que o scoring está calculado
    scoring = calcular_scoring_completo(avaliacao_id)

    # Gerar recomendações
    recomendacoes = gerar_recomendacoes(avaliacao_id, empresa)

    # Identificar pontos fortes (dimensões ≥ 60%)
    pontos_fortes = [
        {
            'dimensao': d['nome'],
            'codigo': d['codigo'],
            'pontuacao': d['pontuacao'],
            'nivel': d['nivel'],
            'destaque': _destaque_ponto_forte(d['codigo'], d['nivel'])
        }
        for d in scoring['dimensoes'] if d['pontuacao'] >= 60
    ]
    pontos_fortes.sort(key=lambda x: x['pontuacao'], reverse=True)

    # Identificar necessidades (dimensões < 60%)
    necessidades = [
        {
            'dimensao': d['nome'],
            'codigo': d['codigo'],
            'pontuacao': d['pontuacao'],
            'nivel': d['nivel'],
            'gap_critico': d['gap_critico'],
            'acao': _acao_necessidade(d['codigo'], d['nivel'])
        }
        for d in scoring['dimensoes'] if d['pontuacao'] < 60
    ]
    necessidades.sort(key=lambda x: x['pontuacao'])

    # Primeiros passos (top 3 ações prioritárias)
    primeiros_passos = []
    for rec in recomendacoes:
        if rec['prioridade'] in ['alta', 'média'] and len(primeiros_passos) < 3:
            primeiros_passos.append({
                'dimensao': rec['dimensao'],
                'acao': rec['acao_sugerida'],
                'ferramenta': rec['ferramentas'][0]['ferramenta']['nome'] if rec['ferramentas'] else None,
            })

    # Construir relatório
    relatorio_data = {
        'titulo': f'Diagnóstico de Maturidade Digital — {empresa.nome}',
        'data_geracao': datetime.now(timezone.utc).isoformat(),
        'empresa': {
            'nome': empresa.nome,
            'setor': empresa.setor,
            'num_colaboradores': empresa.num_colaboradores,
            'localizacao': empresa.localizacao,
            'descricao': empresa.descricao,
        },
        'resumo': {
            'pontuacao_global': scoring['pontuacao_global'],
            'nivel_global': scoring['nivel_global'],
            'nivel_descricao': scoring['nivel_descricao'],
            'total_dimensoes': len(scoring['dimensoes']),
            'gaps_criticos': len(scoring['gaps_criticos']),
        },
        'dimensoes': scoring['dimensoes'],
        'pontos_fortes': pontos_fortes,
        'necessidades': necessidades,
        'primeiros_passos': primeiros_passos,
        'recomendacoes': recomendacoes,
        'radar_data': {
            'labels': [d['nome'] for d in scoring['dimensoes']],
            'values': [d['pontuacao'] for d in scoring['dimensoes']],
            'max': 100,
        },
    }

    # Guardar ou atualizar na BD
    relatorio = Relatorio.query.filter_by(avaliacao_id=avaliacao_id).first()
    if relatorio:
        relatorio.conteudo_json = str(relatorio_data)
        relatorio.gerado_em = datetime.now(timezone.utc)
    else:
        relatorio = Relatorio(
            avaliacao_id=avaliacao_id,
            conteudo_json=str(relatorio_data)
        )
        db.session.add(relatorio)

    db.session.commit()

    return relatorio_data


def _destaque_ponto_forte(codigo, nivel):
    """Destaque positivo por dimensão."""
    destaques = {
        'DADOS': 'A empresa já demonstra práticas de recolha e utilização de dados.',
        'INFRA': 'A infraestrutura tecnológica está num bom nível para o perfil da empresa.',
        'COMP': 'A equipa demonstra competências digitais sólidas.',
        'ESTR': 'A empresa tem uma visão estratégica clara para a digitalização.',
        'CULT': 'A cultura organizacional é aberta à inovação e mudança.',
    }
    return destaques.get(codigo, 'Bom desempenho nesta dimensão.')


def _acao_necessidade(codigo, nivel):
    """Ação prioritária por necessidade."""
    acoes = {
        'DADOS': 'Priorizar a organização e digitalização dos dados do negócio.',
        'INFRA': 'Investir em equipamento e ferramentas digitais básicas.',
        'COMP': 'Promover formação digital para a equipa.',
        'ESTR': 'Definir uma estratégia digital simples e mensurável.',
        'CULT': 'Fomentar uma cultura de abertura à mudança e experimentação.',
    }
    return acoes.get(codigo, 'Identificar oportunidades de melhoria.')
