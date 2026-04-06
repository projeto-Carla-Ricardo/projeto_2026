"""
Modelo: Avaliação (Diagnóstico IALO)
Tabela: avaliacoes
"""
from datetime import datetime, timezone
from app import db


class Avaliacao(db.Model):
    __tablename__ = 'avaliacoes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresas.id'), nullable=False, index=True)
    estado = db.Column(db.String(20), nullable=False, default='em_curso', index=True)
    nivel_global = db.Column(db.Integer)
    pontuacao_global = db.Column(db.Float)
    iniciado_em = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    concluido_em = db.Column(db.DateTime)
    criado_em = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    # Relações
    respostas = db.relationship('Resposta', backref='avaliacao', lazy='dynamic',
                                cascade='all, delete-orphan')
    resultados = db.relationship('ResultadoDimensao', backref='avaliacao', lazy='dynamic',
                                 cascade='all, delete-orphan')
    relatorio = db.relationship('Relatorio', backref='avaliacao', uselist=False,
                                cascade='all, delete-orphan')
    conversas = db.relationship('ConversaIA', backref='avaliacao', lazy='dynamic',
                                cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Avaliacao {self.id} - {self.estado}>'

    def to_dict(self):
        return {
            'id': self.id,
            'empresa_id': self.empresa_id,
            'estado': self.estado,
            'nivel_global': self.nivel_global,
            'pontuacao_global': self.pontuacao_global,
            'iniciado_em': self.iniciado_em.isoformat() if self.iniciado_em else None,
            'concluido_em': self.concluido_em.isoformat() if self.concluido_em else None
        }
