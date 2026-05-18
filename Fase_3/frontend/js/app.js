/**
 * AILO — App Module
 * Inicialização, routing, navbar dinâmica e utilidades globais.
 */

// Toast notifications
function showToast(message, type = 'info') {
    let container = document.querySelector('.toast-container');
    if (!container) { container = document.createElement('div'); container.className = 'toast-container'; document.body.appendChild(container); }
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    container.appendChild(toast);
    setTimeout(() => toast.remove(), 4000);
}

// Update navbar based on auth state
function updateNavbar() {
    const navLinks = document.getElementById('nav-links');
    if (!navLinks) return;
    if (api.isAuthenticated()) {
        const user = api.getUser();
        const isAdmin = user && user.papel === 'admin';
        navLinks.innerHTML = `
            <a href="/pages/dashboard.html" class="nav-link">Dashboard</a>
            <a href="/pages/organizacoes.html" class="nav-link">Organizações</a>
            <a href="/pages/comparacao.html" class="nav-link">Comparação</a>
            ${isAdmin ? '<a href="/pages/admin.html" class="nav-link" style="color:var(--ailo-cognitiva);">⚙️ Admin</a>' : ''}
            <a href="/pages/perfil.html" class="nav-link">👤 ${user ? user.nome : ''}</a>
            <button class="btn btn-sm btn-secondary" onclick="logout()">Sair</button>
        `;
    } else {
        navLinks.innerHTML = `
            <a href="/pages/login.html" class="nav-link">Entrar</a>
            <a href="/pages/register.html" class="btn btn-primary btn-sm">Registar</a>
        `;
    }
}

function logout() {
    api.clearToken();
    window.location.href = '/';
}

function requireAuth() {
    if (!api.isAuthenticated()) { window.location.href = '/pages/login.html'; return false; }
    return true;
}

// Init
document.addEventListener('DOMContentLoaded', updateNavbar);
