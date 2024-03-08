document.querySelectorAll('#excluir-comentario').forEach(button => {
    button.addEventListener('click', function() {
        const livroId = this.getAttribute('data-livro-id');
        const comentarioId = this.getAttribute('data-comentario-id');
        exibirModalComentario(livroId, comentarioId);
    });
});

function exibirModalComentario(livroId, comentarioId) {
    const modal = document.getElementById('modalExcluirComentario');
    const comentarioRemover = document.getElementById('comentarioRemover');
    comentarioRemover.innerHTML = comentarioId;
    modal.style.display = 'block';
    modal.setAttribute('data-livro-id', livroId);
    modal.setAttribute('data-comentario-id', comentarioId);
}

document.getElementById('confirmarExclusaoComentario').addEventListener('click', function() {
    const livroId = document.getElementById('modalExcluirComentario').getAttribute('data-livro-id');
    const comentarioId = document.getElementById('modalExcluirComentario').getAttribute('data-comentario-id');
    window.location.href = `/comentario/${comentarioId}/${livroId}/excluir`;
});

window.addEventListener('click', function(event) {
    const modal = document.getElementById('modalExcluirComentario');
    if (event.target == modal) {
        modal.style.display = 'none';
    }
});

document.querySelector('.closeComentario').addEventListener('click', function() {
    const modal = document.getElementById('modalExcluirComentario');
    modal.style.display = 'none';
});

const comentariosContainer = document.getElementById('comentarios-container');

if (comentariosContainer) {
    comentariosContainer.addEventListener('click', function(event) {
        if (event.target.classList.contains('excluir-comentario')) {
            const livroId = event.target.getAttribute('data-livro-id');
            const comentarioId = event.target.getAttribute('data-comentario-id');
            exibirModalComentario(livroId, comentarioId);
        }
    });
}