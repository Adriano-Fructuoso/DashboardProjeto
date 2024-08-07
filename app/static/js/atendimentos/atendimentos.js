let procedureCount = 1;
let materialCount = 1;

function createProcedureSelect(id, items) {
    return `
        <p>
            <label for="${id}">Procedimento ${id.match(/\d+/)[0]}</label><br>
            <select name="${id}" id="${id}">
                ${items.map(item => `<option value="${item}">${item}</option>`).join('')}
            </select>
        </p>
    `;
}

function createMaterialSelect(id, items) {
    return `
        <p>
            <label for="${id}">Material ${id.match(/\d+/)[0]}</label><br>
            <select name="${id}" id="${id}">
                ${items.map(item => `<option value="${item}">${item}</option>`).join('')}
            </select>
        </p>
        <p>
            <label for="quantidade${id.match(/\d+/)[0]}">Quantidade ${id.match(/\d+/)[0]}</label><br>
            <input type="number" name="quantidade${id.match(/\d+/)[0]}" id="quantidade${id.match(/\d+/)[0]}" value="1">
        </p>
    `;
}

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('addProcedureBtn').addEventListener('click', addProcedure);
    document.getElementById('removeProcedureBtn').addEventListener('click', removeProcedure);
    document.getElementById('addMaterialBtn').addEventListener('click', addMaterial);
    document.getElementById('removeMaterialBtn').addEventListener('click', removeMaterial);
    document.querySelectorAll('.format-date').forEach(function (element) {
        element.addEventListener('input', function () { formatDate(element); });
    });
    document.querySelectorAll('.format-filter-date').forEach(function (element) {
        element.addEventListener('input', function () { formatDate(element); });
    });
});

function addProcedure() {
    procedureCount++;
    const procedureDiv = document.createElement('div');
    procedureDiv.setAttribute('id', `procedimento${procedureCount}`);
    procedureDiv.innerHTML = createProcedureSelect(`procedimento${procedureCount}`, window.procedimentos);
    document.getElementById('procedures').appendChild(procedureDiv);
    document.getElementById('procedureCount').value = procedureCount;
}

function removeProcedure() {
    if (procedureCount > 1) {
        const procedureDiv = document.getElementById(`procedimento${procedureCount}`);
        document.getElementById('procedures').removeChild(procedureDiv);
        procedureCount--;
        document.getElementById('procedureCount').value = procedureCount;
    }
}

function addMaterial() {
    materialCount++;
    const materialDiv = document.createElement('div');
    materialDiv.setAttribute('id', `material${materialCount}`);
    materialDiv.innerHTML = createMaterialSelect(`material${materialCount}`, window.materiais);
    document.getElementById('materials').appendChild(materialDiv);
    document.getElementById('materialCount').value = materialCount;
}

function removeMaterial() {
    if (materialCount > 1) {
        const materialDiv = document.getElementById(`material${materialCount}`);
        document.getElementById('materials').removeChild(materialDiv);
        materialCount--;
        document.getElementById('materialCount').value = materialCount;
    }
}

function formatDate(input) {
    const value = input.value.replace(/\D/g, '');
    let formatted = '';

    if (value.length > 0) {
        formatted += value.substring(0, 2);
    }
    if (value.length > 2) {
        formatted += '/' + value.substring(2, 4);
    }
    if (value.length > 4) {
        formatted += '/' + value.substring(4, 8);
    }

    input.value = formatted;
}
