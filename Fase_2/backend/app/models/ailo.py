"""Modelos do Framework AILO — Camadas, Componentes, Indicadores."""
from app import db


class CamadaAilo(db.Model):
    __tablename__ = 'camadas_ailo'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    nome_en = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    peso = db.Column(db.Float, nullable=False, default=1.0)
    ordem = db.Column(db.Integer, nullable=False)
    cor = db.Column(db.String(20), default='#2E4057')
    icone = db.Column(db.String(50))

    # Relações
    componentes = db.relationship('Componente', backref='camada', lazy=True, order_by='Componente.ordem')

    def to_dict(self, include_componentes=False):
        data = {
            'id': self.id,
            'nome': self.nome,
            'nome_en': self.nome_en,
            'descricao': self.descricao,
            'peso': self.peso,
            'ordem': self.ordem,
            'cor': self.cor,
            'icone': self.icone
        }
        if include_componentes:
            data['componentes'] = [c.to_dict(include_indicadores=True) for c in self.componentes]
        return data


class Componente(db.Model):
    __tablename__ = 'componentes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    camada_id = db.Column(db.Integer, db.ForeignKey('camadas_ailo.id'), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    nome_en = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    peso = db.Column(db.Float, nullable=False, default=1.0)
    ordem = db.Column(db.Integer, nullable=False)

    # Relações
    indicadores = db.relationship('Indicador', backref='componente', lazy=True, order_by='Indicador.ordem')

    def to_dict(self, include_indicadores=False):
        data = {
            'id': self.id,
            'camada_id': self.camada_id,
            'nome': self.nome,
            'nome_en': self.nome_en,
            'descricao': self.descricao,
            'peso': self.peso,
            'ordem': self.ordem,
            'indicadores_count': len(self.indicadores)
        }
        if include_indicadores:
            data['indicadores'] = [i.to_dict() for i in self.indicadores]
        return data


class Indicador(db.Model):
    __tablename__ = 'indicadores'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    componente_id = db.Column(db.Integer, db.ForeignKey('componentes.id'), nullable=False)
    codigo = db.Column(db.String(20), nullable=False, unique=True)
    pergunta = db.Column(db.Text, nullable=False)
    descricao = db.Column(db.Text)
    desc_nivel_1 = db.Column(db.Text, nullable=False)
    desc_nivel_2 = db.Column(db.Text)
    desc_nivel_3 = db.Column(db.Text, nullable=False)
    desc_nivel_4 = db.Column(db.Text)
    desc_nivel_5 = db.Column(db.Text, nullable=False)
    peso = db.Column(db.Float, nullable=False, default=1.0)
    obrigatorio = db.Column(db.Boolean, default=True)
    condicao = db.Column(db.Text)
    ordem = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'componente_id': self.componente_id,
            'codigo': self.codigo,
            'pergunta': self.pergunta,
            'descricao': self.descricao,
            'desc_nivel_1': self.desc_nivel_1,
            'desc_nivel_2': self.desc_nivel_2,
            'desc_nivel_3': self.desc_nivel_3,
            'desc_nivel_4': self.desc_nivel_4,
            'desc_nivel_5': self.desc_nivel_5,
            'peso': self.peso,
            'obrigatorio': self.obrigatorio,
            'condicao': self.condicao,
            'ordem': self.ordem
        }
