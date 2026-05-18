"""Modelos de Resultados — ResultadoCamada e Interdependência."""
from app import db
from datetime import datetime
import json


class ResultadoCamada(db.Model):
    __tablename__ = 'resultados_camada'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    avaliacao_id = db.Column(db.Integer, db.ForeignKey('avaliacoes.id'), nullable=False)
    camada_id = db.Column(db.Integer, db.ForeignKey('camadas_ailo.id'), nullable=False)
    score = db.Column(db.Float, nullable=False)
    nivel = db.Column(db.String(50), nullable=False)
    pontos_fortes = db.Column(db.Text)   # JSON
    lacunas = db.Column(db.Text)          # JSON
    recomendacoes = db.Column(db.Text)    # JSON
    cr_mapeamento = db.Column(db.Text)    # JSON

    __table_args__ = (db.UniqueConstraint('avaliacao_id', 'camada_id'),)

    camada = db.relationship('CamadaAilo', backref='resultados', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'avaliacao_id': self.avaliacao_id,
            'camada_id': self.camada_id,
            'camada_nome': self.camada.nome if self.camada else None,
            'camada_cor': self.camada.cor if self.camada else None,
            'score': round(self.score, 2),
            'nivel': self.nivel,
            'pontos_fortes': json.loads(self.pontos_fortes) if self.pontos_fortes else [],
            'lacunas': json.loads(self.lacunas) if self.lacunas else [],
            'recomendacoes': json.loads(self.recomendacoes) if self.recomendacoes else [],
            'cr_mapeamento': json.loads(self.cr_mapeamento) if self.cr_mapeamento else []
        }


class Interdependencia(db.Model):
    __tablename__ = 'interdependencias'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    avaliacao_id = db.Column(db.Integer, db.ForeignKey('avaliacoes.id'), nullable=False)
    camada_a_id = db.Column(db.Integer, db.ForeignKey('camadas_ailo.id'), nullable=False)
    camada_b_id = db.Column(db.Integer, db.ForeignKey('camadas_ailo.id'), nullable=False)
    tipo_relacao = db.Column(db.String(50), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    impacto = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    camada_a = db.relationship('CamadaAilo', foreign_keys=[camada_a_id])
    camada_b = db.relationship('CamadaAilo', foreign_keys=[camada_b_id])

    def to_dict(self):
        return {
            'id': self.id,
            'camada_a': self.camada_a.nome if self.camada_a else None,
            'camada_b': self.camada_b.nome if self.camada_b else None,
            'tipo_relacao': self.tipo_relacao,
            'descricao': self.descricao,
            'impacto': self.impacto
        }
