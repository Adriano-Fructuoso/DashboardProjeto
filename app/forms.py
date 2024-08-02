from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, TextAreaField, SubmitField, IntegerField  # Adicionada a importação de IntegerField
from wtforms.validators import DataRequired
from .models import Procedimento

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
    nome = StringField('Nome do Procedimento', validators=[DataRequired()])
    valor = FloatField('Valor', validators=[DataRequired()])
    materiais = StringField('Materiais Utilizados', validators=[DataRequired()])
    submit = SubmitField('Salvar')

class MaterialForm(FlaskForm):
    nome = StringField('Nome do Material', validators=[DataRequired()])
    valor = FloatField('Valor de Compra', validators=[DataRequired()])
    quantidade = IntegerField('Quantidade', validators=[DataRequired()])  # Campo de quantidade adicionado
    tipo = SelectField('Tipo', choices=[('Tipo1', 'Tipo 1'), ('Tipo2', 'Tipo 2')], validators=[DataRequired()])  # Campo de tipo adicionado
    submit = SubmitField('Salvar')
