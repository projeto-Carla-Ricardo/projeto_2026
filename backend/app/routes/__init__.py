"""
Registo de blueprints da API.
"""


def register_blueprints(app):
    """Regista todos os blueprints da aplicação."""
    from app.routes.auth import auth_bp
    from app.routes.empresas import empresas_bp
    from app.routes.avaliacoes import avaliacoes_bp
    from app.routes.questionario import questionario_bp
    from app.routes.scoring import scoring_bp
    from app.routes.assistente import assistente_bp
    from app.routes.settings import settings_bp
    from app.routes.relatorios import relatorios_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(empresas_bp)
    app.register_blueprint(avaliacoes_bp)
    app.register_blueprint(questionario_bp)
    app.register_blueprint(scoring_bp)
    app.register_blueprint(assistente_bp)
    app.register_blueprint(settings_bp)
    app.register_blueprint(relatorios_bp)
