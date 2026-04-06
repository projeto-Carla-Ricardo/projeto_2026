"""
Modelo: Dimensão do Framework IALO (dados de referência)
Tabela: dimensoes
"""
from app import db


class Dimensao(db.Model):
    __tablename__ = 'dimensoes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    codigo = db.Column(db.String(10), nullable=False, unique=True)
    nome = db.Column(db.String(50), nullable=False)
    descricao = db.Column(db.Text)
    peso = db.Column(db.Float, nullable=False)
    ordem = db.Column(db.Integer, nullable=False)

    # Relações
    indicadores = db.relationship('Indicador', backref='dimensao', lazy='dynamic',
                                  order_by='Indicador.ordem')
    resultados = db.relationship('ResultadoDimensao', backref='dimensao', lazy='dynamic')
    recomendacoes = db.relationship('Recomendacao', backref='dimensao', lazy='dynamic')

    def __repr__(self):
        return f'<Dimensao {self.codigo} - {self.nome}>'

    def to_dict(self):
        return {
            'id': self.id,
            'codigo': self.codigo,
            'nome': self.nome,
            'descricao': self.descricao,
            'peso': self.peso,
            'ordem': self.ordem
        }
