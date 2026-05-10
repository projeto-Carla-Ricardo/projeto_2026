"""
Flask App Factory — Plataforma AILO
Artificial Intelligence in a Learning Organization
"""
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(config_name='default'):
    """Cria e configura a aplicação Flask."""
    from app.config import config as config_dict

    app = Flask(__name__,
                static_folder='../../frontend',
                static_url_path='/static')

    app.config.from_object(config_dict.get(config_name, config_dict['default']))

    # Inicializar extensões
    db.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Registar blueprints
    from app.routes.auth import auth_bp
    from app.routes.organizacoes import org_bp
    from app.routes.ailo import ailo_bp
    from app.routes.avaliacoes import aval_bp
    from app.routes.respostas import resp_bp
    from app.routes.resultados import result_bp
    from app.routes.chat import chat_bp
    from app.routes.relatorios import relat_bp

    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(org_bp, url_prefix='/api/v1/organizacoes')
    app.register_blueprint(ailo_bp, url_prefix='/api/v1/ailo')
    app.register_blueprint(aval_bp, url_prefix='/api/v1/avaliacoes')
    app.register_blueprint(resp_bp, url_prefix='/api/v1/avaliacoes')
    app.register_blueprint(result_bp, url_prefix='/api/v1/avaliacoes')
    app.register_blueprint(chat_bp, url_prefix='/api/v1/avaliacoes')
    app.register_blueprint(relat_bp, url_prefix='/api/v1')

    # Rota para servir o frontend
    @app.route('/')
    def serve_index():
        return app.send_static_file('index.html')

    @app.route('/pages/<path:filename>')
    def serve_pages(filename):
        return app.send_static_file(f'pages/{filename}')

    # Criar tabelas
    with app.app_context():
        from app.models import utilizador, organizacao, ailo, avaliacao, resposta, resultado, ferramenta, conversa
        db.create_all()

    return app
