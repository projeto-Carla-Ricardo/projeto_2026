"""
Motor de Scoring IALO — O "Cérebro" do sistema.
Implementa as regras do Framework IALO para calcular maturidade digital.
"""
import json
from datetime import datetime, timezone
from app import db
from app.models.dimensao import Dimensao
from app.models.indicador import Indicador
from app.models.pergunta import Pergunta
from app.models.resposta import Resposta
from app.models.resultado import ResultadoDimensao
from app.models.avaliacao import Avaliacao
from app.utils.fuzzy_logic import calculate_fuzzy_value


# Nomes dos níveis de maturidade
NIVEL_NOMES = {
    1: 'Inicial',
    2: 'Em Desenvolvimento',
    3: 'Definido',
    4: 'Gerido',
    5: 'Otimizado'
}


def pontuacao_para_nivel(pontuacao_percentual):
    """
    Converte uma pontuação percentual (0-100) num nível de maturidade (1-5).
    Baseado na tabela definida em docs/fase1/analise_framework_ialo.md
    """
    if pontuacao_percentual <= 20:
        return 1
    elif pontuacao_percentual <= 40:
        return 2
    elif pontuacao_percentual <= 60:
        return 3
    elif pontuacao_percentual <= 80:
        return 4
    else:
        return 5


def calcular_pontuacao_dimensao(avaliacao_id, dimensao):
    """
    Calcula a pontuação de uma dimensão (0-100%) com base nas respostas.

    Fórmula: Pontuação = (Σ valores_fuzzy) / (nº_indicadores × 5) × 100%
    """
    indicadores = Indicador.query.filter_by(dimensao_id=dimensao.id).order_by(Indicador.ordem).all()

    if not indicadores:
        return 0.0, []

    scores_indicador = []

    for indicador in indicadores:
        perguntas = Pergunta.query.filter_by(indicador_id=indicador.id).all()

        if not perguntas:
            scores_indicador.append({
                'codigo': indicador.codigo,
                'nome': indicador.nome,
                'pontuacao': 0.0,
            })
            continue

        soma_fuzzy = 0.0
        n_respostas = 0

        for pergunta in perguntas:
            resposta = Resposta.query.filter_by(
                avaliacao_id=avaliacao_id,
                pergunta_id=pergunta.id
            ).first()

            if resposta:
                # Se já tem valor_fuzzy calculado, usar direto
                if resposta.valor_fuzzy is not None:
                    fuzzy_val = resposta.valor_fuzzy
                else:
                    # Calcular fuzzy a partir da resposta
                    opcoes = None
                    if pergunta.opcoes_json:
                        try:
                            opcoes = json.loads(pergunta.opcoes_json)
                        except (json.JSONDecodeError, TypeError):
                            opcoes = None

                    fuzzy_val = calculate_fuzzy_value(
                        resposta.valor_texto,
                        resposta.valor_numerico,
                        pergunta.tipo_resposta,
                        opcoes
                    )

                    # Guardar o valor fuzzy na resposta para cache
                    resposta.valor_fuzzy = fuzzy_val

                soma_fuzzy += fuzzy_val
                n_respostas += 1

        # Pontuação do indicador: média dos fuzzy das perguntas
        pontuacao_indicador = (soma_fuzzy / n_respostas) if n_respostas > 0 else 0.0
        scores_indicador.append({
            'codigo': indicador.codigo,
            'nome': indicador.nome,
            'pontuacao': round(pontuacao_indicador, 2),
        })

    # Pontuação da dimensão: média dos indicadores, convertida para %
    soma_indicadores = sum(s['pontuacao'] for s in scores_indicador)
    n_indicadores = len(scores_indicador)
    pontuacao_pct = (soma_indicadores / (n_indicadores * 5)) * 100 if n_indicadores > 0 else 0.0

    return round(pontuacao_pct, 1), scores_indicador


def identificar_gap_critico(pontuacao_pct):
    """
    Um gap é crítico quando a pontuação é ≤ 40%.
    """
    return pontuacao_pct <= 40.0


def calcular_scoring_completo(avaliacao_id):
    """
    Calcula o scoring completo para uma avaliação:
    1. Pontuação por dimensão
    2. Índice global ponderado
    3. Identificação de gaps
    4. Nível de maturidade

    Retorna dict com todos os resultados.
    """
    dimensoes = Dimensao.query.order_by(Dimensao.ordem).all()

    resultados_dimensao = []
    pontuacao_global_ponderada = 0.0
    max_pontuacao = 0.0
    min_pontuacao = 100.0

    for dimensao in dimensoes:
        pontuacao_pct, indicadores = calcular_pontuacao_dimensao(avaliacao_id, dimensao)
        nivel = pontuacao_para_nivel(pontuacao_pct)
        gap = identificar_gap_critico(pontuacao_pct)

        # Guardar ou atualizar resultado na BD
        resultado = ResultadoDimensao.query.filter_by(
            avaliacao_id=avaliacao_id,
            dimensao_id=dimensao.id
        ).first()

        if resultado:
            resultado.pontuacao = pontuacao_pct
            resultado.nivel = nivel
            resultado.gap_critico = gap
        else:
            resultado = ResultadoDimensao(
                avaliacao_id=avaliacao_id,
                dimensao_id=dimensao.id,
                pontuacao=pontuacao_pct,
                nivel=nivel,
                gap_critico=gap
            )
            db.session.add(resultado)

        # Contribuição ponderada para o índice global
        pontuacao_global_ponderada += pontuacao_pct * dimensao.peso

        # Track min/max para gap por diferença
        max_pontuacao = max(max_pontuacao, pontuacao_pct)
        min_pontuacao = min(min_pontuacao, pontuacao_pct)

        resultados_dimensao.append({
            'dimensao_id': dimensao.id,
            'codigo': dimensao.codigo,
            'nome': dimensao.nome,
            'peso': dimensao.peso,
            'pontuacao': pontuacao_pct,
            'nivel': nivel,
            'nivel_nome': NIVEL_NOMES.get(nivel, '?'),
            'gap_critico': gap,
            'indicadores': indicadores
        })

    # Índice global
    pontuacao_global = round(pontuacao_global_ponderada, 1)
    nivel_global = pontuacao_para_nivel(pontuacao_global)

    # Gap por diferença entre dimensão mais forte e mais fraca
    diferenca_max = max_pontuacao - min_pontuacao

    # Atualizar avaliação
    avaliacao = Avaliacao.query.get(avaliacao_id)
    if avaliacao:
        avaliacao.pontuacao_global = pontuacao_global
        avaliacao.nivel_global = nivel_global
        avaliacao.estado = 'concluida'
        avaliacao.concluido_em = datetime.now(timezone.utc)

    db.session.commit()

    # Identificar gaps críticos
    gaps_criticos = [
        {
            'dimensao': r['nome'],
            'codigo': r['codigo'],
            'pontuacao': r['pontuacao'],
            'nivel': r['nivel'],
            'acao_sugerida': _sugerir_acao(r['codigo'], r['pontuacao'])
        }
        for r in resultados_dimensao if r['gap_critico']
    ]

    # Ordenar gaps por pontuação (pior primeiro)
    gaps_criticos.sort(key=lambda x: x['pontuacao'])

    return {
        'avaliacao_id': avaliacao_id,
        'pontuacao_global': pontuacao_global,
        'nivel_global': nivel_global,
        'nivel_descricao': NIVEL_NOMES.get(nivel_global, '?'),
        'diferenca_max_min': round(diferenca_max, 1),
        'dimensoes': resultados_dimensao,
        'gaps_criticos': gaps_criticos
    }


def _sugerir_acao(codigo_dimensao, pontuacao):
    """Gera uma sugestão de ação genérica por dimensão com pontuação baixa."""
    sugestoes = {
        'DADOS': 'Começar por digitalizar o registo de vendas e clientes com ferramentas simples como Google Sheets.',
        'INFRA': 'Investir em equipamento básico e ferramentas digitais de gestão. Garantir acesso fiável à internet.',
        'COMP': 'Promover formação digital básica para os colaboradores. Começar por workshops curtos e práticos.',
        'ESTR': 'Definir uma visão digital simples: identificar 2-3 processos que beneficiariam de digitalização.',
        'CULT': 'Promover uma cultura de experimentação. Encorajar sugestões de melhoria e aceitar que erros fazem parte do processo.',
    }
    return sugestoes.get(codigo_dimensao, 'Rever práticas atuais e identificar oportunidades de melhoria.')
