"""Modelo de Organização."""
from app import db
from datetime import datetime


class Organizacao(db.Model):
    __tablename__ = 'organizacoes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('utilizadores.id'), nullable=False)
    nome = db.Column(db.String(200), nullable=False)
    setor = db.Column(db.String(100), nullable=False)
    dimensao = db.Column(db.String(50), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    pais = db.Column(db.String(100), default='Portugal')
    descricao = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relações
    avaliacoes = db.relationship('Avaliacao', backref='organizacao', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'nome': self.nome,
            'setor': self.setor,
            'dimensao': self.dimensao,
            'tipo': self.tipo,
            'pais': self.pais,
            'descricao': self.descricao,
            'avaliacoes_count': len(self.avaliacoes) if self.avaliacoes else 0,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
