"""
Modelo: Indicador de uma Dimensão IALO
Tabela: indicadores
"""
from app import db


class Indicador(db.Model):
    __tablename__ = 'indicadores'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dimensao_id = db.Column(db.Integer, db.ForeignKey('dimensoes.id'), nullable=False, index=True)
    codigo = db.Column(db.String(10), nullable=False, unique=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    ordem = db.Column(db.Integer, nullable=False)

    # Relações
    perguntas = db.relationship('Pergunta', backref='indicador', lazy='dynamic',
                                order_by='Pergunta.ordem')

    def __repr__(self):
        return f'<Indicador {self.codigo} - {self.nome}>'

    def to_dict(self):
        return {
            'id': self.id,
            'dimensao_id': self.dimensao_id,
            'codigo': self.codigo,
            'nome': self.nome,
            'descricao': self.descricao,
            'ordem': self.ordem
        }
