let telas = document.querySelectorAll('.tela');
let currentIndex = 0;

// Mostra a tela ativa
function showTela(index) {
    telas.forEach((tela, i) => {
        tela.classList.toggle('active', i === index);
    });
}

// Inicializa mostrando a primeira tela
showTela(currentIndex);

// Botões de navegação
document.getElementById('prev').addEventListener('click', () => {
    currentIndex = (currentIndex - 1 + telas.length) % telas.length;
    showTela(currentIndex);
});

document.getElementById('next').addEventListener('click', () => {
    currentIndex = (currentIndex + 1) % telas.length;
    showTela(currentIndex);
});

// Corações flutuantes
function criarCoracao() {
    let telaAtiva = document.querySelector('.tela.active .coracoes');
    if (!telaAtiva) return;

    let coracao = document.createElement('div');
    coracao.textContent = '❤️';
    coracao.style.position = 'absolute';
    coracao.style.left = Math.random() * 100 + '%';
    coracao.style.top = '100%';
    coracao.style.fontSize = Math.random() * 24 + 12 + 'px';
    coracao.style.opacity = Math.random();
    telaAtiva.appendChild(coracao);

    let anim = setInterval(() => {
        let top = parseFloat(coracao.style.top);
        if (top < -10) {
            coracao.remove();
            clearInterval(anim);
        } else {
            coracao.style.top = top - 2 + '%';
        }
    }, 30);
}

// Cria corações a cada 500ms
setInterval(criarCoracao, 500);