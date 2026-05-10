"""Modelo de Resposta."""
from app import db
from datetime import datetime


class Resposta(db.Model):
    __tablename__ = 'respostas'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    avaliacao_id = db.Column(db.Integer, db.ForeignKey('avaliacoes.id'), nullable=False)
    indicador_id = db.Column(db.Integer, db.ForeignKey('indicadores.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    justificacao = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint('avaliacao_id', 'indicador_id'),)

    # Relações
    indicador = db.relationship('Indicador', backref='respostas', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'avaliacao_id': self.avaliacao_id,
            'indicador_id': self.indicador_id,
            'codigo': self.indicador.codigo if self.indicador else None,
            'score': self.score,
            'justificacao': self.justificacao,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
