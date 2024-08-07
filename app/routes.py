from flask import render_template, redirect, url_for, flash, request
from . import db
from .forms import AtendimentoForm, ProcedimentoForm, EstoqueForm
from .models import Atendimento, Procedimento, Estoque
from flask import current_app as app
from collections import defaultdict
from datetime import datetime
import json

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/atendimentos', methods=['GET', 'POST'])
def atendimentos():
    form = AtendimentoForm()
    materiais = Estoque.query.all()
    procedimentos = Procedimento.query.all()

    if form.validate_on_submit():
        try:
            procedimentos_list = []
            valor_total = 0.0
            procedure_count = int(request.form.get('procedureCount', 1))

            print("Procedures count:", procedure_count)  # Debugging line

            for i in range(1, procedure_count + 1):
                proc_nome = request.form.get(f'procedimento{i}')
                print(f"Procedimento {i}:", proc_nome)  # Debugging line
                if proc_nome:
                    procedimentos_list.append(proc_nome)
                    proc = Procedimento.query.filter_by(nome=proc_nome).first()
                    if proc:
                        valor_total += proc.valor

            materiais_utilizados = []
            material_count = int(request.form.get('materialCount', 1))

            print("Materials count:", material_count)  # Debugging line

            for i in range(1, material_count + 1):
                mat_nome = request.form.get(f'material{i}')
                print(f"Material {i}:", mat_nome)  # Debugging line
                if mat_nome:
                    materiais_utilizados.append(mat_nome)

            print("Form Data:", form.data_atendimento.data, form.nome_paciente.data, procedimentos_list, valor_total, materiais_utilizados, form.observacoes.data)  # Debugging line

            atendimento = Atendimento(
                data_atendimento=form.data_atendimento.data.strftime('%d/%m/%Y'),
                nome_paciente=form.nome_paciente.data,
                procedimentos=", ".join(procedimentos_list),
                valor_total=valor_total,
                materiais=", ".join(materiais_utilizados),
                observacoes=form.observacoes.data
            )
            db.session.add(atendimento)
            db.session.commit()
            flash('Atendimento adicionado com sucesso!')
            return redirect(url_for('atendimentos'))
        except Exception as e:
            print("Error occurred:", e)  # Debugging line
            flash('Erro ao adicionar atendimento!')
            db.session.rollback()
    else:
        print("Form validation failed", form.errors)  # Debugging line

    atendimentos_query = Atendimento.query
    filter_data = request.args.get('filter_data')
    filter_paciente = request.args.get('filter_paciente')
    filter_procedimento = request.args.get('filter_procedimento')

    if filter_data:
        atendimentos_query = atendimentos_query.filter(Atendimento.data_atendimento.like(f"%{filter_data}%"))
    if filter_paciente:
        atendimentos_query = atendimentos_query.filter(Atendimento.nome_paciente.like(f"%{filter_paciente}%"))
    if filter_procedimento:
        atendimentos_query = atendimentos_query.filter(Atendimento.procedimentos.like(f"%{filter_procedimento}%"))

    atendimentos = atendimentos_query.all()

    somatorio_mensal = {}
    for atendimento in atendimentos:
        data = datetime.strptime(atendimento.data_atendimento, '%d/%m/%Y')
        mes_ano = data.strftime('%m/%Y')
        if mes_ano in somatorio_mensal:
            somatorio_mensal[mes_ano] += atendimento.valor_total
        else:
            somatorio_mensal[mes_ano] = atendimento.valor_total

    pacientes = Atendimento.query.with_entities(Atendimento.nome_paciente).distinct().all()

    procedimentos_json = json.dumps([proc.nome for proc in procedimentos])
    materiais_json = json.dumps([mat.nome for mat in materiais])

    return render_template('atendimento/atendimentos.html', 
                           form=form, 
                           atendimentos=atendimentos, 
                           somatorio_mensal=somatorio_mensal, 
                           pacientes=pacientes,
                           procedimentos_json=procedimentos_json,
                           materiais_json=materiais_json)


def edit_atendimento(id):
    atendimento = Atendimento.query.get_or_404(id)
    form = AtendimentoForm(obj=atendimento)
    procedure_count = len(atendimento.procedimentos.split(', ')) if atendimento.procedimentos else 1
    
    if form.validate_on_submit():
        procedimentos = []
        valor_total = 0.0
        procedure_count = int(request.form.get('procedureCount', 1))

        for i in range(1, procedure_count + 1):
            proc_nome = request.form.get(f'procedimento{i}')
            if proc_nome:
                procedimentos.append(proc_nome)
                proc = Procedimento.query.filter_by(nome=proc_nome).first()
                if proc:
                    valor_total += proc.valor

        atendimento.data_atendimento = form.data_atendimento.data
        atendimento.nome_paciente = form.nome_paciente.data
        atendimento.procedimentos = ", ".join(procedimentos)
        atendimento.valor_total = valor_total
        atendimento.materiais = form.materiais.data
        atendimento.observacoes = form.observacoes.data
        db.session.commit()
        flash('Atendimento atualizado com sucesso!')
        return redirect(url_for('atendimentos'))

    return render_template('atendimento/edit_atendimento.html', form=form, atendimento=atendimento, procedure_count=procedure_count)

@app.route('/atendimentos/delete/<int:id>', methods=['POST'])
def delete_atendimento(id):
    atendimento = Atendimento.query.get_or_404(id)
    db.session.delete(atendimento)
    db.session.commit()
    flash('Atendimento removido com sucesso!')
    return redirect(url_for('atendimentos'))

@app.route('/configurar_procedimentos', methods=['GET', 'POST'])
def configurar_procedimentos():
    procedimentos = Procedimento.query.all()
    form = ProcedimentoForm()
    if form.validate_on_submit():
        procedimento = Procedimento(
            nome=form.nome.data,
            valor=form.valor.data,
            materiais=form.materiais.data
        )
        db.session.add(procedimento)
        db.session.commit()
        flash('Procedimento adicionado/atualizado com sucesso!')
        return redirect(url_for('configurar_procedimentos'))
    return render_template('procedimento/configurar_procedimentos.html', form=form, procedimentos=procedimentos)
@app.route('/procedimentos/edit/<int:id>', methods=['GET', 'POST'])
def edit_procedimento(id):
    procedimento = Procedimento.query.get_or_404(id)
    form = ProcedimentoForm(obj=procedimento)
    if form.validate_on_submit():
        procedimento.nome = form.nome.data
        procedimento.valor = form.valor.data
        procedimento.materiais = form.materiais.data
        db.session.commit()
        flash('Procedimento atualizado com sucesso!')
        return redirect(url_for('configurar_procedimentos'))
    return render_template('procedimento/edit_procedimentos.html', form=form, procedimento=procedimento)

@app.route('/procedimentos/delete/<int:id>', methods=['POST'])
def delete_procedimento(id):
    procedimento = Procedimento.query.get_or_404(id)
    db.session.delete(procedimento)
    db.session.commit()
    flash('Procedimento removido com sucesso!')
    return redirect(url_for('configurar_procedimentos'))


@app.route('/estoque', methods=['GET', 'POST'])
def estoque():
    form = EstoqueForm()
    if form.validate_on_submit():
        material = Estoque(
            nome=form.nome.data,
            categoria=form.categoria.data,
            quantidade=form.quantidade.data,
            unidade_medida=form.unidade_medida.data,
            data_compra=form.data_compra.data,
            valor_unitario=form.valor_unitario.data,
            fornecedor=form.fornecedor.data,
            data_validade=form.data_validade.data,
            observacoes=form.observacoes.data
        )
        db.session.add(material)
        db.session.commit()
        flash('Material adicionado ao estoque com sucesso!')
        return redirect(url_for('estoque'))
    materiais = Estoque.query.all()
    return render_template('estoque/estoque.html', form=form, materiais=materiais)

@app.route('/estoque/edit/<int:id>', methods=['GET', 'POST'])
def edit_estoque(id):
    material = Estoque.query.get_or_404(id)
    form = EstoqueForm(obj=material)
    if form.validate_on_submit():
        material.nome = form.nome.data
        material.categoria = form.categoria.data
        material.quantidade = form.quantidade.data
        material.unidade_medida = form.unidade_medida.data
        material.data_compra = form.data_compra.data
        material.valor_unitario = form.valor_unitario.data
        material.fornecedor = form.fornecedor.data
        material.data_validade = form.data_validade.data
        material.observacoes = form.observacoes.data
        db.session.commit()
        flash('Material atualizado com sucesso!')
        return redirect(url_for('estoque'))
    return render_template('estoque/edit_estoque.html', form=form, material=material)

@app.route('/estoque/delete/<int:id>', methods=['POST'])
def delete_estoque(id):
    material = Estoque.query.get_or_404(id)
    db.session.delete(material)
    db.session.commit()
    flash('Material removido do estoque com sucesso!')
    return redirect(url_for('estoque'))
