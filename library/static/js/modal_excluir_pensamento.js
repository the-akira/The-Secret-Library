document.querySelectorAll('#excluir-pensamento').forEach(button => {
    button.addEventListener('click', function() {
        const autorId = this.getAttribute('data-autor-id');
        const pensamentoId = this.getAttribute('data-pensamento-id');
        exibirModalPensamento(autorId, pensamentoId);
    });
});

function exibirModalPensamento(autorId, pensamentoId) {
    const modal = document.getElementById('modalExcluirPensamento');
    const pensamentoRemover = document.getElementById('pensamentoRemover');
    pensamentoRemover.innerHTML = pensamentoId;
    modal.style.display = 'block';
    modal.setAttribute('data-autor-id', autorId);
    modal.setAttribute('data-pensamento-id', pensamentoId);
}

document.getElementById('confirmarExclusaoPensamento').addEventListener('click', function() {
    const autorId = document.getElementById('modalExcluirPensamento').getAttribute('data-autor-id');
    const pensamentoId = document.getElementById('modalExcluirPensamento').getAttribute('data-pensamento-id');
    window.location.href = `/pensamento/${pensamentoId}/${autorId}/excluir`;
});

window.addEventListener('click', function(event) {
    const modal = document.getElementById('modalExcluirPensamento');
    if (event.target == modal) {
        modal.style.display = 'none';
    }
});

document.querySelector('.closePensamento').addEventListener('click', function() {
    const modal = document.getElementById('modalExcluirPensamento');
    modal.style.display = 'none';
});

const pensamentosContainer = document.getElementById('pensamentos-container');

if (pensamentosContainer) {
    pensamentosContainer.addEventListener('click', function(event) {
        if (event.target.classList.contains('excluir-pensamento')) {
            const autorId = event.target.getAttribute('data-autor-id');
            const pensamentoId = event.target.getAttribute('data-pensamento-id');
            exibirModalPensamento(autorId, pensamentoId);
        }
    });
}