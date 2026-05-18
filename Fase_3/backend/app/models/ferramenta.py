"""Modelos de Ferramentas IA e Recomendações."""
from app import db
from datetime import datetime


class FerramentaIA(db.Model):
    __tablename__ = 'ferramentas_ia'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    camada_id = db.Column(db.Integer, db.ForeignKey('camadas_ailo.id'))
    area_funcional = db.Column(db.String(100), nullable=False)
    custo = db.Column(db.String(20), nullable=False)
    complexidade = db.Column(db.String(20), nullable=False)
    url = db.Column(db.String(500))
    ativo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    camada = db.relationship('CamadaAilo', backref='ferramentas', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'camada': self.camada.nome if self.camada else None,
            'area_funcional': self.area_funcional,
            'custo': self.custo,
            'complexidade': self.complexidade,
            'url': self.url,
            'ativo': self.ativo
        }


class Recomendacao(db.Model):
    __tablename__ = 'recomendacoes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    avaliacao_id = db.Column(db.Integer, db.ForeignKey('avaliacoes.id'), nullable=False)
    ferramenta_id = db.Column(db.Integer, db.ForeignKey('ferramentas_ia.id'), nullable=False)
    camada_id = db.Column(db.Integer, db.ForeignKey('camadas_ailo.id'), nullable=False)
    prioridade = db.Column(db.Integer, nullable=False, default=1)
    justificacao = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    ferramenta = db.relationship('FerramentaIA', backref='recomendacoes_rel', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'prioridade': self.prioridade,
            'ferramenta': self.ferramenta.to_dict() if self.ferramenta else None,
            'justificacao': self.justificacao
        }
