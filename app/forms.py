from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, TextAreaField, SubmitField, IntegerField, DateField
from wtforms.validators import DataRequired, NumberRange
from .models import Procedimento, Estoque

class AtendimentoForm(FlaskForm):
    data_atendimento = StringField('Data do Atendimento', validators=[DataRequired()])
    nome_paciente = StringField('Nome do Paciente', validators=[DataRequired()])

    procedimentos = Procedimento.query.all()
    procedimento_choices = [(proc.nome, f"{proc.nome} - R$ {proc.valor:.2f}") for proc in procedimentos]

    procedimento1 = SelectField('Procedimento 1', choices=procedimento_choices, validators=[DataRequired()])
    materiais = StringField('Materiais Utilizados', validators=[DataRequired()])
    observacoes = TextAreaField('Observações')
    submit = SubmitField('Salvar')

class ProcedimentoForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    valor = FloatField('Valor', validators=[DataRequired()])
    
    # Puxar os materiais do estoque para a lista suspensa
    materiais = SelectField('Materiais', choices=[], coerce=int)
    submit = SubmitField('Salvar')
    
    def __init__(self, *args, **kwargs):
        super(ProcedimentoForm, self).__init__(*args, **kwargs)
        self.materiais.choices = [(material.id, material.nome) for material in Estoque.query.all()]
class EstoqueForm(FlaskForm):
    nome = StringField('Nome do Material', validators=[DataRequired()])
    categoria = StringField('Categoria', validators=[DataRequired()])
    quantidade = IntegerField('Quantidade', validators=[DataRequired(), NumberRange(min=0)])
    unidade_medida = StringField('Unidade de Medida', validators=[DataRequired()])
    data_compra = StringField('Data da Compra', validators=[DataRequired()])
    valor_unitario = FloatField('Valor Unitário', validators=[DataRequired()])
    fornecedor = StringField('Fornecedor', validators=[DataRequired()])
    data_validade = StringField('Data de Validade', validators=[DataRequired()])
    observacoes = TextAreaField('Observações')
    submit = SubmitField('Salvar')

