"""Serviço do Assistente IA — Integração com Google Gemini."""
from flask import current_app
from app import db
from app.models.conversa import ConversaIA
from app.models.ailo import CamadaAilo
from app.models.resposta import Resposta
from app.models.organizacao import Organizacao
from app.models.avaliacao import Avaliacao

SYSTEM_PROMPT = """Tu és o Assistente AILO, um especialista em aprendizagem organizacional e integração de IA nas organizações.

O teu papel é ajudar o utilizador a responder ao questionário de diagnóstico AILO (Artificial Intelligence in a Learning Organization).

Regras:
1. Responde SEMPRE em português de Portugal
2. Sê claro, conciso e usa exemplos práticos
3. Adapta os exemplos ao tipo e setor da organização do utilizador
4. Explica conceitos do framework AILO de forma acessível
5. Quando o utilizador pedir, sugere qual nível de maturidade (1-5) se aplica com base na descrição
6. Alerta para inconsistências entre respostas
7. Não inventes dados — baseia-te no framework AILO publicado

O AILO tem 6 camadas: Organizacional, Humana, Aprendizagem, Cognitiva (IA), Tecnológica e Avaliação.
Cada indicador é pontuado de 1 (Inicial) a 5 (Otimizado)."""

def get_gemini_response(mensagem, avaliacao_id, camada_id=None):
    """Envia mensagem ao Gemini e retorna resposta."""
    api_key = current_app.config.get('GEMINI_API_KEY', '')

    # Construir contexto
    avaliacao = Avaliacao.query.get(avaliacao_id)
    org = avaliacao.organizacao if avaliacao else None
    contexto_org = ""
    if org:
        contexto_org = f"\nOrganização: {org.nome}, Setor: {org.setor}, Dimensão: {org.dimensao}, Tipo: {org.tipo}"

    contexto_camada = ""
    if camada_id:
        camada = CamadaAilo.query.get(camada_id)
        if camada:
            contexto_camada = f"\nCamada atual: {camada.nome} — {camada.descricao}"

    # Histórico recente
    historico = ConversaIA.query.filter_by(avaliacao_id=avaliacao_id).order_by(ConversaIA.created_at.desc()).limit(10).all()
    historico.reverse()

    # Guardar mensagem do utilizador
    msg_user = ConversaIA(avaliacao_id=avaliacao_id, papel='user', mensagem=mensagem, camada_id=camada_id)
    db.session.add(msg_user)

    # Tentar Gemini API
    if api_key:
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(current_app.config.get('GEMINI_MODEL', 'gemini-2.0-flash'))

            full_prompt = SYSTEM_PROMPT + contexto_org + contexto_camada
            chat_history = []
            for h in historico:
                role = 'user' if h.papel == 'user' else 'model'
                chat_history.append({'role': role, 'parts': [h.mensagem]})

            chat = model.start_chat(history=chat_history)
            response = chat.send_message(mensagem)
            resposta_texto = response.text
        except Exception as e:
            resposta_texto = f"Peço desculpa, ocorreu um erro na comunicação com o assistente IA. Por favor, tente novamente. (Erro: {str(e)[:100]})"
    else:
        # Fallback sem API key
        resposta_texto = _fallback_response(mensagem, camada_id)

    # Guardar resposta
    msg_assistant = ConversaIA(avaliacao_id=avaliacao_id, papel='assistant', mensagem=resposta_texto, camada_id=camada_id)
    db.session.add(msg_assistant)
    db.session.commit()

    return resposta_texto


def _fallback_response(mensagem, camada_id=None):
    """Resposta básica quando não há API key configurada."""
    camada_nome = ""
    if camada_id:
        camada = CamadaAilo.query.get(camada_id)
        camada_nome = camada.nome if camada else ""

    return (f"🤖 Assistente AILO (modo offline)\n\n"
            f"Estou a funcionar sem ligação ao modelo de IA. "
            f"Para ativar o assistente completo, configure a chave GEMINI_API_KEY no ficheiro .env.\n\n"
            f"{'Está na camada: ' + camada_nome + '. ' if camada_nome else ''}"
            f"Consulte a documentação do framework AILO na Fase 1 para obter explicações detalhadas sobre cada indicador.")
