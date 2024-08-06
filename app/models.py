from app import db

class Atendimento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data_atendimento = db.Column(db.String(10))
    nome_paciente = db.Column(db.String(64))
    procedimentos = db.Column(db.String(256))  # Armazena uma lista de procedimentos
    valor_total = db.Column(db.Float)
    materiais = db.Column(db.String(256))
    observacoes = db.Column(db.String(256))

class Procedimento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    materiais = db.Column(db.Integer, db.ForeignKey('estoque.id'), nullable=False)  # Supondo que estoque.id � a chave prim�ria

class Estoque(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(64), nullable=False)
    categoria = db.Column(db.String(64), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    unidade_medida = db.Column(db.String(32), nullable=False)
    data_compra = db.Column(db.String(10), nullable=False)
    valor_unitario = db.Column(db.Float, nullable=False)
    fornecedor = db.Column(db.String(64), nullable=False)
    data_validade = db.Column(db.String(10), nullable=False)
    observacoes = db.Column(db.Text, nullable=True)

