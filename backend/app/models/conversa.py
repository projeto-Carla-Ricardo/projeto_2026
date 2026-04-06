"""
Modelo: Conversa com Assistente IA
Tabela: conversas_ia
"""
from datetime import datetime, timezone
from app import db


class ConversaIA(db.Model):
    __tablename__ = 'conversas_ia'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    avaliacao_id = db.Column(db.Integer, db.ForeignKey('avaliacoes.id'), nullable=False, index=True)
    papel = db.Column(db.String(20), nullable=False)  # 'utilizador' ou 'assistente'
    mensagem = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<ConversaIA {self.papel}: {self.mensagem[:30]}>'

    def to_dict(self):
        return {
            'id': self.id,
            'avaliacao_id': self.avaliacao_id,
            'papel': self.papel,
            'mensagem': self.mensagem,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }
