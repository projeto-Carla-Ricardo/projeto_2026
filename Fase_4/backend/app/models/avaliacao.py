"""Modelo de Avaliação."""
from app import db
from datetime import datetime


class Avaliacao(db.Model):
    __tablename__ = 'avaliacoes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    organizacao_id = db.Column(db.Integer, db.ForeignKey('organizacoes.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('utilizadores.id'), nullable=False)
    data_inicio = db.Column(db.DateTime, default=datetime.utcnow)
    data_fim = db.Column(db.DateTime)
    status = db.Column(db.String(20), nullable=False, default='em_curso')
    score_global = db.Column(db.Float)
    nivel_global = db.Column(db.String(50))
    notas = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relações
    respostas = db.relationship('Resposta', backref='avaliacao', lazy=True)
    resultados_camada = db.relationship('ResultadoCamada', backref='avaliacao', lazy=True)
    interdependencias = db.relationship('Interdependencia', backref='avaliacao', lazy=True)
    conversas = db.relationship('ConversaIA', backref='avaliacao', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'organizacao_id': self.organizacao_id,
            'user_id': self.user_id,
            'organizacao': self.organizacao.to_dict() if self.organizacao else None,
            'data_inicio': self.data_inicio.isoformat() if self.data_inicio else None,
            'data_fim': self.data_fim.isoformat() if self.data_fim else None,
            'status': self.status,
            'score_global': self.score_global,
            'nivel_global': self.nivel_global,
            'notas': self.notas,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
