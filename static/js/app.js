/* Comportamentos do front-end do Sistema de Biblioteca (JS puro, sem bibliotecas). */
(function () {
    'use strict';

    const MOVIMENTO_REDUZIDO = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    /**
     * Normaliza texto para a busca: minúsculas e sem acentos.
     */
    function normalizar(texto) {
        return (texto || '')
            .toString()
            .toLowerCase()
            .normalize('NFD')
            .replace(/[̀-ͯ]/g, '');
    }

    /**
     * Menu: hambúrguer em telas pequenas e submenus (Acervo/Pessoas/Circulação).
     */
    function iniciarMenu() {
        const botaoMenu = document.querySelector('.menu-abrir');
        const menu = document.getElementById('menu-principal');

        if (botaoMenu && menu) {
            botaoMenu.addEventListener('click', function () {
                const aberto = menu.classList.toggle('menu-aberto');
                botaoMenu.classList.toggle('ativo', aberto);
                botaoMenu.setAttribute('aria-expanded', aberto ? 'true' : 'false');
                botaoMenu.setAttribute('aria-label', aberto ? 'Fechar menu' : 'Abrir menu');
            });

            // No celular, o menu lateral fecha ao tocar fora dele ou com Esc.
            function fecharLateral() {
                if (!menu.classList.contains('menu-aberto')) {
                    return;
                }
                menu.classList.remove('menu-aberto');
                botaoMenu.classList.remove('ativo');
                botaoMenu.setAttribute('aria-expanded', 'false');
                botaoMenu.setAttribute('aria-label', 'Abrir menu');
            }
            document.addEventListener('click', function (evento) {
                if (!menu.contains(evento.target) && !botaoMenu.contains(evento.target)) {
                    fecharLateral();
                }
            });
            document.addEventListener('keydown', function (evento) {
                if (evento.key === 'Escape') {
                    fecharLateral();
                }
            });
        }

        document.querySelectorAll('.menu-botao').forEach(function (botao) {
            botao.addEventListener('click', function (evento) {
                evento.preventDefault();
                const grupo = botao.closest('.menu-grupo');
                const abrir = !grupo.classList.contains('aberto');
                // Fecha os demais grupos antes de abrir o escolhido.
                document.querySelectorAll('.menu-grupo.aberto').forEach(function (outro) {
                    if (outro !== grupo) {
                        outro.classList.remove('aberto');
                        outro.querySelector('.menu-botao').setAttribute('aria-expanded', 'false');
                    }
                });
                grupo.classList.toggle('aberto', abrir);
                botao.setAttribute('aria-expanded', abrir ? 'true' : 'false');
            });
        });

        // Fecha os submenus ao clicar fora do menu ou ao apertar Esc.
        document.addEventListener('click', function (evento) {
            if (!evento.target.closest('.menu-grupo')) {
                fecharSubmenus();
            }
        });
        document.addEventListener('keydown', function (evento) {
            if (evento.key === 'Escape') {
                fecharSubmenus();
            }
        });

        function fecharSubmenus() {
            document.querySelectorAll('.menu-grupo.aberto').forEach(function (grupo) {
                grupo.classList.remove('aberto');
                grupo.querySelector('.menu-botao').setAttribute('aria-expanded', 'false');
            });
        }
    }

    /**
     * Cabeçalho ganha sombra quando a página é rolada.
     */
    function iniciarCabecalho() {
        const cabecalho = document.getElementById('cabecalho');
        if (!cabecalho) {
            return;
        }
        function atualizar() {
            cabecalho.classList.toggle('rolado', window.scrollY > 8);
        }
        window.addEventListener('scroll', atualizar, { passive: true });
        atualizar();
    }

    /**
     * Busca instantânea: filtra as linhas de tabela ou os cards da listagem.
     * A caixa é <input data-busca>, e cada lista <table data-busca-lista> ou
     * <section data-busca-lista>, refletindo o total em [data-busca-contagem].
     */
    function iniciarBusca() {
        document.querySelectorAll('[data-busca]').forEach(function (campo) {
            const lista = document.querySelector(campo.dataset.buscaAlvo);
            if (!lista) {
                return;
            }
            const contagem = document.querySelector('[data-busca-contagem]');
            const itens = lista.querySelectorAll('tbody tr, .card');
            const rotulos = document.querySelectorAll('[data-busca-vazio]');

            function filtrar() {
                const termo = normalizar(campo.value.trim());
                let visiveis = 0;
                itens.forEach(function (item) {
                    const corresponde = normalizar(item.textContent).indexOf(termo) !== -1;
                    item.hidden = !corresponde;
                    if (corresponde) {
                        visiveis += 1;
                    }
                });
                rotulos.forEach(function (rotulo) {
                    rotulo.hidden = visiveis > 0;
                    if (!rotulo.hidden) {
                        rotulo.textContent = 'Nenhum resultado para "' + campo.value.trim() + '".';
                    }
                });
                if (contagem) {
                    contagem.textContent = visiveis + ' de ' + itens.length;
                }
            }

            campo.addEventListener('input', filtrar);
            campo.addEventListener('keydown', function (evento) {
                if (evento.key === 'Escape') {
                    campo.value = '';
                    filtrar();
                }
            });
            filtrar();
        });
    }

    /**
     * Preview da imagem antes do upload: <input type="file" data-preview="#alvo">.
     */
    function iniciarPreview() {
        document.querySelectorAll('input[type="file"][data-preview]').forEach(function (campo) {
            const alvo = document.querySelector(campo.dataset.preview);
            if (!alvo) {
                return;
            }
            campo.addEventListener('change', function () {
                const arquivo = campo.files && campo.files[0];
                if (!arquivo || !arquivo.type.startsWith('image/')) {
                    alvo.removeAttribute('src');
                    alvo.classList.add('oculto');
                    return;
                }
                const leitor = new FileReader();
                leitor.addEventListener('load', function () {
                    alvo.src = leitor.result;
                    alvo.classList.remove('oculto');
                });
                leitor.readAsDataURL(arquivo);
            });
        });
    }

    /**
     * Máscaras de CPF, telefone e CNPJ: <input data-mascara="cpf|telefone|cnpj">.
     */
    const MASCARAS = {
        cpf: function (digitos) {
            return digitos
                .replace(/^(\d{3})(\d)/, '$1.$2')
                .replace(/^(\d{3})\.(\d{3})(\d)/, '$1.$2.$3')
                .replace(/^(\d{3})\.(\d{3})\.(\d{3})(\d)/, '$1.$2.$3-$4')
                .substring(0, 14);
        },
        cnpj: function (digitos) {
            return digitos
                .replace(/^(\d{2})(\d)/, '$1.$2')
                .replace(/^(\d{2})\.(\d{3})(\d)/, '$1.$2.$3')
                .replace(/^(\d{2})\.(\d{3})\.(\d{3})(\d)/, '$1.$2.$3/$4')
                .replace(/^(\d{2})\.(\d{3})\.(\d{3})\/(\d{4})(\d)/, '$1.$2.$3/$4-$5')
                .substring(0, 18);
        },
        telefone: function (digitos) {
            // Celular (11 dígitos): (51) 99999-0000; fixo (10): (51) 3333-0000.
            if (digitos.length > 10) {
                return digitos.replace(/^(\d{2})(\d{5})(\d{0,4}).*/, '($1) $2-$3');
            }
            return digitos.replace(/^(\d{2})(\d{4})(\d{0,4}).*/, '($1) $2-$3');
        },
    };

    function iniciarMascaras() {
        document.querySelectorAll('input[data-mascara]').forEach(function (campo) {
            const formatar = MASCARAS[campo.dataset.mascara];
            if (!formatar) {
                return;
            }
            campo.addEventListener('input', function () {
                const posicao = campo.selectionEnd;
                const antes = campo.value.length;
                const digitos = campo.value.replace(/\D/g, '');
                campo.value = formatar(digitos);
                // Mantém o cursor próximo de onde estava após formatar.
                const deslocamento = campo.value.length - antes;
                const novaPosicao = Math.max(0, Math.min(campo.value.length, posicao + deslocamento));
                campo.setSelectionRange(novaPosicao, novaPosicao);
            });
        });
    }

    /**
     * Pedido de confirmação: <form data-confirmar="Mensagem">.
     */
    function iniciarConfirmacao() {
        document.querySelectorAll('form[data-confirmar]').forEach(function (form) {
            form.addEventListener('submit', function (evento) {
                if (!window.confirm(form.dataset.confirmar)) {
                    evento.preventDefault();
                }
            });
        });
    }

    /**
     * Mensagens do Django como toasts: botão de fechar e saída automática.
     */
    function iniciarMensagens() {
        document.querySelectorAll('.mensagem').forEach(function (mensagem, indice) {
            mensagem.style.animationDelay = (indice * 90) + 'ms';

            const fechar = document.createElement('button');
            fechar.type = 'button';
            fechar.className = 'mensagem-fechar';
            fechar.setAttribute('aria-label', 'Fechar mensagem');
            fechar.innerHTML = '<svg class="icone" aria-hidden="true"><use href="#ic-fechar"/></svg>';
            mensagem.appendChild(fechar);

            function remover() {
                if (mensagem.classList.contains('saindo')) {
                    return;
                }
                mensagem.classList.add('saindo');
                setTimeout(function () {
                    mensagem.remove();
                }, MOVIMENTO_REDUZIDO ? 0 : 300);
            }

            fechar.addEventListener('click', remover);
            setTimeout(remover, 5200 + indice * 90);
        });
    }

    /**
     * Efeito "onda" (ripple) a partir do ponto do clique nos botões.
     */
    function iniciarOnda() {
        if (MOVIMENTO_REDUZIDO) {
            return;
        }
        document.addEventListener('pointerdown', function (evento) {
            const botao = evento.target.closest('.botao');
            if (!botao) {
                return;
            }
            const area = botao.getBoundingClientRect();
            const tamanho = Math.max(area.width, area.height);
            const onda = document.createElement('span');
            onda.className = 'onda';
            onda.style.width = onda.style.height = tamanho + 'px';
            onda.style.left = (evento.clientX - area.left - tamanho / 2) + 'px';
            onda.style.top = (evento.clientY - area.top - tamanho / 2) + 'px';
            botao.appendChild(onda);
            onda.addEventListener('animationend', function () {
                onda.remove();
            });
        });
    }

    /**
     * Contadores do dashboard animados de 0 até o valor: <span data-contar="12">.
     */
    function iniciarContadores() {
        document.querySelectorAll('[data-contar]').forEach(function (elemento) {
            const alvo = parseInt(elemento.dataset.contar, 10) || 0;
            if (MOVIMENTO_REDUZIDO || alvo === 0) {
                elemento.textContent = alvo;
                return;
            }
            const duracao = 900;
            let inicio = null;
            elemento.textContent = '0';
            function passo(agora) {
                if (inicio === null) {
                    inicio = agora;
                }
                const progresso = Math.min((agora - inicio) / duracao, 1);
                const suavizado = 1 - Math.pow(1 - progresso, 3);
                elemento.textContent = Math.round(alvo * suavizado);
                if (progresso < 1) {
                    requestAnimationFrame(passo);
                }
            }
            requestAnimationFrame(passo);
        });
    }

    /**
     * Entrada em cascata dos elementos quando aparecem na tela.
     */
    function iniciarRevelar() {
        if (MOVIMENTO_REDUZIDO || !('IntersectionObserver' in window)) {
            return;
        }
        // A entrada em cascata existe só no painel (dashboard); nas listas,
        // telas usadas o tempo todo, o conteúdo aparece direto.
        if (!document.querySelector('.painel-contadores')) {
            return;
        }
        const seletores = '.contador, .ocupacao, .acao-rapida, .painel-secao .tabela tbody tr';
        const elementos = document.querySelectorAll(seletores);

        const observador = new IntersectionObserver(function (entradas) {
            entradas.forEach(function (entrada) {
                if (entrada.isIntersecting) {
                    const alvo = entrada.target;
                    alvo.classList.add('visivel');
                    observador.unobserve(alvo);
                    // Ao terminar a entrada, devolve o elemento ao estilo normal
                    // (assim o efeito de hover dos cards volta a funcionar).
                    const atraso = parseInt(alvo.style.getPropertyValue('--atraso'), 10) || 0;
                    setTimeout(function () {
                        alvo.classList.remove('revelar', 'visivel');
                        alvo.style.removeProperty('--atraso');
                    }, atraso + 560);
                }
            });
        }, { threshold: 0.08, rootMargin: '0px 0px -30px 0px' });

        // Atraso escalonado entre irmãos (no máximo 10 por grupo).
        elementos.forEach(function (elemento) {
            const irmaos = Array.prototype.filter.call(elemento.parentElement.children, function (filho) {
                return filho.matches(seletores);
            });
            const posicao = Math.min(irmaos.indexOf(elemento), 10);
            elemento.style.setProperty('--atraso', (posicao * 55) + 'ms');
            elemento.classList.add('revelar');
            observador.observe(elemento);
        });
    }

    /**
     * Texto em portugues para a opcao vazia dos selects (Django usa "---------").
     */
    function iniciarSelects() {
        document.querySelectorAll('select:not([multiple])').forEach(function (select) {
            const primeira = select.options[0];
            if (primeira && primeira.value === '') {
                primeira.textContent = 'Selecione uma opção';
            }
        });
    }

    /**
     * Cor estável a partir de um texto (mesma categoria = mesma cor).
     */
    function corPorTexto(texto, paleta) {
        let soma = 0;
        for (let i = 0; i < texto.length; i += 1) {
            soma = (soma * 31 + texto.charCodeAt(i)) % 100000;
        }
        return paleta[soma % paleta.length];
    }

    /**
     * Livros sem capa ganham uma capa tipográfica com a cor da categoria.
     */
    function iniciarCapas() {
        const paleta = ['#6e1d12', '#1f4e5f', '#7a5212', '#2f4a32', '#3b2f5c', '#2b2622', '#5c2a3d'];
        document.querySelectorAll('.card-livro').forEach(function (card) {
            const capa = card.querySelector('.capa-vazia');
            if (!capa) {
                return;
            }
            const titulo = (card.querySelector('h2') || {}).textContent || '';
            const autor = (card.querySelector('.card-livro-autores') || {}).textContent || '';
            let categoria = '';
            card.querySelectorAll('.card-livro-meta').forEach(function (meta) {
                const texto = meta.textContent.trim();
                if (texto.indexOf('Categoria:') === 0) {
                    categoria = texto.replace('Categoria:', '').trim();
                }
            });
            capa.textContent = '';
            capa.classList.add('capa-gerada');
            capa.style.setProperty('--capa-cor', corPorTexto(categoria || titulo, paleta));
            [['capa-categoria', categoria], ['capa-titulo', titulo.trim()], ['capa-autor', autor.trim()]].forEach(function (parte) {
                const span = document.createElement('span');
                span.className = parte[0];
                span.textContent = parte[1];
                capa.appendChild(span);
            });
        });
    }

    /**
     * Nas tabelas com coluna "Foto", quem não tem foto ganha um avatar com iniciais.
     */
    function iniciarAvatares() {
        const paleta = ['#a86a12', '#0e6680', '#c62a17', '#4d6b3a', '#5b4a8a', '#7a3b2e'];
        document.querySelectorAll('.tabela').forEach(function (tabela) {
            const cabecalhos = Array.prototype.map.call(tabela.querySelectorAll('thead th'), function (th) {
                return th.textContent.trim().toLowerCase();
            });
            const colFoto = cabecalhos.indexOf('foto');
            if (colFoto === -1) {
                return;
            }
            tabela.querySelectorAll('tbody tr').forEach(function (linha) {
                const celula = linha.children[colFoto];
                const celulaNome = linha.children[colFoto + 1];
                if (!celula || !celulaNome || celula.querySelector('img')) {
                    return;
                }
                const nome = celulaNome.textContent.trim();
                const partes = nome.split(/\s+/).filter(Boolean);
                const iniciais = ((partes[0] || '?')[0] + (partes.length > 1 ? partes[partes.length - 1][0] : '')).toUpperCase();
                const avatar = document.createElement('span');
                avatar.className = 'avatar';
                avatar.textContent = iniciais;
                avatar.setAttribute('aria-hidden', 'true');
                avatar.style.setProperty('--avatar-cor', corPorTexto(nome, paleta));
                celula.textContent = '';
                celula.appendChild(avatar);
            });
        });
    }

    document.addEventListener('DOMContentLoaded', function () {
        iniciarMenu();
        iniciarCabecalho();
        iniciarBusca();
        iniciarPreview();
        iniciarMascaras();
        iniciarSelects();
        iniciarCapas();
        iniciarAvatares();
        iniciarConfirmacao();
        iniciarMensagens();
        iniciarOnda();
        iniciarRevelar();
        iniciarContadores();
    });
})();
