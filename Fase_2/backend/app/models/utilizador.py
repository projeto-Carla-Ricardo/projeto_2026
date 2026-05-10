"""Modelo de Utilizador."""
from app import db
from datetime import datetime


class Utilizador(db.Model):
    __tablename__ = 'utilizadores'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    papel = db.Column(db.String(20), nullable=False, default='utilizador')
    ativo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relações
    organizacoes = db.relationship('Organizacao', backref='utilizador', lazy=True)
    avaliacoes = db.relationship('Avaliacao', backref='utilizador', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'papel': self.papel,
            'ativo': self.ativo,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
