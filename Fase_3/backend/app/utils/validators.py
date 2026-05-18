"""Validadores de dados de entrada."""
import re


def validate_email(email):
    """Valida formato de email."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_password(password):
    """Valida força da password (mínimo 6 caracteres)."""
    if len(password) < 6:
        return False, 'Password deve ter pelo menos 6 caracteres'
    return True, ''


def validate_required_fields(data, fields):
    """Verifica campos obrigatórios."""
    missing = [f for f in fields if not data.get(f)]
    if missing:
        return False, f'Campos obrigatórios em falta: {", ".join(missing)}'
    return True, ''


def sanitize_string(text):
    """Remove caracteres potencialmente perigosos."""
    if text is None:
        return None
    # Escapa HTML básico
    text = text.replace('<', '&lt;').replace('>', '&gt;')
    return text.strip()
