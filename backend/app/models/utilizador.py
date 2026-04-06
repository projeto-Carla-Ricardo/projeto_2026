"""
Modelo: Utilizador
Tabela: utilizadores
"""
from datetime import datetime, timezone
from app import db


class Utilizador(db.Model):
    __tablename__ = 'utilizadores'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='empresario')
    criado_em = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    atualizado_em = db.Column(db.DateTime, onupdate=lambda: datetime.now(timezone.utc))
    ativo = db.Column(db.Boolean, nullable=False, default=True)

    # Relações
    empresas = db.relationship('Empresa', backref='proprietario', lazy='dynamic',
                               cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Utilizador {self.email}>'

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'role': self.role,
            'criado_em': self.criado_em.isoformat() if self.criado_em else None,
            'ativo': self.ativo
        }
