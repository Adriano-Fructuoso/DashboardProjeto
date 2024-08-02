from flask import render_template, redirect, url_for, flash, request
from . import db
from .forms import AtendimentoForm, ProcedimentoForm, MaterialForm
from .models import Atendimento, Procedimento, Material
from flask import current_app as app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/atendimentos', methods=['GET', 'POST'])
def atendimentos():
    form = AtendimentoForm()
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

        atendimento = Atendimento(
            data_atendimento=form.data_atendimento.data,
            nome_paciente=form.nome_paciente.data,
            procedimentos=", ".join(procedimentos),
            valor_total=valor_total,
            materiais=form.materiais.data,
            observacoes=form.observacoes.data
        )
        db.session.add(atendimento)
        db.session.commit()
        flash('Atendimento adicionado com sucesso!')
        return redirect(url_for('atendimentos'))
    atendimentos = Atendimento.query.all()
    return render_template('atendimentos.html', form=form, atendimentos=atendimentos)

@app.route('/atendimentos/edit/<int:id>', methods=['GET', 'POST'])
def edit_atendimento(id):
    atendimento = Atendimento.query.get_or_404(id)
    form = AtendimentoForm(obj=atendimento)
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
    return render_template('edit_atendimento.html', form=form, atendimento=atendimento)

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
    return render_template('configurar_procedimentos.html', form=form, procedimentos=procedimentos)

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
    return render_template('edit_procedimento.html', form=form, procedimento=procedimento)

@app.route('/procedimentos/delete/<int:id>', methods=['POST'])
def delete_procedimento(id):
    procedimento = Procedimento.query.get_or_404(id)
    db.session.delete(procedimento)
    db.session.commit()
    flash('Procedimento removido com sucesso!')
    return redirect(url_for('configurar_procedimentos'))

@app.route('/materiais', methods=['GET', 'POST'])
def materiais():
    materiais = Material.query.all()
    form = MaterialForm()
    if form.validate_on_submit():
        material = Material(
            nome=form.nome.data,
            valor=form.valor.data,
            quantidade=form.quantidade.data,
            tipo=form.tipo.data
        )
        db.session.add(material)
        db.session.commit()
        flash('Material adicionado/atualizado com sucesso!')
        return redirect(url_for('materiais'))
    return render_template('materiais.html', form=form, materiais=materiais)

@app.route('/materiais/edit/<int:id>', methods=['GET', 'POST'])
def edit_material(id):
    material = Material.query.get_or_404(id)
    form = MaterialForm(obj=material)
    if form.validate_on_submit():
        material.nome = form.nome.data
        material.valor = form.valor.data
        material.quantidade = form.quantidade.data
        material.tipo = form.tipo.data
        db.session.commit()
        flash('Material atualizado com sucesso!')
        return redirect(url_for('materiais'))
    return render_template('edit_material.html', form=form, material=material)

@app.route('/materiais/delete/<int:id>', methods=['POST'])
def delete_material(id):
    material = Material.query.get_or_404(id)
    db.session.delete(material)
    db.session.commit()
    flash('Material removido com sucesso!')
    return redirect(url_for('materiais'))
