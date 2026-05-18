"""Serviço de Recomendações — cruza diagnóstico com catálogo de ferramentas IA."""
from app import db
from app.models.ferramenta import FerramentaIA, Recomendacao
from app.models.resultado import ResultadoCamada


def gerar_recomendacoes(avaliacao_id):
    """Gera recomendações de ferramentas IA com base nos resultados.
    
    Lógica:
    1. Identifica camadas com score mais baixo (lacunas)
    2. Cruza com ferramentas do catálogo por camada
    3. Prioriza por: gravidade da lacuna × facilidade de implementação
    
    Returns:
        Lista de Recomendacao criadas
    """
    resultados = ResultadoCamada.query.filter_by(avaliacao_id=avaliacao_id).all()
    if not resultados:
        return []

    # Limpar recomendações anteriores desta avaliação
    Recomendacao.query.filter_by(avaliacao_id=avaliacao_id).delete()

    recomendacoes = []
    prioridade = 1

    # Ordenar camadas por score (pior primeiro = mais prioritário)
    resultados_sorted = sorted(resultados, key=lambda r: r.score)

    for resultado in resultados_sorted:
        # Buscar ferramentas da camada
        ferramentas = FerramentaIA.query.filter_by(
            camada_id=resultado.camada_id, ativo=True
        ).all()

        if not ferramentas:
            continue

        # Priorizar ferramentas por complexidade (mais simples primeiro para camadas fracas)
        complexidade_order = {'baixa': 0, 'média': 1, 'media': 1, 'alta': 2}
        ferramentas_sorted = sorted(
            ferramentas,
            key=lambda f: complexidade_order.get(f.complexidade.lower(), 1)
        )

        for ferramenta in ferramentas_sorted[:2]:  # máx 2 ferramentas por camada
            # Gerar justificação contextualizada
            if resultado.score <= 2.0:
                urgencia = "crítica"
                justificacao = (f"A camada {resultado.camada.nome} apresenta um nível {resultado.nivel} "
                               f"(score {resultado.score:.1f}). A implementação de {ferramenta.nome} é "
                               f"prioritária para elevar a maturidade nesta dimensão.")
            elif resultado.score <= 3.5:
                urgencia = "moderada"
                justificacao = (f"A camada {resultado.camada.nome} está no nível {resultado.nivel} "
                               f"(score {resultado.score:.1f}). {ferramenta.nome} pode ajudar a "
                               f"consolidar e avançar para o próximo patamar de maturidade.")
            else:
                urgencia = "melhoria"
                justificacao = (f"A camada {resultado.camada.nome} já apresenta bom desempenho "
                               f"({resultado.nivel}, score {resultado.score:.1f}). {ferramenta.nome} "
                               f"pode otimizar ainda mais os processos existentes.")

            rec = Recomendacao(
                avaliacao_id=avaliacao_id,
                ferramenta_id=ferramenta.id,
                camada_id=resultado.camada_id,
                prioridade=prioridade,
                justificacao=justificacao
            )
            db.session.add(rec)
            recomendacoes.append(rec)
            prioridade += 1

    db.session.commit()
    return recomendacoes
