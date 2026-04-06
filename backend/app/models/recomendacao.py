"""
Modelo: Recomendação (ferramenta sugerida num relatório)
Tabela: recomendacoes
"""
from app import db


class Recomendacao(db.Model):
    __tablename__ = 'recomendacoes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    relatorio_id = db.Column(db.Integer, db.ForeignKey('relatorios.id'), nullable=False)
    ferramenta_id = db.Column(db.Integer, db.ForeignKey('ferramentas_ia.id'))  # pode ser NULL
    dimensao_id = db.Column(db.Integer, db.ForeignKey('dimensoes.id'))
    justificacao = db.Column(db.Text, nullable=False)
    prioridade = db.Column(db.Integer, nullable=False)  # 1 = mais prioritária

    def __repr__(self):
        return f'<Recomendacao rel={self.relatorio_id} prio={self.prioridade}>'

    def to_dict(self):
        return {
            'id': self.id,
            'relatorio_id': self.relatorio_id,
            'ferramenta_id': self.ferramenta_id,
            'dimensao_id': self.dimensao_id,
            'justificacao': self.justificacao,
            'prioridade': self.prioridade
        }
