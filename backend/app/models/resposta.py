"""
Modelo: Resposta do utilizador a uma pergunta
Tabela: respostas
"""
from datetime import datetime, timezone
from app import db


class Resposta(db.Model):
    __tablename__ = 'respostas'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    avaliacao_id = db.Column(db.Integer, db.ForeignKey('avaliacoes.id'), nullable=False)
    pergunta_id = db.Column(db.Integer, db.ForeignKey('perguntas.id'), nullable=False)
    valor_texto = db.Column(db.Text)
    valor_numerico = db.Column(db.Float)
    valor_fuzzy = db.Column(db.Float)
    respondido_em = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    # Constraint: uma resposta por pergunta por avaliação
    __table_args__ = (
        db.UniqueConstraint('avaliacao_id', 'pergunta_id', name='uq_resposta_avaliacao_pergunta'),
    )

    def __repr__(self):
        return f'<Resposta aval={self.avaliacao_id} perg={self.pergunta_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'avaliacao_id': self.avaliacao_id,
            'pergunta_id': self.pergunta_id,
            'valor_texto': self.valor_texto,
            'valor_numerico': self.valor_numerico,
            'valor_fuzzy': self.valor_fuzzy,
            'respondido_em': self.respondido_em.isoformat() if self.respondido_em else None
        }
