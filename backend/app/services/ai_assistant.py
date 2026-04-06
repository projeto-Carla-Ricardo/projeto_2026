"""
Serviço de Assistente IA — Integração com Google Gemini API.
Implementa o assistente conversacional do Framework IALO.
"""
import json
from flask import current_app
from app import db
from app.models.conversa import ConversaIA
from app.models.avaliacao import Avaliacao
from app.models.empresa import Empresa
from app.models.dimensao import Dimensao
from app.models.pergunta import Pergunta
from app.models.resposta import Resposta


# System prompt base para o assistente IALO
SYSTEM_PROMPT = """Tu és o Assistente IALO, um consultor digital amigável e paciente que ajuda micro e pequenas empresas a compreenderem o seu nível de maturidade digital e prontidão para Inteligência Artificial.

O teu papel:
1. TRADUZIR conceitos técnicos para linguagem do dia-a-dia, usando exemplos práticos do setor da empresa
2. GUIAR o empresário pelo questionário de diagnóstico, esclarecendo cada pergunta
3. VALIDAR consistência das respostas, alertando para contradições de forma pedagógica
4. MOTIVAR o utilizador, reforçando o que já fazem bem antes de apontar lacunas

Regras de comunicação:
- Usa português de Portugal (não brasileiro)
- Sê breve e direto nas respostas (máximo 3-4 parágrafos)
- Usa exemplos concretos do setor quando possível
- Nunca uses jargão técnico sem explicar primeiro
- Quando o utilizador perguntar "o que são dados estruturados?", usa o exemplo da lista de contactos vs. mensagens de WhatsApp
- Sê encorajador, nunca condescendente

O Framework IALO avalia 5 dimensões:
1. DADOS (25%) — Como recolhe, armazena e utiliza dados
2. INFRAESTRUTURA (20%) — Equipamentos, software, internet, presença digital
3. COMPETÊNCIAS (20%) — Literacia digital e capacidades técnicas das pessoas
4. ESTRATÉGIA (20%) — Visão e planeamento para digitalização
5. CULTURA (15%) — Abertura à mudança e inovação

Cada dimensão é avaliada de 1 (Inicial) a 5 (Otimizado)."""


def _get_gemini_client():
    """Obtém uma instância configurada do cliente Gemini."""
    api_key = current_app.config.get('GEMINI_API_KEY', '')

    if not api_key:
        return None, "API Key do Gemini não configurada. Configure nas Definições."

    try:
        from google import genai

        client = genai.Client(api_key=api_key)
        return client, None
    except ImportError:
        return None, "Pacote google-genai não instalado. Execute: pip install google-genai"
    except Exception as e:
        return None, f"Erro ao inicializar Gemini: {str(e)}"


def _build_context(avaliacao_id, pergunta_atual_id=None):
    """
    Constrói contexto adicional para o prompt: informação da empresa,
    respostas anteriores e pergunta atual.
    """
    context_parts = []

    avaliacao = Avaliacao.query.get(avaliacao_id)
    if avaliacao and avaliacao.empresa:
        empresa = avaliacao.empresa
        context_parts.append(
            f"Empresa: {empresa.nome}\n"
            f"Setor: {empresa.setor}\n"
            f"Colaboradores: {empresa.num_colaboradores or 'Não indicado'}\n"
            f"Localização: {empresa.localizacao or 'Não indicada'}\n"
            f"Descrição: {empresa.descricao or 'Sem descrição'}"
        )

    # Respostas já dadas (para contexto de consistência)
    respostas = Resposta.query.filter_by(avaliacao_id=avaliacao_id).all()
    if respostas:
        respostas_texto = []
        for r in respostas[-10:]:  # Últimas 10 respostas
            pergunta = Pergunta.query.get(r.pergunta_id)
            if pergunta:
                valor = r.valor_texto or str(r.valor_numerico or '')
                respostas_texto.append(f"- {pergunta.texto[:80]}: {valor}")
        if respostas_texto:
            context_parts.append("Respostas anteriores:\n" + "\n".join(respostas_texto))

    # Pergunta atual
    if pergunta_atual_id:
        pergunta = Pergunta.query.get(pergunta_atual_id)
        if pergunta:
            indicador = pergunta.indicador
            dimensao = indicador.dimensao if indicador else None
            dim_nome = dimensao.nome if dimensao else 'Desconhecida'
            context_parts.append(
                f"Pergunta atual (Dimensão: {dim_nome}):\n"
                f"{pergunta.texto}\n"
                f"Ajuda: {pergunta.ajuda_contextual or 'Sem ajuda'}"
            )

    return "\n\n---\n\n".join(context_parts)


def _get_conversation_history(avaliacao_id, limit=20):
    """Obtém as últimas mensagens da conversa para manter contexto."""
    mensagens = ConversaIA.query.filter_by(
        avaliacao_id=avaliacao_id
    ).order_by(ConversaIA.timestamp.desc()).limit(limit).all()

    # Reverter para ordem cronológica
    mensagens.reverse()

    history = []
    for msg in mensagens:
        role = "user" if msg.papel == "utilizador" else "model"
        history.append({"role": role, "parts": [{"text": msg.mensagem}]})

    return history


def enviar_mensagem(avaliacao_id, mensagem_utilizador, pergunta_atual_id=None):
    """
    Envia uma mensagem ao assistente Gemini e devolve a resposta.
    Mantém contexto conversacional via histórico na BD.
    """
    client, error = _get_gemini_client()
    if error:
        return {
            'resposta': f'⚠️ {error}',
            'alertas_consistencia': [],
            'sugestao_resposta': None,
            'error': True
        }

    model_name = current_app.config.get('GEMINI_MODEL', 'gemini-3.1-flash-lite-preview')

    # Guardar mensagem do utilizador
    msg_user = ConversaIA(
        avaliacao_id=avaliacao_id,
        papel='utilizador',
        mensagem=mensagem_utilizador
    )
    db.session.add(msg_user)
    db.session.flush()

    # Construir contexto
    contexto = _build_context(avaliacao_id, pergunta_atual_id)

    # Montar prompt completo
    full_system = SYSTEM_PROMPT
    if contexto:
        full_system += f"\n\n--- CONTEXTO DA SESSÃO ---\n\n{contexto}"

    # Histórico de conversa
    history = _get_conversation_history(avaliacao_id)

    try:
        # Chamar Gemini API
        response = client.models.generate_content(
            model=model_name,
            contents=[
                {"role": "user", "parts": [{"text": full_system}]},
                {"role": "model", "parts": [{"text": "Entendido! Sou o Assistente IALO e estou aqui para ajudar. Como posso auxiliar?"}]},
                *history,
                {"role": "user", "parts": [{"text": mensagem_utilizador}]},
            ],
        )

        resposta_texto = response.text

        # Guardar resposta do assistente
        msg_assistant = ConversaIA(
            avaliacao_id=avaliacao_id,
            papel='assistente',
            mensagem=resposta_texto
        )
        db.session.add(msg_assistant)
        db.session.commit()

        return {
            'resposta': resposta_texto,
            'alertas_consistencia': [],
            'sugestao_resposta': None,
            'error': False
        }

    except Exception as e:
        db.session.rollback()
        error_msg = str(e)
        if 'API_KEY_INVALID' in error_msg or '401' in error_msg:
            error_msg = 'API Key inválida. Verifique a chave nas Definições.'
        elif 'RESOURCE_EXHAUSTED' in error_msg or '429' in error_msg:
            error_msg = 'Limite de pedidos excedido. Tente novamente em alguns segundos.'
        else:
            error_msg = f'Erro ao comunicar com o Gemini: {error_msg}'

        return {
            'resposta': f'⚠️ {error_msg}',
            'alertas_consistencia': [],
            'sugestao_resposta': None,
            'error': True
        }


def get_historico(avaliacao_id):
    """Retorna o histórico completo de conversa de uma avaliação."""
    mensagens = ConversaIA.query.filter_by(
        avaliacao_id=avaliacao_id
    ).order_by(ConversaIA.timestamp.asc()).all()

    return [m.to_dict() for m in mensagens]


def testar_conexao(api_key=None, model=None):
    """Testa a ligação à API Gemini com a key fornecida."""
    try:
        from google import genai

        key = api_key or current_app.config.get('GEMINI_API_KEY', '')
        mdl = model or current_app.config.get('GEMINI_MODEL', 'gemini-3.1-flash-lite-preview')

        if not key:
            return False, 'API Key não fornecida'

        client = genai.Client(api_key=key)
        response = client.models.generate_content(
            model=mdl,
            contents="Responde apenas com: OK",
        )

        if response and response.text:
            return True, f'Conexão bem sucedida com {mdl}'
        return False, 'Resposta vazia do modelo'

    except Exception as e:
        return False, str(e)
