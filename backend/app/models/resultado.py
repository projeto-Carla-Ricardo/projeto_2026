"""
Modelo: Resultado por Dimensão
Tabela: resultados_dimensao
"""
from app import db


class ResultadoDimensao(db.Model):
    __tablename__ = 'resultados_dimensao'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    avaliacao_id = db.Column(db.Integer, db.ForeignKey('avaliacoes.id'), nullable=False)
    dimensao_id = db.Column(db.Integer, db.ForeignKey('dimensoes.id'), nullable=False)
    pontuacao = db.Column(db.Float, nullable=False)   # 0-100%
    nivel = db.Column(db.Integer, nullable=False)      # 1-5
    gap_critico = db.Column(db.Boolean, nullable=False, default=False)

    # Constraint: um resultado por dimensão por avaliação
    __table_args__ = (
        db.UniqueConstraint('avaliacao_id', 'dimensao_id', name='uq_resultado_avaliacao_dimensao'),
    )

    def __repr__(self):
        return f'<Resultado aval={self.avaliacao_id} dim={self.dimensao_id} pont={self.pontuacao}%>'

    def to_dict(self):
        return {
            'id': self.id,
            'avaliacao_id': self.avaliacao_id,
            'dimensao_id': self.dimensao_id,
            'pontuacao': self.pontuacao,
            'nivel': self.nivel,
            'gap_critico': self.gap_critico
        }
