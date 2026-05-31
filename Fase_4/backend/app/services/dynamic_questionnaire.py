"""Serviço de Questionário Dinâmico — Personalização de perguntas via IA Gemini."""
import json
from flask import current_app
from app.models.ailo import CamadaAilo, Indicador
from app.models.resposta import Resposta
from app.models.avaliacao import Avaliacao
from app.services.knowledge_base import AILO_KNOWLEDGE_BASE

MODELOS_PERMITIDOS = ['gemini-3.5-flash', 'gemini-3.1-flash-lite', 'gemini-3-flash-preview']


def _get_api_config(user):
    """Gets API key and model from user or env config."""
    api_key = ''
    model_name = 'gemini-3.5-flash'
    if user:
        if user.gemini_api_key:
            api_key = user.gemini_api_key
        if user.gemini_model and user.gemini_model in MODELOS_PERMITIDOS:
            model_name = user.gemini_model
    if not api_key:
        api_key = current_app.config.get('GEMINI_API_KEY', '')
    if not api_key:
        raise ValueError('API Gemini não configurada. Configure a sua chave API nas Configurações.')
    return api_key, model_name


def generate_dynamic_layer(avaliacao_id, camada_id, user=None):
    """Generates AI-personalized content for a layer.
    
    Returns dict with:
    - intro_text: Personalized layer introduction for the sector
    - adapted_questions: Dict mapping indicador_id to adapted descriptions
    - tips: List of contextual tips for the sector
    """
    api_key, model_name = _get_api_config(user)
    
    avaliacao = Avaliacao.query.get(avaliacao_id)
    if not avaliacao:
        raise ValueError('Avaliação não encontrada')
    
    org = avaliacao.organizacao
    camada = CamadaAilo.query.get(camada_id)
    if not camada:
        raise ValueError('Camada não encontrada')
    
    # Get existing answers for context
    respostas = {r.indicador_id: r.score for r in Resposta.query.filter_by(avaliacao_id=avaliacao_id).all()}
    
    # Build the list of indicators for this layer
    indicadores_info = []
    for comp in camada.componentes:
        for ind in comp.indicadores:
            indicadores_info.append({
                'id': ind.id,
                'codigo': ind.codigo,
                'pergunta': ind.pergunta,
                'componente': comp.nome,
                'desc_nivel_1': ind.desc_nivel_1 or '',
                'desc_nivel_3': ind.desc_nivel_3 or '',
                'desc_nivel_5': ind.desc_nivel_5 or '',
                'score_atual': respostas.get(ind.id)
            })
    
    # Build prompt for Gemini
    prompt = f"""És o assistente especializado AILO. A organização em avaliação:
- Nome: {org.nome}
- Setor: {org.setor}
- Dimensão: {org.dimensao}
- Tipo: {org.tipo}
- País: {org.pais or 'Portugal'}
{f'- Descrição: {org.descricao}' if org.descricao else ''}

Estás na camada "{camada.nome}": {camada.descricao}

Indicadores desta camada:
{json.dumps(indicadores_info, ensure_ascii=False, indent=2)}

Gera uma resposta JSON com EXATAMENTE esta estrutura:
{{
  "intro_text": "Uma introdução personalizada desta camada para o setor {org.setor}, explicando porque é relevante para este tipo de organização (2-3 frases)",
  "adapted_questions": {{
    "<indicador_id>": {{
      "pergunta_adaptada": "A pergunta reformulada para o contexto do setor {org.setor}",
      "desc_nivel_1": "Descrição do nível 1 adaptada ao setor",
      "desc_nivel_2": "Descrição do nível 2 adaptada ao setor",
      "desc_nivel_3": "Descrição do nível 3 adaptada ao setor",
      "desc_nivel_4": "Descrição do nível 4 adaptada ao setor",
      "desc_nivel_5": "Descrição do nível 5 adaptada ao setor",
      "dica": "Uma dica contextual curta para ajudar o utilizador a avaliar este indicador"
    }}
  }},
  "tips": ["3-4 dicas gerais para esta camada no contexto do setor"]
}}

IMPORTANTE:
- As chaves do adapted_questions DEVEM ser os IDs numéricos dos indicadores (como string)
- Mantém fidelidade ao framework AILO mas adapta linguagem e exemplos ao setor {org.setor}
- Cada nível deve ser uma frase curta (max 50 palavras)
- Responde APENAS com o JSON, sem markdown, sem ```json, apenas o objeto JSON puro"""
    
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(
            model_name,
            system_instruction="És um especialista em maturidade organizacional e IA. Respondes SEMPRE em JSON válido, sem markdown."
        )
        response = model.generate_content(prompt)
        
        # Parse JSON response
        text = response.text.strip()
        # Remove possible markdown wrapping
        if text.startswith('```'):
            text = text.split('\n', 1)[1] if '\n' in text else text[3:]
        if text.endswith('```'):
            text = text[:-3]
        text = text.strip()
        if text.startswith('json'):
            text = text[4:].strip()
        
        result = json.loads(text)
        return result
    except json.JSONDecodeError:
        # If JSON parsing fails, return a basic structure
        return {
            'intro_text': f'Vamos avaliar a camada {camada.nome} para a organização {org.nome} no setor {org.setor}.',
            'adapted_questions': {},
            'tips': [f'Considere o contexto do setor {org.setor} ao avaliar cada indicador.']
        }
    except Exception as e:
        raise ValueError(f'Erro ao gerar perguntas dinâmicas: {str(e)[:200]}')


def generate_ai_commentary(avaliacao_id, current_camada_idx, user=None):
    """Generates AI commentary on answers given so far (between layer transitions)."""
    api_key, model_name = _get_api_config(user)
    
    avaliacao = Avaliacao.query.get(avaliacao_id)
    if not avaliacao:
        raise ValueError('Avaliação não encontrada')
    
    org = avaliacao.organizacao
    respostas = Resposta.query.filter_by(avaliacao_id=avaliacao_id).all()
    
    if not respostas:
        return {'commentary': f'Vamos começar a avaliação da {org.nome}! Responda com atenção a cada indicador.'}
    
    # Build context of answers
    answers_context = []
    for r in respostas:
        if r.indicador:
            answers_context.append(f'{r.indicador.codigo} ({r.indicador.componente.camada.nome}): {r.score}/5')
    
    camadas = CamadaAilo.query.order_by(CamadaAilo.ordem).all()
    next_camada = camadas[current_camada_idx] if current_camada_idx < len(camadas) else None
    
    prompt = f"""Organização: {org.nome} (Setor: {org.setor})

Respostas dadas até agora:
{chr(10).join(answers_context)}

{'Próxima camada: ' + next_camada.nome if next_camada else 'Última camada concluída.'}

Dá um comentário breve (2-3 frases) sobre o progresso, destacando padrões nas respostas e preparando o utilizador para a próxima camada. Sê encorajador mas honesto. Responde em português de Portugal."""
    
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        return {'commentary': response.text.strip()}
    except Exception as e:
        raise ValueError(f'Erro ao gerar comentário: {str(e)[:200]}')
