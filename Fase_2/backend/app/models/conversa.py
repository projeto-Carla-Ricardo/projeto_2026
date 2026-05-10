"""Modelo de Conversas IA e Relatórios."""
from app import db
from datetime import datetime


class ConversaIA(db.Model):
    __tablename__ = 'conversas_ia'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    avaliacao_id = db.Column(db.Integer, db.ForeignKey('avaliacoes.id'), nullable=False)
    papel = db.Column(db.String(20), nullable=False)  # 'user', 'assistant', 'system'
    mensagem = db.Column(db.Text, nullable=False)
    camada_id = db.Column(db.Integer, db.ForeignKey('camadas_ailo.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    camada = db.relationship('CamadaAilo', backref='conversas', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'avaliacao_id': self.avaliacao_id,
            'papel': self.papel,
            'mensagem': self.mensagem,
            'camada_id': self.camada_id,
            'camada_nome': self.camada.nome if self.camada else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Relatorio(db.Model):
    __tablename__ = 'relatorios'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    avaliacao_id = db.Column(db.Integer, db.ForeignKey('avaliacoes.id'), nullable=False, unique=True)
    titulo = db.Column(db.String(300), nullable=False)
    conteudo_json = db.Column(db.Text, nullable=False)
    pdf_path = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    avaliacao = db.relationship('Avaliacao', backref='relatorio', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'avaliacao_id': self.avaliacao_id,
            'titulo': self.titulo,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
