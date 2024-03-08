document.querySelectorAll('#excluir-livro').forEach(button => {
    button.addEventListener('click', function() {
        const livroId = this.getAttribute('data-livro-id');
        const livroTitulo = this.getAttribute('data-livro-titulo');
        exibirModal(livroId, livroTitulo);
    });
});

function exibirModal(livroId, livroTitulo) {
    const modal = document.getElementById('modalExcluirLivro');
    const livroRemover = document.getElementById('livroRemover');
    livroRemover.innerHTML = livroTitulo;
    modal.style.display = 'block';
    modal.setAttribute('data-livro-id', livroId);
}

document.getElementById('confirmarExclusaoLivro').addEventListener('click', function() {
    const livroId = document.getElementById('modalExcluirLivro').getAttribute('data-livro-id');
    window.location.href = `/livro/${livroId}/excluir`;
});

window.addEventListener('click', function(event) {
    const modal = document.getElementById('modalExcluirLivro');
    if (event.target == modal) {
        modal.style.display = 'none';
    }
});

document.querySelector('.closeLivro').addEventListener('click', function() {
    const modal = document.getElementById('modalExcluirLivro');
    modal.style.display = 'none';
});

const livrosContainer = document.getElementById('livros-container');

if (livrosContainer) {
    livrosContainer.addEventListener('click', function(event) {
        if (event.target.classList.contains('excluir-livro')) {
            const livroId = event.target.getAttribute('data-livro-id');
            const livroTitulo = event.target.getAttribute('data-livro-titulo');
            exibirModal(livroId, livroTitulo);
        }
    });
}