"""Análise de Interdependências entre Camadas AILO."""
import json
from app import db
from app.models.resultado import ResultadoCamada, Interdependencia
from app.models.ailo import CamadaAilo

# Pares críticos definidos no framework
PARES_CRITICOS = [
    ('Humana', 'Avaliação', 'Se ambas altas, double-loop learning é provável. Se ambas baixas, a organização não aprende com a experiência.'),
    ('Cognitiva (IA)', 'Tecnológica', 'Se cognitiva alta mas tecnológica baixa, há risco de implementação. A ambição de IA requer infraestrutura adequada.'),
    ('Organizacional', 'Humana', 'Se organizacional alta mas humana baixa, existe estratégia sem capacidade de execução.'),
    ('Avaliação', 'Cognitiva (IA)', 'Se avaliação baixa, a IA pode bypass-ar etapas críticas de absorção de conhecimento (CR5).'),
]

def analisar_interdependencias(avaliacao_id):
    """Analisa pares de camadas e gera interdependências."""
    resultados = ResultadoCamada.query.filter_by(avaliacao_id=avaliacao_id).all()
    scores = {}
    for r in resultados:
        camada = CamadaAilo.query.get(r.camada_id)
        if camada:
            scores[camada.nome] = {'id': camada.id, 'score': r.score}

    interdeps = []
    for nome_a, nome_b, descricao_base in PARES_CRITICOS:
        if nome_a not in scores or nome_b not in scores:
            continue
        sa, sb = scores[nome_a]['score'], scores[nome_b]['score']
        ida, idb = scores[nome_a]['id'], scores[nome_b]['id']

        if sa >= 3.5 and sb >= 3.5:
            tipo, impacto = 'fortalece', 'alto'
            desc = f"Boa maturidade em {nome_a} e {nome_b}. {descricao_base}"
        elif sa >= 3.5 and sb < 2.7:
            tipo, impacto = 'risco', 'alto'
            desc = f"Desequilíbrio: {nome_a} avançada mas {nome_b} em atraso. {descricao_base}"
        elif sa < 2.7 and sb >= 3.5:
            tipo, impacto = 'risco', 'alto'
            desc = f"Desequilíbrio: {nome_b} avançada mas {nome_a} em atraso. {descricao_base}"
        elif sa < 2.7 and sb < 2.7:
            tipo, impacto = 'bloqueia', 'alto'
            desc = f"Ambas as camadas com baixa maturidade. {descricao_base}"
        else:
            tipo, impacto = 'oportunidade', 'medio'
            desc = f"Ambas em desenvolvimento. {descricao_base}"

        interdep = Interdependencia(
            avaliacao_id=avaliacao_id, camada_a_id=ida, camada_b_id=idb,
            tipo_relacao=tipo, descricao=desc, impacto=impacto
        )
        db.session.add(interdep)
        interdeps.append(interdep)

    db.session.commit()
    return interdeps
