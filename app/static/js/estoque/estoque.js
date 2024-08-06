/* static/js/estoque/estoque.js */
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
