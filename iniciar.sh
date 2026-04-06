#!/bin/bash
# ============================================================
# Script de Arranque — Ambiente IALO
# ============================================================

echo "🚀 A iniciar o ambiente IALO..."

# Verificar se as pastas necessárias existem
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo "❌ Erro: As pastas 'backend' ou 'frontend' não foram encontradas nesta diretoria."
    exit 1
fi

# Iniciar backend em background
echo "📦 A iniciar backend na porta 5000..."
cd backend
if [ ! -d "venv" ]; then
    echo "⚙️ Primeira execução detetada. A preparar ambiente virtual, dependências e base de dados..."
    make setup
fi

make dev &
BACKEND_PID=$!
cd ..

# Iniciar frontend em background
echo "🌐 A iniciar frontend nativo na porta 8000..."
cd frontend
python3 -m http.server 8000 &
FRONTEND_PID=$!
cd ..

echo "============================================================"
echo "✅ Backend em funcionamento."
echo "✅ Frontend disponível em http://localhost:8000"
echo "❗ Pressione CTRL+C para encerrar todos os processos."
echo "============================================================"

# Handlers de encerramento
trap "echo -e '\n🛑 A encerrar os servidores...'; kill $BACKEND_PID $FRONTEND_PID; exit 0" INT TERM

# Aguardar os processos terminarem
wait
