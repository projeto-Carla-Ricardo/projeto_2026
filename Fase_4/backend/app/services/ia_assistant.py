"""Serviço do Assistente IA — Integração com Google Gemini + Base de Conhecimento AILO."""
from flask import current_app
from app import db
from app.models.conversa import ConversaIA
from app.models.ailo import CamadaAilo
from app.models.resposta import Resposta
from app.models.organizacao import Organizacao
from app.models.avaliacao import Avaliacao
from app.services.knowledge_base import build_system_prompt

MODELOS_PERMITIDOS = [
    'gemini-3.5-flash',
    'gemini-3.1-flash-lite',
    'gemini-3-flash-preview',
]


def _build_org_context(avaliacao):
    """Constrói contexto da organização a partir da avaliação."""
    org = avaliacao.organizacao if avaliacao else None
    if not org:
        return ""

    context = f"Organização: {org.nome}\nSetor: {org.setor}\nDimensão: {org.dimensao}\nTipo: {org.tipo}\nPaís: {org.pais or 'Portugal'}"
    if org.descricao:
        context += f"\nDescrição: {org.descricao}"

    # Adicionar respostas já dadas para contexto
    respostas = Resposta.query.filter_by(avaliacao_id=avaliacao.id).all()
    if respostas:
        context += f"\n\nRespostas já dadas nesta avaliação ({len(respostas)} indicadores respondidos):"
        for r in respostas:
            if r.indicador:
                context += f"\n  • {r.indicador.codigo}: Score {r.score}/5"

    return context


def _build_camada_context(camada_id):
    """Constrói contexto detalhado da camada atual."""
    if not camada_id:
        return ""
    camada = CamadaAilo.query.get(camada_id)
    if not camada:
        return ""

    context = f"Camada atual: {camada.nome} (ordem {camada.ordem})\nDescrição: {camada.descricao}"

    # Listar os componentes e indicadores desta camada
    if camada.componentes:
        context += f"\n\nComponentes desta camada ({len(camada.componentes)}):"
        for comp in camada.componentes:
            context += f"\n  {comp.nome}: {comp.descricao}"
            if comp.indicadores:
                for ind in comp.indicadores:
                    context += f"\n    → {ind.codigo}: {ind.pergunta}"

    return context


def _get_user_memory(user):
    """Obtém a memória de interações anteriores do utilizador."""
    if not user or not hasattr(user, 'memoria_ia') or not user.memoria_ia:
        return ""
    return user.memoria_ia


def _update_user_memory(user, mensagem, resposta, org_nome=""):
    """Atualiza a memória do utilizador com informações-chave da interação."""
    if not user or not hasattr(user, 'memoria_ia'):
        return

    # Construir entrada de memória
    import datetime
    data = datetime.datetime.utcnow().strftime('%Y-%m-%d')

    # Manter um resumo conciso (máx ~2000 chars)
    memoria_atual = user.memoria_ia or ""
    nova_entrada = f"[{data}]"
    if org_nome:
        nova_entrada += f" Org:{org_nome}"
    nova_entrada += f" Pergunta: {mensagem[:80]}..."

    memoria_atual += "\n" + nova_entrada

    # Limitar tamanho — manter as últimas entradas (máx 2000 chars)
    if len(memoria_atual) > 2000:
        linhas = memoria_atual.strip().split("\n")
        while len("\n".join(linhas)) > 2000 and len(linhas) > 5:
            linhas.pop(0)
        memoria_atual = "\n".join(linhas)

    user.memoria_ia = memoria_atual.strip()


def get_gemini_response(mensagem, avaliacao_id, camada_id=None, user=None):
    """Envia mensagem ao Gemini com base de conhecimento completa e retorna resposta."""
    # Determinar API key: user > env
    api_key = ''
    model_name = 'gemini-3.5-flash'

    if user:
        if user.gemini_api_key:
            api_key = user.gemini_api_key
        if user.gemini_model and user.gemini_model in MODELOS_PERMITIDOS:
            model_name = user.gemini_model

    # Fallback para configuração global (.env)
    if not api_key:
        api_key = current_app.config.get('GEMINI_API_KEY', '')
    if model_name not in MODELOS_PERMITIDOS:
        model_name = current_app.config.get('GEMINI_MODEL', 'gemini-3.5-flash')

    # Construir contextos
    avaliacao = Avaliacao.query.get(avaliacao_id)
    org_context = _build_org_context(avaliacao)
    camada_context = _build_camada_context(camada_id)
    user_memory = _get_user_memory(user)

    # Construir system prompt com base de conhecimento completa
    system_prompt = build_system_prompt(org_context, camada_context, user_memory)

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
            model = genai.GenerativeModel(
                model_name,
                system_instruction=system_prompt
            )

            chat_history = []
            for h in historico:
                role = 'user' if h.papel == 'user' else 'model'
                chat_history.append({'role': role, 'parts': [h.mensagem]})

            chat = model.start_chat(history=chat_history)
            response = chat.send_message(mensagem)
            resposta_texto = response.text

            # Atualizar memória do utilizador
            org_nome = avaliacao.organizacao.nome if avaliacao and avaliacao.organizacao else ""
            _update_user_memory(user, mensagem, resposta_texto, org_nome)

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
            f"Para ativar o assistente completo, configure a sua chave Gemini API "
            f"na página de Configurações (⚙️ no menu).\n\n"
            f"{'Está na camada: ' + camada_nome + '. ' if camada_nome else ''}"
            f"Consulte a documentação do framework AILO para obter explicações detalhadas sobre cada indicador.")
