/**
 * AILO — API Wrapper Module
 * Centraliza todas as chamadas HTTP à API REST.
 */
const API_BASE = '/api/v1';

const api = {
    getToken() { return localStorage.getItem('ailo_token'); },
    setToken(token) { localStorage.setItem('ailo_token', token); },
    clearToken() { localStorage.removeItem('ailo_token'); localStorage.removeItem('ailo_user'); },

    getUser() {
        const u = localStorage.getItem('ailo_user');
        return u ? JSON.parse(u) : null;
    },
    setUser(user) { localStorage.setItem('ailo_user', JSON.stringify(user)); },

    isAuthenticated() { return !!this.getToken(); },

    async request(method, endpoint, data = null) {
        const headers = { 'Content-Type': 'application/json' };
        const token = this.getToken();
        if (token) headers['Authorization'] = `Bearer ${token}`;

        const opts = { method, headers };
        if (data) opts.body = JSON.stringify(data);

        const res = await fetch(`${API_BASE}${endpoint}`, opts);
        const json = await res.json();
        if (!res.ok) throw { status: res.status, ...json };
        return json;
    },

    // Auth
    register: (data) => api.request('POST', '/auth/register', data),
    login: (data) => api.request('POST', '/auth/login', data),
    me: () => api.request('GET', '/auth/me'),

    // Organizações
    getOrganizacoes: () => api.request('GET', '/organizacoes'),
    criarOrganizacao: (data) => api.request('POST', '/organizacoes', data),
    atualizarOrganizacao: (id, data) => api.request('PUT', `/organizacoes/${id}`, data),
    eliminarOrganizacao: (id) => api.request('DELETE', `/organizacoes/${id}`),

    // AILO Framework
    getCamadas: () => api.request('GET', '/ailo/camadas'),
    getIndicadoresCamada: (id) => api.request('GET', `/ailo/camadas/${id}/indicadores`),

    // Avaliações
    getAvaliacoes: () => api.request('GET', '/avaliacoes'),
    criarAvaliacao: (orgId) => api.request('POST', '/avaliacoes', { organizacao_id: orgId }),
    getAvaliacao: (id) => api.request('GET', `/avaliacoes/${id}`),
    finalizarAvaliacao: (id) => api.request('POST', `/avaliacoes/${id}/finalizar`),

    // Respostas
    guardarResposta: (avalId, data) => api.request('POST', `/avaliacoes/${avalId}/respostas`, data),
    guardarRespostasBatch: (avalId, respostas) => api.request('POST', `/avaliacoes/${avalId}/respostas/batch`, { respostas }),
    getRespostas: (avalId) => api.request('GET', `/avaliacoes/${avalId}/respostas`),

    // Resultados
    getResultados: (avalId) => api.request('GET', `/avaliacoes/${avalId}/resultados`),

    // Chat
    enviarMensagem: (avalId, mensagem, camadaId) => api.request('POST', `/avaliacoes/${avalId}/chat`, { mensagem, camada_id: camadaId }),
    getHistoricoChat: (avalId) => api.request('GET', `/avaliacoes/${avalId}/chat/historico`),

    // Relatórios
    gerarRelatorio: (avalId) => api.request('POST', `/avaliacoes/${avalId}/relatorio`),
};
