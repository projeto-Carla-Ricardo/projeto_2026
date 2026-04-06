"""
Lógica Fuzzy — Conversão de respostas qualitativas para valores numéricos.
Implementa as regras definidas na análise do Framework IALO (docs/fase1).
"""

# Mapeamento de respostas qualitativas para valores fuzzy
FUZZY_MAP = {
    # Respostas genéricas
    'nunca': 1.0,
    'não': 1.0,
    'nao': 1.0,
    'raramente': 1.5,
    'quase nunca': 1.5,
    'às vezes': 3.0,
    'as vezes': 3.0,
    'parcialmente': 3.0,
    'frequentemente': 4.0,
    'sim, mas': 4.0,
    'sempre': 5.0,
    'sim': 5.0,
    'sim, completamente': 5.0,

    # Respostas para dados / digitalização
    'caderno': 1.0,
    'caderno/papel': 1.0,
    'papel': 1.0,
    'excel': 2.5,
    'excel/folha de cálculo': 2.5,
    'folha de cálculo': 2.5,
    'software dedicado': 4.0,
    'software': 4.0,
    'erp': 5.0,
    'erp integrado': 5.0,

    # Respostas para armazenamento
    'não tem': 1.0,
    'ficheiro no computador': 2.5,
    'computador': 2.5,
    'sistema na nuvem': 5.0,
    'cloud': 5.0,
    'nuvem': 5.0,

    # Investimento
    'nada': 1.0,
    'pouco': 2.0,
    'algum': 3.5,
    'bastante': 5.0,
}

# Mapeamento de opções por índice (para escolha_multipla)
# Valor 1 = pior, valor crescente = melhor
OPTION_SCALE = {
    0: 1.0,   # Primeira opção = mais básica
    1: 2.5,
    2: 4.0,
    3: 5.0,   # Última opção = mais avançada
}


def text_to_fuzzy(text):
    """
    Converte uma resposta textual para valor fuzzy (1.0 - 5.0).
    Retorna None se não conseguir converter.
    """
    if not text:
        return None

    normalized = text.strip().lower()

    # Procurar correspondência exata
    if normalized in FUZZY_MAP:
        return FUZZY_MAP[normalized]

    # Procurar correspondência parcial
    for key, value in FUZZY_MAP.items():
        if key in normalized or normalized in key:
            return value

    return None


def option_index_to_fuzzy(index, total_options):
    """
    Converte o índice de uma opção selecionada (0-based) para valor fuzzy,
    distribuindo linearmente entre 1.0 e 5.0.
    """
    if total_options <= 1:
        return 3.0  # Valor médio se só há 1 opção

    return 1.0 + (index / (total_options - 1)) * 4.0


def calculate_fuzzy_value(resposta_texto, resposta_numerica, tipo_resposta, opcoes=None):
    """
    Calcula o valor fuzzy final para uma resposta, dependendo do tipo.
    Retorna um float entre 1.0 e 5.0.
    """
    # Escala 1-5: já é numérica
    if tipo_resposta == 'escala_1_5':
        return float(resposta_numerica) if resposta_numerica else 3.0

    # Sim/Não: binário
    if tipo_resposta == 'sim_nao':
        if resposta_texto:
            val = text_to_fuzzy(resposta_texto)
            if val is not None:
                return val
        return 5.0 if resposta_numerica and resposta_numerica >= 1 else 1.0

    # Escolha múltipla: usar a posição na lista de opções
    if tipo_resposta == 'escolha_multipla':
        if resposta_texto and opcoes:
            try:
                idx = opcoes.index(resposta_texto)
                return option_index_to_fuzzy(idx, len(opcoes))
            except (ValueError, TypeError):
                pass
        # Fallback: tentar conversão textual
        if resposta_texto:
            val = text_to_fuzzy(resposta_texto)
            if val is not None:
                return val
        return 3.0  # Valor médio como fallback

    # Texto livre: tentar conversão fuzzy
    if tipo_resposta == 'texto_livre':
        if resposta_texto:
            val = text_to_fuzzy(resposta_texto)
            if val is not None:
                return val
        return 3.0  # Valor médio como fallback

    # Fallback geral
    return resposta_numerica if resposta_numerica else 3.0
