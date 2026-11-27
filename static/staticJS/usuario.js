document.addEventListener('DOMContentLoaded', () => {
<<<<<<< HEAD
    // Interatividade básica para menus em dispositivos móveis
=======
>>>>>>> 0748ac9 (Alterações no prontuário da página do usuário e na página de agendamentos)
    const dropdowns = document.querySelectorAll('.dropdown');

    dropdowns.forEach(dropdown => {
        const link = dropdown.querySelector('a');
<<<<<<< HEAD
        link.addEventListener('click', (e) => {
            if (window.innerWidth <= 850) {
                e.preventDefault();
                dropdown.classList.toggle('open');
            }
        });
    });

    // Navegação entre seções
=======
        if (link) {
            link.addEventListener('click', (e) => {
                if (window.innerWidth <= 850) {
                    e.preventDefault();
                    dropdown.classList.toggle('open');
                }
            });
        }
    });

    // Troca de abas do painel
>>>>>>> 0748ac9 (Alterações no prontuário da página do usuário e na página de agendamentos)
    const linksSecao = document.querySelectorAll('[data-secao]');
    const secoesPainel = document.querySelectorAll('.secao-painel');
    const linksSidebar = document.querySelectorAll('.sidebar-menu a');

    function ativarSecao(nomeSecao) {
        secoesPainel.forEach(secao => {
<<<<<<< HEAD
            secao.classList.toggle('ativa', secao.id === `sec-${nomeSecao}`);
=======
            secao.classList.toggle('ativa', secao.id === 'sec-' + nomeSecao);
>>>>>>> 0748ac9 (Alterações no prontuário da página do usuário e na página de agendamentos)
        });

        linksSidebar.forEach(link => {
            link.classList.toggle('active', link.dataset.secao === nomeSecao);
        });
    }

    linksSecao.forEach(link => {
        link.addEventListener('click', (e) => {
            const secaoAlvo = link.dataset.secao;
            if (secaoAlvo) {
                e.preventDefault();
                ativarSecao(secaoAlvo);
            }
        });
    });

    // ==========================================
    // PREENCHIMENTO AUTOMÁTICO DE ENDEREÇO (VIA CEP)
    // ==========================================
    const inputCep = document.getElementById('cep');
<<<<<<< HEAD

    if (inputCep) {
        inputCep.addEventListener('blur', (e) => {
            let cep = e.target.value.replace(/\D/g, ''); // Remove traços ou pontos

            if (cep.length === 8) {
                const url = `https://viacep.com.br/ws/${cep}/json/`;

                fetch(url)
                    .then(response => response.json())
                    .then(data => {
                        if (!data.erro) {
                            // Preenche os campos do formulário automaticamente
                            document.getElementById('rua').value = data.logradouro || '';
                            document.getElementById('bairro').value = data.bairro || '';
                            document.getElementById('cidade').value = data.localidade || '';
                            document.getElementById('uf').value = data.uf || '';
                            
                            // Joga o foco direto para o campo número
                            document.getElementById('numero').focus();
                        } else {
                            alert('CEP não encontrado na base de dados.');
                        }
                    })
                    .catch(error => {
                        console.error('Erro ao consultar a API ViaCEP:', error);
                        alert('Não foi possível buscar o CEP. Verifique sua conexão.');
                    });
            }
        });
    }

    // Ação opcional ao enviar o formulário de cadastro
    const formCadastro = document.getElementById('form-cadastro');
    if (formCadastro) {
        formCadastro.addEventListener('submit', (e) => {
            e.preventDefault();
            alert('Dados de cadastro salvos com sucesso!');
        });
=======
    const inputRua = document.getElementById('rua');
    const inputBairro = document.getElementById('bairro');
    const inputCidade = document.getElementById('cidade');
    const inputUf = document.getElementById('uf');
    const inputNumero = document.getElementById('numero');

    let ultimoCepBuscado = '';

    function formatarCep(valor) {
        const digitos = valor.replace(/\D/g, '').slice(0, 8);
        if (digitos.length > 5) {
            return digitos.slice(0, 5) + '-' + digitos.slice(5);
        }
        return digitos;
    }

    function buscarViaCep(cepLimpo) {
        if (cepLimpo.length !== 8 || cepLimpo === ultimoCepBuscado) {
            return;
        }
        ultimoCepBuscado = cepLimpo;

        const url = 'https://viacep.com.br/ws/' + cepLimpo + '/json/';

        fetch(url)
            .then(response => response.json())
            .then(data => {
                if (!data.erro) {
                    if (inputRua) inputRua.value = data.logradouro || '';
                    if (inputBairro) inputBairro.value = data.bairro || '';
                    if (inputCidade) inputCidade.value = data.localidade || '';
                    if (inputUf) inputUf.value = data.uf || '';
                    if (inputNumero) inputNumero.focus();
                } else {
                    alert('CEP não encontrado na base de dados.');
                }
            })
            .catch(error => {
                console.error('Erro ao consultar a API ViaCEP:', error);
                alert('Não foi possível buscar o CEP. Verifique sua conexão.');
            });
    }

    if (inputCep) {
        if (inputCep.value) {
            inputCep.value = formatarCep(inputCep.value);
        }

        const tratarCep = (e) => {
            const cepFormatado = formatarCep(e.target.value);
            e.target.value = cepFormatado;

            const cepLimpo = cepFormatado.replace(/\D/g, '');
            if (cepLimpo.length === 8) {
                buscarViaCep(cepLimpo);
            }
        };

        inputCep.addEventListener('input', tratarCep);
        inputCep.addEventListener('blur', tratarCep);
>>>>>>> 0748ac9 (Alterações no prontuário da página do usuário e na página de agendamentos)
    }
});