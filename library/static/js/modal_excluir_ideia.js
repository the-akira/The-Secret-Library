document.querySelectorAll('#excluir-ideia').forEach(button => {
    button.addEventListener('click', function() {
        const ideiaId = this.getAttribute('data-ideia-id');
        exibirModalIdeia(ideiaId);
    });
});

function exibirModalIdeia(ideiaId) {
    const modal = document.getElementById('modalExcluirIdeia');
    const ideiaRemover = document.getElementById('ideiaRemover');
    ideiaRemover.innerHTML = ideiaId;
    modal.style.display = 'block';
    modal.setAttribute('data-ideia-id', ideiaId);
}

document.getElementById('confirmarExclusaoIdeia').addEventListener('click', function() {
    const ideiaId = document.getElementById('modalExcluirIdeia').getAttribute('data-ideia-id');
    window.location.href = `/ideia/${ideiaId}/excluir`;
});

window.addEventListener('click', function(event) {
    const modal = document.getElementById('modalExcluirIdeia');
    if (event.target == modal) {
        modal.style.display = 'none';
    }
});

document.querySelector('.closeIdeia').addEventListener('click', function() {
    const modal = document.getElementById('modalExcluirIdeia');
    modal.style.display = 'none';
});

const ideiasContainer = document.getElementById('ideias-container');

if (ideiasContainer) {
    ideiasContainer.addEventListener('click', function(event) {
        if (event.target.classList.contains('excluir-ideia')) {
            const ideiaId = event.target.getAttribute('data-ideia-id');
            exibirModalIdeia(ideiaId);
        }
    });
}