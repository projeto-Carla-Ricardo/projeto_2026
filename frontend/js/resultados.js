/**
 * Resultados JS — Visualização do relatório com gráfico radar.
 * Usa Canvas puro (sem bibliotecas externas).
 */

const API_BASE = window.location.origin + '/api/v1';
const token = localStorage.getItem('ialo_token');
const avaliacaoId = localStorage.getItem('ialo_avaliacao_id');

document.addEventListener('DOMContentLoaded', () => {
    if (!token || !avaliacaoId) {
        window.location.href = 'dashboard.html';
        return;
    }
    loadResults();
    document.getElementById('btn-download-pdf').addEventListener('click', downloadPDF);
});

function authHeaders() {
    return { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' };
}

async function apiFetch(url) {
    const res = await fetch(`${API_BASE}${url}`, { headers: authHeaders() });
    if (res.status === 401) { localStorage.clear(); window.location.href = 'login.html'; }
    return res.json();
}

// ========== LOAD ==========
async function loadResults() {
    try {
        const data = await apiFetch(`/relatorios/${avaliacaoId}`);
        if (data.status !== 'success') {
            document.getElementById('results-loading').innerHTML = '<p>❌ Erro ao carregar relatório</p>';
            return;
        }
        renderResults(data.data);
    } catch (err) {
        console.error(err);
        document.getElementById('results-loading').innerHTML = '<p>❌ Erro de ligação ao servidor</p>';
    }
}

// ========== RENDER ==========
function renderResults(report) {
    document.getElementById('results-loading').style.display = 'none';
    document.getElementById('results-content').style.display = 'block';

    // Score hero
    const pct = report.resumo.pontuacao_global;
    document.getElementById('score-value').textContent = `${pct}%`;
    document.getElementById('empresa-nome').textContent = report.empresa.nome;
    document.getElementById('score-nivel').textContent = `Nível ${report.resumo.nivel_global} — ${report.resumo.nivel_descricao}`;
    document.getElementById('score-descricao').textContent = getDescricaoNivel(report.resumo.nivel_global);

    // Animate score arc
    const arc = document.getElementById('score-arc');
    const circumference = 2 * Math.PI * 85; // radius = 85
    const offset = circumference - (pct / 100) * circumference;
    setTimeout(() => { arc.style.transition = 'stroke-dashoffset 1.5s ease'; arc.style.strokeDashoffset = offset; }, 100);

    // Radar chart
    drawRadarChart(report.radar_data);

    // Dimension bars
    renderDimBars(report.dimensoes);

    // Strengths
    renderPontosFortes(report.pontos_fortes);

    // Needs
    renderNecessidades(report.necessidades);

    // First steps
    renderPrimeirosPassos(report.primeiros_passos);

    // Recommendations
    renderRecomendacoes(report.recomendacoes);
}

function getDescricaoNivel(nivel) {
    const descs = {
        1: 'A empresa está nos primeiros passos da digitalização. Há oportunidades significativas de melhoria em quase todas as áreas.',
        2: 'Existem já algumas práticas digitais, mas ainda de forma inconsistente. É um bom momento para criar fundações sólidas.',
        3: 'A empresa tem práticas digitais definidas em várias áreas. O foco deve ser na consolidação e otimização.',
        4: 'Nível de maturidade digital elevado. A empresa está bem posicionada para adotar ferramentas de IA.',
        5: 'Excelência digital! A empresa é líder na sua categoria e pode explorar soluções de IA avançadas.',
    };
    return descs[nivel] || '';
}

// ========== RADAR CHART (Canvas puro) ==========
function drawRadarChart(radarData) {
    const canvas = document.getElementById('radar-chart');
    const ctx = canvas.getContext('2d');
    const dpr = window.devicePixelRatio || 1;

    canvas.width = 500 * dpr;
    canvas.height = 400 * dpr;
    ctx.scale(dpr, dpr);

    const centerX = 250;
    const centerY = 190;
    const maxRadius = 140;
    const labels = radarData.labels;
    const values = radarData.values;
    const n = labels.length;
    const angleStep = (2 * Math.PI) / n;
    const startAngle = -Math.PI / 2;

    // Colors
    const gridColor = 'rgba(99, 102, 241, 0.12)';
    const lineColor = 'rgba(99, 102, 241, 0.3)';
    const fillColor = 'rgba(99, 102, 241, 0.15)';
    const strokeColor = 'rgba(99, 102, 241, 0.8)';
    const dotColor = '#6366f1';
    const textColor = '#a0a0b8';
    const valueColor = '#e0e0f0';

    // Grid levels (20%, 40%, 60%, 80%, 100%)
    const levels = [0.2, 0.4, 0.6, 0.8, 1.0];

    // Draw grid
    levels.forEach(level => {
        ctx.beginPath();
        for (let i = 0; i < n; i++) {
            const angle = startAngle + i * angleStep;
            const x = centerX + Math.cos(angle) * maxRadius * level;
            const y = centerY + Math.sin(angle) * maxRadius * level;
            if (i === 0) ctx.moveTo(x, y);
            else ctx.lineTo(x, y);
        }
        ctx.closePath();
        ctx.strokeStyle = gridColor;
        ctx.lineWidth = 1;
        ctx.stroke();
    });

    // Draw axes
    for (let i = 0; i < n; i++) {
        const angle = startAngle + i * angleStep;
        ctx.beginPath();
        ctx.moveTo(centerX, centerY);
        ctx.lineTo(centerX + Math.cos(angle) * maxRadius, centerY + Math.sin(angle) * maxRadius);
        ctx.strokeStyle = lineColor;
        ctx.lineWidth = 1;
        ctx.stroke();
    }

    // Draw data polygon
    ctx.beginPath();
    for (let i = 0; i < n; i++) {
        const angle = startAngle + i * angleStep;
        const val = values[i] / 100;
        const x = centerX + Math.cos(angle) * maxRadius * val;
        const y = centerY + Math.sin(angle) * maxRadius * val;
        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
    }
    ctx.closePath();
    ctx.fillStyle = fillColor;
    ctx.fill();
    ctx.strokeStyle = strokeColor;
    ctx.lineWidth = 2;
    ctx.stroke();

    // Draw dots and values
    for (let i = 0; i < n; i++) {
        const angle = startAngle + i * angleStep;
        const val = values[i] / 100;
        const x = centerX + Math.cos(angle) * maxRadius * val;
        const y = centerY + Math.sin(angle) * maxRadius * val;

        ctx.beginPath();
        ctx.arc(x, y, 5, 0, 2 * Math.PI);
        ctx.fillStyle = dotColor;
        ctx.fill();
        ctx.strokeStyle = '#fff';
        ctx.lineWidth = 2;
        ctx.stroke();
    }

    // Draw labels
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';

    for (let i = 0; i < n; i++) {
        const angle = startAngle + i * angleStep;
        const labelRadius = maxRadius + 28;
        const lx = centerX + Math.cos(angle) * labelRadius;
        const ly = centerY + Math.sin(angle) * labelRadius;

        // Label name
        ctx.font = '600 12px Inter, sans-serif';
        ctx.fillStyle = textColor;
        ctx.fillText(labels[i], lx, ly);

        // Value under label
        ctx.font = '700 11px Inter, sans-serif';
        ctx.fillStyle = valueColor;
        ctx.fillText(`${values[i]}%`, lx, ly + 16);
    }

    // Level labels (on the top axis)
    ctx.textAlign = 'left';
    ctx.font = '400 9px Inter, sans-serif';
    ctx.fillStyle = 'rgba(160,160,184,0.5)';
    levels.forEach(level => {
        const y = centerY - maxRadius * level;
        ctx.fillText(`${Math.round(level * 100)}%`, centerX + 4, y - 2);
    });
}

// ========== DIMENSION BARS ==========
function renderDimBars(dimensoes) {
    const el = document.getElementById('dim-bars');
    el.innerHTML = dimensoes.map(d => {
        const cls = d.pontuacao >= 60 ? 'high' : d.pontuacao >= 40 ? 'medium' : 'low';
        const badge = d.gap_critico
            ? '<span class="dim-bar-badge badge--gap">GAP</span>'
            : '<span class="dim-bar-badge badge--ok">OK</span>';
        return `
        <div class="dim-bar-row">
            <div class="dim-bar-label">
                <strong>${d.codigo}</strong> — ${d.nome}
                <small>Nível ${d.nivel} · ${d.nivel_nome}</small>
            </div>
            <div class="dim-bar-track">
                <div class="dim-bar-fill dim-bar-fill--${cls}" style="width:0%"
                     data-target="${d.pontuacao}">${d.pontuacao}%</div>
            </div>
            <span class="dim-bar-score">${d.pontuacao}%</span>
            ${badge}
        </div>`;
    }).join('');

    // Animate bars
    setTimeout(() => {
        el.querySelectorAll('.dim-bar-fill').forEach(bar => {
            bar.style.width = bar.dataset.target + '%';
        });
    }, 200);
}

// ========== STRENGTHS ==========
function renderPontosFortes(fortes) {
    const el = document.getElementById('pontos-fortes');
    if (!fortes || fortes.length === 0) {
        el.innerHTML = '<div class="list-item"><p>Nenhum ponto forte identificado acima de 60%.</p></div>';
        return;
    }
    el.innerHTML = fortes.map(f => `
        <div class="list-item">
            <span class="list-item__icon">💪</span>
            <div><strong>${f.dimensao} (${f.pontuacao}%)</strong><p>${f.destaque}</p></div>
        </div>
    `).join('');
}

// ========== NEEDS ==========
function renderNecessidades(needs) {
    const el = document.getElementById('necessidades');
    if (!needs || needs.length === 0) {
        el.innerHTML = '<div class="list-item"><p>Nenhuma necessidade crítica — parabéns!</p></div>';
        return;
    }
    el.innerHTML = needs.map(n => `
        <div class="list-item">
            <span class="list-item__icon">${n.gap_critico ? '🔴' : '🟡'}</span>
            <div><strong>${n.dimensao} (${n.pontuacao}%)</strong><p>${n.acao}</p></div>
        </div>
    `).join('');
}

// ========== FIRST STEPS ==========
function renderPrimeirosPassos(passos) {
    const el = document.getElementById('primeiros-passos');
    if (!passos || passos.length === 0) {
        el.innerHTML = '<div class="step-item"><p>Continue com as boas práticas atuais.</p></div>';
        return;
    }
    el.innerHTML = passos.map((p, i) => `
        <div class="step-item">
            <span class="step-num">${i + 1}</span>
            <div class="step-text">
                <strong>${p.dimensao}</strong>
                <p>${p.acao}</p>
                ${p.ferramenta ? `<div class="step-tool">💡 Ferramenta sugerida: ${p.ferramenta}</div>` : ''}
            </div>
        </div>
    `).join('');
}

// ========== RECOMMENDATIONS ==========
function renderRecomendacoes(recs) {
    const el = document.getElementById('recomendacoes');
    if (!recs || recs.length === 0) {
        el.innerHTML = '<p style="color:var(--color-text-muted)">Sem recomendações disponíveis.</p>';
        return;
    }

    let cards = [];
    recs.forEach(rec => {
        rec.ferramentas.forEach(f => {
            if (cards.length < 9) {  // Max 9 cards
                cards.push({
                    ...f.ferramenta,
                    razao: f.razao,
                    dimensao: rec.codigo,
                    prioridade: rec.prioridade
                });
            }
        });
    });

    el.innerHTML = cards.map(c => `
        <div class="rec-card">
            <div class="rec-card__header">
                <span class="rec-card__name">${c.nome}</span>
                <span class="rec-card__cost">${c.custo || 'N/A'}</span>
            </div>
            <div class="rec-card__desc">${c.descricao || ''}</div>
            <div class="rec-card__reason">${c.razao || ''}</div>
            <span class="rec-card__dim">${c.dimensao}</span>
        </div>
    `).join('');
}

// ========== PDF DOWNLOAD ==========
async function downloadPDF() {
    const btn = document.getElementById('btn-download-pdf');
    btn.textContent = '⏳ A gerar PDF...';
    btn.disabled = true;

    try {
        const res = await fetch(`${API_BASE}/relatorios/${avaliacaoId}/pdf`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (res.ok) {
            const blob = await res.blob();
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `IALO_Diagnostico.pdf`;
            a.click();
            URL.revokeObjectURL(url);
        } else {
            alert('Erro ao gerar PDF');
        }
    } catch (err) {
        alert('Erro de ligação');
    } finally {
        btn.textContent = '📄 Descarregar PDF';
        btn.disabled = false;
    }
}
