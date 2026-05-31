"""Serviço de Sugestões Imediatas — Ações práticas não-técnicas geradas pela IA."""
import json
from flask import current_app
from app.models.avaliacao import Avaliacao
from app.models.resultado import ResultadoCamada, Interdependencia
from app.models.resposta import Resposta

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
        raise ValueError('API Gemini não configurada')
    return api_key, model_name


def generate_immediate_suggestions(avaliacao_id, user=None):
    """Generates immediate, non-technical suggestions based on evaluation results.
    
    Returns dict with:
    - sugestoes: List of suggestion objects with categoria, acao, esforco, impacto
    - pontos_criticos: List of critical points
    - nivel_maturidade: Detailed maturity level description
    """
    api_key, model_name = _get_api_config(user)
    
    avaliacao = Avaliacao.query.get(avaliacao_id)
    if not avaliacao:
        raise ValueError('Avaliação não encontrada')
    
    org = avaliacao.organizacao
    resultados = ResultadoCamada.query.filter_by(avaliacao_id=avaliacao_id).all()
    interdeps = Interdependencia.query.filter_by(avaliacao_id=avaliacao_id).all()
    respostas = Resposta.query.filter_by(avaliacao_id=avaliacao_id).all()
    
    # Build comprehensive context
    resultados_ctx = []
    for r in resultados:
        pf = json.loads(r.pontos_fortes) if r.pontos_fortes else []
        lac = json.loads(r.lacunas) if r.lacunas else []
        resultados_ctx.append({
            'camada': r.camada.nome if r.camada else '?',
            'score': r.score,
            'nivel': r.nivel,
            'pontos_fortes': pf,
            'lacunas': lac
        })
    
    interdeps_ctx = []
    for i in interdeps:
        interdeps_ctx.append({
            'camada_a': i.camada_a.nome if i.camada_a else '?',
            'camada_b': i.camada_b.nome if i.camada_b else '?',
            'tipo': i.tipo_relacao,
            'impacto': i.impacto
        })
    
    # Low-scoring indicators
    indicadores_fracos = []
    for r in respostas:
        if r.score <= 2 and r.indicador:
            indicadores_fracos.append({
                'codigo': r.indicador.codigo,
                'pergunta': r.indicador.pergunta,
                'score': r.score,
                'camada': r.indicador.componente.camada.nome if r.indicador.componente else '?'
            })
    indicadores_fracos.sort(key=lambda x: x['score'])
    
    prompt = f"""És um consultor especialista em maturidade organizacional AILO.

Organização: {org.nome}
Setor: {org.setor}
Dimensão: {org.dimensao}
Tipo: {org.tipo}
Score Global: {avaliacao.score_global}/5.0
Nível Global: {avaliacao.nivel_global}

Resultados por camada:
{json.dumps(resultados_ctx, ensure_ascii=False, indent=2)}

Interdependências:
{json.dumps(interdeps_ctx, ensure_ascii=False, indent=2)}

Indicadores com score mais baixo (≤ 2):
{json.dumps(indicadores_fracos[:10], ensure_ascii=False, indent=2)}

Gera uma resposta JSON com EXATAMENTE esta estrutura:
{{
  "nivel_maturidade": {{
    "nivel": "{avaliacao.nivel_global}",
    "score": {avaliacao.score_global},
    "descricao": "Descrição detalhada do que significa este nível para uma organização do setor {org.setor} (3-4 frases)",
    "proximo_nivel": "Nome do próximo nível de maturidade",
    "gap_proximo_nivel": "O que falta para atingir o próximo nível (2-3 frases)"
  }},
  "pontos_criticos": [
    {{
      "titulo": "Título curto do ponto crítico",
      "descricao": "Explicação do porque é crítico (1-2 frases)",
      "severidade": "alta|media",
      "camada": "Nome da camada afetada"
    }}
  ],
  "sugestoes_imediatas": [
    {{
      "categoria": "Organizacional|Formação|Processos|Documentação|Comunicação",
      "acao": "Descrição clara e acionável da sugestão (1-2 frases)",
      "esforco": "baixo|medio",
      "impacto": "alto|medio",
      "prazo": "1 semana|2 semanas|1 mês",
      "indicadores_afetados": ["códigos dos indicadores que esta ação melhora"]
    }}
  ]
}}

IMPORTANTE:
- Gera 3-5 pontos críticos (os mais urgentes)
- Gera 5-8 sugestões imediatas que NÃO requerem departamento técnico/IT
- As sugestões devem ser práticas e implementáveis por um gestor não-técnico
- Adapta ao setor {org.setor}
- Responde APENAS com JSON válido, sem markdown"""
    
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(
            model_name,
            system_instruction='És um consultor AILO. Respondes SEMPRE em JSON válido em português de Portugal.'
        )
        response = model.generate_content(prompt)
        
        text = response.text.strip()
        if text.startswith('```'):
            text = text.split('\n', 1)[1] if '\n' in text else text[3:]
        if text.endswith('```'):
            text = text[:-3]
        text = text.strip()
        if text.startswith('json'):
            text = text[4:].strip()
        
        return json.loads(text)
    except json.JSONDecodeError:
        # Basic fallback with actual data
        return {
            'nivel_maturidade': {
                'nivel': avaliacao.nivel_global,
                'score': avaliacao.score_global,
                'descricao': f'A organização encontra-se no nível {avaliacao.nivel_global} com score {avaliacao.score_global}/5.',
                'proximo_nivel': '',
                'gap_proximo_nivel': ''
            },
            'pontos_criticos': [{'titulo': i['pergunta'][:60], 'descricao': f'Score {i["score"]}/5', 'severidade': 'alta', 'camada': i['camada']} for i in indicadores_fracos[:5]],
            'sugestoes_imediatas': []
        }
    except Exception as e:
        raise ValueError(f'Erro ao gerar sugestões: {str(e)[:200]}')
