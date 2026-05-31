#!/bin/bash
# ══════════════════════════════════════════════════════
#  AILO — Launcher da Plataforma (Fase 4)
#  Artificial Intelligence in a Learning Organization
# ══════════════════════════════════════════════════════

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$SCRIPT_DIR/backend"
VENV_DIR="$BACKEND_DIR/venv"
VENV_PYTHON="$VENV_DIR/bin/python"
VENV_PIP="$VENV_DIR/bin/python -m pip"
PORT=5000

echo "══════════════════════════════════════════════════════"
echo "  🧠 AILO — Artificial Intelligence in a Learning Organization"
echo "  📦 Fase 4 — Plataforma de Diagnóstico de Maturidade"
echo "══════════════════════════════════════════════════════"
echo ""

# 1. Verificar Python do sistema
PYTHON=""
if command -v python3 &>/dev/null; then
    PYTHON=python3
elif command -v python &>/dev/null; then
    PYTHON=python
else
    echo "❌ Python 3 não encontrado. Por favor instale o Python 3.10+."
    echo ""
    read -p "Pressione ENTER para sair..."
    exit 1
fi
echo "✅ Python do sistema: $($PYTHON --version)"

# 2. Criar venv se não existir
if [ ! -d "$VENV_DIR" ]; then
    echo "📦 A criar ambiente virtual..."
    $PYTHON -m venv "$VENV_DIR"
    if [ $? -ne 0 ]; then
        echo "❌ Erro ao criar ambiente virtual."
        read -p "Pressione ENTER para sair..."
        exit 1
    fi
    echo "✅ Ambiente virtual criado"
fi

# Verificar que o Python do venv existe
if [ ! -f "$VENV_PYTHON" ]; then
    echo "❌ Python do venv não encontrado em: $VENV_PYTHON"
    echo "   A recriar o ambiente virtual..."
    rm -rf "$VENV_DIR"
    $PYTHON -m venv "$VENV_DIR"
fi
echo "✅ Ambiente virtual: $("$VENV_PYTHON" --version)"

# 3. Instalar dependências (usando o Python do venv diretamente)
echo "📦 A verificar dependências..."
"$VENV_PYTHON" -m pip install -q -r "$BACKEND_DIR/requirements.txt" 2>&1
if [ $? -ne 0 ]; then
    echo "⚠️  Algumas dependências podem não ter sido instaladas."
    echo "   A tentar continuar..."
fi
echo "✅ Dependências verificadas"

# 4. Criar .env se não existir
if [ ! -f "$BACKEND_DIR/.env" ]; then
    if [ -f "$BACKEND_DIR/.env.example" ]; then
        cp "$BACKEND_DIR/.env.example" "$BACKEND_DIR/.env"
        echo "✅ Ficheiro .env criado a partir do .env.example"
        echo "⚠️  NOTA: Edite o ficheiro backend/.env para configurar a GEMINI_API_KEY"
    fi
fi

# 5. Executar seed (popular BD)
echo ""
echo "🌱 A popular base de dados..."
cd "$BACKEND_DIR"
"$VENV_PYTHON" seed.py
if [ $? -ne 0 ]; then
    echo "⚠️  Aviso: O seed pode não ter sido executado corretamente."
fi
echo ""

# 6. Abrir browser (em background, após delay)
(sleep 3 && xdg-open "http://localhost:$PORT" 2>/dev/null) &

# 7. Iniciar servidor
echo "══════════════════════════════════════════════════════"
echo "  🚀 Servidor AILO a iniciar em http://localhost:$PORT"
echo ""
echo "  📋 Credenciais de Acesso:"
echo "     Admin:      admin@ailo.pt / Admin2026!"
echo "     Utilizador: demo@ailo.pt  / Demo2026!"
echo ""
echo "  Pressione Ctrl+C para parar o servidor"
echo "══════════════════════════════════════════════════════"
echo ""

"$VENV_PYTHON" run.py

# Se o servidor parar, manter o terminal aberto
echo ""
echo "⚠️  O servidor foi encerrado."
echo ""
read -p "Pressione ENTER para fechar..."
