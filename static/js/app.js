/* Comportamentos gerais do front-end (serão ampliados na Fase 5). */
document.addEventListener('DOMContentLoaded', function () {
    // Esconde automaticamente as mensagens do Django após alguns segundos.
    const mensagens = document.querySelectorAll('.mensagem');
    mensagens.forEach(function (mensagem) {
        setTimeout(function () {
            mensagem.style.transition = 'opacity 0.5s';
            mensagem.style.opacity = '0';
            setTimeout(function () {
                mensagem.remove();
            }, 500);
        }, 5000);
    });
});
