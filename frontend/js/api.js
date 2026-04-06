/**
 * IALO — Cliente API
 * Wrapper para comunicação com o backend Flask
 */
const API = {
    BASE_URL: '/api/v1',

    /**
     * Obtém o token JWT guardado.
     */
    getToken() {
        return localStorage.getItem('ialo_token');
    },

    /**
     * Guarda os tokens JWT.
     */
    setTokens(token, refreshToken) {
        localStorage.setItem('ialo_token', token);
        if (refreshToken) {
            localStorage.setItem('ialo_refresh_token', refreshToken);
        }
    },

    /**
     * Remove os tokens (logout).
     */
    clearTokens() {
        localStorage.removeItem('ialo_token');
        localStorage.removeItem('ialo_refresh_token');
    },

    /**
     * Verifica se o utilizador está autenticado.
     */
    isAuthenticated() {
        return !!this.getToken();
    },

    /**
     * Faz um pedido HTTP à API.
     */
    async request(method, endpoint, body = null) {
        const url = `${this.BASE_URL}${endpoint}`;
        const headers = {
            'Content-Type': 'application/json',
        };

        const token = this.getToken();
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const config = { method, headers };
        if (body && (method === 'POST' || method === 'PUT' || method === 'PATCH')) {
            config.body = JSON.stringify(body);
        }

        try {
            const response = await fetch(url, config);
            const data = await response.json();

            if (!response.ok) {
                // Se 401, tentar refresh
                if (response.status === 401 && endpoint !== '/auth/login') {
                    const refreshed = await this.refreshToken();
                    if (refreshed) {
                        return this.request(method, endpoint, body);
                    }
                    // Se não conseguiu refresh, limpar tokens
                    this.clearTokens();
                    window.location.href = '/pages/login.html';
                }
                throw { status: response.status, ...data };
            }

            return data;
        } catch (error) {
            if (error.status) throw error;
            console.error('Erro de rede:', error);
            throw { status: 0, error: { message: 'Erro de ligação ao servidor' } };
        }
    },

    /**
     * Tenta renovar o token JWT.
     */
    async refreshToken() {
        const refreshToken = localStorage.getItem('ialo_refresh_token');
        if (!refreshToken) return false;

        try {
            const response = await fetch(`${this.BASE_URL}/auth/refresh`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ refresh_token: refreshToken })
            });

            if (response.ok) {
                const data = await response.json();
                this.setTokens(data.data.token, data.data.refresh_token);
                return true;
            }
        } catch (e) {
            console.error('Erro ao renovar token:', e);
        }
        return false;
    },

    // === Atalhos ===
    get(endpoint)          { return this.request('GET', endpoint); },
    post(endpoint, body)   { return this.request('POST', endpoint, body); },
    put(endpoint, body)    { return this.request('PUT', endpoint, body); },
    delete(endpoint)       { return this.request('DELETE', endpoint); },

    // === Auth ===
    login(email, password) { return this.post('/auth/login', { email, password }); },
    register(nome, email, password) { return this.post('/auth/register', { nome, email, password }); },

    // === Empresas ===
    getEmpresas()          { return this.get('/empresas'); },
    getEmpresa(id)         { return this.get(`/empresas/${id}`); },
    createEmpresa(data)    { return this.post('/empresas', data); },

    // === Avaliações ===
    getAvaliacoes(empresaId) { return this.get(`/avaliacoes?empresa_id=${empresaId}`); },
    createAvaliacao(empresaId) { return this.post('/avaliacoes', { empresa_id: empresaId }); },
    concluirAvaliacao(id)  { return this.post(`/avaliacoes/${id}/concluir`); },

    // === Questionário ===
    getDimensoes()         { return this.get('/questionario/dimensoes'); },
    saveRespostas(data)    { return this.post('/questionario/respostas', data); },
    getProgresso(avalId)   { return this.get(`/questionario/progresso/${avalId}`); },

    // === Scoring ===
    getScoring(avalId)     { return this.get(`/scoring/${avalId}`); },

    // === Relatórios ===
    gerarRelatorio(avalId) { return this.post('/relatorios', { avaliacao_id: avalId }); },
    getRelatorio(id)       { return this.get(`/relatorios/${id}`); },

    // === Assistente IA ===
    sendMessage(avalId, msg, perguntaId) {
        return this.post('/assistente/mensagem', {
            avaliacao_id: avalId,
            mensagem: msg,
            pergunta_atual_id: perguntaId
        });
    },

    // === Health ===
    health()               { return this.get('/health'); }
};
