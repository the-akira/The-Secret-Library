document.querySelectorAll('#excluir-mensagem').forEach(button => {
    button.addEventListener('click', function() {
        const mensagemId = this.getAttribute('data-mensagem-id');
        const caixaSaida = this.getAttribute('data-caixa-saida');
        exibirModalMensagem(mensagemId, caixaSaida);
    });
});

function exibirModalMensagem(mensagemId, caixaSaida) {
    const modal = document.getElementById('modalExcluirMensagem');
    const mensagemRemover = document.getElementById('mensagemRemover');
    mensagemRemover.innerHTML = mensagemId;
    modal.style.display = 'block';
    modal.setAttribute('data-mensagem-id', mensagemId);
    modal.setAttribute('data-caixa-saida', caixaSaida);
}

document.getElementById('confirmarExclusaoMensagem').addEventListener('click', function() {
    const mensagemId = document.getElementById('modalExcluirMensagem').getAttribute('data-mensagem-id');
    const caixaSaida = document.getElementById('modalExcluirMensagem').getAttribute('data-caixa-saida');
    if (caixaSaida === "null") {
        window.location.href = `/mensagem/${mensagemId}/excluir`;
    } else if (caixaSaida === 'saida') {
        window.location.href = `/mensagem_saida/${mensagemId}/excluir`;
    }
});

window.addEventListener('click', function(event) {
    const modal = document.getElementById('modalExcluirMensagem');
    if (event.target == modal) {
        modal.style.display = 'none';
    }
});

document.querySelector('.closeMensagem').addEventListener('click', function() {
    const modal = document.getElementById('modalExcluirMensagem');
    modal.style.display = 'none';
});