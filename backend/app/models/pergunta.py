"""
Modelo: Pergunta do Questionário IALO
Tabela: perguntas
"""
from app import db


class Pergunta(db.Model):
    __tablename__ = 'perguntas'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    indicador_id = db.Column(db.Integer, db.ForeignKey('indicadores.id'), nullable=False, index=True)
    texto = db.Column(db.Text, nullable=False)
    tipo_resposta = db.Column(db.String(30), nullable=False)  # escala_1_5, escolha_multipla, sim_nao, texto_livre
    opcoes_json = db.Column(db.Text)  # JSON string com opções para escolha múltipla
    ordem = db.Column(db.Integer, nullable=False)
    obrigatoria = db.Column(db.Boolean, nullable=False, default=True)
    ajuda_contextual = db.Column(db.Text)

    # Relações
    respostas = db.relationship('Resposta', backref='pergunta', lazy='dynamic')

    def __repr__(self):
        return f'<Pergunta {self.id} - {self.texto[:40]}>'

    def to_dict(self):
        import json
        opcoes = None
        if self.opcoes_json:
            try:
                opcoes = json.loads(self.opcoes_json)
            except (json.JSONDecodeError, TypeError):
                opcoes = self.opcoes_json
        return {
            'id': self.id,
            'indicador_id': self.indicador_id,
            'texto': self.texto,
            'tipo_resposta': self.tipo_resposta,
            'opcoes': opcoes,
            'ordem': self.ordem,
            'obrigatoria': self.obrigatoria,
            'ajuda_contextual': self.ajuda_contextual
        }
