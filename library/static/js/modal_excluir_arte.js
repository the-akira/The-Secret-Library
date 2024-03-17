document.querySelectorAll('#excluir-arte').forEach(button => {
    button.addEventListener('click', function() {
        const arteId = this.getAttribute('data-arte-id');
        const arteTitulo = this.getAttribute('data-arte-titulo');
        exibirModalArte(arteId, arteTitulo);
    });
});

function exibirModalArte(arteId, arteTitulo) {
    const modal = document.getElementById('modalExcluirArte');
    const arteRemover = document.getElementById('arteRemover');
    arteRemover.innerHTML = arteTitulo;
    modal.style.display = 'block';
    modal.setAttribute('data-arte-id', arteId);
}

document.getElementById('confirmarExclusaoArte').addEventListener('click', function() {
    const arteId = document.getElementById('modalExcluirArte').getAttribute('data-arte-id');
    window.location.href = `/arte/${arteId}/excluir`;
});

window.addEventListener('click', function(event) {
    const modal = document.getElementById('modalExcluirArte');
    if (event.target == modal) {
        modal.style.display = 'none';
    }
});

document.querySelector('.closeArte').addEventListener('click', function() {
    const modal = document.getElementById('modalExcluirArte');
    modal.style.display = 'none';
});

const artesContainer = document.getElementById('artes-container');

if (artesContainer) {
    artesContainer.addEventListener('click', function(event) {
        if (event.target.classList.contains('excluir-arte')) {
            const arteId = event.target.getAttribute('data-arte-id');
            const arteTitulo = event.target.getAttribute('data-arte-titulo');
            exibirModalArte(arteId, arteTitulo);
        }
    });
}