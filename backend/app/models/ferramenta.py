"""
Modelo: Ferramenta IA (catálogo de referência)
Tabela: ferramentas_ia
"""
from app import db


class FerramentaIA(db.Model):
    __tablename__ = 'ferramentas_ia'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    categoria = db.Column(db.String(50), nullable=False)    # atendimento, gestao, marketing, operacoes, dados, automacao
    custo = db.Column(db.String(30), nullable=False)         # gratuito, freemium, baixo_custo, pago
    complexidade = db.Column(db.String(30), nullable=False)  # muito_facil, facil, medio, avancado
    url = db.Column(db.String(500))
    setores_alvo = db.Column(db.Text)  # JSON array de setores
    ativo = db.Column(db.Boolean, nullable=False, default=True)

    # Relações
    recomendacoes = db.relationship('Recomendacao', backref='ferramenta', lazy='dynamic')

    def __repr__(self):
        return f'<FerramentaIA {self.nome}>'

    def to_dict(self):
        import json
        setores = None
        if self.setores_alvo:
            try:
                setores = json.loads(self.setores_alvo)
            except (json.JSONDecodeError, TypeError):
                setores = self.setores_alvo
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'categoria': self.categoria,
            'custo': self.custo,
            'complexidade': self.complexidade,
            'url': self.url,
            'setores_alvo': setores,
            'ativo': self.ativo
        }
