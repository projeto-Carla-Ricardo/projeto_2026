"""
Flask Application Factory — Projeto IALO
"""
import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from app.config import config

# Extensões (inicializadas sem app)
db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()
limiter = Limiter(key_func=get_remote_address)


def create_app(config_name=None):
    """Factory que cria e configura a aplicação Flask."""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')

    frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'frontend'))
    app = Flask(__name__, instance_relative_config=True,
                static_folder=frontend_dir, static_url_path='/static')
    app.config.from_object(config[config_name])

    # Garantir que a pasta instance existe
    os.makedirs(app.instance_path, exist_ok=True)

    # Inicializar extensões
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)
    CORS(app)

    # Importar modelos para que o Alembic os detete
    from app.models import (  # noqa: F401
        utilizador, empresa, avaliacao, dimensao, indicador,
        pergunta, resposta, resultado, relatorio, ferramenta,
        recomendacao, conversa
    )

    # Registar blueprints
    from app.routes import register_blueprints
    register_blueprints(app)

    # Health check endpoint
    @app.route('/api/v1/health')
    def health():
        return jsonify({'status': 'ok', 'message': 'IALO API operacional'}), 200

    # Servir frontend (páginas HTML)
    from flask import send_from_directory

    @app.route('/')
    def serve_index():
        return send_from_directory(frontend_dir, 'index.html')

    @app.route('/pages/<path:filename>')
    def serve_pages(filename):
        return send_from_directory(os.path.join(frontend_dir, 'pages'), filename)

    @app.route('/css/<path:filename>')
    def serve_css(filename):
        return send_from_directory(os.path.join(frontend_dir, 'css'), filename)

    @app.route('/js/<path:filename>')
    def serve_js(filename):
        return send_from_directory(os.path.join(frontend_dir, 'js'), filename)

    return app
