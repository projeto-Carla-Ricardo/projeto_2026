"""Motor de Scoring AILO — Cálculo multicamada de maturidade organizacional."""
import json
from app.models.ailo import CamadaAilo, Componente, Indicador
from app.models.resposta import Resposta
from app.models.resultado import ResultadoCamada
from app.models.avaliacao import Avaliacao
from app import db

# Mapeamento CR por camada
CR_MAP = {
    'Organizacional': ['CR3', 'CR6'],
    'Humana': ['CR2', 'CR3'],
    'Aprendizagem': ['CR4'],
    'Cognitiva (IA)': ['CR1'],
    'Tecnológica': ['CR3', 'CR6'],
    'Avaliação': ['CR5'],
}

NIVEIS = [
    (1.0, 1.8, 'Inicial'),
    (1.9, 2.6, 'Em Desenvolvimento'),
    (2.7, 3.4, 'Definido'),
    (3.5, 4.2, 'Gerido'),
    (4.3, 5.0, 'Otimizado'),
]

def classificar_nivel(score):
    for low, high, nome in NIVEIS:
        if low <= score <= high:
            return nome
    return 'Indefinido'

def calcular_scoring(avaliacao_id):
    """Calcula todos os scores para uma avaliação completa."""
    avaliacao = Avaliacao.query.get(avaliacao_id)
    if not avaliacao:
        return None

    respostas = {r.indicador_id: r.score for r in Resposta.query.filter_by(avaliacao_id=avaliacao_id).all()}
    camadas = CamadaAilo.query.order_by(CamadaAilo.ordem).all()
    resultados = []
    scores_camada = {}

    for camada in camadas:
        scores_comp = []
        pontos_fortes = []
        lacunas = []
        recomendacoes = []

        for comp in camada.componentes:
            ind_scores = []
            for ind in comp.indicadores:
                s = respostas.get(ind.id)
                if s is not None:
                    ind_scores.append(s * ind.peso)
                    if s >= 4:
                        pontos_fortes.append(f"{comp.nome}: {ind.pergunta[:80]}")
                    elif s <= 2:
                        lacunas.append(f"{comp.nome}: {ind.pergunta[:80]}")
                        recomendacoes.append(f"Melhorar {comp.nome.lower()}: {ind.desc_nivel_5[:100]}")

            if ind_scores:
                total_peso = sum(ind.peso for ind in comp.indicadores if respostas.get(ind.id) is not None)
                comp_score = sum(ind_scores) / total_peso if total_peso > 0 else 0
                scores_comp.append((comp_score, comp.peso))

        if scores_comp:
            total_peso = sum(p for _, p in scores_comp)
            camada_score = sum(s * p for s, p in scores_comp) / total_peso if total_peso > 0 else 0
        else:
            camada_score = 0

        scores_camada[camada.id] = camada_score
        nivel = classificar_nivel(camada_score)
        crs = CR_MAP.get(camada.nome, [])

        # Limitar listas
        pontos_fortes = pontos_fortes[:5]
        lacunas = lacunas[:5]
        recomendacoes = recomendacoes[:5]

        resultado = ResultadoCamada(
            avaliacao_id=avaliacao_id, camada_id=camada.id,
            score=round(camada_score, 2), nivel=nivel,
            pontos_fortes=json.dumps(pontos_fortes, ensure_ascii=False),
            lacunas=json.dumps(lacunas, ensure_ascii=False),
            recomendacoes=json.dumps(recomendacoes, ensure_ascii=False),
            cr_mapeamento=json.dumps(crs)
        )
        db.session.add(resultado)
        resultados.append(resultado)

    # Score global (média ponderada das camadas)
    total_peso = sum(c.peso for c in camadas)
    score_global = sum(scores_camada.get(c.id, 0) * c.peso for c in camadas) / total_peso if total_peso > 0 else 0
    nivel_global = classificar_nivel(score_global)

    avaliacao.score_global = round(score_global, 2)
    avaliacao.nivel_global = nivel_global

    db.session.commit()
    return {'score_global': round(score_global, 2), 'nivel_global': nivel_global, 'resultados': resultados}
