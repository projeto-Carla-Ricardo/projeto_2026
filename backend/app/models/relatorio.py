"""
Modelo: Relatório gerado
Tabela: relatorios
"""
from datetime import datetime, timezone
from app import db


class Relatorio(db.Model):
    __tablename__ = 'relatorios'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    avaliacao_id = db.Column(db.Integer, db.ForeignKey('avaliacoes.id'), nullable=False, unique=True)
    conteudo_json = db.Column(db.Text)
    pontos_fortes = db.Column(db.Text)
    necessidades = db.Column(db.Text)
    recomendacoes_texto = db.Column(db.Text)
    caminho_pdf = db.Column(db.String(500))
    gerado_em = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    # Relações
    recomendacoes = db.relationship('Recomendacao', backref='relatorio', lazy='dynamic',
                                    cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Relatorio aval={self.avaliacao_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'avaliacao_id': self.avaliacao_id,
            'pontos_fortes': self.pontos_fortes,
            'necessidades': self.necessidades,
            'recomendacoes_texto': self.recomendacoes_texto,
            'caminho_pdf': self.caminho_pdf,
            'gerado_em': self.gerado_em.isoformat() if self.gerado_em else None
        }
