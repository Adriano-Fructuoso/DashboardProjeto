let procedureCount = 1;

function addProcedure() {
    procedureCount++;
    const procedureDiv = document.createElement('div');
    procedureDiv.setAttribute('id', `procedure${procedureCount}`);
    procedureDiv.innerHTML = `
        <p>
            <label for="procedimento${procedureCount}">Procedimento ${procedureCount}</label><br>
            <select name="procedimento${procedureCount}" id="procedimento${procedureCount}">
                {% for proc in form.procedimento1.choices %}
                    <option value="{{ proc[0] }}">{{ proc[1] }}</option>
                {% endfor %}
            </select>
        </p>
    `;
    document.getElementById('procedures').appendChild(procedureDiv);
    document.getElementById('procedureCount').value = procedureCount;
}

function removeProcedure() {
    if (procedureCount > 1) {
        const procedureDiv = document.getElementById(`procedure${procedureCount}`);
        document.getElementById('procedures').removeChild(procedureDiv);
        procedureCount--;
        document.getElementById('procedureCount').value = procedureCount;
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
