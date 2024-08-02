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
    nome = db.Column(db.String(64), unique=True, nullable=False)
    valor = db.Column(db.Float, nullable=False)
    materiais = db.Column(db.String(256))  # Adicionar o campo materiais

class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(64), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)  # Campo de quantidade adicionado
    tipo = db.Column(db.String(64), nullable=False)  # Campo de tipo adicionado
