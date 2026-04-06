"""
Motor de Recomendação — Sugere ferramentas IA com base no perfil e gaps da empresa.
"""
from app.models.ferramenta import FerramentaIA
from app.models.resultado import ResultadoDimensao


# Mapeamento de dimensões para categorias de ferramentas (conforme seeds/ferramentas_ia.json)
DIMENSAO_CATEGORIAS = {
    'DADOS': ['dados', 'gestao', 'automacao'],
    'INFRA': ['operacoes', 'automacao', 'gestao'],
    'COMP': ['marketing', 'atendimento', 'gestao'],
    'ESTR': ['gestao', 'dados', 'operacoes'],
    'CULT': ['atendimento', 'marketing', 'automacao'],
}

# Complexidade máxima recomendada por nível
COMPLEXIDADE_POR_NIVEL = {
    1: 'Básica',
    2: 'Básica',
    3: 'Intermédia',
    4: 'Intermédia',
    5: 'Avançada',
}

# Custo máximo sugerido por número de colaboradores
def _custo_adequado(num_colaboradores):
    if not num_colaboradores or num_colaboradores <= 5:
        return ['Gratuito', 'Freemium']
    elif num_colaboradores <= 20:
        return ['Gratuito', 'Freemium', 'Pago (baixo custo)']
    else:
        return ['Gratuito', 'Freemium', 'Pago (baixo custo)', 'Pago']


def gerar_recomendacoes(avaliacao_id, empresa=None):
    """
    Gera recomendações de ferramentas IA personalizadas com base nos resultados.
    
    Retorna uma lista de recomendações agrupadas por prioridade.
    """
    resultados = ResultadoDimensao.query.filter_by(avaliacao_id=avaliacao_id).all()
    if not resultados:
        return []

    ferramentas = FerramentaIA.query.filter_by(ativo=True).all()
    if not ferramentas:
        return []

    num_colab = empresa.num_colaboradores if empresa else None
    custos_ok = _custo_adequado(num_colab)

    recomendacoes = []

    # Ordenar resultados por pontuação (gaps primeiro)
    resultados_sorted = sorted(resultados, key=lambda r: r.pontuacao)

    for resultado in resultados_sorted:
        dimensao = resultado.dimensao
        if not dimensao:
            continue

        nivel = resultado.nivel or 1
        complexidade_max = COMPLEXIDADE_POR_NIVEL.get(nivel, 'Intermédia')
        categorias = DIMENSAO_CATEGORIAS.get(dimensao.codigo, [])

        # Filtrar ferramentas relevantes
        ferramentas_match = []
        for f in ferramentas:
            # Score de relevância
            score = 0

            # Verificar se a categoria da ferramenta corresponde
            if f.categoria and f.categoria in categorias:
                score += 5

            # Verificar custo adequado
            if f.custo in custos_ok:
                score += 2

            # Verificar complexidade adequada
            complexidades_ok = ['Básica']
            if complexidade_max in ['Intermédia', 'Avançada']:
                complexidades_ok.append('Intermédia')
            if complexidade_max == 'Avançada':
                complexidades_ok.append('Avançada')

            if f.complexidade in complexidades_ok:
                score += 1

            if score >= 3:  # Threshold mínimo de relevância
                ferramentas_match.append({
                    'ferramenta': f.to_dict(),
                    'score_relevancia': score,
                    'razao': _gerar_razao(dimensao, resultado, f)
                })

        # Ordenar por relevância
        ferramentas_match.sort(key=lambda x: x['score_relevancia'], reverse=True)

        prioridade = 'alta' if resultado.gap_critico else ('média' if resultado.pontuacao < 60 else 'baixa')

        recomendacoes.append({
            'dimensao': dimensao.nome,
            'codigo': dimensao.codigo,
            'pontuacao': resultado.pontuacao,
            'nivel': resultado.nivel,
            'gap_critico': resultado.gap_critico,
            'prioridade': prioridade,
            'ferramentas': ferramentas_match[:5],  # Top 5 por dimensão
            'acao_sugerida': _acao_por_nivel(dimensao.codigo, resultado.nivel)
        })

    return recomendacoes


def _gerar_razao(dimensao, resultado, ferramenta):
    """Gera uma explicação de porque esta ferramenta é recomendada."""
    if resultado.gap_critico:
        return f"A dimensão '{dimensao.nome}' é um gap crítico ({resultado.pontuacao}%). O {ferramenta.nome} pode ajudar a acelerar a melhoria nesta área."
    elif resultado.pontuacao < 60:
        return f"A dimensão '{dimensao.nome}' tem espaço para crescimento ({resultado.pontuacao}%). O {ferramenta.nome} pode impulsionar os resultados."
    else:
        return f"Para consolidar os bons resultados em '{dimensao.nome}' ({resultado.pontuacao}%), o {ferramenta.nome} é uma ferramenta adequada."


def _acao_por_nivel(codigo, nivel):
    """Sugere a ação concreta por dimensão e nível."""
    acoes = {
        'DADOS': {
            1: 'Começar por registar vendas e clientes numa folha de cálculo simples (Google Sheets).',
            2: 'Organizar os dados existentes com categorias e criar backup regular.',
            3: 'Implementar um sistema de gestão básico (CRM simples ou ERP leve).',
            4: 'Automatizar recolha de dados e criar dashboards de monitorização.',
            5: 'Explorar analytics avançado e modelos preditivos com IA.',
        },
        'INFRA': {
            1: 'Garantir internet fiável e computador/tablet funcional para gestão.',
            2: 'Adotar ferramentas cloud básicas (Google Workspace ou Microsoft 365).',
            3: 'Criar presença digital (website, Google Business, redes sociais).',
            4: 'Implementar sistemas integrados e automatizações entre ferramentas.',
            5: 'Explorar infraestrutura escalável e soluções IoT/IA.',
        },
        'COMP': {
            1: 'Promover formação digital básica (email, internet, Office).',
            2: 'Workshops práticos sobre ferramentas do dia-a-dia (3-4 horas).',
            3: 'Formação específica nas ferramentas de gestão adotadas.',
            4: 'Desenvolver competências de análise de dados e automação.',
            5: 'Formação avançada em IA e inovação digital contínua.',
        },
        'ESTR': {
            1: 'Definir 2-3 processos que beneficiariam de digitalização.',
            2: 'Criar um plano simples de digitalização com metas claras.',
            3: 'Alinhar a estratégia digital com os objetivos de negócio.',
            4: 'Implementar métricas de sucesso e revisão periódica da estratégia.',
            5: 'Desenvolver cultura de inovação contínua e experimentação com IA.',
        },
        'CULT': {
            1: 'Encorajar sugestões de melhoria e aceitar que erros fazem parte do processo.',
            2: 'Criar momentos de partilha de boas práticas digitais na equipa.',
            3: 'Estabelecer processos de experimentação com novas ferramentas.',
            4: 'Premiar inovação e criar um ambiente de aprendizagem contínua.',
            5: 'Liderar pelo exemplo e partilhar casos de sucesso com a comunidade.',
        },
    }
    return acoes.get(codigo, {}).get(nivel, 'Rever práticas e identificar oportunidades de melhoria.')
