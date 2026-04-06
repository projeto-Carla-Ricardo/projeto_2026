/**
 * Dashboard JS — Main dashboard logic.
 * Handles sidebar navigation, stats loading, company/assessment CRUD, and settings.
 */

const API_BASE = window.location.origin + '/api/v1';
let token = localStorage.getItem('ialo_token');
let user = JSON.parse(localStorage.getItem('ialo_user') || '{}');

document.addEventListener('DOMContentLoaded', () => {
    if (!token) { window.location.href = 'login.html'; return; }

    initSidebar();
    initUser();
    loadOverview();
    initSettings();
    loadSettings();
    initModals();
});

// ========== AUTH ==========
function authHeaders() {
    return { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' };
}

async function apiFetch(url, opts = {}) {
    opts.headers = { ...authHeaders(), ...opts.headers };
    const res = await fetch(`${API_BASE}${url}`, opts);
    if (res.status === 401) { localStorage.clear(); window.location.href = 'login.html'; }
    return res.json();
}

// ========== SIDEBAR ==========
function initSidebar() {
    document.querySelectorAll('.sidebar__link').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const section = link.dataset.section;
            switchSection(section);
        });
    });

    document.getElementById('btn-logout').addEventListener('click', (e) => {
        e.preventDefault();
        localStorage.clear();
        window.location.href = 'login.html';
    });
}

function switchSection(name) {
    document.querySelectorAll('.content-section').forEach(s => s.classList.remove('active'));
    document.querySelectorAll('.sidebar__link').forEach(l => l.classList.remove('sidebar__link--active'));

    document.getElementById(`section-${name}`).classList.add('active');
    document.querySelector(`[data-section="${name}"]`).classList.add('sidebar__link--active');

    if (name === 'empresas') loadEmpresas();
    if (name === 'avaliacoes') loadAvaliacoes();
    if (name === 'settings') loadSettings();
}

function initUser() {
    document.getElementById('user-name').textContent = user.nome || 'Utilizador';
    const avatar = document.getElementById('user-avatar');
    avatar.textContent = (user.nome || 'U')[0].toUpperCase();
}

// ========== OVERVIEW ==========
async function loadOverview() {
    try {
        const [empData, avalData] = await Promise.all([
            apiFetch('/empresas'),
            apiFetch('/avaliacoes')
        ]);

        const empresas = empData.data || [];
        const avaliacoes = avalData.data || [];
        const concluidas = avaliacoes.filter(a => a.estado === 'concluida');

        document.getElementById('stat-empresas').textContent = empresas.length;
        document.getElementById('stat-avaliacoes').textContent = avaliacoes.length;
        document.getElementById('stat-concluidas').textContent = concluidas.length;

        if (concluidas.length > 0) {
            const media = concluidas.reduce((s, a) => s + (a.pontuacao_global || 0), 0) / concluidas.length;
            document.getElementById('stat-media').textContent = `${Math.round(media)}%`;
        }

        // Recent assessments
        const recentEl = document.getElementById('recent-avaliacoes');
        if (avaliacoes.length > 0) {
            recentEl.innerHTML = avaliacoes.slice(0, 5).map(a => {
                const empresa = empresas.find(e => e.id === a.empresa_id);
                const badge = a.estado === 'concluida' ? 'done' : 'pending';
                const label = a.estado === 'concluida' ? `${a.pontuacao_global}%` : 'Em curso';
                return `<div class="recent-item">
                    <div class="recent-item__info">
                        <span class="recent-item__title">${empresa?.nome || 'Empresa'}</span>
                        <span class="recent-item__date">${new Date(a.iniciado_em).toLocaleDateString('pt-PT')}</span>
                    </div>
                    <span class="card__badge card__badge--${badge}">${label}</span>
                </div>`;
            }).join('');
        }

        // Quick action handlers
        document.getElementById('btn-nova-empresa').onclick = () => openModal('modal-empresa');
        document.getElementById('btn-novo-diagnostico').onclick = () => switchSection('empresas');

    } catch (err) { console.error('Erro ao carregar overview:', err); }
}

// ========== EMPRESAS ==========
async function loadEmpresas() {
    const data = await apiFetch('/empresas');
    const el = document.getElementById('empresas-list');
    const empresas = data.data || [];

    if (empresas.length === 0) {
        el.innerHTML = '<p class="empty-state">Nenhuma empresa registada. Crie a primeira!</p>';
        return;
    }

    el.innerHTML = empresas.map(e => `
        <div class="card">
            <h3 class="card__title">${e.nome}</h3>
            <div class="card__meta">
                <span>📌 ${e.setor}</span>
                ${e.num_colaboradores ? `<span>👥 ${e.num_colaboradores} colab.</span>` : ''}
                ${e.localizacao ? `<span>📍 ${e.localizacao}</span>` : ''}
            </div>
            <div class="card__actions">
                <button class="btn btn--primary btn--sm" onclick="iniciarDiagnostico(${e.id})">🔍 Novo Diagnóstico</button>
            </div>
        </div>
    `).join('');

    document.getElementById('btn-add-empresa').onclick = () => openModal('modal-empresa');
}

window.iniciarDiagnostico = async function(empresaId) {
    const data = await apiFetch('/avaliacoes', {
        method: 'POST',
        body: JSON.stringify({ empresa_id: empresaId })
    });

    if (data.status === 'success') {
        localStorage.setItem('ialo_avaliacao_id', data.data.id);
        window.location.href = 'questionario.html';
    }
};

// ========== AVALIAÇÕES ==========
async function loadAvaliacoes() {
    const [avalData, empData] = await Promise.all([
        apiFetch('/avaliacoes'),
        apiFetch('/empresas')
    ]);

    const el = document.getElementById('avaliacoes-list');
    const avaliacoes = avalData.data || [];
    const empresas = empData.data || [];

    if (avaliacoes.length === 0) {
        el.innerHTML = '<p class="empty-state">Nenhum diagnóstico realizado.</p>';
        return;
    }

    el.innerHTML = avaliacoes.map(a => {
        const empresa = empresas.find(e => e.id === a.empresa_id);
        const estado = a.estado === 'concluida' ? 'done' : a.estado === 'em_curso' ? 'pending' : 'active';
        const estadoLabel = a.estado === 'concluida' ? 'Concluído' : a.estado === 'em_curso' ? 'Em Curso' : a.estado;
        let actions = '';
        if (a.estado === 'em_curso') {
            actions = `<button class="btn btn--primary btn--sm" onclick="continuarDiagnostico(${a.id})">▶️ Continuar</button>`;
        } else if (a.estado === 'concluida') {
            actions = `<span style="font-size:0.9rem">🎯 Pontuação: <strong>${a.pontuacao_global}%</strong> (Nível ${a.nivel_global})</span>`;
        }
        return `<div class="card">
            <h3 class="card__title">${empresa?.nome || 'Empresa'}</h3>
            <div class="card__meta">
                <span>📅 ${new Date(a.iniciado_em).toLocaleDateString('pt-PT')}</span>
                <span class="card__badge card__badge--${estado}">${estadoLabel}</span>
            </div>
            <div class="card__actions">${actions}</div>
        </div>`;
    }).join('');
}

window.continuarDiagnostico = function(avaliacaoId) {
    localStorage.setItem('ialo_avaliacao_id', avaliacaoId);
    window.location.href = 'questionario.html';
};

// ========== SETTINGS ==========
function initSettings() {
    document.getElementById('btn-toggle-key').addEventListener('click', () => {
        const input = document.getElementById('gemini-api-key');
        input.type = input.type === 'password' ? 'text' : 'password';
    });

    document.getElementById('btn-test-ai').addEventListener('click', testAI);
    document.getElementById('btn-save-ai').addEventListener('click', saveAI);
    document.getElementById('btn-clear-key').addEventListener('click', clearAIKey);
}

async function loadSettings() {
    try {
        const data = await apiFetch('/settings/ai');
        if (data.status === 'success') {
            const { available_models, model, api_key_masked, api_key_set } = data.data;
            const select = document.getElementById('gemini-model');
            select.innerHTML = available_models.map(m =>
                `<option value="${m}" ${m === model ? 'selected' : ''}>${m}</option>`
            ).join('');

            if (api_key_set) {
                document.getElementById('gemini-api-key').placeholder = `Chave atual: ${api_key_masked}`;
            }
        }
    } catch (err) {
        // User might not be admin
        const select = document.getElementById('gemini-model');
        select.innerHTML = '<option value="gemini-3.1-flash-lite-preview">gemini-3.1-flash-lite-preview</option>';
    }
}

async function testAI() {
    const statusEl = document.getElementById('ai-status');
    statusEl.style.display = 'block';
    statusEl.className = 'ai-status';
    statusEl.textContent = '⏳ A testar conexão...';

    const apiKey = document.getElementById('gemini-api-key').value;
    const model = document.getElementById('gemini-model').value;

    if (!apiKey) {
        statusEl.className = 'ai-status ai-status--error';
        statusEl.textContent = '❌ Insira a API Key antes de testar';
        return;
    }

    try {
        // Guardar primeiro para que o backend tenha a key
        await apiFetch('/settings/ai', {
            method: 'PUT',
            body: JSON.stringify({ api_key: apiKey, model })
        });

        const data = await apiFetch('/settings/ai/test', {
            method: 'POST',
            body: JSON.stringify({ api_key: apiKey, model })
        });

        if (data.data && data.data.connected) {
            statusEl.className = 'ai-status ai-status--success';
            statusEl.textContent = `✅ ${data.data.message}`;
        } else {
            statusEl.className = 'ai-status ai-status--error';
            statusEl.textContent = `❌ ${data.data?.message || data.error?.message || 'Falha na conexão'}`;
        }
    } catch (err) {
        statusEl.className = 'ai-status ai-status--error';
        statusEl.textContent = `❌ Erro ao testar conexão: ${err.message || 'Verifique a API Key'}`;
    }
}

async function saveAI() {
    const apiKey = document.getElementById('gemini-api-key').value;
    const model = document.getElementById('gemini-model').value;

    const body = {};
    if (apiKey) body.api_key = apiKey;
    if (model) body.model = model;

    const statusEl = document.getElementById('ai-status');
    try {
        const data = await apiFetch('/settings/ai', {
            method: 'PUT',
            body: JSON.stringify(body)
        });

        statusEl.style.display = 'block';
        statusEl.className = 'ai-status ai-status--success';
        statusEl.textContent = `✅ ${data.message || 'Configuração guardada'}`;
    } catch (err) {
        statusEl.style.display = 'block';
        statusEl.className = 'ai-status ai-status--error';
        statusEl.textContent = '❌ Erro ao guardar configuração';
    }
}

async function clearAIKey() {
    if (!confirm('Tem a certeza que deseja apagar a API Key guardada?')) return;

    const statusEl = document.getElementById('ai-status');
    try {
        const data = await apiFetch('/settings/ai', { method: 'DELETE' });
        document.getElementById('gemini-api-key').value = '';
        document.getElementById('gemini-api-key').placeholder = 'Cole aqui a sua API Key do Gemini';
        statusEl.style.display = 'block';
        statusEl.className = 'ai-status ai-status--success';
        statusEl.textContent = `✅ ${data.message || 'API Key removida'}`;
    } catch (err) {
        statusEl.style.display = 'block';
        statusEl.className = 'ai-status ai-status--error';
        statusEl.textContent = '❌ Erro ao apagar API Key';
    }
}

// ========== MODALS ==========
function initModals() {
    document.querySelectorAll('[data-close-modal]').forEach(btn => {
        btn.addEventListener('click', () => {
            btn.closest('.modal-overlay').style.display = 'none';
        });
    });

    document.getElementById('form-empresa').addEventListener('submit', async (e) => {
        e.preventDefault();
        const body = {
            nome: document.getElementById('emp-nome').value,
            setor: document.getElementById('emp-setor').value,
            num_colaboradores: parseInt(document.getElementById('emp-colaboradores').value) || null,
            localizacao: document.getElementById('emp-localizacao').value || null,
            descricao: document.getElementById('emp-descricao').value || null,
        };

        const data = await apiFetch('/empresas', { method: 'POST', body: JSON.stringify(body) });
        if (data.status === 'success') {
            document.getElementById('modal-empresa').style.display = 'none';
            e.target.reset();
            loadOverview();
            switchSection('empresas');
        }
    });
}

function openModal(id) {
    document.getElementById(id).style.display = 'flex';
}
