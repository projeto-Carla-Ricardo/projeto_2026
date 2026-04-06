"""
Modelo: Empresa
Tabela: empresas
"""
from datetime import datetime, timezone
from app import db


class Empresa(db.Model):
    __tablename__ = 'empresas'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    utilizador_id = db.Column(db.Integer, db.ForeignKey('utilizadores.id'), nullable=False, index=True)
    nome = db.Column(db.String(200), nullable=False)
    setor = db.Column(db.String(100), nullable=False)
    num_colaboradores = db.Column(db.Integer)
    localizacao = db.Column(db.String(200))
    ano_fundacao = db.Column(db.Integer)
    descricao = db.Column(db.Text)
    criado_em = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    atualizado_em = db.Column(db.DateTime, onupdate=lambda: datetime.now(timezone.utc))
    ativo = db.Column(db.Boolean, nullable=False, default=True)

    # Relações
    avaliacoes = db.relationship('Avaliacao', backref='empresa', lazy='dynamic',
                                 cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Empresa {self.nome}>'

    def to_dict(self):
        return {
            'id': self.id,
            'utilizador_id': self.utilizador_id,
            'nome': self.nome,
            'setor': self.setor,
            'num_colaboradores': self.num_colaboradores,
            'localizacao': self.localizacao,
            'ano_fundacao': self.ano_fundacao,
            'descricao': self.descricao,
            'criado_em': self.criado_em.isoformat() if self.criado_em else None,
            'ativo': self.ativo
        }
