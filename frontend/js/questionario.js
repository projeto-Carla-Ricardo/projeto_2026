/**
 * Questionário JS — Interactive questionnaire with AI assistant.
 */

const API_BASE = window.location.origin + '/api/v1';
const token = localStorage.getItem('ialo_token');
const avaliacaoId = localStorage.getItem('ialo_avaliacao_id');

let dimensoes = [];
let currentDimIndex = 0;
let currentPerguntaIndex = 0;
let allPerguntas = [];
let respostasMap = {};  // { pergunta_id: { valor_texto, valor_numerico } }

document.addEventListener('DOMContentLoaded', () => {
    if (!token || !avaliacaoId) {
        window.location.href = 'dashboard.html';
        return;
    }
    loadQuestionario();
    initChat();
    initNavigation();
});

function authHeaders() {
    return { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' };
}

async function apiFetch(url, opts = {}) {
    opts.headers = { ...authHeaders(), ...opts.headers };
    return fetch(`${API_BASE}${url}`, opts).then(r => r.json());
}

// ========== LOAD QUESTIONARIO ==========
async function loadQuestionario() {
    try {
        const [dimData, respData] = await Promise.all([
            apiFetch('/questionario/dimensoes'),
            apiFetch(`/questionario/respostas/${avaliacaoId}`)
        ]);

        dimensoes = dimData.data || [];
        const respostasExistentes = respData.data || [];

        // Map existing answers
        respostasExistentes.forEach(r => {
            respostasMap[r.pergunta_id] = {
                valor_texto: r.valor_texto,
                valor_numerico: r.valor_numerico
            };
        });

        // Flatten all questions
        allPerguntas = [];
        dimensoes.forEach(dim => {
            dim.indicadores.forEach(ind => {
                ind.perguntas.forEach(p => {
                    allPerguntas.push({ ...p, dimensao: dim, indicador: ind });
                });
            });
        });

        renderDimensionTabs();
        renderQuestion();
        updateProgress();
    } catch (err) {
        console.error('Erro ao carregar questionário:', err);
    }
}

// ========== RENDER ==========
function renderDimensionTabs() {
    const container = document.getElementById('quiz-dimensions');
    container.innerHTML = dimensoes.map((dim, i) => {
        const totalPerguntas = dim.indicadores.reduce((s, ind) => s + ind.perguntas.length, 0);
        const respondidas = dim.indicadores.reduce((s, ind) => 
            s + ind.perguntas.filter(p => respostasMap[p.id]).length, 0);
        const complete = respondidas >= totalPerguntas;
        return `<button class="dim-tab ${i === currentDimIndex ? 'dim-tab--active' : ''} ${complete ? 'dim-tab--complete' : ''}" 
                        data-dim="${i}" title="${dim.nome}: ${respondidas}/${totalPerguntas}">
            ${dim.codigo}
        </button>`;
    }).join('');

    container.querySelectorAll('.dim-tab').forEach(tab => {
        tab.addEventListener('click', () => {
            const dimIdx = parseInt(tab.dataset.dim);
            jumpToDimension(dimIdx);
        });
    });
}

function jumpToDimension(dimIdx) {
    currentDimIndex = dimIdx;
    // Find first question of this dimension
    const dim = dimensoes[dimIdx];
    const firstPergunta = dim.indicadores[0]?.perguntas[0];
    if (firstPergunta) {
        currentPerguntaIndex = allPerguntas.findIndex(p => p.id === firstPergunta.id);
    }
    renderQuestion();
    renderDimensionTabs();
}

function renderQuestion() {
    const body = document.getElementById('quiz-body');
    if (currentPerguntaIndex >= allPerguntas.length) {
        showFinishScreen();
        return;
    }

    const pergunta = allPerguntas[currentPerguntaIndex];
    const resposta = respostasMap[pergunta.id];
    const total = allPerguntas.length;

    let answerHTML = '';
    if (pergunta.tipo_resposta === 'escala_1_5') {
        answerHTML = renderScale(pergunta, resposta);
    } else if (pergunta.tipo_resposta === 'escolha_multipla' && pergunta.opcoes) {
        answerHTML = renderOptions(pergunta, resposta);
    } else if (pergunta.tipo_resposta === 'sim_nao') {
        answerHTML = renderSimNao(pergunta, resposta);
    } else {
        answerHTML = renderTexto(pergunta, resposta);
    }

    body.innerHTML = `
        <div class="question-card">
            <span class="question-dim-badge">${pergunta.dimensao.nome}</span>
            <div class="question-number">Pergunta ${currentPerguntaIndex + 1} de ${total} — ${pergunta.indicador.nome}</div>
            <h2 class="question-text">${pergunta.texto}</h2>
            ${pergunta.ajuda_contextual ? `<div class="question-help">💡 ${pergunta.ajuda_contextual}</div>` : ''}
            <div class="answer-area">${answerHTML}</div>
        </div>
    `;

    // Update nav buttons
    document.getElementById('btn-prev').disabled = currentPerguntaIndex === 0;
    const isLast = currentPerguntaIndex >= total - 1;
    document.getElementById('btn-next').style.display = isLast ? 'none' : 'inline-flex';
    document.getElementById('btn-finish').style.display = isLast ? 'inline-flex' : 'none';

    // Update dimension tab
    const dimIdx = dimensoes.findIndex(d => d.id === pergunta.dimensao.id);
    if (dimIdx !== currentDimIndex) {
        currentDimIndex = dimIdx;
        renderDimensionTabs();
    }
}

function renderScale(pergunta, resposta) {
    const selected = resposta?.valor_numerico || null;
    return `
        <div class="scale-options">
            ${[1, 2, 3, 4, 5].map(v => `
                <button class="scale-btn ${selected === v ? 'scale-btn--selected' : ''}" 
                        onclick="selectScale(${pergunta.id}, ${v})">${v}</button>
            `).join('')}
        </div>
        <div class="scale-labels">
            <span>Nunca / Nada</span>
            <span>Sempre / Totalmente</span>
        </div>`;
}

function renderOptions(pergunta, resposta) {
    return `<div class="answer-options">
        ${pergunta.opcoes.map((opt, i) => {
            const selected = resposta?.valor_texto === opt;
            return `<label class="answer-option ${selected ? 'answer-option--selected' : ''}" 
                           onclick="selectOption(${pergunta.id}, '${opt.replace(/'/g, "\\'")}', ${i})">
                <input type="radio" name="q${pergunta.id}" value="${opt}" ${selected ? 'checked' : ''}>
                <span class="answer-radio"></span>
                <span class="answer-label">${opt}</span>
            </label>`;
        }).join('')}
    </div>`;
}

function renderSimNao(pergunta, resposta) {
    return `<div class="answer-options">
        ${['Sim', 'Não'].map(opt => {
            const selected = resposta?.valor_texto === opt;
            return `<label class="answer-option ${selected ? 'answer-option--selected' : ''}" 
                           onclick="selectOption(${pergunta.id}, '${opt}', ${opt === 'Sim' ? 1 : 0})">
                <input type="radio" name="q${pergunta.id}" value="${opt}" ${selected ? 'checked' : ''}>
                <span class="answer-radio"></span>
                <span class="answer-label">${opt}</span>
            </label>`;
        }).join('')}
    </div>`;
}

function renderTexto(pergunta, resposta) {
    return `<textarea class="form-input form-textarea" rows="3" placeholder="Escreva a sua resposta..." 
                onchange="selectTexto(${pergunta.id}, this.value)">${resposta?.valor_texto || ''}</textarea>`;
}

// ========== ANSWER HANDLERS ==========
window.selectScale = function(perguntaId, valor) {
    respostasMap[perguntaId] = { valor_numerico: valor, valor_texto: null };
    renderQuestion();
    updateProgress();
};

window.selectOption = function(perguntaId, texto, numerico) {
    respostasMap[perguntaId] = { valor_texto: texto, valor_numerico: numerico };
    renderQuestion();
    updateProgress();
};

window.selectTexto = function(perguntaId, texto) {
    respostasMap[perguntaId] = { valor_texto: texto, valor_numerico: null };
    updateProgress();
};

// ========== NAVIGATION ==========
function initNavigation() {
    document.getElementById('btn-prev').addEventListener('click', () => {
        if (currentPerguntaIndex > 0) { currentPerguntaIndex--; renderQuestion(); }
    });
    document.getElementById('btn-next').addEventListener('click', () => {
        if (currentPerguntaIndex < allPerguntas.length - 1) { currentPerguntaIndex++; renderQuestion(); }
    });
    document.getElementById('btn-save').addEventListener('click', saveProgress);
    document.getElementById('btn-finish').addEventListener('click', finishDiagnostico);
}

function updateProgress() {
    const total = allPerguntas.length;
    const respondidas = Object.keys(respostasMap).length;
    const pct = Math.round((respondidas / total) * 100);
    document.getElementById('progress-fill').style.width = `${pct}%`;
    document.getElementById('progress-text').textContent = `${pct}%`;
    renderDimensionTabs();
}

async function saveProgress() {
    const respostas = Object.entries(respostasMap).map(([pid, val]) => ({
        pergunta_id: parseInt(pid),
        ...val
    }));

    const data = await apiFetch('/questionario/respostas', {
        method: 'POST',
        body: JSON.stringify({ avaliacao_id: parseInt(avaliacaoId), respostas })
    });

    if (data.status === 'success') {
        const btn = document.getElementById('btn-save');
        btn.textContent = '✅ Guardado!';
        setTimeout(() => btn.textContent = '💾 Guardar Progresso', 2000);
    }
}

async function finishDiagnostico() {
    await saveProgress();
    const data = await apiFetch(`/avaliacoes/${avaliacaoId}/concluir`, { method: 'POST' });
    if (data.status === 'success') {
        showResults(data.data);
    }
}

function showFinishScreen() {
    document.getElementById('quiz-body').innerHTML = `
        <div class="quiz-loading">
            <h2>✅ Todas as perguntas respondidas!</h2>
            <p>Clique em "Concluir Diagnóstico" para ver os resultados.</p>
        </div>`;
}

function showResults(data) {
    // Redirecionar para a página de resultados
    window.location.href = 'resultados.html';
}

// ========== CHAT ==========
function initChat() {
    const input = document.getElementById('chat-input-field');
    const btn = document.getElementById('btn-send-chat');

    btn.addEventListener('click', sendMessage);
    input.addEventListener('keypress', e => { if (e.key === 'Enter') sendMessage(); });
}

async function sendMessage() {
    const input = document.getElementById('chat-input-field');
    const mensagem = input.value.trim();
    if (!mensagem) return;

    input.value = '';
    addChatMessage(mensagem, 'user');

    // Show typing indicator
    const typingEl = addChatMessage('', 'assistant', true);

    const perguntaAtualId = allPerguntas[currentPerguntaIndex]?.id;

    try {
        const data = await apiFetch('/assistente/mensagem', {
            method: 'POST',
            body: JSON.stringify({
                avaliacao_id: parseInt(avaliacaoId),
                mensagem,
                pergunta_atual_id: perguntaAtualId
            })
        });

        typingEl.remove();
        addChatMessage(data.data?.resposta || 'Sem resposta', 'assistant');
    } catch (err) {
        typingEl.remove();
        addChatMessage('⚠️ Erro ao contactar o assistente', 'assistant');
    }
}

function addChatMessage(text, role, typing = false) {
    const container = document.getElementById('chat-messages');
    const div = document.createElement('div');
    div.className = `chat-message chat-message--${role === 'user' ? 'user' : 'assistant'} ${typing ? 'chat-message--typing' : ''}`;

    const avatar = role === 'user' ? '👤' : '🤖';
    div.innerHTML = `
        <div class="chat-message__avatar">${avatar}</div>
        <div class="chat-message__bubble">${typing ? '' : `<p>${text}</p>`}</div>
    `;

    container.appendChild(div);
    container.scrollTop = container.scrollHeight;
    return div;
}
