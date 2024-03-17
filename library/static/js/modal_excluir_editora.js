document.querySelectorAll('#excluir-editora').forEach(button => {
    button.addEventListener('click', function() {
        const editoraId = this.getAttribute('data-editora-id');
        const editoraNome = this.getAttribute('data-editora-nome');
        exibirModalEditora(editoraId, editoraNome);
    });
});

function exibirModalEditora(editoraId, editoraNome) {
    const modal = document.getElementById('modalExcluirEditora');
    const editoraRemover = document.getElementById('editoraRemover');
    editoraRemover.innerHTML = editoraNome;
    modal.style.display = 'block';
    modal.setAttribute('data-editora-id', editoraId);
}

document.getElementById('confirmarExclusaoEditora').addEventListener('click', function() {
    const editoraId = document.getElementById('modalExcluirEditora').getAttribute('data-editora-id');
    window.location.href = `/editora/${editoraId}/excluir`;
});

window.addEventListener('click', function(event) {
    const modal = document.getElementById('modalExcluirEditora');
    if (event.target == modal) {
        modal.style.display = 'none';
    }
});

document.querySelector('.closeEditora').addEventListener('click', function() {
    const modal = document.getElementById('modalExcluirEditora');
    modal.style.display = 'none';
});

const editorasContainer = document.getElementById('editoras-container');

if (editorasContainer) {
    editorasContainer.addEventListener('click', function(event) {
        if (event.target.classList.contains('excluir-editora')) {
            const editoraId = event.target.getAttribute('data-editora-id');
            const editoraNome = event.target.getAttribute('data-editora-nome');
            exibirModalEditora(editoraId, editoraNome);
        }
    });
}