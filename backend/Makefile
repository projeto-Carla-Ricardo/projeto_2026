# ============================================================
# IALO — Makefile de Build/Deploy
# Projeto Final — Engenharia Informática · Universidade Aberta
# ============================================================

.PHONY: setup install migrate seed run dev test clean reset help

# Variáveis
PYTHON := python3
PIP := pip
FLASK := flask
VENV := venv

help: ## Mostrar esta ajuda
	@echo "╔══════════════════════════════════════════════╗"
	@echo "║        IALO — Comandos Disponíveis          ║"
	@echo "╚══════════════════════════════════════════════╝"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

setup: ## Configurar ambiente completo (venv + deps + BD + seed)
	@echo "🔧 A criar ambiente virtual..."
	$(PYTHON) -m venv $(VENV)
	@echo "📦 A instalar dependências..."
	$(VENV)/bin/$(PIP) install -r requirements.txt
	@echo "📋 A copiar .env..."
	@test -f .env || cp .env.example .env
	@echo "🗄️  A criar base de dados..."
	$(VENV)/bin/$(FLASK) db upgrade
	@echo "🌱 A popular dados iniciais..."
	$(VENV)/bin/$(PYTHON) seed.py
	@echo ""
	@echo "✅ Setup completo! Executa 'make run' para arrancar."

install: ## Instalar dependências Python
	$(VENV)/bin/$(PIP) install -r requirements.txt

migrate: ## Aplicar migrations da base de dados
	$(VENV)/bin/$(FLASK) db upgrade

seed: ## Popular base de dados com dados iniciais
	$(VENV)/bin/$(PYTHON) seed.py

run: ## Arrancar o servidor (produção)
	@echo "🚀 A arrancar servidor IALO..."
	$(VENV)/bin/$(PYTHON) run.py

dev: ## Arrancar o servidor em modo desenvolvimento (debug + reload)
	@echo "🔧 Modo desenvolvimento ativo..."
	FLASK_ENV=development FLASK_DEBUG=1 $(VENV)/bin/$(PYTHON) run.py

test: ## Executar testes
	$(VENV)/bin/$(PYTHON) -m pytest tests/ -v

clean: ## Limpar ficheiros temporários
	@echo "🧹 A limpar..."
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	rm -rf .pytest_cache 2>/dev/null || true

reset: ## Reset completo da base de dados (CUIDADO!)
	@echo "⚠️  A fazer reset da base de dados..."
	rm -f instance/ialo_dev.db
	$(VENV)/bin/$(FLASK) db upgrade
	$(VENV)/bin/$(PYTHON) seed.py
	@echo "✅ Base de dados recriada."
