document.querySelectorAll('#excluir-autor').forEach(button => {
    button.addEventListener('click', function() {
        const autorId = this.getAttribute('data-autor-id');
        const autorNome = this.getAttribute('data-autor-nome');
        exibirModalAutor(autorId, autorNome);
    });
});

function exibirModalAutor(autorId, autorNome) {
    const modal = document.getElementById('modalExcluirAutor');
    const autorRemover = document.getElementById('autorRemover');
    autorRemover.innerHTML = autorNome;
    modal.style.display = 'block';
    modal.setAttribute('data-autor-id', autorId);
}

document.getElementById('confirmarExclusaoAutor').addEventListener('click', function() {
    const autorId = document.getElementById('modalExcluirAutor').getAttribute('data-autor-id');
    window.location.href = `/autor/${autorId}/excluir`;
});

window.addEventListener('click', function(event) {
    const modal = document.getElementById('modalExcluirAutor');
    if (event.target == modal) {
        modal.style.display = 'none';
    }
});

document.querySelector('.close').addEventListener('click', function() {
    const modal = document.getElementById('modalExcluirAutor');
    modal.style.display = 'none';
});

const autoresContainer = document.getElementById('autores-container');

if (autoresContainer) {
    autoresContainer.addEventListener('click', function(event) {
        if (event.target.classList.contains('excluir-autor')) {
            const autorId = event.target.getAttribute('data-autor-id');
            const autorNome = event.target.getAttribute('data-autor-nome');
            exibirModalAutor(autorId, autorNome);
        }
    });
}