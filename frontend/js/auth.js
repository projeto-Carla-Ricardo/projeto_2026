/**
 * Auth JS — Login + Register Logic
 * Handles form submission and JWT storage.
 */

const API_BASE = window.location.origin + '/api/v1';

document.addEventListener('DOMContentLoaded', () => {
    // If already logged in, redirect to dashboard
    if (localStorage.getItem('ialo_token')) {
        window.location.href = 'dashboard.html';
        return;
    }

    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');

    if (loginForm) loginForm.addEventListener('submit', handleLogin);
    if (registerForm) registerForm.addEventListener('submit', handleRegister);
});

async function handleLogin(e) {
    e.preventDefault();
    const btn = document.getElementById('btn-login');
    const errorDiv = document.getElementById('auth-error');

    setLoading(btn, true);
    errorDiv.style.display = 'none';

    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;

    try {
        const res = await fetch(`${API_BASE}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });

        const data = await res.json();

        if (res.ok && data.status === 'success') {
            localStorage.setItem('ialo_token', data.data.token);
            localStorage.setItem('ialo_refresh', data.data.refresh_token);
            localStorage.setItem('ialo_user', JSON.stringify(data.data.user));
            window.location.href = 'dashboard.html';
        } else {
            showError(errorDiv, data.error?.message || 'Erro ao entrar');
        }
    } catch (err) {
        showError(errorDiv, 'Erro de ligação ao servidor');
    } finally {
        setLoading(btn, false);
    }
}

async function handleRegister(e) {
    e.preventDefault();
    const btn = document.getElementById('btn-register');
    const errorDiv = document.getElementById('auth-error');

    const password = document.getElementById('password').value;
    const passwordConfirm = document.getElementById('password-confirm').value;

    if (password !== passwordConfirm) {
        showError(errorDiv, 'As passwords não coincidem');
        return;
    }

    setLoading(btn, true);
    errorDiv.style.display = 'none';

    const nome = document.getElementById('nome').value.trim();
    const email = document.getElementById('email').value.trim();

    try {
        const res = await fetch(`${API_BASE}/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ nome, email, password })
        });

        const data = await res.json();

        if (res.ok && data.status === 'success') {
            // Auto-login after registration
            const loginRes = await fetch(`${API_BASE}/auth/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            });
            const loginData = await loginRes.json();

            if (loginRes.ok) {
                localStorage.setItem('ialo_token', loginData.data.token);
                localStorage.setItem('ialo_refresh', loginData.data.refresh_token);
                localStorage.setItem('ialo_user', JSON.stringify(loginData.data.user));
                window.location.href = 'dashboard.html';
            }
        } else {
            showError(errorDiv, data.error?.message || 'Erro ao criar conta');
        }
    } catch (err) {
        showError(errorDiv, 'Erro de ligação ao servidor');
    } finally {
        setLoading(btn, false);
    }
}

function showError(el, msg) {
    el.textContent = msg;
    el.style.display = 'block';
}

function setLoading(btn, loading) {
    const text = btn.querySelector('.btn-text');
    const spinner = btn.querySelector('.btn-loading');
    if (loading) {
        text.style.display = 'none';
        spinner.style.display = 'inline';
        btn.disabled = true;
    } else {
        text.style.display = 'inline';
        spinner.style.display = 'none';
        btn.disabled = false;
    }
}
